"""
Panel de controles lateral derecho.

Contiene sliders, botones y controles organizados en secciones 
para manipular las propiedades de la imagen.
"""
import tkinter as tk
from tkinter import ttk
from app.config import COLORS, FONTS


class CollapsibleSection(tk.Frame):
    """
    Sección con título y contenido.

    Args:
        parent: Widget padre.
        title: Título de la sección.
    """

    def __init__(self, parent, title):
        super().__init__(parent, bg=COLORS["bg_panel"])
        self._expanded = True

        self._header = tk.Frame(self, bg=COLORS["bg_card"], cursor="hand2")
        self._header.pack(fill="x", pady=(0, 1))

        self._arrow = tk.Label(
            self._header, text="▼",
            bg=COLORS["bg_card"], fg=COLORS["accent"], font=FONTS["small"],
        )
        self._arrow.pack(side="left", padx=(8, 4), pady=4)

        self._title_label = tk.Label(
            self._header, text=title,
            bg=COLORS["bg_card"], fg=COLORS["text_primary"], font=FONTS["button"],
        )
        self._title_label.pack(side="left", pady=4)

        self._content = tk.Frame(self, bg=COLORS["bg_panel"])
        self._content.pack(fill="x", padx=5, pady=(0, 5))

        for w in (self._header, self._arrow, self._title_label):
            w.bind("<Button-1>", self._toggle)

    def _toggle(self, _event=None):
        if self._expanded:
            self._content.pack_forget()
            self._arrow.config(text="▶")
        else:
            self._content.pack(fill="x", padx=5, pady=(0, 5))
            self._arrow.config(text="▼")
        self._expanded = not self._expanded

    @property
    def content(self):
        """Frame interior donde se colocan los controles."""
        return self._content


