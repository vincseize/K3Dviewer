# tree.py
# Génère l'arborescence du projet Kviewer3D

import os
import sys
from datetime import datetime

def generate_tree(startpath, output_file="project_tree.txt", exclude_dirs=None, exclude_files=None):
    """
    Génère l'arborescence d'un projet
    
    Args:
        startpath: Chemin racine du projet
        output_file: Fichier de sortie
        exclude_dirs: Liste des dossiers à exclure
        exclude_files: Liste des fichiers à exclure
    """
    
    if exclude_dirs is None:
        exclude_dirs = ['__pycache__', '.git', '.vscode', 'venv', 'env', 'build', 'dist']
    
    if exclude_files is None:
        exclude_files = ['.pyc', '.pyo', '.pyd', '.db', 'project_tree.txt']
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # En-tête
        f.write("=" * 80 + "\n")
        f.write(f"ARBORESCENCE DU PROJET Kviewer3D\n")
        f.write(f"Généré le : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Racine : {os.path.abspath(startpath)}\n")
        f.write("=" * 80 + "\n\n")
        
        # Structure
        f.write("📁 STRUCTURE DES DOSSIERS\n")
        f.write("-" * 40 + "\n\n")
        
        for root, dirs, files in os.walk(startpath):
            # Filtrer les dossiers exclus
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            
            # Niveau d'indentation
            level = root.replace(startpath, '').count(os.sep)
            indent = '│   ' * level
            
            # Nom du dossier courant
            folder_name = os.path.basename(root)
            if level == 0:
                f.write(f"📁 {folder_name}/\n")
            else:
                f.write(f"{indent}├── 📁 {folder_name}/\n")
            
            # Afficher les fichiers
            subindent = '│   ' * (level + 1)
            file_count = 0
            
            # Trier les fichiers
            for file in sorted(files):
                # Filtrer les fichiers exclus
                if any(file.endswith(ext) for ext in exclude_files):
                    continue
                
                file_count += 1
                # Obtenir la taille du fichier
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                
                # Formater la taille
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024 * 1024:
                    size_str = f"{size / 1024:.1f} KB"
                else:
                    size_str = f"{size / (1024 * 1024):.1f} MB"
                
                # Icône selon extension
                if file.endswith('.py'):
                    icon = "🐍"
                elif file.endswith('.ico'):
                    icon = "🎨"
                elif file.endswith('.svg'):
                    icon = "🖼️"
                elif file.endswith('.md'):
                    icon = "📝"
                elif file.endswith('.txt'):
                    icon = "📄"
                elif file.endswith('.exe'):
                    icon = "⚡"
                else:
                    icon = "📄"
                
                # Dernier fichier ?
                if file_count == len([f for f in files if not any(f.endswith(ext) for ext in exclude_files)]):
                    f.write(f"{subindent}└── {icon} {file} ({size_str})\n")
                else:
                    f.write(f"{subindent}├── {icon} {file} ({size_str})\n")
            
            if file_count > 0:
                f.write(f"{subindent}\n")
        
        # Statistiques
        f.write("\n" + "=" * 80 + "\n")
        f.write("📊 STATISTIQUES\n")
        f.write("-" * 40 + "\n\n")
        
        # Compter les fichiers
        total_files = 0
        total_size = 0
        py_files = 0
        py_size = 0
        
        for root, dirs, files in os.walk(startpath):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in files:
                if any(file.endswith(ext) for ext in exclude_files):
                    continue
                file_path = os.path.join(root, file)
                size = os.path.getsize(file_path)
                total_files += 1
                total_size += size
                
                if file.endswith('.py'):
                    py_files += 1
                    py_size += size
        
        f.write(f"📁 Dossiers analysés : {sum(1 for _ in os.walk(startpath))}\n")
        f.write(f"📄 Fichiers total : {total_files}\n")
        f.write(f"🐍 Fichiers Python : {py_files}\n")
        f.write(f"💾 Taille totale : {total_size / (1024 * 1024):.2f} MB\n")
        f.write(f"🐍 Taille code Python : {py_size / 1024:.1f} KB\n")
        
        # Liste des modules
        f.write("\n" + "=" * 80 + "\n")
        f.write("📦 MODULES DU PROJET\n")
        f.write("-" * 40 + "\n\n")
        
        for root, dirs, files in os.walk(startpath):
            dirs[:] = [d for d in dirs if d not in exclude_dirs]
            for file in sorted(files):
                if file.endswith('.py') and file != 'tree.py':
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, startpath)
                    size = os.path.getsize(file_path)
                    f.write(f"   • {rel_path} ({size} bytes)\n")
        
        f.write("\n" + "=" * 80 + "\n")
        f.write("✅ Arborescence générée avec succès !\n")

def print_tree_console(startpath, exclude_dirs=None):
    """Affiche l'arborescence dans la console"""
    
    if exclude_dirs is None:
        exclude_dirs = ['__pycache__', '.git', '.vscode', 'venv', 'env', 'build', 'dist']
    
    print("\n" + "=" * 60)
    print(f"📁 ARBORESCENCE : {os.path.basename(startpath)}")
    print("=" * 60 + "\n")
    
    for root, dirs, files in os.walk(startpath):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        level = root.replace(startpath, '').count(os.sep)
        indent = '│   ' * level
        
        folder_name = os.path.basename(root)
        if level == 0:
            print(f"📁 {folder_name}/")
        else:
            print(f"{indent}├── 📁 {folder_name}/")
        
        subindent = '│   ' * (level + 1)
        for i, file in enumerate(sorted(files)):
            if file.endswith(('.pyc', '.pyo', '.db')):
                continue
            
            is_last = i == len([f for f in files if not f.endswith(('.pyc', '.pyo', '.db'))]) - 1
            
            if file.endswith('.py'):
                icon = "🐍"
            elif file.endswith('.ico'):
                icon = "🎨"
            elif file.endswith('.svg'):
                icon = "🖼️"
            else:
                icon = "📄"
            
            if is_last:
                print(f"{subindent}└── {icon} {file}")
            else:
                print(f"{subindent}├── {icon} {file}")

if __name__ == "__main__":
    # Chemin du projet (dossier courant)
    project_path = os.path.dirname(os.path.abspath(__file__))
    
    print("🚀 Génération de l'arborescence du projet...\n")
    
    # Générer le fichier texte
    generate_tree(project_path, "project_tree.txt")
    
    # Afficher dans la console
    print_tree_console(project_path)
    
    print("\n" + "=" * 60)
    print("✅ Fichier généré : project_tree.txt")
    print("=" * 60)