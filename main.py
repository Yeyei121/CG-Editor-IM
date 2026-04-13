"""
Editor de Imágenes - Controlador principal.

Inicializa la aplicación y arranca el bucle de eventos de tkinter.
"""
from app.application import Application
from utils.animation_utils import show_startup_logo_splash as show_logo

if __name__ == "__main__":
    # Logo inicial
    show_logo("assets/startup.png")
    app = Application()
    app.run()

