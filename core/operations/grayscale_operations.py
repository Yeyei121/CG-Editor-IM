"""
Operaciones de escala de grises.

Cada clase encapsula una técnica de conversión a grises
usando a la Libreria_Imagenes.
"""
import numpy as np
from core.operations.base_operation import BaseOperation
from Libreria_Imagenes import promedio, luminosidad, midgray


class PromedioOperation(BaseOperation):
    """Convierte a escala de grises usando promedio de canales."""

    def apply(self, img: np.ndarray) -> np.ndarray:
        return promedio(img)

    @property
    def name(self) -> str:
        return "Grises (Promedio)"


class LuminosidadOperation(BaseOperation):
    """Convierte a escala de grises usando ponderación de luminosidad."""

    def apply(self, img: np.ndarray) -> np.ndarray:
        return luminosidad(img)

    @property
    def name(self) -> str:
        return "Grises (Luminosidad)"


class MidgrayOperation(BaseOperation):
    """Convierte a escala de grises usando promedio de max y min."""

    def apply(self, img: np.ndarray) -> np.ndarray:
        return midgray(img)

    @property
    def name(self) -> str:
        return "Grises (Midgray)"
