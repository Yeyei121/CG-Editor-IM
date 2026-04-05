"""
Utilidades de animación para la interfaz tkinter.

Implementa animaciones usando el método after() de tkinter:
transiciones de color, toast notifications y spinner de carga.
"""
import os
import tkinter as tk
from PIL import Image, ImageTk


def interpolate_color(color1, color2, factor):
    """
    Interpola linealmente entre dos colores hex.

    Args:
        color1: Color hex inicial (ej: "#FF0000").
        color2: Color hex final.
        factor: Factor de interpolación (0.0 = color1, 1.0 = color2).

    Returns:
        Color hex interpolado.
    """
    r1, g1, b1 = int(color1[1:3], 16), int(color1[3:5], 16), int(color1[5:7], 16)
    r2, g2, b2 = int(color2[1:3], 16), int(color2[3:5], 16), int(color2[5:7], 16)
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def animate_color_transition(widget, attr, color_from, color_to, steps=8, delay=18):
    """
    Anima la transición de un atributo de color de un widget.

    Args:
        widget: Widget tkinter a animar.
        attr: Nombre del atributo de configuración (ej: "bg").
        color_from: Color hex inicial.
        color_to: Color hex final.
        steps: Número de pasos de la animación.
        delay: Milisegundos entre cada paso.
    """
    def step(i):
        if i <= steps:
            color = interpolate_color(color_from, color_to, i / steps)
            try:
                widget.configure(**{attr: color})
            except tk.TclError:
                return
            widget.after(delay, step, i + 1)
    step(0)


def show_toast(parent, message, bg="#6A13CE", fg="#FFFFFF", duration=2300):
    """
    Muestra una notificación toast animada en la esquina inferior derecha.

    Args:
        parent: Widget padre de tkinter.
        message: Texto del toast.
        bg: Color de fondo.
        fg: Color del texto.
        duration: Duración en ms antes de desaparecer.

    Returns:
        El Frame del toast (para cancelación manual si es necesario).
    """
    toast = tk.Frame(parent, bg=bg, padx=16, pady=8)
    label = tk.Label(
        toast, text=message, bg=bg, fg=fg,
        font=("Segoe UI", 10, "bold"),
    )
    label.pack()

    toast.place(relx=1.0, rely=1.0, anchor="se", x=-30, y=-75)
    toast.lift()

    def destroy_toast():
        try:
            toast.destroy()
        except tk.TclError:
            pass

    parent.after(duration, destroy_toast)
    return toast


class LoadingSpinner:
    """
    Spinner de carga animado dibujado en un Canvas de tkinter.

    Args:
        parent: Widget padre.
        size: Tamaño del spinner en píxeles.
        color: Color del arco.
    """

    def __init__(self, parent, size=40, color="#4F8EF7"):
        bg = "#0D0F14"
        try:
            bg = parent.cget("bg")
        except (tk.TclError, AttributeError):
            pass
        self._canvas = tk.Canvas(
            parent, width=size, height=size,
            highlightthickness=0, bg=bg,
        )
        self._size = size
        self._color = color
        self._angle = 0
        self._running = False
        pad = 4
        self._arc = self._canvas.create_arc(
            pad, pad, size - pad, size - pad,
            start=0, extent=90, outline=color, width=3, style="arc",
        )

    def start(self):
        """Inicia la animación del spinner."""
        self._running = True
        self._animate()

    def stop(self):
        """Detiene la animación del spinner."""
        self._running = False

    def _animate(self):
        if not self._running:
            return
        self._angle = (self._angle + 12) % 360
        self._canvas.itemconfigure(self._arc, start=self._angle)
        self._canvas.after(30, self._animate)

    def show(self, **kwargs):
        """Muestra el spinner en la posición especificada."""
        self._canvas.place(**kwargs)
        self.start()

    def hide(self):
        """Oculta el spinner y detiene la animación."""
        self.stop()
        self._canvas.place_forget()


def _center_window(win, width, height):
    """Centra una ventana en la pantalla."""
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = max((sw - width) // 2, 0)
    y = max((sh - height) // 2, 0)
    win.geometry(f"{width}x{height}+{x}+{y}")


def show_startup_logo_splash(image_path, duration=2500, max_width=520, max_height=320):
    """
    Muestra un splash minimalista con solo el logo.

    Args:
        image_path: Ruta al archivo de imagen del logo.
        duration: Duracion total del splash en ms.
        max_width: Ancho maximo permitido para el logo.
        max_height: Alto maximo permitido para el logo.
    """
    splash = tk.Tk()
    splash.configure(bg="black")
    splash.resizable(False, False)
    splash.overrideredirect(True)

    logo_label = tk.Label(splash, bg="black", bd=0, highlightthickness=0)
    logo_label.pack(fill="both", expand=True)

    if image_path and os.path.exists(image_path):
        try:
            img = Image.open(image_path)
            if img.mode not in ("RGB", "RGBA"):
                img = img.convert("RGBA")

            # Recorta bordes transparentes para evitar que el logo se vea pegado
            # a una esquina por padding interno del PNG.
            if img.mode == "RGBA":
                alpha = img.getchannel("A")
                bbox = alpha.getbbox()
                if bbox:
                    img = img.crop(bbox)

            # Limita el tamano para que el splash no sea excesivamente grande.
            w, h = img.size
            scale = min(max_width / max(1, w), max_height / max(1, h), 1.0)
            if scale < 1.0:
                new_w = max(1, int(w * scale))
                new_h = max(1, int(h * scale))
                img = img.resize((new_w, new_h), Image.LANCZOS)

            photo = ImageTk.PhotoImage(img)
            logo_label.configure(image=photo)
            logo_label.image = photo
            w, h = img.size
            _center_window(splash, w, h)
            splash.after(10, lambda: _center_window(splash, w, h))
        except Exception:
            fallback_w, fallback_h = 360, 120
            _center_window(splash, fallback_w, fallback_h)
            logo_label.configure(
                text="No se pudo cargar startup.png",
                fg="#FCA5A5",
                bg="#0D0F14",
                font=("Segoe UI", 10, "bold"),
            )
    else:
        fallback_w, fallback_h = 360, 120
        _center_window(splash, fallback_w, fallback_h)
        logo_label.configure(
            text="Falta assets/startup.png",
            fg="#A5B4FC",
            bg="#0D0F14",
            font=("Segoe UI", 10, "bold"),
        )

    splash.attributes("-topmost", True)
    splash.after(20, lambda: splash.attributes("-topmost", False))

    splash.after(duration, splash.destroy)
    splash.mainloop()
