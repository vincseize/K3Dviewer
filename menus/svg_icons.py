# menus/svg_icons.py

SVG_ICONS = {
    "persp": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#ddd" stroke-width="2"/></svg>""",
    
    "ortho": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 3H21V21H3V3Z" stroke="#ddd" stroke-width="2"/><path d="M12 3V21M3 12H21" stroke="#ddd" stroke-opacity="0.3"/></svg>""",
    
    "home": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 9L12 2L21 9V20a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" stroke="#ddd" stroke-width="2"/><path d="M9 22V12h6v10" stroke="#ddd" stroke-width="2"/></svg>""",
    
    "grid": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M3 3h7v7H3V3zm11 0h7v7h-7V3zm0 11h7v7h-7v-7zM3 14h7v7H3v-7z" stroke="#ddd" stroke-width="2"/></svg>""",
    
    "axes_on": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><line x1="3" y1="12" x2="21" y2="12" stroke="#f00" stroke-width="2"/><line x1="12" y1="3" x2="12" y2="21" stroke="#0f0" stroke-width="2"/><circle cx="12" cy="12" r="2" fill="#00f"/></svg>""",
    
    "axes_off": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><line x1="3" y1="12" x2="21" y2="12" stroke="#f00" stroke-width="2" stroke-opacity="0.3"/><line x1="12" y1="3" x2="12" y2="21" stroke="#0f0" stroke-width="2" stroke-opacity="0.3"/><circle cx="12" cy="12" r="2" fill="#00f" fill-opacity="0.3"/><line x1="3" y1="21" x2="21" y2="3" stroke="#d00" stroke-width="2"/></svg>""",
    
    "zoom": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><circle cx="11" cy="11" r="8" stroke="#ddd" stroke-width="2"/><path d="M21 21L16.65 16.65" stroke="#ddd" stroke-width="2"/><path d="M11 8V14M8 11H14" stroke="#ddd" stroke-width="2"/></svg>""",
    
    "pan": """<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 2V22M12 2L8 6M12 2L16 6M12 22L8 18M12 22L16 18" stroke="#ddd" stroke-width="2"/><circle cx="12" cy="12" r="3" stroke="#ddd" stroke-width="2"/><path d="M5 12H2M22 12H19" stroke="#ddd" stroke-width="2"/></svg>"""
}