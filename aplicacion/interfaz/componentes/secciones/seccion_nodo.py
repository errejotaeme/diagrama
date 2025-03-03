import queue
import tkinter as tk
from tkinter import ttk
from aplicacion.interfaz import comunes
from aplicacion.interfaz.componentes.elementos import emergente
from aplicacion.interfaz.componentes.secciones.subsecciones import nodo


class EdicionNodo:
    """
    Clase encargada de construir los artefactos que permiten editar
    los atributos de los nodos del diagrama.

    :param ancestro: El artefacto que contiene al marco principal del área. 
    :type ancestro: tk.Frame
    :param gestor: La instancia de la clase encargada de gestionar la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor 
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk
    """  

    def __init__(self, ancestro: tk.Frame, gestor, raiz: tk.Tk):
        """
        Constructor de la clase EdicionNodo.
        """
        self._gestor = gestor
        self._raiz: tk.Tk = raiz       
        self._nodos_existentes: dict[str, str | None] = {}  # Contiene el id y valor de los nodos ingresados
        self._nodos_ubicados: dict[str, tk.Frame] = {}  # Contiene a los marcos generados dinámicamente
        self._pila_atributos_nodo: queue.LifoQueue = queue.LifoQueue() # Permite deshacer cambios
        self._contenedor_sec_nodo: tk.Frame = tk.Frame(  # Se ubica con una señal del ancestro
            ancestro, **comunes.atrb_contenedor_artf
        )
        self._contenedor_lista_nodos: tk.Frame = tk.Frame(
            self._contenedor_sec_nodo, **comunes.atrb_contenedor_artf
        )
        self._contenedor_lista_nodos.grid( 
            row=0, column=0, sticky="n", padx=(0, 20)
        )                
        self._marco_ids_nodos: tk.Frame = tk.Frame(
            self._contenedor_lista_nodos, **comunes.atrb_contenedor_artf
        )
        self._marco_ids_nodos.grid(row=0, column=0, sticky="n")
        self._construir_encab_nodos(self._marco_ids_nodos)
        self._construir_lista_nodos(self._contenedor_lista_nodos)       
        self._edicion_nodo: tk.Frame = tk.Frame(  # Contiene a la parte de edicion
            self._contenedor_sec_nodo, **comunes.atrb_contenedor_artf
        )
        self._edicion_nodo.grid(row=0, column=1, sticky="n")
        self._encabezado_ed_nodo: tk.Frame = tk.Frame(
            self._edicion_nodo, **comunes.atrb_contenedor_artf
        )
        self._encabezado_ed_nodo.grid(row=0, column=0)
        
        self._nodo_individual: nodo.EditorNodo = nodo.EditorNodo(  # Módulo de edición de nodo
            self._edicion_nodo, self._gestor, self._raiz
        )
        self._opc_nodo: tk.Frame = self._nodo_individual.artefacto()
        self._opc_nodo.grid(row=1, column=0)
        self._botonera_editar_nodo: tk.Frame = tk.Frame(  # Botonera superior de la sección
            ancestro, **comunes.atrb_contenedor_artf
        )
        self._construir_botonera_ed_nodo(
            self._botonera_editar_nodo, self._nodo_individual
        )
        self._etq_aviso: tk.Label = tk.Label(  # Notificaciones
            ancestro, text = "", **comunes.atrb_etq_aviso
        )
        self._etq_aviso.grid(
            row=2, column=0, padx=(0, 0), pady=(20,10), sticky="e"
        )        

    def activar_seccion(self) -> None:
        """
        Obtiene los nodos existentes y los ubica en el contenedor.
        """
        self._eliminar_nodos_existentes()
        self._nodos_existentes = self._obtener_nodos()
        if not self._lista_nodos is None:
            self._lista_nodos.destroy()            
        self._construir_lista_nodos(self._contenedor_lista_nodos)
        self._cargar_nodos()
        self._cargar_de_nuevo()

    def forma_nodo(self, forma: str) -> None:
        """
        Recibe la opción seleccionada en el menú asociado y la manda a ingresar
        al diccionario de modificaciones pendientes.

        :param forma: La forma del nodo.
        :type forma: str
        """
        self._nodo_individual.actualizar_forma(forma)

    def mostrar_aviso(self, aviso:str) -> None:
        """
        Actualiza la etiqueta de avisos con el texto recibido.

        :param aviso: La notificación a mostrar.
        :type aviso: str
        """
        self._etq_aviso.config(text=aviso)
        self._etq_aviso.update_idletasks()

    def ocultar_aviso(self):
        """
        Oculta el aviso que esté activo.
        """
        self._etq_aviso.config(text="")
        self._etq_aviso.update_idletasks()

    def olvidar_ubicacion(self) -> None:
        """
        Oculta el módulo cuando es seleccionado otro modo de edición.
        """
        self._contenedor_sec_nodo.grid_forget()
        self._botonera_editar_nodo.grid_forget()

    def reiniciar_opciones(self) -> None:
        """
        Restablece los valores por defecto de las entradas y los menú de
        opciones.
        """
        self._nodo_individual.reiniciar_entradas()
        self._ingr_id_nodo_editar.delete(0, tk.END)
        
    def reiniciar_pila(self) -> None:
        """
        Crea una nueva pila donde almacenar los cambios, olvidando la anterior.
        """
        self._pila_atributos_nodo = queue.LifoQueue()

    def ubicar(self) -> None:
        """
        Hace visible el módulo cuando se lo selecciona como modo de edición.
        """
        self._contenedor_sec_nodo.grid(
            row=1, column=0, sticky="ew", padx=(50,0), pady=(20,10)
        )
        self._botonera_editar_nodo.grid(
            row=0, column=0, sticky="e", pady=(25,5)
        )
        
    def vaciar_atributos(self) -> None:
        """
        Vacía el diccionario que almacena los cambios por aplicar.
        """
        self._nodo_individual.reiniciar_cambios()

    def _apilar_atributos_nodo(self, id_nodo: str) -> None:
        """
        Obtiene los atributos del nodo a partir del id y los almacena.

        :param id_nodo: El id del nodo del cual se obtienen los atributos.
        :type id_nodo: str
        """
        nodo_editado: tuple[str, dict[str, str]] = self._gestor.obtener_atributos("nodo", id_nodo)
        self._pila_atributos_nodo.put(nodo_editado)
        
    def _aplicar_cambios_nodo(self, instancia: nodo.EditorNodo) -> None: 
        """
        Aplica la edición realizada sobre el nodo.
        
        :param instancia: El módulo de edición de nodo.
        :type instancia: nodo.EditorNodo
        """
        operacion: bool = False
        id_nodo: str = self._id_nodo_editar.get()
        id_ok: bool = self._comprobar_id_nodo(id_nodo)
        valores_ingresados_ok: bool = instancia.actualizar_dict_nodo()
        if id_ok and valores_ingresados_ok:
            self._apilar_atributos_nodo(id_nodo)
            operacion = self._gestor.actualizar_elemento(
                "nodo", id_nodo , instancia.obtener_cambios()
            )
        if operacion:
            self.reiniciar_opciones() 
            self.vaciar_atributos()
        else:
            self._desapilar_atributos_nodo()

    def _cargar_de_nuevo(self) -> None:
        """
        Vuelve visible la barra de desplazamiento vertical cuando la lista
        de nodos es demasiado grande.
        """
        self._marco_desplazable_n.update_idletasks()
        alto: int = self._marco_desplazable_n.winfo_height()
        if alto > 270:
            self._barra_n.grid(row=0, column=1, sticky="ns")
        else:
            self._barra_n.grid_forget()
            
    def _cargar_nodos(self) -> None:
        """
        Ubica los nodos existentes en el contenedor de la lista de nodos.
        """
        fila: int = 0       
        for id_nodo, tex_nodo in self._nodos_existentes.items():
            marco: tk.Frame = tk.Frame(
                self._marco_desplazable_n, **comunes.atrb_contenedor_artf
            )
            t_aux: str = id_nodo + " :"
            etq_id: tk.Label = tk.Label(
                marco, text=t_aux, **comunes.atrb_etq_ayuda
            )
            etq_id.grid(row=0, column=0, sticky="w", padx=(0, 5))
            valor_nodo: tk.Text = tk.Text(marco, **comunes.atrb_filas_nodo)
            valor_nodo.tag_config("entidad", **comunes.tag_entidad)
            valor_nodo.insert(tk.END, tex_nodo)  # type: ignore
            valor_nodo.tag_add("entidad", "1.0", "end")
            valor_nodo.config(state=tk.DISABLED) 
            valor_nodo.grid(row=0, column=1)
            marco.grid(row=fila, column=0, sticky="ew", pady=(5,0))
            self._nodos_ubicados[id_nodo] = marco
            fila += 1
        
    def _comprobar_id_nodo(self, id_nodo: str) -> bool:
        """
        Verifica que el id ingresado sea válido.

        :return: El resultado de la verificación.
        :rtype: bool
        """
        res: bool = False
        if id_nodo in self._nodos_existentes.keys():
            res = True
        else:
            self._ingr_id_nodo_editar.focus_set()
            self._ingr_id_nodo_editar.select_range(0, tk.END)
        return res

    def _construir_botonera_ed_nodo(
        self, ancestro: tk.Frame, instancia: nodo.EditorNodo 
    ) -> None:
        """
        Construye la botonera superior de la sección.
        
        :param ancestro: El artefacto que contiene a la botonera.
        :type ancestro: tk.Frame
        :param instancia: El módulo de edición de nodo.
        :type instancia: nodo.EditorNodo
        """
        # Nota emergente (ne)
        self._etq_ne_id_n: tk.Label = tk.Label( 
            ancestro, text="( ? )", **comunes.atrb_etq_ayuda
        )
        tex_ne: str = "Ingresar un ID de los disponibles en la lista de nodos"
        self.ne_id_n: emergente.NotaEmergente = emergente.NotaEmergente( 
            self._etq_ne_id_n, tex_ne           
        ) 
        self._etq_ne_id_n.bind("<Enter>", self.ne_id_n.mostrar)
        self._etq_ne_id_n.bind("<Leave>", self.ne_id_n.ocultar)
        self._etq_ne_id_n.grid(row=0, column=0, padx=(0,5))
        # Nodo a editar
        self._etq_id_nodo_editar: tk.Label = tk.Label(
            ancestro, text="ID:", **comunes.atrb_etq_ayuda
        )
        self._etq_id_nodo_editar.grid(row=0, column=1, padx=(0,5))        
        self._id_nodo_editar: tk.StringVar = tk.StringVar()
        self._ingr_id_nodo_editar: tk.Entry = tk.Entry( 
            ancestro,
            textvariable=self._id_nodo_editar,
            width=3,
            **comunes.atrb_entrada
        )
        self._ingr_id_nodo_editar.grid(row=0, column=2, padx=(0,10))
        # Botones
        self._btn_aplicar_cambios_nodo: tk.Button = tk.Button(
            ancestro,
            text="Aplicar",
            command=lambda:self._aplicar_cambios_nodo(instancia),
            **comunes.atrb_btn_aplicar
        )
        self._btn_aplicar_cambios_nodo.grid(row=0, column=3, padx=(0,10))
        self._btn_deshacer_nodo: tk.Button = tk.Button(
            ancestro,
            text="Deshacer",
            command=lambda:self._deshacer_ed_nodo(),
            **comunes.atrb_btn_restablecer
        )
        self._btn_deshacer_nodo.grid(row=0, column=4)
    
    def _construir_encab_nodos(self, ancestro: tk.Frame) -> None:
        """
        Construye el encabezado de la lista de nodos.

        :param ancestro: El artefacto que contiene al encabezado.
        :type ancestro: tk.Frame
        """
        self._sep_ids_nodos_sup: ttk.Separator = ttk.Separator( 
            ancestro, orient="horizontal"
        )
        self._sep_ids_nodos_sup.grid(
            row=0, column=0, sticky="ew", padx=(0,0), pady=(3,3)
        )        
        self._etq_ids_nodos: tk.Label = tk.Label( 
            ancestro, text="LISTA DE NODOS", **comunes.atrb_etq_ayuda
        )
        self._etq_ids_nodos.grid(
            row=1, column=0, sticky="ew", padx=(20,20), pady=(3,3)
        )        
        self._sep_ids_nodos_inf: ttk.Separator = ttk.Separator(
            ancestro, orient="horizontal"
        )     
        self._sep_ids_nodos_inf.grid(
            row=2, column=0, sticky="ew", padx=(0,0), pady=(3,13)
        )

    def _construir_lista_nodos(self, ancestro: tk.Frame) -> None:
        """
        Construye el contenedor donde se cargan dinámicamente
        los nodos existentes.

        :param ancestro: El artefacto que contiene a la lista de nodos.
        :type ancestro: tk.Frame
        """
        self._estilo_lista_n: ttk.Style = ttk.Style()
        self._estilo_lista_n.configure("TFrame")
        self._estilo_lista_n.configure(
            "ListaN.TFrame", background=comunes.color_fondo_gral
        )
        self._lista_nodos: ttk.Frame = ttk.Frame(
            ancestro, style="ListaN.TFrame"
        )
        self._lista_nodos.grid(
            row=1, column=0, sticky="n", pady=(0,0)
        )
        self._cv_nodos: tk.Canvas = tk.Canvas(
            self._lista_nodos,
            width=180,
            height=280,
            highlightthickness=0,
            **comunes.atrb_contenedor_artf
        )
        self._barra_n: ttk.Scrollbar = ttk.Scrollbar(
            self._lista_nodos, orient="vertical", command=self._cv_nodos.yview
        )        
        self._marco_desplazable_n: ttk.Frame = ttk.Frame(
            self._cv_nodos, style="ListaN.TFrame"
        )
        self._marco_desplazable_n.bind(
            "<Configure>",
            lambda e: self._cv_nodos.configure(
                scrollregion=self._cv_nodos.bbox("all")
            )
        )
        self._cv_nodos.create_window(
            (0, 0), window=self._marco_desplazable_n, anchor="nw"
        )
        self._cv_nodos.grid(row=0, column=0, sticky="ew", padx=(5,5))
        self._cv_nodos.configure(yscrollcommand=self._barra_n.set)

    def _desapilar_atributos_nodo(self) -> tuple[str, dict[str, str]] | tuple[()]:
        """
        Desapila la última tupla ingresada con los atributos del nodo antes
        de realizar los cambios.

        :return: La tupla con los atributos anteriores.
        :rtype: tuple[str, dict[str, str]] | tuple[()]
        """
        try:
            res: tuple[str, dict[str, str]] = self._pila_atributos_nodo.get_nowait()
            return res
        except queue.Empty:
            return ()
        
    def _deshacer_ed_nodo(self) -> None:
        """
        Obtiene los atributos anteriores y los restablece.
        """
        cambios: tuple[str, dict[str, str]] | tuple[()] = self._desapilar_atributos_nodo()
        if cambios:
            if cambios[0] in self._gestor.lista_ids("nodo"):
                self._gestor.actualizar_elemento("nodo", cambios[0], cambios[1])
                self.reiniciar_opciones() 
                self.vaciar_atributos()

    def _eliminar_nodos_existentes(self) -> None:
        """
        Vacía las entradas con los nodos generadas dinámicamente.
        """
        for marco in self._nodos_ubicados.values():
            marco.destroy()
        self._nodos_ubicados.clear()
                
    def _obtener_nodos(self) -> dict[str, str | None]:
        """
        Devuelve los nodos registrados hasta el momento.
        """
        return self._gestor.nodos_existentes()
