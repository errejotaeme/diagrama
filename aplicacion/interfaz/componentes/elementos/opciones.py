import tkinter as tk

class MenuOpciones:
    """
    Clase encargada de construir un OptionMenu y comunicarlo
    con el Gestor.

    :param ancestro: El marco donde se ubicará.
    :type ancestro: Frame
    :param opc_inicial: La opción visible cuando se crea el artefacto.
    :type opc_inicial: str
    :param opciones: Cada opción del menú desplegable.
    :type opciones: list[str]
    :param atributos: El estilo del artefacto.
    :type atributos: dict[str, str | int]
    :param ref_instancia: Un nombre que permite al gestor identificar la instancia y enrutar la opción elegida al módulo correspondiente.
    :type ref_instancia: str
    :param gestor: La instancia de la clase encargada de gestionar la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor
    """

    def __init__(
        self,
        ancestro: tk.Frame,
        opc_inicial: str,
        opciones: list[str],
        atributos: dict[str, str | int],
        ref_instancia: str,
        gestor
    ):  
        self._gestor = gestor
        self._instancia: str = ref_instancia
        self._eleccion: tk.StringVar = tk.StringVar()  # Almacenará la opción elegida
        self._eleccion.trace("w", self._cambio_opc)
        self._eleccion.set(opc_inicial)        
        self._menu_opciones: tk.OptionMenu = tk.OptionMenu(
            ancestro, self._eleccion, *opciones
        )
        self._menu_opciones.config(**atributos)  # type: ignore

    def artefacto(self) -> tk.OptionMenu:
        """
        Retorna el menú de opciones.

        :return: El menú de opciones.
        :rtype: tk.OptionMenu
        """
        return self._menu_opciones

    def obtener_eleccion(self) -> str:
        """
        Retorna la opción elegida.

        :return: Una opción del menú.
        :rtype: str
        """
        return self._eleccion.get()

    def opcion_inicial(self, opcion: str) -> None:
        """
        Establece la opción que será visible en el menú, antes que
        se interactúe con él.

        :param opcion: La opción incial.
        :type opcion: str
        """
        self._eleccion.set(opcion)

    def _cambio_opc(self, *args) -> None:
        """
        Envía al gestor la opción seleccionada. Args captura el evento de
        interacción con la instancia del artefacto.        
        """
        mensaje: list[str] = [self._instancia, self._eleccion.get()]
        self._gestor.enrutar(mensaje)
        
        
