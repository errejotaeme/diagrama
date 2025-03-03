import copy
import tkinter as tk
from aplicacion.interfaz import comunes
from aplicacion.interfaz.componentes.elementos import emergente, opciones
from aplicacion.interfaz.componentes.secciones.subsecciones import nodo, vertice, grafo


class EdicionGrafo:
    """
    Clase encargada de construir los artefactos que permiten editar de forma
    general los atributos del diagrama.

    :param ancestro: El artefacto que contiene al marco principal del área. 
    :type ancestro: tk.Frame
    :param gestor: La instancia de la clase encargada de gestionar la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor 
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk
    """  

    def __init__(self, ancestro: tk.Frame, gestor, raiz: tk.Tk):
        """
        Constructor de la clase EdicionGrafo.
        """
        self._gestor = gestor
        self._raiz: tk.Tk = raiz
        self._almacenar_valores_por_defecto()
        self._contenedor_opc_gral: tk.Frame = tk.Frame(  # Marco principal
            ancestro, **comunes.atrb_contenedor_artf
        )
        # Instancias de los módulos de edición
        self._nodo_general: nodo.EditorNodo = nodo.EditorNodo(
            self._contenedor_opc_gral, self._gestor, self._raiz
        )
        self._opc_gral_nodos: tk.Frame = self._nodo_general.artefacto()
        self._opc_gral_nodos.grid(
            row=0, column=0, sticky="nw", padx=(10,10), pady=(3,3)
        )
        self._vertice_gral: vertice.EditorVertice = vertice.EditorVertice(
            self._contenedor_opc_gral, self._gestor, self._raiz
        )        
        self._opc_gral_vertices: tk.Frame = self._vertice_gral.artefacto()
        self._opc_gral_vertices.grid(
            row=0, column=1, sticky="nw", padx=(10,10), pady=(3,3)
        )
        self._grafo: grafo.EditorGrafo = grafo.EditorGrafo(
            self._contenedor_opc_gral, self._gestor, self._raiz
        )
        self._opc_gral_grafo: tk.Frame = self._grafo.artefacto()
        self._opc_gral_grafo.grid(
            row=1, column=0, columnspan=2, sticky="nw",padx=(10,10), pady=(3,3)
        )
        self._construir_botonera(ancestro)


    def crecimiento(self, direccion: str) -> None:
        """
        Recibe la opción seleccionada en el menú asociado y la manda a ingresar
        al diccionario de modificaciones pendientes.

        :param direccion: La dirección de crecimiento del grafo.
        :type direccion: str
        """
        if direccion == "arriba":
            self._grafo.actualizar_crecimiento("BT")
        elif direccion == "abajo":
            self._grafo.actualizar_crecimiento("TB")
        elif direccion == "izquierda":
            self._grafo.actualizar_crecimiento("RL")
        else:
            self._grafo.actualizar_crecimiento("LR")
            
    def direccion(self, sentido: str) -> None:
        """
        Recibe la opción seleccionada en el menú asociado y la manda a ingresar
        al diccionario de modificaciones pendientes.

        :param sentido: El sentido del vértice que une las entidades.
        :type sentido: str
        """
        self._vertice_gral.actualizar_direccion(sentido)

    def flecha_d(self, tipo: str) -> None:
        """
        Recibe la opción seleccionada en el menú asociado y la manda a ingresar
        al diccionario de modificaciones pendientes.

        :param tipo: El tipo de flecha delantera.
        :type tipo: str
        """
        self._vertice_gral.actualizar_flecha_d(tipo)

    def flecha_t(self, tipo: str) -> None:
        """
        Recibe la opción seleccionada en el menú asociado y la manda a ingresar
        al diccionario de modificaciones pendientes.

        :param tipo: El tipo de flecha trasera.
        :type tipo: str
        """
        self._vertice_gral.actualizar_flecha_t(tipo)
        
    def forma_nodo(self, forma: str) -> None:
        """
        Recibe la opción seleccionada en el menú asociado y la manda a ingresar
        al diccionario de modificaciones pendientes.

        :param forma: La forma de los nodos.
        :type forma: str
        """        
        self._nodo_general.actualizar_forma(forma)      

    def justificado(self, tipo: str) -> None:
        """
        Recibe la opción seleccionada en el menú asociado y la manda a ingresar
        al diccionario de modificaciones pendientes.

        :param tipo: El alineado del texto de nodos y vértices.
        :type tipo: str
        """
        if tipo == "centrado":
            self._grafo.actualizar_justificado("n")
        elif tipo == "a la izquierda":
            self._grafo.actualizar_justificado("l")
        else:
            self._grafo.actualizar_justificado("r")
        
    def interruptor_opc_peso(self) -> None:
        """
        Permite ocultar o mostrar la opción de peso del vínculo, disponible
        solo cuando se modifica un vértice específico.
        """
        self._vertice_gral.interruptor_relacion()        

    def olvidar_ubicacion(self) -> None:
        """
        Oculta el módulo cuando es seleccionado otro modo de edición.
        """
        self._contenedor_opc_gral.grid_forget()
        self._contenedor_botones.grid_forget()

    def reiniciar_opciones(self) -> None:
        """
        Restablece los valores por defecto de las entradas y los menú de
        opciones.
        """
        self._nodo_general.reiniciar_entradas()
        self._vertice_gral.reiniciar_entradas()
        self._grafo.reiniciar_entradas()

    def ubicar(self) -> None:
        """
        Hace visible el módulo cuando se lo selecciona como modo de edición.
        """
        self._contenedor_opc_gral.grid(
            row=1, column=0, sticky="ew", padx=(50,0), pady=(10,10)
        )
        self._contenedor_botones.grid(
            row=0, column=0, sticky="e", padx=(0,20), pady=(20,0)
        )
        
    def vaciar_atributos(self) -> None:
        """
        Vacía los diccionarios que almacenan los cambios por aplicar.
        """
        self._nodo_general.reiniciar_cambios()
        self._vertice_gral.reiniciar_cambios()
        self._grafo.reiniciar_cambios()

    def _almacenar_valores_por_defecto(self) -> None:
        """
        Almacena los atributos originales del diagrama para poder recuperarlos.
        """
        dict_nodos: dict[str, str] = copy.deepcopy(comunes.atrb_nodos)
        del dict_nodos["id"]
        del dict_nodos["label"]
        dict_vertices: dict[str, str] = copy.deepcopy(comunes.atrb_vertices)
        del dict_vertices["id"]
        del dict_vertices["label"]
        dict_grafo: dict[str, str] = {}        
        dict_grafo["cota"] = "25"
        dict_grafo["crecimiento"] = "TB"
        dict_grafo["fondo"] = comunes.color_fondo_grafo       
        dict_grafo["justificado"] = "n"
        self._valores_por_defecto: list[dict[str, str]] = [
            dict_nodos, dict_vertices, dict_grafo
        ]

    def _aplicar_cambios_gral(self) -> None:
        """
        Aplica los cambios ingresados.
        """
        operacion: bool = False
        cond1: bool = self._grafo.actualizar_dict_grafo() 
        cond2: bool = self._nodo_general.actualizar_dict_nodo()
        cond3: bool = self._vertice_gral.actualizar_dict_vertice()
        if cond1 or cond2 or cond3:
            cambios: list[dict[str, str | None]] = [
                self._nodo_general.obtener_cambios(),
                self._vertice_gral.obtener_cambios(), 
                self._grafo.obtener_cambios() 
            ]
            operacion = self._gestor.actualizar_grafo(cambios)
        if operacion:
            self.reiniciar_opciones()
            self.vaciar_atributos()
        
    def _aplicar_valores_iniciales(self) -> None:
        """
        Restablece los atributos originales del diagrama.
        """
        self._gestor.actualizar_grafo(self._valores_por_defecto)
        self.reiniciar_opciones()
        self.vaciar_atributos()     



    def _construir_botonera(self, ancestro: tk.Frame) -> None:
        """
        Construye la botonera superior de la sección.
        """
        self._contenedor_botones: tk.Frame = tk.Frame(
            ancestro, **comunes.atrb_contenedor_artf
        )       
        self._btn_aplicar_cambios: tk.Button = tk.Button(
            self._contenedor_botones,
            text="Aplicar",
            command=lambda:self._aplicar_cambios_gral(),
            **comunes.atrb_btn_aplicar
        )
        self._btn_aplicar_cambios.grid(
            row=0, column=0, sticky="ew", padx=(0,10), pady=(0,0)
        )
        self._btn_restablecer_todos: tk.Button = tk.Button(
            self._contenedor_botones,
            text="Valores iniciales",
            command=lambda:self._aplicar_valores_iniciales(),
            **comunes.atrb_btn_restablecer
        )                
        self._btn_restablecer_todos.grid(
            row=0, column=1, sticky="ew", padx=(10,0), pady=(0,0)
        )
