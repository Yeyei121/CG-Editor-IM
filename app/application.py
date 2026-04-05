"""
Clase principal Application — controlador raíz.

Coordina el modelo de datos, el procesador de imágenes,
el historial de operaciones y la interfaz gráfica.
"""
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import numpy as np

from app.config import COLORS, SUPPORTED_FORMATS, HISTORY_MAX_STEPS
from core.image_model import ImageModel
from core.history_manager import HistoryManager
from core.image_processor import ImageProcessor
from ui.main_window import MainWindow
from utils.animation_utils import show_toast


class Application:
    """
    Controlador raíz de la aplicación.

    Crea y conecta todos los componentes: modelo, historial,
    procesador y ventana principal. Maneja los eventos de alto nivel.
    """

    def __init__(self):
        self.root = tk.Tk()
        self.model = ImageModel()
        self.history = HistoryManager(max_steps=HISTORY_MAX_STEPS)
        self.processor = ImageProcessor()

        # Estado temporal para operaciones con sliders
        self._slider_base = None

        # Ventana principal
        self.window = MainWindow(self.root, self)

        # Suscripción a cambios en el modelo para actualizar la UI
        self.model.subscribe(self._on_model_changed)

        # Atajos de teclado
        self._setup_bindings()

    def run(self):
        """Inicia el bucle de eventos de tkinter."""
        self.root.mainloop()

    # Modelo de Observador

    def _on_model_changed(self):
        """Callback invocado cuando el modelo cambia de estado."""
        self.window.canvas_panel.update_display(self.model)
        self.window.status_bar.update_info(self.model)
        if self.model.filepath:
            filename = os.path.basename(self.model.filepath)
            dirty = " *" if self.model.is_dirty else ""
            self.window.update_topbar_info(f"{filename}{dirty}")

    # Saltos de teclado y operaciones de alto nivel

    def _setup_bindings(self):
        """Registra atajos de teclado globales."""
        self.root.bind("<Control-o>", lambda _: self.open_image())
        self.root.bind("<Control-s>", lambda _: self.save_image())
        self.root.bind("<Control-z>", lambda _: self.undo())
        self.root.bind("<Control-y>", lambda _: self.redo())
        self.root.bind("<Control-r>", lambda _: self.reset_image())

    # Operaciones de archivo

    def open_image(self):
        """Abre un diálogo para cargar una imagen."""
        path = filedialog.askopenfilename(
            title="Abrir imagen",
            filetypes=SUPPORTED_FORMATS,
        )
        if not path:
            return
        try:
            self.model.load(path)
            self.history.clear()
            self.window.control_panel.reset_sliders()
            self.window.status_bar.set_status("Imagen cargada")
            self.show_toast("Imagen cargada")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir la imagen:\n{e}")

    def save_image(self):
        """Abre un diálogo para guardar la imagen actual."""
        if not self.model.has_image:
            messagebox.showinfo("Aviso", "No hay imagen para guardar.")
            return
        path = filedialog.asksaveasfilename(
            title="Guardar imagen",
            defaultextension=".png",
            filetypes=[("PNG", "*.png"), ("JPEG", "*.jpg *.jpeg")],
        )
        if not path:
            return
        try:
            from utils.image_utils import save_array_as_image
            save_array_as_image(self.model.current, path)
            self.model.mark_saved()
            self.window.status_bar.set_status("Imagen guardada")
            self.show_toast("Imagen guardada")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar:\n{e}")

    # Historial de operaciones

    def undo(self):
        """Deshace la última operación."""
        if not self.model.has_image:
            return
        state = self.history.undo(self.model.current)
        if state is not None:
            self.model.update(state)
            self.window.status_bar.set_status("Deshacer")
        else:
            self.window.status_bar.set_status("Nada que deshacer")

    def redo(self):
        """Rehace la última operación deshecha."""
        if not self.model.has_image:
            return
        state = self.history.redo(self.model.current)
        if state is not None:
            self.model.update(state)
            self.window.status_bar.set_status("Rehacer")
        else:
            self.window.status_bar.set_status("Nada que rehacer")

    def reset_image(self):
        """Restaura la imagen original."""
        if not self.model.has_image:
            return
        self.history.push(self.model.current)
        self.model.reset()
        self.window.control_panel.reset_sliders()
        self.window.status_bar.set_status("Imagen restaurada")
        self.show_toast("Imagen restaurada")

    # Operación genérica

    def apply_operation(self, operation):
        """
        Aplica una operación BaseOperation a la imagen actual.

        Args:
            operation: Instancia de BaseOperation.
        """
        if not self.model.has_image:
            return
        try:
            self.history.push(self.model.current)
            result = self.processor.apply(operation, self.model.current)
            result = self.processor.ensure_3channel(result)
            self.model.update(result)
            self.window.status_bar.set_status(operation.name)
            self.show_toast(operation.name)
        except Exception as e:
            self.history.pop_last_push()
            messagebox.showerror("Error", f"Error al aplicar {operation.name}:\n{e}")

    # Vista previa de sliders

    def start_slider_preview(self):
        """Guarda el estado base antes de iniciar preview con slider."""
        if self.model.has_image:
            self._slider_base = np.copy(self.model.current)

    def apply_slider_preview(self, operation):
        """
        Aplica una operación sobre el estado base del slider.

        Args:
            operation: Instancia de BaseOperation.
        """
        if self._slider_base is None:
            return
        try:
            result = operation.apply(self._slider_base)
            result = self.processor.ensure_3channel(result)
            self.model.update(result)
        except Exception:
            pass

    def commit_slider(self, name=""):
        """
        Confirma la operación del slider en el historial.

        Args:
            name: Nombre descriptivo de la operación para el toast.
        """
        if self._slider_base is not None:
            self.history.push(self._slider_base)
            self._slider_base = None
            self.window.status_bar.set_status(name)
            if name:
                self.show_toast(name)

    # Operaciones de imagen específicas

    def apply_invert(self):
        from core.operations.color_operations import InvertOperation
        self.apply_operation(InvertOperation())

    def apply_reconstruct(self):
        from core.operations.color_operations import ReconstructOperation
        self.apply_operation(ReconstructOperation())

    def apply_red_layer(self):
        from core.operations.color_operations import RedLayerOperation
        self.apply_operation(RedLayerOperation())

    def apply_green_layer(self):
        from core.operations.color_operations import GreenLayerOperation
        self.apply_operation(GreenLayerOperation())

    def apply_blue_layer(self):
        from core.operations.color_operations import BlueLayerOperation
        self.apply_operation(BlueLayerOperation())

    def apply_cyan_layer(self):
        from core.operations.color_operations import CyanLayerOperation
        self.apply_operation(CyanLayerOperation())

    def apply_magenta_layer(self):
        from core.operations.color_operations import MagentaLayerOperation
        self.apply_operation(MagentaLayerOperation())

    def apply_yellow_layer(self):
        from core.operations.color_operations import YellowLayerOperation
        self.apply_operation(YellowLayerOperation())

    def apply_grayscale_avg(self):
        from core.operations.grayscale_operations import PromedioOperation
        self.apply_operation(PromedioOperation())

    def apply_grayscale_lum(self):
        from core.operations.grayscale_operations import LuminosidadOperation
        self.apply_operation(LuminosidadOperation())

    def apply_grayscale_mid(self):
        from core.operations.grayscale_operations import MidgrayOperation
        self.apply_operation(MidgrayOperation())

    # Funciones de UI adicionales

    def show_histogram(self):
        """Muestra el histograma de la imagen actual en una ventana separada."""
        if not self.model.has_image:
            messagebox.showinfo("Aviso", "No hay imagen cargada.")
            return
        try:
            self.processor.show_histogram(self.model.current)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar histograma:\n{e}")

    def show_info(self):
        """Muestra información de la imagen actual."""
        if not self.model.has_image:
            messagebox.showinfo("Aviso", "No hay imagen cargada.")
            return
        info = self.processor.get_image_info(self.model.current)
        shape = info["shape"]
        msg = (
            f"Dimensiones (shape): {shape}\n"
            f"Tipo de dato (dtype): {info['dtype']}\n"
            f"Tamaño total: {info['size']:,} elementos\n"
            f"Valor máximo: {info['max']}\n"
            f"Valor mínimo: {info['min']}"
        )
        if len(shape) >= 2:
            msg += f"\n\nResolución: {shape[1]} × {shape[0]} px"
        messagebox.showinfo("Información de imagen", msg)

    def show_fusion_dialog(self):
        """Abre el diálogo de fusión de imágenes."""
        if not self.model.has_image:
            messagebox.showinfo("Aviso", "Carga una imagen primero.")
            return
        from ui.dialogs.fusion_dialog import FusionDialog
        FusionDialog(self.root, self)

    def show_crop_dialog(self):
        """Abre el diálogo de recorte."""
        if not self.model.has_image:
            messagebox.showinfo("Aviso", "Carga una imagen primero.")
            return
        from ui.dialogs.recorte_dialog import RecorteDialog
        RecorteDialog(self.root, self)

    # Funciones de notificación (Toast)

    def show_toast(self, message):
        """
        Muestra una notificación toast breve.

        Args:
            message: Texto del toast.
        """
        show_toast(self.root, message)
