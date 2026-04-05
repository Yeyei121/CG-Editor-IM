"""
Configuración global del Editor de Imágenes.

Define constantes de colores, fuentes, dimensiones y temas
utilizados por todos los componentes de la interfaz.
"""

COLORS = {
    "bg_dark":        "#0D0F14",
    "bg_panel":       "#151820",
    "bg_card":        "#1C2030",
    "bg_hover":       "#252A3A",
    "accent":         "#7010A4",
    "accent_soft":    "#2D5AB8",
    "success":        "#3DD68C",
    "warning":        "#F7A84F",
    "error":          "#E74C3C",
    "text_primary":   "#E8ECF4",
    "text_secondary": "#8892A4",
    "border":         "#2A3045",
    "slider_trough":  "#1C2030",
}

FONTS = {
    "title":  ("Segoe UI", 13, "bold"),
    "label":  ("Segoe UI", 10),
    "small":  ("Segoe UI", 9),
    "mono":   ("Consolas", 9),
    "button": ("Segoe UI", 10, "bold"),
}

DIMENSIONS = {
    "toolbar_width":       140,
    "control_panel_width": 280,
    "status_bar_height":   30,
    "button_padding":      8,
    "window_min_width":    1200,
    "window_min_height":   700,
}

APP_TITLE = "Editor IM"

HISTORY_MAX_STEPS = 20 # Máximo número de pasos de deshacer/rehacer

SUPPORTED_FORMATS = [
    ("Imágenes", "*.jpg *.jpeg *.png"),
    ("JPEG", "*.jpg *.jpeg"),
    ("PNG", "*.png"),
    ("Todos", "*.*"),
]