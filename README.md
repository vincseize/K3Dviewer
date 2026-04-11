# K3Dviewer

Un visualiseur 3D léger et performant basé sur **PyQt5** et **OpenGL**. Ce projet propose une navigation fluide de type "Turntable" (similaire à Blender) avec une gestion précise des axes et une grille de référence optimisée.

---

## 📁 Structure du Projet

```text
K3Dviewer/
├── 📄 K3Dviewer.spec     # Fichier de configuration PyInstaller
├── 📄 README.md           # Documentation du projet
├── 🐍 main.py             # Code source principal
├── 📄 project_tree.txt    # Export de l'arborescence
└── 🐍 tree.py             # Script utilitaire d'arborescence

---

libs
QT5, openGl etc...
pip install pyrr


## 📁 Compilation
python -v  --> 3.7
pyinstaller --noconfirm --onefile --windowed --name "K3Dviewer" main.py