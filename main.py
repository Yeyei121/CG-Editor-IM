"""
Editor de Imágenes - Controlador principal.

Inicializa la aplicación y arranca el bucle de eventos de tkinter.
"""
import os
from app.application import Application
from utils.animation_utils import show_startup_logo_splash

if __name__ == "__main__":
    # Logo inicial
    splash_ms = int(os.environ.get("EDITOR_SPLASH_MS", "2500"))
    show_startup_logo_splash("assets/startup.png", duration=splash_ms)

    app = Application()
    app.run()

