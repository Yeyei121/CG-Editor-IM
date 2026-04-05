"""
Gestor de historial de operaciones.

Implementa un sistema de deshacer/rehacer con un stack doble
y límite configurable de pasos.
"""
import numpy as np


class HistoryManager:
    """
    Gestiona el historial de estados de imagen para deshacer y rehacer.
    Implementa un stack doble: undo_stack y redo_stack.

    Args:
        max_steps: Número máximo de estados en el historial.
    """

    def __init__(self, max_steps=20):
        self._undo_stack = []
        self._redo_stack = []
        self._max_steps = max_steps

    def push(self, state):
        """
        Guarda un estado en el historial antes de aplicar una operación.

        Args:
            state: Estado actual de la imagen (numpy array) a guardar.
        """
        self._undo_stack.append(np.copy(state))
        if len(self._undo_stack) > self._max_steps:
            self._undo_stack.pop(0)
        self._redo_stack.clear()

    def undo(self, current_state):
        """
        Deshace la última operación.

        Args:
            current_state: Estado actual antes de deshacer.

        Returns:
            Estado anterior como numpy array, o None si no hay historial.
        """
        if not self._undo_stack:
            return None
        self._redo_stack.append(np.copy(current_state))
        return self._undo_stack.pop()

    def redo(self, current_state):
        """
        Rehace la última operación deshecha.

        Args:
            current_state: Estado actual antes de rehacer.

        Returns:
            Estado siguiente como numpy array, o None si no hay historial.
        """
        if not self._redo_stack:
            return None
        self._undo_stack.append(np.copy(current_state))
        return self._redo_stack.pop()

    def can_undo(self):
        """Indica si hay operaciones que deshacer."""
        return len(self._undo_stack) > 0

    def can_redo(self):
        """Indica si hay operaciones que rehacer."""
        return len(self._redo_stack) > 0

    def clear(self):
        """Limpia todo el historial."""
        self._undo_stack.clear()
        self._redo_stack.clear()

    def pop_last_push(self):
        """Remueve el último estado guardado (para recuperación de errores)."""
        if self._undo_stack:
            self._undo_stack.pop()
