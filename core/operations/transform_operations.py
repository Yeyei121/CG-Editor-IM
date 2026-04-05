"""
Operaciones de transformación geométrica.

Cada clase encapsula una transformación espacial
usando a la Libreria_Imagenes.
"""
import numpy as np
from core.operations.base_operation import BaseOperation
from Libreria_Imagenes import (
    rotacion,
    traslacion,
    recorte,
    reducir_resolucion,
    zoom_central,
)


class RotationOperation(BaseOperation):
    """
    Rota la imagen por un ángulo dado.

    Args:
        angle: Ángulo de rotación en grados.
    """

    def __init__(self, angle: float):
        self._angle = angle

    def apply(self, img: np.ndarray) -> np.ndarray:
        return rotacion(img, self._angle)

    @property
    def name(self) -> str:
        return f"Rotación ({self._angle}°)"


class TranslationOperation(BaseOperation):
    """
    Traslada la imagen.

    Args:
        dx: Desplazamiento horizontal.
        dy: Desplazamiento vertical.
    """

    def __init__(self, dx: int, dy: int):
        self._dx = dx
        self._dy = dy

    def apply(self, img: np.ndarray) -> np.ndarray:
        return traslacion(img, self._dx, self._dy)

    @property
    def name(self) -> str:
        return f"Traslación (dx={self._dx}, dy={self._dy})"


class CropOperation(BaseOperation):
    """
    Recorta la imagen en coordenadas dadas.

    Args:
        x_ini, x_fin: Rango horizontal.
        y_ini, y_fin: Rango vertical.
    """

    def __init__(self, x_ini: int, x_fin: int, y_ini: int, y_fin: int):
        self._x_ini = x_ini
        self._x_fin = x_fin
        self._y_ini = y_ini
        self._y_fin = y_fin

    def apply(self, img: np.ndarray) -> np.ndarray:
        return recorte(img, self._x_ini, self._x_fin, self._y_ini, self._y_fin)

    @property
    def name(self) -> str:
        return f"Recorte ({self._x_ini}:{self._x_fin}, {self._y_ini}:{self._y_fin})"


class ReduceResolutionOperation(BaseOperation):
    """
    Reduce la resolución de la imagen.

    Args:
        factor: Factor de reducción entero (1-10).
    """

    def __init__(self, factor: int):
        self._factor = factor

    def apply(self, img: np.ndarray) -> np.ndarray:
        return reducir_resolucion(img, self._factor)

    @property
    def name(self) -> str:
        return f"Reducir resolución (×{self._factor})"


class ZoomCentralOperation(BaseOperation):
    """
    Aplica zoom a la región central de la imagen.

    Args:
        zoom_area: Tamaño del área central a recortar.
        zoom_factor: Factor de zoom (repetición de píxeles).
    """

    def __init__(self, zoom_area: int, zoom_factor: int):
        self._zoom_area = zoom_area
        self._zoom_factor = zoom_factor

    def apply(self, img: np.ndarray) -> np.ndarray:
        return zoom_central(img, self._zoom_area, self._zoom_factor)

    @property
    def name(self) -> str:
        return f"Zoom central (área={self._zoom_area}, ×{self._zoom_factor})"
