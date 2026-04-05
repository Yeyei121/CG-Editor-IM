"""
Interfaz base para operaciones de imagen.

Define el contrato que deben cumplir todas las operaciones
de procesamiento de imagen, siguiendo el principio Open/Closed.
"""
from abc import ABC, abstractmethod
import numpy as np


class BaseOperation(ABC):
    """Contrato que deben cumplir todas las operaciones de imagen."""

    @abstractmethod
    def apply(self, img: np.ndarray) -> np.ndarray:
        """
        Aplica la operación sobre la imagen y retorna el resultado.

        Args:
            img: Array numpy de la imagen de entrada.

        Returns:
            Array numpy con la operación aplicada.
        """
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre descriptivo de la operación."""
        pass