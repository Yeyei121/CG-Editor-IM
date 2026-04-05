"""
Diálogo para fusión de dos imágenes.

Permite al usuario cargar una segunda imagen y ajustar
el factor de mezcla con un slider.
"""
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np
from app.config import COLORS, FONTS, SUPPORTED_FORMATS
from utils.image_utils import load_image_as_array, numpy_to_photoimage


class FusionDialog(tk.Toplevel):
    """
    Diálogo para fusionar dos imágenes.

    Args:
        parent: Widget padre.
        app: Referencia a la aplicación principal.
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self._app = app
        self._second_image = None
        self._photo_preview = None

        self.title("Fusión de imágenes")
        self.configure(bg=COLORS["bg_dark"])
        self.geometry("500x450")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._create_widgets()

    def _create_widgets(self):
        # Instrucciones
        tk.Label(
            self, text="Fusión de imágenes",
            bg=COLORS["bg_dark"], fg=COLORS["text_primary"], font=FONTS["title"],
        ).pack(pady=(15, 5))

        tk.Label(
            self, text="Carga una segunda imagen y ajusta el factor de mezcla.",
            bg=COLORS["bg_dark"], fg=COLORS["text_secondary"], font=FONTS["label"],
        ).pack(pady=(0, 10))

        # Botón de carga y etiqueta de archivo
        btn_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        btn_frame.pack(fill="x", padx=20)

        tk.Button(
            btn_frame, text="Cargar segunda imagen",
            command=self._load_second_image,
            bg=COLORS["accent"], fg="white", font=FONTS["button"],
            relief="flat", padx=12, pady=6, cursor="hand2",
        ).pack(fill="x")

        self._file_label = tk.Label(
            btn_frame, text="Ninguna imagen seleccionada",
            bg=COLORS["bg_dark"], fg=COLORS["text_secondary"], font=FONTS["small"],
        )
        self._file_label.pack(pady=(5, 0))

        # Previsualización de la fusión
        self._preview_canvas = tk.Canvas(
            self, width=440, height=200,
            bg=COLORS["bg_card"], highlightthickness=0,
        )
        self._preview_canvas.pack(padx=20, pady=10)

        # Factor de mezcla
        slider_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        slider_frame.pack(fill="x", padx=20)

        tk.Label(
            slider_frame, text="Factor de mezcla:",
            bg=COLORS["bg_dark"], fg=COLORS["text_secondary"], font=FONTS["label"],
        ).pack(anchor="w")

        self._factor_scale = tk.Scale(
            slider_frame, from_=0.0, to=1.0, resolution=0.025,
            orient="horizontal",
            bg=COLORS["bg_dark"], fg=COLORS["text_primary"],
            troughcolor=COLORS["slider_trough"],
            highlightthickness=0, activebackground=COLORS["accent"],
            font=FONTS["small"], length=440,
            command=self._on_factor_change,
        )
        self._factor_scale.set(0.5)
        self._factor_scale.pack(fill="x")

        # Botones de aplicar y cancelar
        btn_row = tk.Frame(self, bg=COLORS["bg_dark"])
        btn_row.pack(fill="x", padx=20, pady=(10, 15))

        tk.Button(
            btn_row, text="Aplicar", command=self._apply,
            bg=COLORS["success"], fg="white", font=FONTS["button"],
            relief="flat", padx=20, pady=6, cursor="hand2",
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        tk.Button(
            btn_row, text="Cancelar", command=self.destroy,
            bg=COLORS["bg_card"], fg=COLORS["text_primary"], font=FONTS["button"],
            relief="flat", padx=20, pady=6, cursor="hand2",
        ).pack(side="right", expand=True, fill="x", padx=(5, 0))

    def _load_second_image(self):
        path = filedialog.askopenfilename(
            title="Seleccionar segunda imagen",
            filetypes=SUPPORTED_FORMATS,
            parent=self,
        )
        if not path:
            return
        try:
            self._second_image = load_image_as_array(path)
            self._file_label.config(text=path.split("/")[-1].split("\\")[-1])
            self._update_preview()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{e}", parent=self)

    def _on_factor_change(self, _value):
        self._update_preview()

    def _update_preview(self):
        if self._second_image is None or not self._app.model.has_image:
            return
        try:
            factor = float(self._factor_scale.get())
            result = self._app.processor.fuse_images(
                self._app.model.current, self._second_image, factor,
            )
            self._photo_preview = numpy_to_photoimage(result, (440, 200))
            self._preview_canvas.delete("all")
            self._preview_canvas.create_image(220, 100, image=self._photo_preview, anchor="center")
        except Exception:
            pass

    def _apply(self):
        if self._second_image is None:
            messagebox.showwarning("Aviso", "Carga una segunda imagen primero.", parent=self)
            return
        if not self._app.model.has_image:
            return
        try:
            factor = float(self._factor_scale.get())
            result = self._app.processor.fuse_images(
                self._app.model.current, self._second_image, factor,
            )
            self._app.history.push(self._app.model.current)
            from core.image_processor import ImageProcessor
            result = ImageProcessor.ensure_3channel(result)
            self._app.model.update(result)
            self._app.show_toast(f"Fusión (factor={factor:.2f})")
            self.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Error al fusionar:\n{e}", parent=self)
