"""
Barra de estado inferior.

Muestra información del estado actual: dimensiones de imagen,
tipo de dato, estado de guardado y mensajes de estado.
"""
import tkinter as tk
from app.config import COLORS, FONTS


class StatusBar(tk.Frame):
    """
    Barra inferior de estado que muestra info de la imagen y mensajes.

    Args:
        parent: Widget padre de tkinter.
    """

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg_panel"], height=30)
        self.pack_propagate(False)
        self._create_widgets()

    def _create_widgets(self):
        """Crea los widgets internos de la barra de estado."""
        self._status_label = tk.Label(
            self, text="Estado: Listo",
            bg=COLORS["bg_panel"], fg=COLORS["text_primary"],
            font=FONTS["small"], anchor="w",
        )
        self._status_label.pack(side="left", padx=10)

        sep1 = tk.Frame(self, bg=COLORS["border"], width=1)
        sep1.pack(side="left", fill="y", padx=5, pady=4)

        self._dimensions_label = tk.Label(
            self, text="",
            bg=COLORS["bg_panel"], fg=COLORS["text_secondary"],
            font=FONTS["mono"], anchor="w",
        )
        self._dimensions_label.pack(side="left", padx=10)

        sep2 = tk.Frame(self, bg=COLORS["border"], width=1)
        sep2.pack(side="left", fill="y", padx=5, pady=4)

        self._type_label = tk.Label(
            self, text="",
            bg=COLORS["bg_panel"], fg=COLORS["text_secondary"],
            font=FONTS["mono"], anchor="w",
        )
        self._type_label.pack(side="left", padx=10)

        self._dirty_label = tk.Label(
            self, text="",
            bg=COLORS["bg_panel"], fg=COLORS["success"],
            font=FONTS["small"], anchor="e",
        )
        self._dirty_label.pack(side="right", padx=10)

    def update_info(self, model):
        """
        Actualiza la barra con info del modelo actual.

        Args:
            model: Instancia de ImageModel.
        """
        if model.has_image:
            img = model.current
            if img.ndim == 2:
                h, w = img.shape
                ch_text = "Grayscale"
            else:
                h, w = img.shape[:2]
                channels = img.shape[2]
                ch_text = f"RGB {img.dtype}" if channels == 3 else f"{channels}ch {img.dtype}"

            self._dimensions_label.config(text=f"{w}×{h} px")
            self._type_label.config(text=ch_text)

            if model.is_dirty:
                self._dirty_label.config(
                    text="● Cambios sin guardar", fg=COLORS["warning"],
                )
            else:
                self._dirty_label.config(
                    text="Sin cambios", fg=COLORS["success"],
                )
        else:
            self._dimensions_label.config(text="")
            self._type_label.config(text="")
            self._dirty_label.config(text="")

    def set_status(self, message):
        """
        Establece el mensaje de estado.

        Args:
            message: Texto a mostrar.
        """
        self._status_label.config(text=f"Estado: {message}")
