import tkinter as tk
from tkinter import colorchooser, font, scrolledtext, ttk
from aplicacion.interfaz import comunes
from aplicacion.interfaz.componentes.elementos import emergente, opciones


class EditorVertice:
    """
    Clase encargada de editar los atributos de los vértices del diagrama.

    :param ancestro: El marco donde se ubica el contenedor principal y/o los artefactos instanciados por la clase.
    :type ancestro: Frame
    :param gestor: La instancia de la clase encargada de gestionar la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor 
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk 
    """

    def __init__(self, ancestro: tk.Frame, gestor, raiz: tk.Tk):
        """
        Constructor de la clase EditorVertice.
        """
        self._gestor = gestor
        self._raiz: tk.Tk = raiz
        self._ancestro: tk.Frame = ancestro    
        self._prop_vertice: dict[str, str | None] = {}  # Almacenará los cambios
        self._indicador_relacion: bool = True  # Interruptor de entrada "peso"
        self._contenedor_opc_vertices = tk.Frame(  # Marco principal
            ancestro, **comunes.atrb_contenedor_artf
        )
        self._construir_opciones_vertice()
        
    def artefacto(self) -> tk.Frame:
        """
        Retorna el contenedor que contiene a todos los artefactos de la sección.

        :return: El marco principal de la subsección.
        :rtype: Frame      
        """
        return self._contenedor_opc_vertices

    def actualizar_dict_vertice(self) -> bool:
        """
        Antes de actualizar, efectúa las comprobaciones necesarias
        en los valores ingresados.

        :return: El resultado de la verificación.
        :rtype: bool
        """
        res: bool = False
        
        tipo_flecha_d: str = self._opc_tipo_flecha_d.obtener_eleccion()
        if tipo_flecha_d != "Delantera":
            self._prop_vertice["arrowhead"] =  tipo_flecha_d
        tipo_flecha_t = self._opc_tipo_flecha_t.obtener_eleccion()
        if tipo_flecha_t != "Trasera":
            self._prop_vertice["arrowtail"] =  tipo_flecha_t
            
        tamaño_flecha: str = self._tamaño_flecha.get()
        if tamaño_flecha:
            cond1:bool = False
            cond2:bool = False
            try:
                cond1 = type(int(tamaño_flecha)) is int
                cond_aux: bool = int(tamaño_flecha) > 0
                cond1 = cond1 and cond_aux
            except:
                pass
            try:                
                cond2 = type(float(tamaño_flecha)) is float
                cond_aux = float(tamaño_flecha) > 0
                cond2 = cond2 and cond_aux
            except:
                pass
            if cond1 or cond2:
                self._prop_vertice["arrowsize"] = tamaño_flecha
                res = True
            else:
                self._ingr_tamaño_flecha.focus_set() 
                self._ingr_tamaño_flecha.select_range(0, tk.END)
                return False
            
        peso: str = self._peso_relacion.get()
        if peso:
            cond1 = False
            cond2 = False
            try:
                cond1 = type(int(peso)) is int
                cond_aux = int(peso) > 0
                cond1 = cond1 and cond_aux
            except:
                pass
            try:                
                cond2 = type(float(peso)) is float
                cond_aux = float(peso) > 0
                cond2 = cond2 and cond_aux                
            except:
                pass
            if cond1 or cond2:
                self._prop_vertice["peso"] = peso
                res = True
            else:
                self._ingr_peso_relacion.focus_set() 
                self._ingr_peso_relacion.select_range(0, tk.END)
                return False

        fuente_v: str = self._tipo_fuente_v.get()
        if fuente_v:
            self._prop_vertice["fontname"] = self._tipo_fuente_v.get()

        tamaño_fuente_v: str = self._tamaño_fuente_v.get()
        if tamaño_fuente_v:
            try:
                tamaño_valido_v = type(int(tamaño_fuente_v)) is int
                cond_aux = int(tamaño_fuente_v) > 0
                tamaño_valido_v = tamaño_valido_v and cond_aux
                if tamaño_valido_v:
                    self._prop_vertice["fontsize"] = tamaño_fuente_v
                    res = True
            except:
                self._ingr_tamaño_fuente_v.focus_set() 
                self._ingr_tamaño_fuente_v.select_range(0, tk.END)
                return False        
        if self._prop_vertice:  # Si hay algún cambio 
            res = True  
        return res


    def actualizar_flecha_d(self, tipo:str) -> None:
        """
        Actualiza la entrada del diccionario de cambios.

        :param tipo: La forma de la flecha delantera.
        :type tipo: str
        """
        self._prop_vertice["arrowhead"] = tipo

    def actualizar_flecha_t(self, tipo:str) -> None:
        """
        Actualiza la entrada del diccionario de cambios.

        :param tipo: La forma de la flecha trasera.
        :type tipo: str
        """
        self._prop_vertice["arrowtail"] = tipo

    def actualizar_direccion(self, sentido:str) -> None:
        """
        Actualiza la entrada del diccionario de cambios.

        :param sentido: La orientacion de las flechas.
        :type sentido: str
        """
        self._prop_vertice["dir"] = sentido

    def activar_interruptor(self) -> None:
        """
        Alterna el valor de verdad del interruptor que permite ocultar
        o mostrar la opción de editar el "peso" de una relación.
        """
        self._indicador_relacion = not self._indicador_relacion
     
    def interruptor_relacion(self) -> None:
        """
        Hace visible la opción de "peso" de la relación cuando se modifica
        un vértice específico. Para ello modifica la ubicación de los artefactos
        que se encuentran en las celdas siguientes a la cual ocupa en la retícula.
        """
        if self._indicador_relacion:
            # Peso relación
            self._etq_peso_relacion.grid_forget()
            self._ingr_peso_relacion.grid_forget()
            self._etq_ne_peso_relacion.grid_forget()
            # Tipo de fuente
            self._etq_tipo_fuente_v.grid(row=8, column=0, sticky="ew", pady=(3,3))
            self._ingr_tipo_fuente_v.grid(row=8, column=1, sticky="ew", pady=(3,3))
            self._etq_ne_tipo_fuente_v.grid(
                row=8, column=2, sticky="w", padx=(0,0), pady=(3,3)
            )
            self._btn_ver_fuentes_v.grid(row=9, column=1, pady=(3,3))
            # Tamaño
            self._etq_tamaño_fuente_v.grid(
                row=10, column=0, sticky="ew", pady=(3,3)
            )
            self._ingr_tamaño_fuente_v.grid(
                row=10, column=1, sticky="ew", pady=(3,3)
            )
            self._etq_ne_tamaño_fuente_v.grid(
                row=10, column=2, sticky="w", padx=(0,0), pady=(3,3)
            )
            # Dirección
            self._etq_direccion.grid(row=11, column=0, sticky="ew", pady=(3,3))
            self._artf_direccion.grid(row=11, column=1, pady=(3,3))
        else:
            # Peso relación
            self._etq_peso_relacion.grid(row=8, column=0, sticky="ew", pady=(3,3))
            self._ingr_peso_relacion.grid(
                row=8, column=1, sticky="ew", pady=(3,3)
            )
            self._etq_ne_peso_relacion.grid(
                row=8, column=2, sticky="w", padx=(0,0), pady=(3,3)
            )
            # Tipo de fuente
            self._etq_tipo_fuente_v.grid(row=9, column=0, sticky="ew", pady=(3,3))
            self._ingr_tipo_fuente_v.grid(
                row=9, column=1, sticky="ew", pady=(3,3)
            )
            self._etq_ne_tipo_fuente_v.grid(
                row=9, column=2, sticky="w", padx=(0,0), pady=(3,3)
            )
            self._btn_ver_fuentes_v.grid(row=10, column=1, pady=(3,3))
            # Tamaño
            self._etq_tamaño_fuente_v.grid(
                row=11, column=0, sticky="ew", pady=(3,3)
            )
            self._ingr_tamaño_fuente_v.grid(
                row=11, column=1, sticky="ew", pady=(3,3)
            )
            self._etq_ne_tamaño_fuente_v.grid(
                row=11, column=2, sticky="w", padx=(0,0), pady=(3,3)
            )
            # Dirección
            self._etq_direccion.grid(row=12, column=0, sticky="ew", pady=(3,3))
            self._artf_direccion.grid(row=12, column=1, pady=(3,3))

    def obtener_cambios(self) -> dict[str, str | None]:
        """
        Retorna el diccionario de cambios en el vértice.

        :return: Las modificaciones efectuadas.
        :rtype: dict[str, str | None]
        """
        return self._prop_vertice
    
    def reiniciar_cambios(self) -> None:
        """
        Vacía el diccionario de cambios.
        """
        self._prop_vertice = {}

    def reiniciar_entradas(self) -> None:
        """
        Vacía los artefactos donde se ingresan los cambios.
        """
        self._opc_tipo_flecha_d.opcion_inicial("Delantera")
        self._opc_tipo_flecha_t.opcion_inicial("Trasera")
        self._ingr_tamaño_flecha.delete(0, tk.END)
        self._ingr_peso_relacion.delete(0, tk.END)
        self._ingr_tipo_fuente_v.delete(0, tk.END)
        self._ingr_tamaño_fuente_v.delete(0, tk.END)
        self._opc_direccion.opcion_inicial("Sentido")
  
    def _color_vertice(self) -> None:
        """
        Abre un selector de color y actualiza el diccionario de cambios.
        """
        color = colorchooser.askcolor(title ="Elegir color del vértice")
        self._prop_vertice["color"] = color[1]
        
    def _color_texto_v(self) -> None:
        """
        Abre un selector de color y actualiza el diccionario de cambios.
        """
        color = colorchooser.askcolor(title ="Elegir color del texto")
        self._prop_vertice["fontcolor"] = color[1]

    def _construir_opciones_vertice(self) -> None:
        """
        Construye los artefactos que permiten ingresar los cambios.
        """
        # Titulo de sección
        self._sep_vertice_sup: ttk.Separator = ttk.Separator( 
            self._contenedor_opc_vertices, orient="horizontal"
        )
        self._etq_sec_opc_vertices: tk.Label = tk.Label( 
            self._contenedor_opc_vertices,
            text = "ATRIBUTOS DE VÉRTICE",
            **comunes.atrb_etq_ayuda
        )
        self._sep_vertice_inf: ttk.Separator = ttk.Separator(
            self._contenedor_opc_vertices, orient="horizontal"
        )
        # Color vértice
        self._etq_relleno_vertice: tk.Label = tk.Label( 
            self._contenedor_opc_vertices,
            text = "Color de vértice:",
            **comunes.atrb_etq_ayuda
        )
        self._btn_elegir_color_vertice: tk.Button = tk.Button(
            self._contenedor_opc_vertices,
            text="Elegir",
            command=self._color_vertice,
            **comunes.atrb_btn_opc
        )
        # Color texto vértice
        self._etq_texto_vertice: tk.Label = tk.Label(
            self._contenedor_opc_vertices,
            text = "Color del texto:",
            **comunes.atrb_etq_ayuda
        )
        self._btn_elegir_color_texto_v: tk.Button = tk.Button(
            self._contenedor_opc_vertices,
            text="Elegir",
            command=self._color_texto_v,
            **comunes.atrb_btn_opc
        )
        # Tipos de flechas
        self._etq_tipo_flecha: tk.Label = tk.Label( 
            self._contenedor_opc_vertices,
            text = "Tipo de flechas:",
            **comunes.atrb_etq_ayuda
        )       
        self._opc_tipo_flecha_d = opciones.MenuOpciones(
            self._contenedor_opc_vertices,
            "Delantera",
            comunes.tipos_flechas,
            comunes.atrb_menu_opc,
            "opc_tipo_flecha_d",
            self._gestor
        )
        self._artf_tipo_flecha_d: tk.OptionMenu = self._opc_tipo_flecha_d.artefacto()
        self._opc_tipo_flecha_t = opciones.MenuOpciones(
            self._contenedor_opc_vertices,
            "Trasera",
            comunes.tipos_flechas,
            comunes.atrb_menu_opc,
            "opc_tipo_flecha_t",
            self._gestor
        )
        self._artf_tipo_flecha_t: tk.OptionMenu = self._opc_tipo_flecha_t.artefacto()
        self._ne_tipo_flecha = emergente.NotaEmergente(
            self._artf_tipo_flecha_t, 'Solo para Dirección "back" o "both"'
        ) 
        self._artf_tipo_flecha_t.bind("<Enter>", self._ne_tipo_flecha.mostrar)
        self._artf_tipo_flecha_t.bind("<Leave>", self._ne_tipo_flecha.ocultar)
        # Tamaño de flecha
        self._etq_tamaño_flecha: tk.Label = tk.Label(
            self._contenedor_opc_vertices,
            text = "Tamaño de flecha:",
            **comunes.atrb_etq_ayuda
        )        
        self._tamaño_flecha: tk.StringVar = tk.StringVar() 
        self._ingr_tamaño_flecha: tk.Entry = tk.Entry( 
            self._contenedor_opc_vertices,
            textvariable = self._tamaño_flecha,
            **comunes.atrb_entrada
        )
        self._etq_ne_tamaño_flecha: tk.Label = tk.Label( 
            self._contenedor_opc_vertices,
            text = "( ? )",
            **comunes.atrb_etq_ayuda
        )
        tex_aux1: str = 'Ingresar un número entero o decimal > 0. Por ejemplo: "0.7"'
        tex_aux1 = tex_aux1 + ', "1", "2.5", etc.'
        self._ne_tamaño_flecha = emergente.NotaEmergente( 
            self._etq_ne_tamaño_flecha, tex_aux1
        )
        self._etq_ne_tamaño_flecha.bind("<Enter>", self._ne_tamaño_flecha.mostrar)
        self._etq_ne_tamaño_flecha.bind("<Leave>", self._ne_tamaño_flecha.ocultar)  
        # Peso relación
        self._etq_peso_relacion: tk.Label = tk.Label( 
            self._contenedor_opc_vertices,
            text = "Peso de relación:",
            **comunes.atrb_etq_ayuda
        )        
        self._peso_relacion: tk.StringVar = tk.StringVar() 
        self._ingr_peso_relacion: tk.Entry = tk.Entry( 
            self._contenedor_opc_vertices,
            textvariable = self._peso_relacion,
            **comunes.atrb_entrada
        )
        self._etq_ne_peso_relacion: tk.Label = tk.Label( 
            self._contenedor_opc_vertices,
            text = "( ? )",
            **comunes.atrb_etq_ayuda
        )  
        self._ne_peso_relacion = emergente.NotaEmergente( 
            self._etq_ne_peso_relacion, "Ingresar un número entero o decimal > 0"
        )   
        self._etq_ne_peso_relacion.bind("<Enter>", self._ne_peso_relacion.mostrar)
        self._etq_ne_peso_relacion.bind("<Leave>", self._ne_peso_relacion.ocultar)
        # Tipo de fuente
        self._etq_tipo_fuente_v: tk.Label = tk.Label( 
            self._contenedor_opc_vertices,
            text = "Tipo de fuente:",
            **comunes.atrb_etq_ayuda
        )        
        self._tipo_fuente_v: tk.StringVar = tk.StringVar() 
        self._ingr_tipo_fuente_v: tk.Entry = tk.Entry( 
            self._contenedor_opc_vertices,
            textvariable = self._tipo_fuente_v,
            **comunes.atrb_entrada
        )
        self._btn_ver_fuentes_v: tk.Button = tk.Button(
            self._contenedor_opc_vertices,
            text="Disponibles",
            command=self._explorar_fuentes,
            **comunes.atrb_btn_fuentes
        )
        self._etq_ne_tipo_fuente_v: tk.Label = tk.Label( 
            self._contenedor_opc_vertices,
            text = "( ? )",
            **comunes.atrb_etq_ayuda
        )
        tex_aux2: str = "Ingresar una combinación de la forma: {fuente disponible}"
        tex_aux2 = tex_aux2 + "-{estilo},\n o bien el nombre de la fuente. "
        tex_aux2 = tex_aux2 + 'Por ejemplo: "times-italic", "Droid Sans", etc.' 
        self._ne_tipo_fuente_v = emergente.NotaEmergente(
            self._etq_ne_tipo_fuente_v, tex_aux2
        )            
        self._etq_ne_tipo_fuente_v.bind("<Enter>", self._ne_tipo_fuente_v.mostrar)
        self._etq_ne_tipo_fuente_v.bind("<Leave>", self._ne_tipo_fuente_v.ocultar)        
        # Tamaño de fuente
        self._etq_tamaño_fuente_v: tk.Label = tk.Label( 
            self._contenedor_opc_vertices,
            text = "Tamaño del texto:",
            **comunes.atrb_etq_ayuda
        )        
        self._tamaño_fuente_v: tk.StringVar = tk.StringVar() 
        self._ingr_tamaño_fuente_v: tk.Entry = tk.Entry( 
            self._contenedor_opc_vertices,
            textvariable = self._tamaño_fuente_v,
            **comunes.atrb_entrada
        )
        self._etq_ne_tamaño_fuente_v: tk.Label = tk.Label( 
            self._contenedor_opc_vertices,
            text = "( ? )",
            **comunes.atrb_etq_ayuda
        )     
        self._ne_tamaño_fuente_v = emergente.NotaEmergente( 
            self._etq_ne_tamaño_fuente_v, "Ingresar un número entero"
        )  
        self._etq_ne_tamaño_fuente_v.bind("<Enter>", self._ne_tamaño_fuente_v.mostrar)
        self._etq_ne_tamaño_fuente_v.bind("<Leave>", self._ne_tamaño_fuente_v.ocultar)
        # Dirección
        self._etq_direccion: tk.Label = tk.Label( 
            self._contenedor_opc_vertices,
            text = "Dirección:",
            **comunes.atrb_etq_ayuda
        )
        self._opc_direccion = opciones.MenuOpciones(
            self._contenedor_opc_vertices,
            "Sentido",
            comunes.direcciones,
            comunes.atrb_menu_opc,
            "opc_direccion",
            self._gestor
        )
        self._artf_direccion: tk.OptionMenu = self._opc_direccion.artefacto()        
        # Ubicación de los elementos en el contenedor de opciones vértices
        self._sep_vertice_sup.grid(
            row=0, column=0, columnspan=2, sticky="ew", pady=(3,3)
        )
        self._etq_sec_opc_vertices.grid(
            row=1, column=0, columnspan=2, sticky="ew", pady=(3,3)
        )
        self._sep_vertice_inf.grid(
            row=2, column=0, columnspan=2, sticky="ew", pady=(3,13)
        )
        # Color borde
        self._etq_relleno_vertice.grid(row=3, column=0, sticky="ew", pady=(3,3))
        self._btn_elegir_color_vertice.grid(row=3, column=1, pady=(3,3))
        # Color relleno
        self._etq_texto_vertice.grid(row=4, column=0, sticky="ew", pady=(3,3))
        self._btn_elegir_color_texto_v.grid(row=4, column=1, pady=(3,3))
        # Tipo de flecha
        self._etq_tipo_flecha.grid(row=5, column=0, sticky="ew", pady=(3,3))
        self._artf_tipo_flecha_d.grid(row=5, column=1, pady=(3,3))
        self._artf_tipo_flecha_t.grid(row=6, column=1, pady=(3,3))
        # Tamaño flecha
        self._etq_tamaño_flecha.grid(row=7, column=0, sticky="ew", pady=(3,3))
        self._ingr_tamaño_flecha.grid(row=7, column=1, sticky="ew", pady=(3,3))
        self._etq_ne_tamaño_flecha.grid(
            row=7, column=2, sticky="w", padx=(0,0), pady=(3,3)
        )
        # Peso relación
        self._etq_peso_relacion.grid(row=8, column=0, sticky="ew", pady=(3,3))
        self._ingr_peso_relacion.grid(row=8, column=1, sticky="ew", pady=(3,3))
        self._etq_ne_peso_relacion.grid(
            row=8, column=2, sticky="w", padx=(0,0), pady=(3,3)
        )
        # Tipo de fuente
        self._etq_tipo_fuente_v.grid(row=9, column=0, sticky="ew", pady=(3,3))
        self._ingr_tipo_fuente_v.grid(row=9, column=1, sticky="ew", pady=(3,3))
        self._etq_ne_tipo_fuente_v.grid(
            row=9, column=2, sticky="w", padx=(0,0), pady=(3,3)
        )
        self._btn_ver_fuentes_v.grid(row=10, column=1, pady=(3,3))
        # Tamaño
        self._etq_tamaño_fuente_v.grid(row=11, column=0, sticky="ew", pady=(3,3))
        self._ingr_tamaño_fuente_v.grid(row=11, column=1, sticky="ew", pady=(3,3))
        self._etq_ne_tamaño_fuente_v.grid(
            row=11, column=2, sticky="w", padx=(0,0), pady=(3,3)
        )
        # Dirección
        self._etq_direccion.grid(row=12, column=0, sticky="ew", pady=(3,3))
        self._artf_direccion.grid(row=12, column=1, pady=(3,3))


    def _explorar_fuentes(self) -> None:
        """
        Construye una ventana independiente donde se muestran las fuentes
        disponibles en el sistema.
        """
        fuentes_disponibles = list(font.families())
        fuentes_disponibles_conj = set(fuentes_disponibles)
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
        ancho_pantalla: int = self._raiz.winfo_screenwidth()
        alto_pantalla: int = self._raiz.winfo_screenheight()
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
            **comunes.atrb_area_txt
        )
        caja_fuentes.pack(side=tk.TOP, pady=(0,5))
        caja_fuentes.delete(1.0, tk.END)
        caja_fuentes.insert(tk.END, texto_fuentes)
