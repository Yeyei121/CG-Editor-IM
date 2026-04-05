"""
Panel central de visualización de imagen.

Muestra la imagen original y la imagen procesada en paralelo,
con escalado automático y zoom interactivo con scroll.
"""
import tkinter as tk
import numpy as np
from app.config import COLORS, FONTS
from utils.image_utils import numpy_to_photoimage


class CanvasPanel(tk.Frame):
    """
    Panel central de visualización.

    Muestra la imagen original y la imagen procesada en paralelo.
    Se actualiza automáticamente al recibir notificaciones del ImageModel.

    Args:
        parent: Widget padre de tkinter.
    """

    def __init__(self, parent):
        super().__init__(parent, bg=COLORS["bg_dark"])
        self._photo_original = None
        self._photo_current = None
        self._zoom_level = 1.0
        self._last_model = None
        self._create_widgets()

    def _create_widgets(self):
        """Crea los canvas para imagen original y resultado."""
        # Contenedor 
        self._container = tk.Frame(self, bg=COLORS["bg_dark"])
        self._container.pack(fill="both", expand=True, padx=5, pady=5)

        # Panel izquierdo (original)
        self._left_frame = tk.Frame(
            self._container, bg=COLORS["bg_card"],
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        self._left_frame.pack(side="left", fill="both", expand=True, padx=(0, 3))

        self._left_title = tk.Label(
            self._left_frame, text="Original",
            bg=COLORS["bg_card"], fg=COLORS["text_secondary"], font=FONTS["label"],
        )
        self._left_title.pack(pady=(5, 0))

        self._canvas_original = tk.Canvas(
            self._left_frame, bg=COLORS["bg_dark"],
            highlightthickness=0, cursor="crosshair",
        )
        self._canvas_original.pack(fill="both", expand=True, padx=5, pady=5)

        self._left_info = tk.Label(
            self._left_frame, text="",
            bg=COLORS["bg_card"], fg=COLORS["text_secondary"], font=FONTS["small"],
        )
        self._left_info.pack(pady=(0, 5))

        # Panel derecho (resultado)
        self._right_frame = tk.Frame(
            self._container, bg=COLORS["bg_card"],
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        self._right_frame.pack(side="right", fill="both", expand=True, padx=(3, 0))

        self._right_title = tk.Label(
            self._right_frame, text="Resultado",
            bg=COLORS["bg_card"], fg=COLORS["text_secondary"], font=FONTS["label"],
        )
        self._right_title.pack(pady=(5, 0))

        self._canvas_current = tk.Canvas(
            self._right_frame, bg=COLORS["bg_dark"],
            highlightthickness=0, cursor="crosshair",
        )
        self._canvas_current.pack(fill="both", expand=True, padx=5, pady=5)

        self._right_info = tk.Label(
            self._right_frame, text="",
            bg=COLORS["bg_card"], fg=COLORS["text_secondary"], font=FONTS["small"],
        )
        self._right_info.pack(pady=(0, 5))

        # Placeholder central (Abrir imagen)
        self._placeholder = tk.Label(
            self,
            text="Abre una imagen para comenzar\n\nCtrl+O para abrir",
            bg=COLORS["bg_dark"], fg=COLORS["text_secondary"],
            font=FONTS["title"],
        )
        self._placeholder.place(relx=0.5, rely=0.5, anchor="center")

        # Eventos de zoom con scroll
        self._canvas_current.bind("<MouseWheel>", self._on_zoom)
        self._canvas_original.bind("<MouseWheel>", self._on_zoom)

    def _on_zoom(self, event):
        """Maneja el zoom con la rueda del mouse."""
        if event.delta > 0:
            self._zoom_level = min(5.0, self._zoom_level * 1.1)
        else:
            self._zoom_level = max(0.1, self._zoom_level / 1.1)
        if self._last_model is not None and self._last_model.has_image:
            self._render_model(self._last_model)

    def update_display(self, model):
        """
        Actualiza la visualización con los datos del modelo.

        Args:
            model: Instancia de ImageModel con las imágenes.
        """
        self._last_model = model

        if not model.has_image:
            self._placeholder.place(relx=0.5, rely=0.5, anchor="center")
            return

        self._placeholder.place_forget() # Método de tkinter para ocultar el widget
        self._render_model(model)

    def _render_model(self, model):
        """Renderiza las imágenes del modelo en los canvas."""
        self.update_idletasks() # Asegura que los tamaños de los canvas estén actualizados, también es método de tkinter

        canvas_w = max(self._canvas_original.winfo_width(), 200)
        canvas_h = max(self._canvas_original.winfo_height(), 200)
        max_size = (
            int(canvas_w * self._zoom_level),
            int(canvas_h * self._zoom_level),
        )

        # Original
        if model.original is not None:
            self._photo_original = numpy_to_photoimage(model.original, max_size)
            self._canvas_original.delete("all")
            self._canvas_original.create_image(
                canvas_w // 2, canvas_h // 2,
                image=self._photo_original, anchor="center",
            )
            h, w = model.original.shape[:2]
            self._left_info.config(text=f"{w} × {h} px")

        # Resultado
        if model.current is not None:
            cur = model.current
            self._photo_current = numpy_to_photoimage(cur, max_size)
            self._canvas_current.delete("all")
            cx = max(self._canvas_current.winfo_width(), 200) // 2
            cy = max(self._canvas_current.winfo_height(), 200) // 2
            self._canvas_current.create_image(
                cx, cy, image=self._photo_current, anchor="center",
            )
            if cur.ndim == 2:
                h, w = cur.shape
            else:
                h, w = cur.shape[:2]
            self._right_info.config(text=f"{w} × {h} px")
