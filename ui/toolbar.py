"""
Barra de herramientas lateral izquierda.

Contiene botones para las operaciones principales: abrir, guardar,
deshacer, rehacer, y acceso rápido a filtros y herramientas.
"""
from pathlib import Path
import tkinter as tk

from PIL import Image, ImageTk

from app.config import COLORS, FONTS
from utils.animation_utils import animate_color_transition


class ToolbarButton(tk.Frame):
    """
    Botón estilizado para la barra de herramientas con animación.

    Args:
        parent: Widget padre.
        text: Texto del botón.
        command: Función a ejecutar al hacer clic.
        icon_image: Imagen del icono opcional (PhotoImage).
    """

    def __init__(self, parent, text, command=None, icon_image=None):
        super().__init__(parent, bg=COLORS["bg_panel"], cursor="hand2")
        self._command = command
        self._normal_bg = COLORS["bg_panel"]
        self._hover_bg = COLORS["bg_hover"]
        self._icon_image = icon_image  # Mantiene referencia para evitar GC.

        self._label = tk.Label(
            self,
            text=text,
            image=self._icon_image,
            compound="left",
            bg=COLORS["bg_panel"],
            fg=COLORS["text_primary"],
            font=FONTS["button"],
            anchor="w",
            padx=10,
            pady=6,
        )
        self._label.pack(fill="x")

        for widget in (self, self._label):
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            widget.bind("<Button-1>", self._on_click)

    def _on_enter(self, _event):
        animate_color_transition(self, "bg", self._normal_bg, self._hover_bg)
        self._label.config(bg=self._hover_bg)

    def _on_leave(self, _event):
        self.config(bg=self._normal_bg)
        self._label.config(bg=self._normal_bg)

    def _on_click(self, _event):
        if self._command:
            self._command()


class Toolbar(tk.Frame):
    """
    Barra de herramientas lateral izquierda.

    Args:
        parent: Widget padre de tkinter.
        app: Referencia a la aplicación principal para callbacks.
    """

    ICON_SIZE = (24, 24)  

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_panel"], width=180)
        self.pack_propagate(False)
        self._app = app
        self._icons = {}
        self._load_icons()
        self._create_widgets()

    def _theme_rgb(self, color_value):
        """
        Convierte cualquier color valido de tkinter (hex o nombre) a RGB 8-bit.
        """
        r16, g16, b16 = self.winfo_rgb(color_value)
        return (r16 // 256, g16 // 256, b16 // 256)

    def _load_icon_resized_tinted(self, icon_path, tint_rgb):
        """
        Carga PNG, redimensiona a ICON_SIZE y aplica tinte uniforme
        conservando el canal alfa.
        """
        try:
            image = Image.open(icon_path).convert("RGBA")
            image = image.resize(self.ICON_SIZE, Image.Resampling.LANCZOS)

            # Usamos el alfa original como mascara para colorear el icono
            alpha = image.getchannel("A")
            tinted = Image.new("RGBA", image.size, tint_rgb + (0,))
            tinted.putalpha(alpha)

            return ImageTk.PhotoImage(tinted)
        except Exception:
            return None

    def _load_icons(self):
        project_root = Path(__file__).resolve().parent.parent
        icons_dir = project_root / "assets" / "icons"

        icon_files = {
            "open": "open.png",
            "save": "save.png",
            "undo": "undo.png",
            "redo": "redo.png",
            "reset": "reset.png",
            "invert": "invert.png",
            "reconstruct": "reconstruct.png",
            "histogram": "histogram.png",
            "info": "info.png",
            "fusion": "fusion.png",
            "crop": "crop.png",
        }

        # Color principal del texto para unificar estilo visual
        tint_rgb = self._theme_rgb(COLORS["text_primary"])

        for key, filename in icon_files.items():
            self._icons[key] = self._load_icon_resized_tinted(
                icons_dir / filename,
                tint_rgb,
            )

    def _add_separator(self):
        tk.Frame(self, bg=COLORS["border"], height=1).pack(fill="x", padx=5, pady=5)

    def _add_section_label(self, text):
        tk.Label(
            self,
            text=text,
            bg=COLORS["bg_panel"],
            fg=COLORS["text_secondary"],
            font=FONTS["small"],
        ).pack(padx=10, anchor="w", pady=(5, 2))

    def _add_button(self, text, command, icon_key):
        ToolbarButton(
            self,
            text=text,
            command=command,
            icon_image=self._icons.get(icon_key),
        ).pack(fill="x")

    def _create_widgets(self):
        tk.Label(
            self,
            text="Herramientas",
            bg=COLORS["bg_panel"],
            fg=COLORS["accent"],
            font=FONTS["title"],
        ).pack(pady=(10, 5), padx=5, anchor="w")

        self._add_separator()

        # Archivo
        self._add_button("Abrir", self._app.open_image, "open")
        self._add_button("Guardar", self._app.save_image, "save")

        self._add_separator()

        # Historial
        self._add_button("Deshacer", self._app.undo, "undo")
        self._add_button("Rehacer", self._app.redo, "redo")
        self._add_button("Reset", self._app.reset_image, "reset")

        self._add_separator()

        # Filtros
        self._add_section_label("Filtros")
        self._add_button("Invertir", self._app.apply_invert, "invert")
        self._add_button("Reconstruir", self._app.apply_reconstruct, "reconstruct")

        self._add_separator()

        # Utilidades
        self._add_section_label("Utilidades")
        self._add_button("Histograma", self._app.show_histogram, "histogram")
        self._add_button("Info", self._app.show_info, "info")
        self._add_button("Fusión", self._app.show_fusion_dialog, "fusion")
        self._add_button("Recorte", self._app.show_crop_dialog, "crop")