class ControlPanel(tk.Frame):
    """
    Panel derecho con controles de ajuste de imagen.

    Contiene secciones para ajustes de brillo, capas RGB,
    transformaciones y escala de grises.

    Args:
        parent: Widget padre de tkinter.
        app: Referencia a la aplicación principal para callbacks.
    """

    def __init__(self, parent, app):
        super().__init__(parent, bg=COLORS["bg_panel"], width=280)
        self.pack_propagate(False)
        self._app = app

        # Scrollable contenedor interno para secciones
        self._canvas = tk.Canvas(self, bg=COLORS["bg_panel"], highlightthickness=0)
        self._scrollbar = tk.Scrollbar(
            self,
            orient="vertical",
            command=self._canvas.yview,
            bg=COLORS["accent"],
            activebackground=COLORS["accent"],
            troughcolor=COLORS["bg_card"],
            relief="flat",
            bd=0,
            highlightthickness=0,
        )
        self._scroll_frame = tk.Frame(self._canvas, bg=COLORS["bg_panel"])

        self._scroll_frame.bind(
            "<Configure>",
            lambda _: self._canvas.configure(scrollregion=self._canvas.bbox("all")),
        )
        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self._scroll_frame, anchor="nw",
        )
        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        self._canvas.bind(
            "<Configure>",
            lambda e: self._canvas.itemconfig(self._canvas_window, width=e.width),
        )

        self._scrollbar.pack(side="right", fill="y")
        self._canvas.pack(side="left", fill="both", expand=True)

        self._canvas.bind("<Enter>", self._bind_mousewheel)
        self._canvas.bind("<Leave>", self._unbind_mousewheel)

        self._create_sections()

    # Scroll ayuda a hacer scroll con la rueda del mouse cuando el cursor está sobre el panel

    def _bind_mousewheel(self, _event):
        self._canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mousewheel(self, _event):
        self._canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self._canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    # Helpers para crear controles con estilos
    
    def _make_label(self, parent, text):
        return tk.Label(
            parent, text=text,
            bg=COLORS["bg_panel"], fg=COLORS["text_secondary"], font=FONTS["small"],
        )

    def _make_scale(self, parent, from_, to_, command, default=0):
        scale = tk.Scale(
            parent, from_=from_, to=to_, orient="horizontal",
            bg=COLORS["bg_panel"], fg=COLORS["text_primary"],
            troughcolor=COLORS["slider_trough"],
            highlightthickness=0, sliderrelief="flat",
            activebackground=COLORS["accent"],
            font=FONTS["small"], length=220,
        )
        scale.set(default)
        scale.config(command=command)
        return scale

    def _make_button(self, parent, text, command):
        btn = tk.Button(
            parent, text=text, command=command,
            bg=COLORS["bg_card"], fg=COLORS["text_primary"],
            activebackground=COLORS["accent"], activeforeground="white",
            font=FONTS["small"], relief="flat", padx=8, pady=4, cursor="hand2",
        )
        btn.bind("<Enter>", lambda _: btn.config(bg=COLORS["bg_hover"]))
        btn.bind("<Leave>", lambda _: btn.config(bg=COLORS["bg_card"]))
        return btn

    # Secciones de controles

    def _create_sections(self):
        self._create_adjustments_section()
        self._create_rgb_section()
        self._create_transform_section()
        self._create_grayscale_section()

    # Ajustes 

    def _create_adjustments_section(self):
        section = CollapsibleSection(self._scroll_frame, "Ajustes")
        section.pack(fill="x", pady=(5, 0))
        c = section.content

        # Brillo global
        self._make_label(c, "Brillo global").pack(anchor="w")
        self._brightness_scale = self._make_scale(c, -255, 255, self._on_brightness, 0)
        self._brightness_scale.pack(fill="x")
        self._brightness_scale.bind("<ButtonPress-1>", self._on_slider_start)
        self._brightness_scale.bind("<ButtonRelease-1>", self._on_brightness_commit)

        # Brillo por canal
        self._make_label(c, "Brillo por canal").pack(anchor="w", pady=(8, 0))
        ch_frame = tk.Frame(c, bg=COLORS["bg_panel"])
        ch_frame.pack(fill="x")

        self._channel_var = tk.StringVar(value="Red")
        for ch, color in [("Red", "#FF4444"), ("Green", "#44FF44"), ("Blue", "#4444FF")]:
            tk.Radiobutton(
                ch_frame, text=ch, variable=self._channel_var, value=ch,
                bg=COLORS["bg_panel"], fg=color,
                selectcolor=COLORS["bg_card"],
                activebackground=COLORS["bg_panel"], activeforeground=color,
                font=FONTS["small"],
            ).pack(side="left", padx=4)

        self._ch_brightness_scale = self._make_scale(c, -255, 255, self._on_ch_brightness, 0)
        self._ch_brightness_scale.pack(fill="x")
        self._ch_brightness_scale.bind("<ButtonPress-1>", self._on_slider_start)
        self._ch_brightness_scale.bind("<ButtonRelease-1>", self._on_ch_brightness_commit)

        # Binarización
        self._make_label(c, "Binarización (umbral)").pack(anchor="w", pady=(8, 0))
        self._threshold_scale = self._make_scale(c, 0, 255, self._on_threshold, 128)
        self._threshold_scale.pack(fill="x")
        self._threshold_scale.bind("<ButtonPress-1>", self._on_slider_start)
        self._threshold_scale.bind("<ButtonRelease-1>", self._on_threshold_commit)

    # Capas RGB y CMY

    def _create_rgb_section(self):
        section = CollapsibleSection(self._scroll_frame, "Capas de Color")
        section.pack(fill="x", pady=(5, 0))
        c = section.content

        rgb_frame = tk.Frame(c, bg=COLORS["bg_panel"])
        rgb_frame.pack(fill="x", pady=2)
        for text, cmd, color in [
            ("R", self._app.apply_red_layer, "#FF4444"),
            ("G", self._app.apply_green_layer, "#44FF44"),
            ("B", self._app.apply_blue_layer, "#4444FF"),
        ]:
            tk.Button(
                rgb_frame, text=text, command=cmd,
                bg=color, fg="white", font=FONTS["button"],
                relief="flat", width=4, cursor="hand2",
            ).pack(side="left", padx=2, expand=True, fill="x")

        cmy_frame = tk.Frame(c, bg=COLORS["bg_panel"])
        cmy_frame.pack(fill="x", pady=2)
        for text, cmd, color in [
            ("C", self._app.apply_cyan_layer, "#00CCCC"),
            ("M", self._app.apply_magenta_layer, "#CC00CC"),
            ("Y", self._app.apply_yellow_layer, "#CCCC00"),
        ]:
            tk.Button(
                cmy_frame, text=text, command=cmd,
                bg=color, fg="white", font=FONTS["button"],
                relief="flat", width=4, cursor="hand2",
            ).pack(side="left", padx=2, expand=True, fill="x")

    # Trasnformaciones

    def _create_transform_section(self):
        section = CollapsibleSection(self._scroll_frame, "Transformaciones")
        section.pack(fill="x", pady=(5, 0))
        c = section.content

        # Rotación
        self._make_label(c, "Rotación (grados)").pack(anchor="w")
        self._rotation_scale = self._make_scale(c, 0, 360, self._on_rotation, 0)
        self._rotation_scale.pack(fill="x")
        self._rotation_scale.bind("<ButtonPress-1>", self._on_slider_start)
        self._rotation_scale.bind("<ButtonRelease-1>", self._on_rotation_commit)

        # Traslación
        self._make_label(c, "Traslación X").pack(anchor="w", pady=(8, 0))
        self._dx_scale = self._make_scale(c, -500, 500, self._on_translation, 0)
        self._dx_scale.pack(fill="x")
        self._dx_scale.bind("<ButtonPress-1>", self._on_slider_start)
        self._dx_scale.bind("<ButtonRelease-1>", self._on_translation_commit)

        self._make_label(c, "Traslación Y").pack(anchor="w")
        self._dy_scale = self._make_scale(c, -500, 500, self._on_translation, 0)
        self._dy_scale.pack(fill="x")
        self._dy_scale.bind("<ButtonPress-1>", self._on_slider_start)
        self._dy_scale.bind("<ButtonRelease-1>", self._on_translation_commit)

        # Reducir resolución
        self._make_label(c, "Reducir resolución (factor)").pack(anchor="w", pady=(8, 0))
        self._reduce_scale = self._make_scale(c, 1, 10, self._on_reduce, 1)
        self._reduce_scale.pack(fill="x")
        self._reduce_scale.bind("<ButtonPress-1>", self._on_slider_start)
        self._reduce_scale.bind("<ButtonRelease-1>", self._on_reduce_commit)

        # Zoom central
        self._make_label(c, "Zoom — área").pack(anchor="w", pady=(8, 0))
        self._zoom_area_scale = self._make_scale(c, 10, 200, lambda _: None, 50)
        self._zoom_area_scale.pack(fill="x")

        self._make_label(c, "Zoom — factor").pack(anchor="w")
        self._zoom_factor_scale = self._make_scale(c, 1, 10, lambda _: None, 2)
        self._zoom_factor_scale.pack(fill="x")

        self._make_button(c, "Aplicar Zoom", self._on_zoom_apply).pack(fill="x", pady=4)

    # Escala de grises

    def _create_grayscale_section(self):
        section = CollapsibleSection(self._scroll_frame, "Escala de Grises")
        section.pack(fill="x", pady=(5, 0))
        c = section.content

        row = tk.Frame(c, bg=COLORS["bg_panel"])
        row.pack(fill="x", pady=2)

        self._make_button(row, "Promedio", self._app.apply_grayscale_avg).pack(
            side="left", padx=2, expand=True, fill="x")
        self._make_button(row, "Luminosidad", self._app.apply_grayscale_lum).pack(
            side="left", padx=2, expand=True, fill="x")
        self._make_button(row, "Midgray", self._app.apply_grayscale_mid).pack(
            side="left", padx=2, expand=True, fill="x")

    # Callbacks de controles

    def _on_slider_start(self, _event):
        """Guarda el estado base antes de que el slider empiece a moverse."""
        self._app.start_slider_preview()

    # Brillo global
    def _on_brightness(self, value):
        from core.operations.adjustment_operations import BrightnessOperation
        self._app.apply_slider_preview(BrightnessOperation(int(float(value))))

    def _on_brightness_commit(self, _event):
        v = self._brightness_scale.get()
        self._app.commit_slider(f"Brillo ({v:+d})")

    # Brillo canal
    def _on_ch_brightness(self, value):
        from core.operations.adjustment_operations import ChannelBrightnessOperation
        ch = self._channel_var.get()
        self._app.apply_slider_preview(ChannelBrightnessOperation(ch, int(float(value))))

    def _on_ch_brightness_commit(self, _event):
        v = self._ch_brightness_scale.get()
        ch = self._channel_var.get()
        self._app.commit_slider(f"Brillo {ch} ({v:+d})")

    # Binarización
    def _on_threshold(self, value):
        from core.operations.adjustment_operations import BinarizationOperation
        self._app.apply_slider_preview(BinarizationOperation(int(float(value))))

    def _on_threshold_commit(self, _event):
        v = self._threshold_scale.get()
        self._app.commit_slider(f"Binarización (umbral={v})")

    # Rotación
    def _on_rotation(self, value):
        from core.operations.transform_operations import RotationOperation
        self._app.apply_slider_preview(RotationOperation(int(float(value))))

    def _on_rotation_commit(self, _event):
        v = self._rotation_scale.get()
        self._app.commit_slider(f"Rotación ({v}°)")

    # Traslación
    def _on_translation(self, _value):
        from core.operations.transform_operations import TranslationOperation
        dx = int(float(self._dx_scale.get()))
        dy = int(float(self._dy_scale.get()))
        self._app.apply_slider_preview(TranslationOperation(dx, dy))

    def _on_translation_commit(self, _event):
        dx = int(float(self._dx_scale.get()))
        dy = int(float(self._dy_scale.get()))
        self._app.commit_slider(f"Traslación (dx={dx}, dy={dy})")

    # Reducir resolución
    def _on_reduce(self, value):
        from core.operations.transform_operations import ReduceResolutionOperation
        self._app.apply_slider_preview(ReduceResolutionOperation(int(float(value))))

    def _on_reduce_commit(self, _event):
        v = self._reduce_scale.get()
        self._app.commit_slider(f"Reducir resolución (×{v})")

    # Zoom central (botón, no slider continuo)
    def _on_zoom_apply(self):
        if not self._app.model.has_image:
            return
        from core.operations.transform_operations import ZoomCentralOperation
        area = int(float(self._zoom_area_scale.get()))
        factor = int(float(self._zoom_factor_scale.get()))
        self._app.apply_operation(ZoomCentralOperation(area, factor))

    # Resetear sliders
    def reset_sliders(self):
        """Resetea todos los sliders a sus valores por defecto."""
        self._brightness_scale.set(0)
        self._ch_brightness_scale.set(0)
        self._threshold_scale.set(128)
        self._rotation_scale.set(0)
        self._dx_scale.set(0)
        self._dy_scale.set(0)
        self._reduce_scale.set(1)
        self._zoom_area_scale.set(50)
        self._zoom_factor_scale.set(2)
