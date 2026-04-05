"""
Cuadro de diálogo para definir coordenadas de recorte.

Permite al usuario ingresar las coordenadas xIni, xFin, yIni, yFin
para recortar la imagen actual.
"""
import tkinter as tk
from tkinter import messagebox
from app.config import COLORS, FONTS


class RecorteDialog(tk.Toplevel):
    """
    Diálogo para recortar la imagen con coordenadas específicas.

    Args:
        parent: Widget padre.
        app: Referencia a la aplicación principal.
    """

    def __init__(self, parent, app):
        super().__init__(parent)
        self._app = app

        self.title("Recorte de imagen")
        self.configure(bg=COLORS["bg_dark"])
        self.geometry("360x320")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self._create_widgets()

    def _create_widgets(self):
        tk.Label(
            self, text="Recorte de imagen",
            bg=COLORS["bg_dark"], fg=COLORS["text_primary"], font=FONTS["title"],
        ).pack(pady=(15, 5))

        # Mostrar dimensiones actuales si hay imagen cargada
        if self._app.model.has_image:
            h, w = self._app.model.current.shape[:2]
            tk.Label(
                self, text=f"Dimensiones actuales: {w} × {h} px",
                bg=COLORS["bg_dark"], fg=COLORS["text_secondary"], font=FONTS["small"],
            ).pack(pady=(0, 10))

        # Inputs de coordenadas
        fields_frame = tk.Frame(self, bg=COLORS["bg_dark"])
        fields_frame.pack(padx=30, fill="x")

        self._entries = {}
        for label, key, default in [
            ("X inicio:", "x_ini", "0"),
            ("X fin:", "x_fin", str(w) if self._app.model.has_image else "100"),
            ("Y inicio:", "y_ini", "0"),
            ("Y fin:", "y_fin", str(h) if self._app.model.has_image else "100"),
        ]:
            row = tk.Frame(fields_frame, bg=COLORS["bg_dark"])
            row.pack(fill="x", pady=4)

            tk.Label(
                row, text=label, width=10, anchor="w",
                bg=COLORS["bg_dark"], fg=COLORS["text_secondary"], font=FONTS["label"],
            ).pack(side="left")

            entry = tk.Entry(
                row, bg=COLORS["bg_card"], fg=COLORS["text_primary"],
                insertbackground=COLORS["text_primary"],
                font=FONTS["mono"], relief="flat", width=12,
            )
            entry.insert(0, default)
            entry.pack(side="left", padx=(5, 0), fill="x", expand=True)
            self._entries[key] = entry

        # Botones de aplicar y cancelar
        btn_row = tk.Frame(self, bg=COLORS["bg_dark"])
        btn_row.pack(fill="x", padx=30, pady=(20, 15))

        tk.Button(
            btn_row, text="Recortar", command=self._apply,
            bg=COLORS["success"], fg="white", font=FONTS["button"],
            relief="flat", padx=20, pady=6, cursor="hand2",
        ).pack(side="left", expand=True, fill="x", padx=(0, 5))

        tk.Button(
            btn_row, text="Cancelar", command=self.destroy,
            bg=COLORS["bg_card"], fg=COLORS["text_primary"], font=FONTS["button"],
            relief="flat", padx=20, pady=6, cursor="hand2",
        ).pack(side="right", expand=True, fill="x", padx=(5, 0))

    def _apply(self):
        if not self._app.model.has_image:
            return
        try:
            x_ini = int(self._entries["x_ini"].get())
            x_fin = int(self._entries["x_fin"].get())
            y_ini = int(self._entries["y_ini"].get())
            y_fin = int(self._entries["y_fin"].get())
        except ValueError:
            messagebox.showerror(
                "Error", "Las coordenadas deben ser números enteros.", parent=self,
            )
            return

        if x_ini >= x_fin or y_ini >= y_fin:
            messagebox.showerror(
                "Error",
                "Los valores iniciales deben ser menores que los finales.",
                parent=self,
            )
            return

        from core.operations.transform_operations import CropOperation
        op = CropOperation(x_ini, x_fin, y_ini, y_fin)
        self._app.apply_operation(op)
        self.destroy()
