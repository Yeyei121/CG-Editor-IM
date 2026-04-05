"""
Modelo de datos de la imagen activa.

Mantiene el estado de la imagen original y procesada,
y notifica a los observadores cuando el estado cambia.
"""
import numpy as np
from PIL import Image


class ImageModel:
    """
    Mantiene el estado completo de la imagen activa.
    Notifica a los observadores registrados cuando el estado cambia.

    Attributes:
        original:  Imagen original sin modificar.
        current:   Imagen con las operaciones aplicadas.
        filepath:  Ruta del archivo cargado.
        is_dirty:  True si hay cambios sin guardar.
    """

    def __init__(self):
        self._original = None
        self._current = None
        self._filepath = None
        self._is_dirty = False
        self._observers = [] #Lista de funciones a llamar cuando el estado cambia.

    #Getters para acceder a los atributos de forma controlada. 
    @property
    def original(self):
        """Array numpy de la imagen original."""
        return self._original

    @property
    def current(self):
        """Array numpy de la imagen actual (con operaciones aplicadas)."""
        return self._current

    @property
    def filepath(self):
        """Ruta del archivo de imagen cargado."""
        return self._filepath

    @property
    def is_dirty(self):
        """Indica si hay cambios sin guardar."""
        return self._is_dirty

    @property
    def has_image(self):
        """Indica si hay una imagen cargada."""
        return self._current is not None

    # Métodos para modificar el estado de la imagen y notificar a los observadores.
    def load(self, filepath):
        """
        Carga una imagen desde archivo.

        Args:
            filepath: Ruta al archivo de imagen.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            PIL.UnidentifiedImageError: Si el archivo no es una imagen válida.
        """
        pil_img = Image.open(filepath).convert("RGB")
        arr = np.array(pil_img, dtype=np.uint8)
        self._original = arr
        self._current = np.copy(arr)
        self._filepath = filepath
        self._is_dirty = False
        self.notify()

    def update(self, new_array):
        """
        Actualiza la imagen actual con un nuevo array.

        Args:
            new_array: Nuevo array numpy de la imagen.
        """
        self._current = new_array
        self._is_dirty = True
        self.notify()

    def reset(self):
        """Restaura la imagen a su estado original."""
        if self._original is not None:
            self._current = np.copy(self._original)
            self._is_dirty = False
            self.notify()

    def mark_saved(self):
        """Marca la imagen como guardada (sin cambios pendientes)."""
        self._is_dirty = False
        self.notify()

    def subscribe(self, callback):
        """
        Registra un observador que será notificado al cambiar el estado.

        Args:
            callback: Función sin argumentos a llamar en cada cambio.
        """
        self._observers.append(callback)

    def notify(self):
        """Notifica a todos los observadores registrados."""
        for cb in self._observers:
            cb()
