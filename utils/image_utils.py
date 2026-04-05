"""
Utilidades de conversión de formatos de imagen.

Provee funciones para convertir entre numpy arrays, PIL Images
y tkinter PhotoImages.
"""
import numpy as np
from PIL import Image, ImageTk


def numpy_to_pil(arr):
    """
    Convierte un array numpy a PIL Image.

    Args:
        arr: Array numpy (uint8, float, 2D o 3D).

    Returns:
        PIL.Image en modo L, RGB o RGBA según la entrada.
    """
    if arr.dtype != np.uint8:
        arr = np.clip(arr, 0, 255).astype(np.uint8)
    if arr.ndim == 2:
        return Image.fromarray(arr, mode="L")
    elif arr.shape[2] == 4:
        return Image.fromarray(arr, mode="RGBA")
    else:
        return Image.fromarray(arr, mode="RGB")


def numpy_to_photoimage(arr, max_size=None):
    """
    Convierte un array numpy a PhotoImage de tkinter.

    Args:
        arr: Array numpy (uint8, RGB, RGBA o L(grayscale)).
        max_size: Tupla (max_width, max_height) para redimensionar.

    Returns:
        ImageTk.PhotoImage para usar en tkinter.
    """
    pil_img = numpy_to_pil(arr)
    if max_size:
        pil_img.thumbnail(max_size, Image.LANCZOS) # LANCZOS es un algoritmo para redimensionar imágenes de alta calidad, se ajusta al tamaño máximo sin distorsionar la imagen.
    return ImageTk.PhotoImage(pil_img)


def load_image_as_array(filepath):
    """
    Carga una imagen desde archivo y la convierte a numpy array RGB uint8.

    Args:
        filepath: Ruta al archivo de imagen.

    Returns:
        numpy array de la imagen en formato RGB uint8.
    """
    pil_img = Image.open(filepath).convert("RGB")
    return np.array(pil_img, dtype=np.uint8)


def save_array_as_image(arr, filepath):
    """
    Guarda un numpy array como archivo de imagen.

    Args:
        arr: Array numpy de la imagen.
        filepath: Ruta de destino.
    """
    pil_img = numpy_to_pil(arr)
    if pil_img.mode == "RGBA" and filepath.lower().endswith((".jpg", ".jpeg")): # jpg no soporta transparencia, convertir a RGB
        pil_img = pil_img.convert("RGB")
    pil_img.save(filepath)
