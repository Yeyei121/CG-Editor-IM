"""
Operaciones de filtros de color.

Cada clase encapsula una operación de capa de color
usando a la Libreria_Imagenes.
"""
import numpy as np
from core.operations.base_operation import BaseOperation
from Libreria_Imagenes import (
    invertir_imagen2,
    capa_roja,
    capa_verde,
    capa_azul,
    capa_cyan,
    capa_magenta,
    capa_amarilla,
    reconstruir_imagen,
)


class InvertOperation(BaseOperation):
    """Invierte los colores de la imagen (negativo)."""

    def apply(self, img: np.ndarray) -> np.ndarray:
        return invertir_imagen2(img)

    @property
    def name(self) -> str:
        return "Invertir colores"


class RedLayerOperation(BaseOperation):
    """Extrae la capa roja de la imagen."""

    def apply(self, img: np.ndarray) -> np.ndarray:
        return capa_roja(img)

    @property
    def name(self) -> str:
        return "Capa Roja"


class GreenLayerOperation(BaseOperation):
    """Extrae la capa verde de la imagen."""

    def apply(self, img: np.ndarray) -> np.ndarray:
        return capa_verde(img)

    @property
    def name(self) -> str:
        return "Capa Verde"


class BlueLayerOperation(BaseOperation):
    """Extrae la capa azul de la imagen."""

    def apply(self, img: np.ndarray) -> np.ndarray:
        return capa_azul(img)

    @property
    def name(self) -> str:
        return "Capa Azul"


class CyanLayerOperation(BaseOperation):
    """Extrae la capa cyan de la imagen."""

    def apply(self, img: np.ndarray) -> np.ndarray:
        return capa_cyan(img)

    @property
    def name(self) -> str:
        return "Capa Cyan"


class MagentaLayerOperation(BaseOperation):
    """Extrae la capa magenta de la imagen."""

    def apply(self, img: np.ndarray) -> np.ndarray:
        return capa_magenta(img)

    @property
    def name(self) -> str:
        return "Capa Magenta"


class YellowLayerOperation(BaseOperation):
    """Extrae la capa amarilla de la imagen."""

    def apply(self, img: np.ndarray) -> np.ndarray:
        return capa_amarilla(img)

    @property
    def name(self) -> str:
        return "Capa Amarilla"


class ReconstructOperation(BaseOperation):
    """Reconstruye la imagen a partir de sus capas RGB."""

    def apply(self, img: np.ndarray) -> np.ndarray:
        r = capa_roja(img)
        g = capa_verde(img)
        b = capa_azul(img)
        return reconstruir_imagen(r, g, b)

    @property
    def name(self) -> str:
        return "Reconstruir imagen"
