import queue
import tkinter as tk
from tkinter import ttk
from aplicacion.interfaz import comunes
from aplicacion.interfaz.componentes.elementos import emergente
from aplicacion.interfaz.componentes.secciones.subsecciones import vertice


class EdicionVertice:
    """
    Clase encargada de construir los artefactos que permiten editar
    los atributos de los vértices del diagrama.

    :param ancestro: El artefacto que contiene al marco principal del área. 
    :type ancestro: tk.Frame
    :param gestor: La instancia de la clase encargada de gestionar la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor 
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk
    """  

    def __init__(self, ancestro: tk.Frame, gestor, raiz: tk.Tk):
        """
        Constructor de la clase EdicionVertice.
        """
        self._gestor = gestor
        self._raiz: tk.Tk = raiz        
        self._vertices_existentes: dict[str, list[list[str | None]]] = {}  # Contiene el id y valor de los vertices ingresados
        self._vertices_ubicados: dict[str, tk.Frame] = {}  # Contiene a los marcos generados dinámicamente
        self._pila_atributos_vertice: queue.LifoQueue = queue.LifoQueue()  # Permite deshacer cambios
        self._contenedor_sec_vertice: tk.Frame = tk.Frame(  # Se ubica con una señal del ancestro
            ancestro, **comunes.atrb_contenedor_artf
        )
        self._contenedor_lista_vertices: tk.Frame = tk.Frame(
            self._contenedor_sec_vertice,**comunes.atrb_contenedor_artf
        )
        self._contenedor_lista_vertices.grid(
            row=0, column=0, sticky="n", padx=(20, 10), pady=(0,0)
        )
        self._encabezado_lista_vertices: tk.Frame = tk.Frame(
            self._contenedor_lista_vertices,**comunes.atrb_contenedor_artf
        )
        self._encabezado_lista_vertices.grid(row=0, column=0, sticky="n")
        self._construir_encab_vertices(self._encabezado_lista_vertices)
        self._construir_lista_vertices(self._contenedor_lista_vertices)
        self._vertice_individual: vertice.EditorVertice = vertice.EditorVertice(  # Módulo de edición de vértice
            self._contenedor_sec_vertice, self._gestor, self._raiz
        )
        self._opc_vertice: tk.Frame = self._vertice_individual.artefacto()
        self._opc_vertice.grid(row=0, column=1, sticky="e")
        self._vertice_individual.activar_interruptor()  # Muestra la opción peso
        self._botonera_ed_vertice: tk.Frame = tk.Frame(  # Botonera superior de la sección
            ancestro, **comunes.atrb_contenedor_artf
        )
        self._construir_botonera_vertices(
            self._botonera_ed_vertice, self._vertice_individual
        )
        self._etq_aviso: tk.Label = tk.Label(  # Notificaciones
            ancestro, text = "", **comunes.atrb_etq_aviso
        )
        self._etq_aviso.grid(
            row=2, column=0, padx=(0, 0), pady=(20,10), sticky="e"
        )

    def activar_seccion(self) -> None:
        """
        Obtiene los vértices existentes y los ubica en el contenedor.
        """
        self._eliminar_vertices_existentes()
        self._vertices_existentes = self._obtener_vertices()
        if not self._lista_vertices is None:
            self._lista_vertices.destroy()            
        self._construir_lista_vertices(self._contenedor_lista_vertices)
        self._cargar_vertices()
        self._cargar_de_nuevo()
        
    def direccion(self, sentido: str) -> None:
        """
        Recibe la opción seleccionada en el menú asociado y la manda a ingresar
        al diccionario de modificaciones pendientes.

        :param sentido: El sentido del vértice que une las entidades.
        :type sentido: str
        """
        self._vertice_individual.actualizar_direccion(sentido)

    def flecha_d(self, tipo: str) -> None:
        """
        Recibe la opción seleccionada en el menú asociado y la manda a ingresar
        al diccionario de modificaciones pendientes.

        :param tipo: El tipo de flecha delantera.
        :type tipo: str
        """
        self._vertice_individual.actualizar_flecha_d(tipo)

    def flecha_t(self, tipo: str) -> None:
        """
        Recibe la opción seleccionada en el menú asociado y la manda a ingresar
        al diccionario de modificaciones pendientes.

        :param tipo: El tipo de flecha trasera.
        :type tipo: str
        """
        self._vertice_individual.actualizar_flecha_t(tipo)

    def interruptor_opc_peso(self) -> None:
        """
        Permite ocultar o mostrar la opción de peso del vínculo, disponible
        solo cuando se modifica un vértice específico.
        """
        self._vertice_individual.interruptor_relacion()
        
    def mostrar_aviso(self, aviso:str) -> None:
        """
        Actualiza la etiqueta de avisos con el texto recibido.

        :param aviso: La notificación a mostrar.
        :type aviso: str
        """
        self._etq_aviso.config(text=aviso)
        self._etq_aviso.update_idletasks()

    def ocultar_aviso(self) -> None:
        """
        Oculta el aviso que esté visible.
        """
        self._etq_aviso.config(text="")
        self._etq_aviso.update_idletasks()
        
    def olvidar_ubicacion(self) -> None:
        """
        Oculta el módulo cuando es seleccionado otro modo de edición.
        """
        self._botonera_ed_vertice.grid_forget()
        self._contenedor_sec_vertice.grid_forget()

    def reiniciar_opciones(self) -> None:
        """
        Restablece los valores por defecto de las entradas y los menú de
        opciones.
        """
        self._vertice_individual.reiniciar_entradas()
        self._ingr_id_vertice_editar.delete(0, tk.END)     

    def reiniciar_pila(self) -> None:
        """
        Crea una nueva pila donde almacenar los cambios, olvidando la anterior.
        """
        self._pila_atributos_vertice = queue.LifoQueue()

    def ubicar(self) -> None:
        """
        Hace visible el módulo cuando se lo selecciona como modo de edición.
        """
        self._contenedor_sec_vertice.grid(
            row=1, column=0, sticky="ew",padx=(10,0), pady=(20,10)
        )
        self._botonera_ed_vertice.grid(
            row=0, column=0, sticky="e", padx=(0,0), pady=(25,5)
        )
        
    def vaciar_atributos(self) -> None:
        """
        Vacía el diccionario que almacena los cambios por aplicar.
        """
        self._vertice_individual.reiniciar_cambios()

    def _apilar_atributos_vertice(self, id_vertice: str) -> None:
        """
        Obtiene los atributos del vértice a partir del id y los almacena.

        :param id_vertice: El id del vértice del cual se obtienen los atributos.
        :type id_vertice: str
        """
        vertice_editado: tuple[str, dict[str, str]] = self._gestor.obtener_atributos(
            "vertice", id_vertice
        )
        self._pila_atributos_vertice.put(vertice_editado)

    def _aplicar_cambios_vertice(self, instancia: vertice.EditorVertice) -> None:
        """
        Aplica la edición realizada sobre el vértice.
        
        :param instancia: El módulo de edición de vértice.
        :type instancia: vertice.EditorVertice
        """
        operacion: bool = False
        id_vertice: str = self._id_vertice_editar.get()
        id_ok: bool = self._comprobar_id_vertice(id_vertice)
        valores_ingresados_ok: bool = instancia.actualizar_dict_vertice()
        if id_ok and valores_ingresados_ok:
            self._apilar_atributos_vertice(id_vertice)
            operacion = self._gestor.actualizar_elemento(
                "vertice", id_vertice, instancia.obtener_cambios()
            )
        if operacion:
            self.reiniciar_opciones() 
            self.vaciar_atributos()
        else:
            self._desapilar_atributos_vertice()
        pass
        
    def _cargar_de_nuevo(self) -> None:
        """
        Vuelve visible la barra de desplazamiento vertical cuando la lista
        de vértices es demasiado grande.
        """
        self._marco_desplazable_v.update_idletasks()
        alto: int = self._marco_desplazable_v.winfo_height()
        if alto > 350:
            self._barra_v.grid(row=0, column=1, sticky="ns")
        else:
            self._barra_v.grid_forget()

    def _cargar_vertices(self) -> None:
        """
        Ubica los nodos existentes en el contenedor de la lista de vértices.
        """    
        fila:int = 0
        for id_vertice, relaciones in self._vertices_existentes.items():
            marco: tk.Frame = tk.Frame(
                self._marco_desplazable_v, **comunes.atrb_contenedor_artf
            )
            t_aux:str = "ID : " + id_vertice
            etq_id: tk.Label = tk.Label(
                marco, text=t_aux, **comunes.atrb_etq_ayuda
            )
            etq_id.grid(row=0, column=0, sticky="w", pady=(0,5))
            fila_marco:int = 1
            for relacion in relaciones:  # type: ignore            
                ent1: tk.Text = tk.Text(marco, **comunes.atrb_filas_vertice)
                ent1.tag_config("entidad", **comunes.tag_entidad)
                ent1.insert(tk.END, relacion[0])  # type: ignore
                ent1.config(state=tk.DISABLED)
                ent1.tag_add("entidad", "1.0", "end")
                ent1.grid(row=fila_marco, column=0, padx=(0,10), pady=(0,7))                
                rel: tk.Text = tk.Text(marco, **comunes.atrb_filas_vertice)
                rel.tag_config("relacion", **comunes.tag_relacion)
                rel.insert(tk.END, relacion[1])  # type: ignore
                rel.config(state=tk.DISABLED)
                rel.tag_add("relacion", "1.0", "end")
                rel.grid(row=fila_marco, column=1, padx=(10,10), pady=(0,7))
                ent2: tk.Text = tk.Text(marco, **comunes.atrb_filas_vertice)
                ent2.tag_config("entidad", **comunes.tag_entidad)
                ent2.insert(tk.END, relacion[2])  # type: ignore
                ent2.config(state=tk.DISABLED)
                ent2.tag_add("entidad", "1.0", "end")
                ent2.grid(row=fila_marco, column=2, padx=(10,0), pady=(0,7))           
                fila_marco += 1
            marco.grid(row=fila, column=0, sticky="ew", padx=(5,5), pady=(0,5))
            self._vertices_ubicados[id_vertice] = marco
            fila += 1

    def _comprobar_id_vertice(self, id_vertice:str) -> bool:
        """
        Verifica que el id ingresado sea válido.

        :return: El resultado de la verificación.
        :rtype: bool
        """
        res: bool = False
        if id_vertice in self._vertices_existentes.keys():
            res = True
        else:
            self._ingr_id_vertice_editar.focus_set()
            self._ingr_id_vertice_editar.select_range(0, tk.END)
        return res

    def _construir_botonera_vertices(
        self, ancestro: tk.Frame, instancia: vertice.EditorVertice
    ) -> None:
        """
        Construye la botonera superior de la sección.
        
        :param ancestro: El artefacto que contiene a la botonera.
        :type ancestro: tk.Frame
        :param instancia: El módulo de edición de vértice.
        :type instancia: vertice.EditorVertice
        """
        # Nota emergente
        self._etq_ne_id_v: tk.Label = tk.Label( 
            ancestro, text ="( ? )", **comunes.atrb_etq_ayuda
        )
        tex_ne: str = "Ingresar un ID de los disponibles en la lista de relaciones"
        self.ne_id_v: emergente.NotaEmergente = emergente.NotaEmergente( 
            self._etq_ne_id_v, tex_ne
        )  
        self._etq_ne_id_v.bind("<Enter>", self.ne_id_v.mostrar)
        self._etq_ne_id_v.bind("<Leave>", self.ne_id_v.ocultar)
        self._etq_ne_id_v.grid(row=0, column=0, padx=(0,0))
        # Vértice a editar
        self._etq_id_vertice_editar: tk.Label = tk.Label(
            ancestro, text="ID:", **comunes.atrb_etq_ayuda
        )
        self._etq_id_vertice_editar.grid(row=0, column=1, padx=(5,5))        
        self._id_vertice_editar: tk.StringVar = tk.StringVar()
        self._ingr_id_vertice_editar: tk.Entry = tk.Entry( 
            ancestro,
            textvariable=self._id_vertice_editar,
            width=3,
            **comunes.atrb_entrada
        )
        self._ingr_id_vertice_editar.grid(row=0, column=2, padx=(0,10))     
        # Botones
        self._btn_aplicar_cambios_vertice: tk.Button = tk.Button(
            ancestro,
            text="Aplicar",
            command=lambda:self._aplicar_cambios_vertice(instancia),
            **comunes.atrb_btn_aplicar
        )
        self._btn_aplicar_cambios_vertice.grid(row=0, column=3, padx=(0,10))
        self._btn_deshacer_vertice: tk.Button = tk.Button(
            ancestro,
            text="Deshacer",
            command=lambda:self._deshacer_ed_vertice(),
            **comunes.atrb_btn_restablecer
        )
        self._btn_deshacer_vertice.grid(row=0, column=4, padx=(0,10))

    def _construir_encab_vertices(self, ancestro: tk.Frame) -> None:
        """
        Construye el encabezado de la lista de vértices.

        :param ancestro: El artefacto que contiene al encabezado.
        :type ancestro: tk.Frame
        """
        self._sep_ids_vertices_sup: ttk.Separator = ttk.Separator( 
            ancestro, orient="horizontal"
        )
        self._sep_ids_vertices_sup.grid(
            row=0, column=0, sticky="ew", pady=(3,3)
        )
        t_aux:str = "LISTA DE RELACIONES"
        self._etq_ids_vertices: tk.Label = tk.Label( 
            ancestro, text=t_aux, **comunes.atrb_etq_ayuda
        )
        self._etq_ids_vertices.grid(
            row=1, column=0, sticky="ew", padx=(20,20), pady=(3,3)
        )        
        self._sep_ids_vertices_inf: ttk.Separator = ttk.Separator(
            ancestro, orient="horizontal"
        )     
        self._sep_ids_vertices_inf.grid(
            row=2, column=0, sticky="ew", pady=(3,13)
        )

    def _construir_lista_vertices(self, ancestro: tk.Frame) -> None:
        """
        Construye el contenedor donde se cargan dinámicamente
        los vértices existentes.

        :param ancestro: El artefacto que contiene a la lista de vértices.
        :type ancestro: tk.Frame
        """
        self._estilo_lista_v: ttk.Style = ttk.Style()
        self._estilo_lista_v.configure("TFrame")
        self._estilo_lista_v.configure(
            "ListaV.TFrame", background=comunes.color_fondo_gral
        )
        self._lista_vertices: ttk.Frame = ttk.Frame(
            ancestro, style="ListaV.TFrame"
        )
        self._lista_vertices.grid(
            row=1, column=0, sticky="n", pady=(0,0)
        )
        self._cv_vertices: tk.Canvas = tk.Canvas(
            self._lista_vertices,
            width=220,
            height=360,
            highlightthickness=0,
            **comunes.atrb_contenedor_artf
        )
        self._barra_v = ttk.Scrollbar(
            self._lista_vertices, orient="vertical",
            command=self._cv_vertices.yview
        )        
        self._marco_desplazable_v: ttk.Frame = ttk.Frame(
            self._cv_vertices, style="ListaV.TFrame"
        )
        self._marco_desplazable_v.bind(
            "<Configure>",
            lambda e: self._cv_vertices.configure(
                scrollregion=self._cv_vertices.bbox("all")
            )
        )
        self._cv_vertices.create_window(
            (0, 0), window=self._marco_desplazable_v, anchor="nw"
        )
        self._cv_vertices.grid(row=0, column=0, sticky="ew", padx=(5,5))
        self._cv_vertices.configure(yscrollcommand=self._barra_v.set)

    def _desapilar_atributos_vertice(self) -> tuple[str, dict[str, str]] | tuple[()]:
        """
        Desapila la última tupla ingresada con los atributos del vértice antes
        de realizar los cambios.

        :return: La tupla con los atributos anteriores.
        :rtype: tuple[str, dict[str, str]] | tuple[()]
        """
        try:
            res: tuple[str, dict[str, str]] = self._pila_atributos_vertice.get_nowait()
            return res
        except queue.Empty:
            return ()        
 
    def _deshacer_ed_vertice(self) -> None:
        """
        Obtiene los atributos anteriores y los restablece.
        """
        cambios: tuple[str, dict[str, str]] | tuple[()] = self._desapilar_atributos_vertice()
        if cambios:
            if cambios[0] in self._gestor.lista_ids("vértice"):
                self._gestor.actualizar_elemento("vertice", cambios[0], cambios[1])
                self.reiniciar_opciones() 
                self.vaciar_atributos()
            
    def _eliminar_vertices_existentes(self) -> None:
        """
        Vacía las entradas con los vértices generadas dinámicamente.
        """
        for marco in self._vertices_ubicados.values():
            marco.destroy()
        self._vertices_ubicados.clear()

    def _obtener_vertices(self)-> dict[str, list[list[str | None]]]:
        """
        Devuelve los vértices registrados hasta el momento.
        """
        return self._gestor.vertices_existentes()
