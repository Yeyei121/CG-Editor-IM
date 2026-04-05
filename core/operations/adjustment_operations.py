"""
Operaciones de ajuste de imagen.

Cada clase encapsula un ajuste paramétrico (brillo, canal, umbral)
usando a la Libreria_Imagenes.
"""
import numpy as np
from core.operations.base_operation import BaseOperation
from Libreria_Imagenes import ajuste_brillo, ajuste_brillo_canal, binarizacion


class BrightnessOperation(BaseOperation):
    """
    Ajusta el brillo global de la imagen.

    Args:
        value: Valor de brillo (-255 a 255).
    """

    def __init__(self, value: int):
        self._value = value

    def apply(self, img: np.ndarray) -> np.ndarray:
        return ajuste_brillo(img, self._value)

    @property
    def name(self) -> str:
        return f"Brillo ({self._value:+d})"


class ChannelBrightnessOperation(BaseOperation):
    """
    Ajusta el brillo de un canal específico.

    Args:
        channel: "Red", "Green" o "Blue".
        value: Valor de brillo (-255 a 255).
    """

    def __init__(self, channel: str, value: int):
        self._channel = channel
        self._value = value

    def apply(self, img: np.ndarray) -> np.ndarray:
        return ajuste_brillo_canal(img, self._channel, self._value)

    @property
    def name(self) -> str:
        return f"Brillo {self._channel} ({self._value:+d})"


class BinarizationOperation(BaseOperation):
    """
    Binariza la imagen según un umbral.

    Args:
        threshold: Valor de umbral (0-255).
    """

    def __init__(self, threshold: int):
        self._threshold = threshold

    def apply(self, img: np.ndarray) -> np.ndarray:
        return binarizacion(img, self._threshold)

    @property
    def name(self) -> str:
        return f"Binarización (umbral={self._threshold})"
