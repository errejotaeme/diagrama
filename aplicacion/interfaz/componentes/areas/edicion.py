import tkinter as tk
from tkinter import ttk
from aplicacion.interfaz import comunes
from aplicacion.interfaz.componentes.elementos import opciones
from aplicacion.interfaz.componentes.secciones import (
    seccion_grafo, seccion_nodo, seccion_vertice, seccion_relacion
)


class AreaEdicion:
    """
    Clase encargada de construir las secciones que permiten modificar
    los atributos del diagrama.

    :param ancestro: El artefacto que contiene al marco principal del área. 
    :type ancestro: ttk.Notebook
    :param gestor: Gestiona la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk
    """    

    def __init__(self, ancestro: ttk.Notebook, gestor, raiz : tk.Tk):
        """
        Constructor de la clase AreaEdicion.
        """
        self._gestor = gestor
        self._raiz: tk.Tk = raiz
        self._seccion_activa: str = ""
        self._contenedor_artf: tk.Frame = tk.Frame(  # Marco principal
            ancestro, **comunes.atrb_contenedor_artf
        )
        self._contenedor_artf.pack()

        self._opc_edicion: opciones.MenuOpciones = opciones.MenuOpciones(
            self._contenedor_artf, 
            "Elegir modo", 
            comunes.opc_edicion,  
            comunes.atrb_menu_ed,  
            "opc_edicion",
            gestor  
        )
        self._artf_edicion:tk.OptionMenu = self._opc_edicion.artefacto()
        self._artf_edicion.grid(
            row=0, column=0, sticky="w",
            padx=(20,10), pady=(20,5)
        )

        self._etq_aviso_grafo: tk.Label = tk.Label(  # Muestra las notificaciones
            self._contenedor_artf,
            text = "",
            **comunes.atrb_etq_aviso
        )
        self._etq_aviso_grafo.grid(
            row=0, column=0,
            padx=(150, 10), pady=(20,5),
            sticky="w"
        )        
        self._seccion_grafo = seccion_grafo.EdicionGrafo(
            self._contenedor_artf, self._gestor, self._raiz
        )        
        self._seccion_nodo = seccion_nodo.EdicionNodo(
            self._contenedor_artf, self._gestor, self._raiz
        )
        self._seccion_vertice = seccion_vertice.EdicionVertice(
            self._contenedor_artf, self._gestor, self._raiz
        )
        self._seccion_relacion = seccion_relacion.EdicionRelacion(
            self._contenedor_artf, self._gestor, self._raiz
        )

 
    def artefacto(self) -> tk.Frame:
        """
        Retorna el contenedor principal de la sección.

        :return: El marco principal de la sección.
        :rtype: tk.Frame
        """
        return self._contenedor_artf
           
    def cambio_en_forma_nodo(self, mensaje: str) -> None:
        """
        Envía a la sección correspondiente el mensaje recibido desde el Gestor
        con la actualización en el menú de opción que está asociado a este
        método.

        :param mensaje: La opción seleccionada.
        :type mensaje: str
        """
        if mensaje != "Formas":
            if not self._seccion_nodo is None:
                self._seccion_nodo.forma_nodo(mensaje)
            if not self._seccion_grafo is None:
                self._seccion_grafo.forma_nodo(mensaje)               

    def cambio_en_crecimiento(self, mensaje: str) -> None:
        """
        Envía a la sección correspondiente el mensaje recibido desde el Gestor
        con la actualización en el menú de opción que está asociado a este
        método.

        :param mensaje: La opción seleccionada.
        :type mensaje: str
        """
        if mensaje != "Hacia":
            if not self._seccion_grafo is None:
                self._seccion_grafo.crecimiento(mensaje)
                
    def cambio_en_direccion(self, mensaje: str) -> None:
        """
        Envía a la sección correspondiente el mensaje recibido desde el Gestor
        con la actualización en el menú de opción que está asociado a este
        método.

        :param mensaje: La opción seleccionada.
        :type mensaje: str
        """
        if mensaje != "Sentido":
            if not self._seccion_grafo is None:
                self._seccion_grafo.direccion(mensaje)
            if not self._seccion_vertice is None:
                self._seccion_vertice.direccion(mensaje)

    def cambio_en_flecha_d(self, mensaje: str) -> None:
        """
        Envía a la sección correspondiente el mensaje recibido desde el Gestor
        con la actualización en el menú de opción que está asociado a este
        método.

        :param mensaje: La opción seleccionada.
        :type mensaje: str
        """
        if mensaje != "Delantera":
            if not self._seccion_grafo is None:
                self._seccion_grafo.flecha_d(mensaje)
            if not self._seccion_vertice is None:
                self._seccion_vertice.flecha_d(mensaje)
                
    def cambio_en_flecha_t(self, mensaje: str) -> None:
        """
        Envía a la sección correspondiente el mensaje recibido desde el Gestor
        con la actualización en el menú de opción que está asociado a este
        método.

        :param mensaje: La opción seleccionada.
        :type mensaje: str
        """
        if mensaje != "Trasera":
            if not self._seccion_grafo is None:
                self._seccion_grafo.flecha_t(mensaje)
            if not self._seccion_vertice is None:
                self._seccion_vertice.flecha_t(mensaje)

    def cambio_en_justificado(self, mensaje: str) -> None:
        """
        Envía a la sección correspondiente el mensaje recibido desde el Gestor
        con la actualización en el menú de opción que está asociado a este
        método.

        :param mensaje: La opción seleccionada.
        :type mensaje: str
        """
        if mensaje != "Párrafo":
            if not self._seccion_grafo is None:
                self._seccion_grafo.justificado(mensaje)

    def cambio_en_opc(self, mensaje: str) -> None:
        """
        Recibe desde el Gestor un mensaje con alguna de las opciones del
        menú de edición, activa la sección recibida en el mensaje y oculta
        las que corresponde.
        """
        if mensaje == "Editar grafo":
            self._vaciar_dicc_atributos()          
            self._seccion_grafo.interruptor_opc_peso()
            self._seccion_nodo.olvidar_ubicacion()
            self._seccion_vertice.olvidar_ubicacion()
            self._seccion_relacion.olvidar_ubicacion()
            self._seccion_grafo.ubicar()            
            self._seccion_activa = "Grafo"
            
        elif mensaje == "Editar nodo":
            self._vaciar_dicc_atributos()            
            self._seccion_grafo.olvidar_ubicacion()
            self._seccion_vertice.olvidar_ubicacion()
            self._seccion_relacion.olvidar_ubicacion()
            self._seccion_nodo.activar_seccion()
            self._seccion_nodo.ubicar()
            self._seccion_activa = "Nodo"
            
        elif mensaje == "Editar vértice":
            self._vaciar_dicc_atributos()
            self._seccion_vertice.interruptor_opc_peso()
            self._seccion_grafo.olvidar_ubicacion()           
            self._seccion_nodo.olvidar_ubicacion()
            self._seccion_relacion.olvidar_ubicacion()
            self._seccion_vertice.activar_seccion()
            self._seccion_vertice.ubicar()
            self._seccion_activa = "Vértice"

        elif mensaje == "Editar relación":
            self._vaciar_dicc_atributos()
            self._seccion_nodo.olvidar_ubicacion()
            self._seccion_vertice.olvidar_ubicacion()
            self._seccion_grafo.olvidar_ubicacion()
            self._seccion_relacion.activar_seccion()
            self._seccion_relacion.ubicar()            
            self._seccion_activa = "Relación"

    def mostrar_aviso_grafo(self, aviso: str) -> None:
        """
        Actualiza la etiqueta de avisos con el texto recibido.

        :param aviso: La notificación a mostrar.
        :type aviso: str
        """
        self._etq_aviso_grafo.config(text=aviso)
        self._etq_aviso_grafo.update_idletasks()

    def mostrar_aviso_nodo(self, aviso:str) -> None:
        """
        Actualiza la etiqueta de avisos de la sección Nodo
        con el texto recibido.

        :param aviso: La notificación a mostrar.
        :type aviso: str
        """        
        self._seccion_nodo.mostrar_aviso(aviso)

    def mostrar_aviso_relacion(self, aviso:str) -> None:
        """
        Actualiza la etiqueta de avisos de la sección Relación
        con el texto recibido.

        :param aviso: La notificación a mostrar.
        :type aviso: str
        """         
        self._seccion_relacion.mostrar_aviso(aviso)

    def mostrar_aviso_vertice(self, aviso:str) -> None:
        """
        Actualiza la etiqueta de avisos de la sección Vértice
        con el texto recibido.

        :param aviso: La notificación a mostrar.
        :type aviso: str
        """ 
        self._seccion_vertice.mostrar_aviso(aviso)

    def ocultar_aviso_grafo(self) -> None:
        """
        Oculta el aviso que esté visible.
        """
        self._etq_aviso_grafo.config(text="")
        self._etq_aviso_grafo.update_idletasks()

    def ocultar_aviso_nodo(self) -> None:
        """
        Oculta el aviso que esté visible en la sección Nodo.
        """
        self._seccion_nodo.ocultar_aviso()

    def ocultar_aviso_relacion(self) -> None:
        """
        Oculta el aviso que esté visible en la sección Relación.
        """
        self._seccion_relacion.ocultar_aviso()

    def ocultar_aviso_vertice(self) -> None:
        """
        Oculta el aviso que esté visible en la sección Vértice.
        """
        self._seccion_vertice.ocultar_aviso()

    def reiniciar_edicion(self) -> None:
        """
        Permite restablecer los valores iniciales de las secciones de edición.
        """
        self._seccion_nodo.reiniciar_pila()
        self._seccion_vertice.reiniciar_pila()
        self._reiniciar_opciones()

    def volver_a_cargar_nodos(self) -> None:
        """
        Luego de realizada una modificación en los nodos desde la sección,
        actualiza las opciones disponibles incluyendo los nuevos datos. Para
        ello, vuelve a activar la sección actual.
        """
        if self._seccion_activa == "Nodo":
            self.cambio_en_opc("Editar nodo")
            
    def volver_a_cargar_relaciones(self) -> None:
        """
        Luego de realizada una modificación en las relaciones desde la sección,
        actualiza las opciones disponibles incluyendo los nuevos datos. Para
        ello, vuelve a activar la sección actual.
        """
        if self._seccion_activa == "Relación":
            self.cambio_en_opc("Editar relación")

    def volver_a_cargar_vertices(self) -> None:
        """
        Luego de realizada una modificación en los vértices desde la sección,
        actualiza las opciones disponibles incluyendo los nuevos datos. Para
        ello, vuelve a activar la sección actual.
        """
        if self._seccion_activa == "Vértice":
            self.cambio_en_opc("Editar vértice")

    def _reiniciar_opciones(self) -> None:
        """
        Vacía las entradas y restablece los menú de opciones.
        """
        if not self._seccion_nodo is None: 
            self._seccion_nodo.reiniciar_opciones()
        if not self._seccion_vertice is None: 
            self._seccion_vertice.reiniciar_opciones()
        if not self._seccion_grafo is None: 
            self._seccion_grafo.reiniciar_opciones()

    def _vaciar_dicc_atributos(self) -> None:
        """
        Al navegar entre secciones, vacía los diccionarios que almacenan las
        modificaciones a realizar, para prevenir cambios no deseados.
        """          
        if not self._seccion_grafo is None:
            self._seccion_grafo.vaciar_atributos()
        if not self._seccion_nodo is None:
            self._seccion_nodo.vaciar_atributos()
        if not self._seccion_vertice is None:
            self._seccion_vertice.vaciar_atributos()            
