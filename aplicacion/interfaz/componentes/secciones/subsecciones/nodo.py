import tkinter as tk
from tkinter import colorchooser, font, scrolledtext, ttk
from aplicacion.interfaz import comunes
from aplicacion.interfaz.componentes.elementos import emergente, opciones


class EditorNodo:
    """
    Clase encargada de editar los atributos de los nodos del diagrama.

    :param ancestro: El marco donde se ubica el contenedor principal y/o los artefactos instanciados por la clase.
    :type ancestro: Frame
    :param gestor: La instancia de la clase encargada de gestionar la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor 
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk            
    """

    def __init__(self, ancestro: tk.Frame, gestor, raiz: tk.Tk):
        """
        Constructor de la clase EditorNodo.
        """        
        self._gestor = gestor
        self._raiz: tk.Tk = raiz
        self._ancestro: tk.Frame = ancestro        
        self._prop_nodo: dict[str, str | None] = {}  # Almacenará los cambios
        self._contenedor_opc_nodos = tk.Frame(  # Marco principal
            ancestro, **comunes.atrb_contenedor_artf
        )
        self._construir_opciones_nodo()    

    def artefacto(self) -> tk.Frame:
        """
        Retorna el contenedor que contiene a todos los artefactos de la sección.

        :return: El marco principal de la subsección.
        :rtype: Frame
        """
        return self._contenedor_opc_nodos

    def actualizar_forma(self, forma: str) -> None:
        """
        Actualiza la entrada del diccionario de cambios.
        """
        self._prop_nodo["shape"] = forma

    def actualizar_dict_nodo(self) -> bool:
        """
        Antes de actualizar, efectúa las comprobaciones necesarias
        en los valores ingresados.

        :return: El resultado de la verificación.
        :rtype: bool
        """
        res: bool = False
        
        fuente_n: str = self._tipo_fuente_n.get()
        if fuente_n:
            self._prop_nodo["fontname"] = self._tipo_fuente_n.get()

        tamaño_fuente_n: str = self._tamaño_fuente_n.get()
        if tamaño_fuente_n:
            try:
                tamaño_valido_n: bool = type(int(tamaño_fuente_n)) is int
                cond_aux: bool = int(tamaño_fuente_n) > 0
                tamaño_valido_n = tamaño_valido_n and cond_aux
                if tamaño_valido_n:
                    self._prop_nodo["fontsize"] = tamaño_fuente_n
                    res = True
            except:
                self._ingr_tamaño_fuente_n.focus_set() 
                self._ingr_tamaño_fuente_n.select_range(0, tk.END)
        else:
            if self._prop_nodo:  # Si hay algún cambio 
                res = True
        return res

    def obtener_cambios(self) -> dict[str, str | None]:
        """
        Retorna el diccionario de cambios en el nodo.

        :return: Las modificaciones efectuadas.
        :rtype: dict[str, str | None]
        """
        return self._prop_nodo

    def reiniciar_cambios(self) -> None:
        """
        Vacía el diccionario de cambios.
        """
        self._prop_nodo = {}
        

    def reiniciar_entradas(self) -> None:
        """
        Vacía los artefactos donde se ingresan los cambios.
        """
        self._ingr_tipo_fuente_n.delete(0, tk.END)
        self._ingr_tamaño_fuente_n.delete(0, tk.END)            
        self._opc_forma_nodo.opcion_inicial("Formas") 

    def _color_borde_n(self) -> None:
        """
        Abre un selector de color y actualiza el diccionario de cambios.
        """
        color = colorchooser.askcolor(title ="Elegir color de borde")
        self._prop_nodo["color"] = color[1]

    def _color_relleno_n(self) -> None:
        """
        Abre un selector de color y actualiza el diccionario de cambios.
        """
        color = colorchooser.askcolor(title ="Elegir color de relleno")
        self._prop_nodo["fillcolor"] = color[1]
        
    def _color_texto_n(self) -> None:
        """
        Abre un selector de colores y actualiza el diccionario de cambios.
        """
        color = colorchooser.askcolor(title ="Elegir color del texto")
        self._prop_nodo["fontcolor"] = color[1]


    def _construir_opciones_nodo(self) -> None:
        """
        Construye los artefactos que permiten ingresar los cambios.
        """        
        # Encabezado
        self._sep_nodo_sup: ttk.Separator = ttk.Separator(
            self._contenedor_opc_nodos, orient="horizontal"
        )
        self._etq_sec_opc_nodos: tk.Label = tk.Label( 
            self._contenedor_opc_nodos,
            text = "ATRIBUTOS DE NODO",
            **comunes.atrb_etq_ayuda
        )
        self._sep_nodo_inf: ttk.Separator = ttk.Separator( 
            self._contenedor_opc_nodos, orient="horizontal"
        )
        # Color borde nodo
        self._etq_borde_nodo: tk.Label = tk.Label(
            self._contenedor_opc_nodos,
            text = "Color del borde:",
            **comunes.atrb_etq_ayuda
        )
        self._btn_elegir_color_borde: tk.Button = tk.Button(
            self._contenedor_opc_nodos,
            text = "Elegir",
            command=self._color_borde_n,
            **comunes.atrb_btn_opc
        )
        # Color relleno nodo
        self._etq_relleno_nodo: tk.Label = tk.Label( 
            self._contenedor_opc_nodos,
            text = "Color de relleno:",
            **comunes.atrb_etq_ayuda
        )
        self._btn_elegir_color_relleno: tk.Button = tk.Button(
            self._contenedor_opc_nodos,
            text="Elegir",
            command=self._color_relleno_n,
            **comunes.atrb_btn_opc
        )
        # Color texto nodo
        self._etq_texto_nodo: tk.Label = tk.Label( 
            self._contenedor_opc_nodos,
            text = "Color del texto:",
            **comunes.atrb_etq_ayuda
        )
        self._btn_elegir_color_texto_n: tk.Button = tk.Button(
            self._contenedor_opc_nodos,
            text = "Elegir",
            command=self._color_texto_n,
            **comunes.atrb_btn_opc
        )
        # Tipo de fuente
        self._etq_tipo_fuente_n: tk.Label = tk.Label(
            self._contenedor_opc_nodos,
            text = "Tipo de fuente:",
            **comunes.atrb_etq_ayuda
        )        
        self._tipo_fuente_n: tk.StringVar = tk.StringVar() 
        self._ingr_tipo_fuente_n: tk.Entry = tk.Entry( 
            self._contenedor_opc_nodos,
            textvariable = self._tipo_fuente_n,
            **comunes.atrb_entrada
        )
        self._btn_ver_fuentes_n: tk.Button = tk.Button(
            self._contenedor_opc_nodos,
            text="Disponibles",
            command=self._explorar_fuentes,
            **comunes.atrb_btn_fuentes
        )
        self._etq_ne_tipo_fuente_n: tk.Label = tk.Label( 
            self._contenedor_opc_nodos,
            text = "( ? )",
            **comunes.atrb_etq_ayuda
        )
        tex_aux: str = "Ingresar una combinación de la forma: {fuente disponible}"
        tex_aux = tex_aux + "-{estilo},\n o bien el nombre de la fuente. "
        tex_aux = tex_aux + 'Por ejemplo: "times-italic", "Droid Sans", etc.'
        self._ne_tipo_fuente_n = emergente.NotaEmergente( 
            self._etq_ne_tipo_fuente_n, tex_aux
        ) 
        self._etq_ne_tipo_fuente_n.bind(
            "<Enter>", self._ne_tipo_fuente_n.mostrar
        )
        self._etq_ne_tipo_fuente_n.bind(
            "<Leave>", self._ne_tipo_fuente_n.ocultar
        )        
        # Tamaño de fuente
        self._etq_tamaño_fuente_n: tk.Label = tk.Label(
            self._contenedor_opc_nodos,
            text = "Tamaño del texto:",
            **comunes.atrb_etq_ayuda
        )        
        self._tamaño_fuente_n: tk.StringVar = tk.StringVar() 
        self._ingr_tamaño_fuente_n: tk.Entry = tk.Entry( 
            self._contenedor_opc_nodos,
            textvariable = self._tamaño_fuente_n,
            **comunes.atrb_entrada
        )
        self._etq_ne_tamaño_fuente_n: tk.Label = tk.Label( 
            self._contenedor_opc_nodos,
            text = "( ? )",
            **comunes.atrb_etq_ayuda
        )  
        self._ne_tamaño_fuente_n = emergente.NotaEmergente( 
            self._etq_ne_tamaño_fuente_n, "Ingresar un número entero") 
        self._etq_ne_tamaño_fuente_n.bind(
            "<Enter>", self._ne_tamaño_fuente_n.mostrar
        )
        self._etq_ne_tamaño_fuente_n.bind(
            "<Leave>", self._ne_tamaño_fuente_n.ocultar
        )    
        # Forma nodo
        self._etq_forma_nodo: tk.Label = tk.Label(
            self._contenedor_opc_nodos,
            text = "Forma del nodo:",
            **comunes.atrb_etq_ayuda
        )       
        self._opc_forma_nodo = opciones.MenuOpciones(
            self._contenedor_opc_nodos,
            "Formas",
            comunes.formas_nodo,
            comunes.atrb_menu_opc,
            "opc_forma_nodo",
            self._gestor
        )
        self._artf_forma_nodo: tk.OptionMenu = self._opc_forma_nodo.artefacto()        
        # Ubicación de los elementos en el contenedor de opciones nodos
        self._sep_nodo_sup.grid(
            row=0, column=0, columnspan=2, sticky="ew", pady=(3,3)
        )
        self._etq_sec_opc_nodos.grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=(3,3)
        )
        self._sep_nodo_inf.grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(3,13)
        )
        # Color borde
        self._etq_borde_nodo.grid(row=3, column=0, sticky="ew", pady=(3,3))
        self._btn_elegir_color_borde.grid(row=3, column=1, pady=(3,3))
        # Color relleno
        self._etq_relleno_nodo.grid(row=4, column=0, sticky="ew", pady=(3,3))
        self._btn_elegir_color_relleno.grid(row=4, column=1, pady=(3,3))
        # Color texto
        self._etq_texto_nodo.grid(row=5, column=0, sticky="ew", pady=(3,3))
        self._btn_elegir_color_texto_n.grid(row=5, column=1, pady=(3,3))
        # Tipo de fuente
        self._etq_tipo_fuente_n.grid(row=6, column=0, sticky="ew", pady=(3,3))
        self._ingr_tipo_fuente_n.grid(row=6, column=1, sticky="ew", pady=(3,3))
        self._etq_ne_tipo_fuente_n.grid(
            row=6, column=2, sticky="w", padx=(0,0), pady=(3,3)
        )
        self._btn_ver_fuentes_n.grid(row=7, column=1, pady=(3,3))
        # Tamaño
        self._etq_tamaño_fuente_n.grid(row=8, column=0, sticky="ew", pady=(3,3))
        self._ingr_tamaño_fuente_n.grid(row=8, column=1, sticky="ew", pady=(3,3))
        self._etq_ne_tamaño_fuente_n.grid(
            row=8, column=2, sticky="w", padx=(0,0), pady=(3,3)
        )
        # Forma nodo
        self._etq_forma_nodo.grid(row=9, column=0, sticky="ew", pady=(3,3))        
        self._artf_forma_nodo.grid(row=9, column=1, pady=(3,3))
 
    def _explorar_fuentes(self) -> None:
        """
        Construye una ventana independiente donde se muestran las fuentes
        disponibles en el sistema.
        """
        fuentes_disponibles: list[str] = list(font.families())
        fuentes_disponibles_conj: set[str] = set(fuentes_disponibles)
        fuentes_disponibles = list(fuentes_disponibles_conj)
        fuentes_disponibles.sort()
        texto_fuentes: str = "\n".join(
            [fuente for fuente in fuentes_disponibles]
        )
        # Creo la ventana emergente
        nueva_ventana: tk.Toplevel = tk.Toplevel(
            self._ancestro, **comunes.atrb_contenedor_artf
        )
        nueva_ventana.title("Fuentes disponibles")
        # Obtengo los datos para centrarla en la pantalla
        self._raiz.update_idletasks()
        ancho: int = 500 
        alto: int = 200 
        ancho_pantalla:int = self._raiz.winfo_screenwidth()
        alto_pantalla:int = self._raiz.winfo_screenheight()
        x: int = (ancho_pantalla - ancho) // 2
        y: int = (alto_pantalla - alto) // 2
        nueva_ventana.geometry(f"{ancho}x{alto}+{x}+{y}")        
        # Creo el artefacto que mostrará el nombre de las fuentes
        caja_fuentes = scrolledtext.ScrolledText(
            nueva_ventana,
            wrap=tk.WORD,
            state=tk.NORMAL,
            undo=True,
            maxundo=5,
            **comunes.atrb_area_txt)
        caja_fuentes.pack(side=tk.TOP, pady=(0,5))
        caja_fuentes.delete(1.0, tk.END)
        caja_fuentes.insert(tk.END, texto_fuentes)
