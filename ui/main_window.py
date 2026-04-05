"""
Ventana principal del Editor de Imágenes.

Construye y organiza el layout general: topbar, toolbar, canvas,
control panel y status bar.
"""
import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from app.config import COLORS, FONTS, DIMENSIONS, APP_TITLE
from ui.toolbar import Toolbar
from ui.canvas_panel import CanvasPanel
from ui.control_panel import ControlPanel
from ui.status_bar import StatusBar


class MainWindow:
    """
    Construye la ventana principal y organiza los componentes visuales.

    Args:
        root: Instancia de tk.Tk (ventana raíz).
        app: Referencia a la aplicación principal para callbacks.
    """

    def __init__(self, root, app):
        self.root = root
        self._app = app
        self._configure_root()
        self._configure_styles()
        self._create_layout()

    def _configure_root(self):
        """Configura las propiedades de la ventana raíz."""
        self.root.title(APP_TITLE)
        self.root.configure(bg=COLORS["bg_dark"])
        self.root.minsize(
            DIMENSIONS["window_min_width"],
            DIMENSIONS["window_min_height"],
        )
        # Intentar maximizar
        try:
            self.root.state("zoomed")
        except tk.TclError:
            self.root.geometry("1400x800")

    def _configure_styles(self):
        """Configura estilos ttk para theme oscuro."""
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.TFrame", background=COLORS["bg_dark"])
        style.configure(
            "Dark.Vertical.TScrollbar",
            background=COLORS["bg_card"],
            troughcolor=COLORS["bg_panel"],
            arrowcolor=COLORS["text_secondary"],
        )

    def _create_layout(self):
        """Crea y posiciona todos los componentes de la ventana."""
        # Top bar (título e info)
        self._topbar = tk.Frame(self.root, bg=COLORS["bg_panel"], height=42)
        self._topbar.pack(side="top", fill="x")
        self._topbar.pack_propagate(False)

        emoji_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "assets",
            "emoji_principal.png",
        )
        self._topbar_emoji = ImageTk.PhotoImage(
            Image.open(emoji_path).resize((26, 26), Image.LANCZOS)
        )

        tk.Label(
            self._topbar, text=f"  {APP_TITLE}", image=self._topbar_emoji, compound="left",
            bg=COLORS["bg_panel"], fg=COLORS["accent"],
            font=FONTS["title"],
        ).pack(side="left", padx=15)

        self._topbar_info = tk.Label(
            self._topbar, text="",
            bg=COLORS["bg_panel"], fg=COLORS["text_secondary"],
            font=FONTS["small"],
        )
        self._topbar_info.pack(side="right", padx=15)

        # Separador debajo de la topbar
        tk.Frame(self.root, bg=COLORS["border"], height=1).pack(side="top", fill="x")

        # Status bar (abajo)
        self.status_bar = StatusBar(self.root)
        self.status_bar.pack(side="bottom", fill="x")

        # Separador sobre la barra de estado
        tk.Frame(self.root, bg=COLORS["border"], height=1).pack(side="bottom", fill="x")

        # Toolbar (izquierda)
        self.toolbar = Toolbar(self.root, self._app)
        self.toolbar.pack(side="left", fill="y")

        # Separador derecho de la toolbar
        tk.Frame(self.root, bg=COLORS["border"], width=1).pack(side="left", fill="y")

        # Panel de controles (derecha)
        self.control_panel = ControlPanel(self.root, self._app)
        self.control_panel.pack(side="right", fill="y")

        # Separador izquierdo del panel de controles
        tk.Frame(self.root, bg=COLORS["border"], width=1).pack(side="right", fill="y")

        # Canvas principal (centro)
        self.canvas_panel = CanvasPanel(self.root)
        self.canvas_panel.pack(side="left", fill="both", expand=True)

    def update_topbar_info(self, text):
        """
        Actualiza el texto informativo en la topbar.

        Args:
            text: Texto a mostrar (ej: nombre del archivo).
        """
        self._topbar_info.config(text=text)
