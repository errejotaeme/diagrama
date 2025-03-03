import tkinter as tk
from aplicacion.interfaz import comunes

class NotaEmergente:
    """
    Clase encargada de gestionar y generar una nota emergente.

    :param elemento_asociado: Artefacto sobre el cual será visible la nota.
    :type elemento_asociado: Widget
    :param texto: Contenido de la nota.
    :type texto: str
    """
    
    def __init__(self, elemento_asociado, texto: str):
        """
        Constructor de la clase NotaEmergente.
        """    
        self._elemento_asociado = elemento_asociado
        self._texto: str = texto

    def mostrar(self, *args) -> None:
        """
        Vuelve visible la nota emergente si está oculta. Args captura
        los eventos vinculados a los artefactos que llaman a éste método.
        """
        x, y, _, _ = self._elemento_asociado.bbox("insert")
        x += self._elemento_asociado.winfo_rootx() + 25
        y += self._elemento_asociado.winfo_rooty() - 25

        self._ventana_nota: tk.Toplevel | None = tk.Toplevel(
            self._elemento_asociado
        )
        self._ventana_nota.wm_overrideredirect(True)
        self._ventana_nota.wm_geometry(f"+{x}+{y}")

        self._etq_texto: tk.Label = tk.Label(
            self._ventana_nota, text = self._texto, **comunes.atrb_ne
        )
        self._etq_texto.pack(ipadx=1)

    def ocultar(self, *args) -> None:
        """
        Si está visible, oculta la ventana que contiene a la nota emergente.
        Args captura los eventos vinculados a los artefactos que llaman a
        éste método.
        """
        if self._ventana_nota:
            self._ventana_nota.destroy()
            self._ventana_nota = None
