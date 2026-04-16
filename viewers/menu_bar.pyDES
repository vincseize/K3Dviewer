# viewers/menu_bar.py

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from config.settings import *

class MenuBar:
    # Variables de style
    TEXT_COLOR_NORMAL = (0.75, 0.75, 0.75)  # Gris clair
    TEXT_COLOR_HOVER = (1.0, 1.0, 1.0)      # Blanc
    BG_COLOR = (0.18, 0.18, 0.18, 1.0)      # Gris foncé
    SEPARATOR_COLOR = (0.3, 0.3, 0.3, 1.0)
    BAR_HEIGHT = 28
    TEXT_FONT = GLUT_BITMAP_HELVETICA_12
    TEXT_FONT_SUBMENU = GLUT_BITMAP_HELVETICA_12
    TEXT_Y_OFFSET = 8  # Décalage vertical du texte
    MENU_SPACING = 45  # Espace entre les menus
    MARGIN_X = 12
    
    # Zones cliquables
    menu_items = {}
    active_menu = None
    
    @staticmethod
    def draw_text(x, y, text, font=None):
        """Affiche du texte en coordonnées pixels."""
        if font is None:
            font = MenuBar.TEXT_FONT
        glRasterPos2f(x, y)
        for char in text:
            glutBitmapCharacter(font, ord(char))
    
    @staticmethod
    def get_text_width(text, font=None):
        """Calcule la largeur approximative du texte en pixels."""
        if font is None:
            font = MenuBar.TEXT_FONT
        
        # Largeurs approximatives pour GLUT_BITMAP_HELVETICA_12
        char_widths = {
            'A': 8, 'B': 8, 'C': 8, 'D': 8, 'E': 7, 'F': 7, 'G': 8, 'H': 9,
            'I': 4, 'J': 7, 'K': 8, 'L': 7, 'M': 10, 'N': 8, 'O': 8, 'P': 8,
            'Q': 8, 'R': 8, 'S': 7, 'T': 7, 'U': 8, 'V': 8, 'W': 10, 'X': 8,
            'Y': 8, 'Z': 7, 'a': 7, 'b': 7, 'c': 6, 'd': 7, 'e': 7, 'f': 4,
            'g': 7, 'h': 7, 'i': 3, 'j': 3, 'k': 6, 'l': 3, 'm': 11, 'n': 7,
            'o': 7, 'p': 7, 'q': 7, 'r': 5, 's': 6, 't': 4, 'u': 7, 'v': 6,
            'w': 9, 'x': 6, 'y': 6, 'z': 6, '0': 7, '1': 6, '2': 7, '3': 7,
            '4': 7, '5': 7, '6': 7, '7': 7, '8': 7, '9': 7, ' ': 4
        }
        width = 0
        for char in text:
            width += char_widths.get(char, 6)
        return width

    @staticmethod
    def render(width, height, mouse_x=None, mouse_y=None):
        """Affiche la barre de menu avec interaction."""
        if width == 0 or height == 0:
            return
            
        # --- Configuration de la vue 2D (Overlay) ---
        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        gluOrtho2D(0, width, 0, height)
        
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()
        
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # --- 1. Arrière-plan de la barre ---
        glColor4f(*MenuBar.BG_COLOR)
        glBegin(GL_QUADS)
        glVertex2f(0, height - MenuBar.BAR_HEIGHT)
        glVertex2f(width, height - MenuBar.BAR_HEIGHT)
        glVertex2f(width, height)
        glVertex2f(0, height)
        glEnd()

        # --- 2. Ligne de séparation ---
        glColor4f(*MenuBar.SEPARATOR_COLOR)
        glLineWidth(1.0)
        glBegin(GL_LINES)
        glVertex2f(0, height - MenuBar.BAR_HEIGHT)
        glVertex2f(width, height - MenuBar.BAR_HEIGHT)
        glEnd()

        # --- 3. Menu à GAUCHE ---
        text_y = height - MenuBar.TEXT_Y_OFFSET - 12
        
        menus = [
            ("File", ["New", "Open", "Save", "Import", "Export", "---", "Exit"]),
            ("Edit", ["Undo", "Redo", "---", "Cut", "Copy", "Paste", "---", "Preferences"]),
            ("View", ["Perspective", "Orthographic", "---", "Show Grid", "Show Axes", "---", "Reset View"]),
            ("Render", ["Render Image", "Render Animation", "---", "Settings"]),
            ("Window", ["Default Layout", "---", "Fullscreen"])
        ]
        
        current_x = MenuBar.MARGIN_X
        
        # Vider les items avant de les recréer
        MenuBar.menu_items.clear()
        
        for label, submenu in menus:
            text_width = MenuBar.get_text_width(label)
            is_hovered = (mouse_x is not None and 
                         current_x <= mouse_x <= current_x + text_width and 
                         height - MenuBar.BAR_HEIGHT <= mouse_y <= height)
            
            # Changer la couleur si survolé (sans clic)
            if is_hovered:
                glColor3f(*MenuBar.TEXT_COLOR_HOVER)
            else:
                glColor3f(*MenuBar.TEXT_COLOR_NORMAL)
            
            # Sauvegarder la zone cliquable
            MenuBar.menu_items[label] = {
                'x': current_x,
                'y': height - MenuBar.BAR_HEIGHT,
                'width': text_width,
                'height': MenuBar.BAR_HEIGHT,
                'submenu': submenu
            }
            
            MenuBar.draw_text(current_x, text_y, label)
            current_x += MenuBar.MENU_SPACING
        
        # --- 4. Help à DROITE ---
        help_label = "Help"
        help_width = MenuBar.get_text_width(help_label)
        help_x = width - help_width - 20
        
        is_help_hovered = (mouse_x is not None and 
                          help_x <= mouse_x <= help_x + help_width and 
                          height - MenuBar.BAR_HEIGHT <= mouse_y <= height)
        
        if is_help_hovered:
            glColor3f(*MenuBar.TEXT_COLOR_HOVER)
        else:
            glColor3f(*MenuBar.TEXT_COLOR_NORMAL)
        
        MenuBar.menu_items["Help"] = {
            'x': help_x,
            'y': height - MenuBar.BAR_HEIGHT,
            'width': help_width,
            'height': MenuBar.BAR_HEIGHT,
            'submenu': ["About", "Documentation", "---", "License"]
        }
        
        MenuBar.draw_text(help_x, text_y, help_label)
        
        # --- 5. Afficher le sous-menu si actif ---
        if MenuBar.active_menu and MenuBar.active_menu in MenuBar.menu_items:
            MenuBar.draw_submenu(MenuBar.menu_items[MenuBar.active_menu], mouse_x, mouse_y)
        
        # --- Restauration ---
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)
        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)
    
    @staticmethod
    def draw_submenu(menu_item, mouse_x=None, mouse_y=None):
        """Affiche un sous-menu déroulant."""
        submenu_width = 160
        submenu_bg = (0.22, 0.22, 0.22, 0.95)
        hover_bg = (0.35, 0.35, 0.35, 0.95)
        
        submenu_x = menu_item['x']
        submenu_y = menu_item['y']
        
        sub_items = menu_item['submenu']
        item_height = 22
        
        # Calculer la hauteur totale du sous-menu
        visible_items = [item for item in sub_items if item != "---"]
        total_height = len(visible_items) * item_height + sub_items.count("---") * 8
        
        # Dessiner l'arrière-plan du sous-menu
        glColor4f(*submenu_bg)
        glBegin(GL_QUADS)
        glVertex2f(submenu_x, submenu_y - total_height)
        glVertex2f(submenu_x + submenu_width, submenu_y - total_height)
        glVertex2f(submenu_x + submenu_width, submenu_y)
        glVertex2f(submenu_x, submenu_y)
        glEnd()
        
        # Bordure du sous-menu
        glColor4f(0.4, 0.4, 0.4, 1.0)
        glLineWidth(1.0)
        glBegin(GL_LINE_LOOP)
        glVertex2f(submenu_x, submenu_y - total_height)
        glVertex2f(submenu_x + submenu_width, submenu_y - total_height)
        glVertex2f(submenu_x + submenu_width, submenu_y)
        glVertex2f(submenu_x, submenu_y)
        glEnd()
        
        # Dessiner les items du sous-menu
        text_y_start = submenu_y - 6
        y_offset = 0
        
        for item in sub_items:
            if item == "---":
                # Ligne de séparation
                line_y = submenu_y - y_offset - 10
                glColor4f(0.4, 0.4, 0.4, 1.0)
                glBegin(GL_LINES)
                glVertex2f(submenu_x + 10, line_y)
                glVertex2f(submenu_x + submenu_width - 10, line_y)
                glEnd()
                y_offset += 8
            else:
                item_y = text_y_start - y_offset
                
                # Vérifier si la souris survole cet item
                is_item_hovered = (mouse_x is not None and 
                                  submenu_x <= mouse_x <= submenu_x + submenu_width and 
                                  item_y - item_height <= mouse_y <= item_y)
                
                if is_item_hovered:
                    # Fond de survol
                    glColor4f(*hover_bg)
                    glBegin(GL_QUADS)
                    glVertex2f(submenu_x, item_y - item_height + 2)
                    glVertex2f(submenu_x + submenu_width, item_y - item_height + 2)
                    glVertex2f(submenu_x + submenu_width, item_y + 2)
                    glVertex2f(submenu_x, item_y + 2)
                    glEnd()
                    glColor3f(*MenuBar.TEXT_COLOR_HOVER)
                else:
                    glColor3f(*MenuBar.TEXT_COLOR_NORMAL)
                
                MenuBar.draw_text(submenu_x + 10, item_y, item, MenuBar.TEXT_FONT_SUBMENU)
                y_offset += item_height
    
    @staticmethod
    def handle_click(x, y, height):
        """Gère les clics sur la barre de menu."""
        # Vérifier si le clic est dans la barre de menu
        if y > height - MenuBar.BAR_HEIGHT:
            for label, item in MenuBar.menu_items.items():
                if (item['x'] <= x <= item['x'] + item['width'] and
                    height - item['height'] <= y <= height):
                    # Toggle du menu
                    if MenuBar.active_menu == label:
                        MenuBar.active_menu = None
                    else:
                        MenuBar.active_menu = label
                    return True
        else:
            # Clic en dehors de la barre ferme les sous-menus
            MenuBar.active_menu = None
        
        # Vérifier les clics dans les sous-menus
        if MenuBar.active_menu and MenuBar.active_menu in MenuBar.menu_items:
            menu_item = MenuBar.menu_items[MenuBar.active_menu]
            submenu_x = menu_item['x']
            submenu_y = menu_item['y']
            submenu_width = 160
            sub_items = menu_item['submenu']
            item_height = 22
            
            # Calculer la hauteur totale
            total_height = len([item for item in sub_items if item != "---"]) * item_height + sub_items.count("---") * 8
            
            # Vérifier si le clic est dans le sous-menu
            if (submenu_x <= x <= submenu_x + submenu_width and
                submenu_y - total_height <= y <= submenu_y):
                # Clic sur un item du sous-menu
                y_offset = 0
                for item in sub_items:
                    if item == "---":
                        y_offset += 8
                    else:
                        item_y_start = submenu_y - 6
                        item_y = item_y_start - y_offset
                        if item_y - item_height <= y <= item_y:
                            print(f"Menu sélectionné: {MenuBar.active_menu} -> {item}")
                            MenuBar.active_menu = None
                            return True
                        y_offset += item_height
        
        return False