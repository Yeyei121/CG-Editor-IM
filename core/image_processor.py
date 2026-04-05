"""
Adaptador entre la interfaz de usuario y Libreria_Imagenes.

Centraliza todas las llamadas a Libreria_Imagenes y además 
usa operaciones que no se mapean directamente a una operación
BaseOperation (Clase Abstracta).
"""
import numpy as np
from core.operations.base_operation import BaseOperation
from Libreria_Imagenes import (
    histograma_de_imagen,
    info_imagen,
    fusionar_imagenes,
    estandarizar_imagen,
)


class ImageProcessor:
    """
    Procesador de imágenes — fachada sobre Libreria_Imagenes.

    Aplica operaciones BaseOperation y provee acceso a funciones
    utilitarias como histograma, info y fusión.
    """

    @staticmethod
    def apply(operation: BaseOperation, img: np.ndarray) -> np.ndarray:
        """
        Aplica una operación sobre una imagen.

        Args:
            operation: Operación que implementa BaseOperation.
            img: Array numpy de la imagen.

        Returns:
            Array numpy con la operación aplicada.
        """
        return operation.apply(img)

    @staticmethod
    def show_histogram(img: np.ndarray) -> None:
        """
        Muestra el histograma RGB de la imagen.

        Args:
            img: Array numpy de la imagen (3 canales).
        """
        histograma_de_imagen(img)

    @staticmethod
    def get_image_info(img: np.ndarray) -> dict:
        """
        Obtiene información de la imagen.

        Args:
            img: Array numpy de la imagen.

        Returns:
            dict con shape, dtype, size, max y min.
        """
        return info_imagen(img)

    @staticmethod
    def fuse_images(img1: np.ndarray, img2: np.ndarray, factor: float = 0.5) -> np.ndarray:
        """
        Fusiona dos imágenes con un factor de mezcla.

        Args:
            img1: Primera imagen.
            img2: Segunda imagen.
            factor: Factor de mezcla (0.0 a 1.0).

        Returns:
            Imagen fusionada como numpy array uint8.
        """
        return fusionar_imagenes(img1, img2, factor)

    @staticmethod
    def standardize(img: np.ndarray) -> np.ndarray:
        """
        Estandariza la imagen a uint8.

        Args:
            img: Array numpy de la imagen.

        Returns:
            Array numpy uint8.
        """
        return estandarizar_imagen(img)

    @staticmethod
    def ensure_3channel(img: np.ndarray) -> np.ndarray:
        """
        Asegura que la imagen tenga 3 canales (RGB).
        Convierte imágenes 2D (grayscale) a 3 canales idénticos.

        Args:
            img: Array numpy de la imagen (2D o 3D).

        Returns:
            Array numpy 3D con 3 canales, dtype uint8.
        """
        if img.ndim == 2:
            img = np.clip(img, 0, 255).astype(np.uint8)
            return np.stack([img, img, img], axis=2)
        if img.dtype != np.uint8:
            img = np.clip(img, 0, 255).astype(np.uint8)
        return img
