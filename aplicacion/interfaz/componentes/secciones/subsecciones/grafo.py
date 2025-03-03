import tkinter as tk
from tkinter import colorchooser, font, scrolledtext, ttk
from aplicacion.interfaz import comunes
from aplicacion.interfaz.componentes.elementos import emergente, opciones

class EditorGrafo:
    """
    Clase encargada de editar los atributos generales del diagrama.

    :param ancestro: El marco donde se ubica el contenedor principal y/o los artefactos instanciados por la clase.
    :type ancestro: Frame
    :param gestor: La instancia de la clase encargada de gestionar la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor 
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk 
    """
    
    def __init__(self, ancestro: tk.Frame, gestor, raiz: tk.Tk):
        """
        Constructor de la clase EditorGrafo.
        """
        self._gestor = gestor
        self._raiz: tk.Tk = raiz
        self._ancestro: tk.Frame = ancestro
        self._prop_grafo: dict[str, str | None] = {}  # Almacenará los cambios
        self._contenedor_opc_grafo: tk.Frame = tk.Frame(  # Marco principal
            ancestro, **comunes.atrb_contenedor_artf
        )
        self._construir_opciones_grafo()
           

    def artefacto(self) -> tk.Frame:
        """
        Retorna el contenedor que contiene a todos los artefactos de la sección.

        :return: El marco principal de la subsección.
        :rtype: Frame
        """
        return self._contenedor_opc_grafo


    def actualizar_dict_grafo(self) -> bool:
        """
        Antes de actualizar, efectúa las comprobaciones necesarias en
        los valores ingresados.

        :return: El resultado de la verificación.
        :rtype: bool
        """
        res:bool = False
        # Compruebo que se ingresó una cota y que sea válida
        cota: str = self._cota.get()
        if cota:
            try:
                cota_valida: bool = type(int(cota)) is int
                cond_aux: bool = int(cota) > 0
                cota_valida = cota_valida and cond_aux
                if cota_valida:
                    self._prop_grafo["cota"] = cota
                    res = True
            except:
                self._ingr_cota.focus_set() 
                self._ingr_cota.select_range(0, tk.END)
        else:       
            if self._prop_grafo:  # Si hay otros cambios registrados
                res = True                
        return res

    def actualizar_crecimiento(self, valor:str) -> None:
        """
        Actualiza la entrada del diccionario de cambios.

        :param valor: La dirección y el sentido en que crecerá el grafo.
        :type valor: str
        """
        self._prop_grafo["crecimiento"] = valor

    def actualizar_justificado(self, valor:str) -> None:
        """
        Actualiza la entrada del diccionario de cambios.

        :param valor: La alineación del texto de nodos y vértices respecto a los márgenes.
        :type valor: str
        """
        self._prop_grafo["justificado"] = valor

    def obtener_cambios(self) -> dict[str, str | None]:
        """
        Retorna el diccionario de cambios en el grafo.

        :return: Las modificaciones efectuadas.
        :rtype: dict[str, str| None]
        """
        return self._prop_grafo

    def reiniciar_cambios(self) -> None:
        """
        Vacía el diccionario de cambios.
        """
        self._prop_grafo = {}

    def reiniciar_entradas(self) -> None:
        """
        Vacía los artefactos donde se ingresan los cambios.
        """
        self._opc_crecimiento.opcion_inicial("Hacia")
        self._ingr_cota.delete(0, tk.END)
        self._opc_justificado.opcion_inicial("Párrafo")       

    def _color_fondo_grafo(self) -> None:
        """
        Abre un selector de color y actualiza el diccionario de cambios.
        """
        titulo: str = "Elegir color de fondo"
        tipo_color = tuple[None, None] | tuple[tuple[int, int, int], str]
        color: tipo_color = colorchooser.askcolor(title=titulo)
        self._prop_grafo["fondo"] = color[1]

    def _construir_opciones_grafo(self) -> None:
        """
        Construye los artefactos que permiten ingresar los cambios.
        """
        # Encabezado
        self._sep_grafo_sup: ttk.Separator = ttk.Separator(
            self._contenedor_opc_grafo, orient="horizontal"
        )
        self._etq_sec_opc_grafo: tk.Label = tk.Label( 
            self._contenedor_opc_grafo,
            text = "ATRIBUTOS DE GRAFO",
            **comunes.atrb_etq_ayuda
        )
        self._sep_grafo_inf: ttk.Separator = ttk.Separator(
            self._contenedor_opc_grafo, orient="horizontal"
        )
        # Color de fondo
        self._etq_fondo_grafo: tk.Label = tk.Label(
            self._contenedor_opc_grafo,
            text = "Color de fondo:",
            **comunes.atrb_etq_ayuda
        )
        self._btn_elegir_color_fondo: tk.Button = tk.Button(
            self._contenedor_opc_grafo,
            text = "Elegir",
            command=self._color_fondo_grafo,
            **comunes.atrb_btn_opc
        )
        # Direccion de crecimiento
        self._etq_crecimiento: tk.Label = tk.Label( 
            self._contenedor_opc_grafo,
            text = "Crecimiento:",
            **comunes.atrb_etq_ayuda
        )       
        self._opc_crecimiento = opciones.MenuOpciones(
            self._contenedor_opc_grafo,
            "Hacia",
            comunes.crecimiento,
            comunes.atrb_menu_opc,
            "opc_crecimiento",
            self._gestor
        )
        self._artf_crecimiento: tk.OptionMenu = self._opc_crecimiento.artefacto()
        # Longitud de líneas
        self._etq_cota: tk.Label = tk.Label( 
            self._contenedor_opc_grafo,
            text = "Longitud de línea:",
            **comunes.atrb_etq_ayuda
        )        
        self._cota: tk.StringVar = tk.StringVar() 
        self._ingr_cota: tk.Entry = tk.Entry( 
            self._contenedor_opc_grafo,
            textvariable = self._cota,
            **comunes.atrb_entrada
        )
        self._etq_ne_cota: tk.Label = tk.Label( 
            self._contenedor_opc_grafo,
            text = "( ? )",
            **comunes.atrb_etq_ayuda
        )
        tex_aux: str =  "Ingresar un número entero que establezca la cantidad "
        tex_aux = tex_aux + "máxima \nde caracteres por línea (aproximado por arriba)"
        self._ne_cota = emergente.NotaEmergente(self._etq_ne_cota, tex_aux)  
        self._etq_ne_cota.bind("<Enter>", self._ne_cota.mostrar)
        self._etq_ne_cota.bind("<Leave>", self._ne_cota.ocultar)
        # Justificado
        self._etq_justificado: tk.Label = tk.Label(
            self._contenedor_opc_grafo,
            text = "Justificado:",
            **comunes.atrb_etq_ayuda
        )       
        self._opc_justificado = opciones.MenuOpciones(
            self._contenedor_opc_grafo,
            "Párrafo",
            comunes.opciones_parrafo,
            comunes.atrb_menu_opc,
            "opc_justificado",
            self._gestor
        )
        self._artf_justificado: tk.OptionMenu = self._opc_justificado.artefacto()        

        # Ubicación de los elementos en contenedor grafo
        self._sep_grafo_sup.grid(
            row=0, column=0, columnspan=5, sticky="ew", pady=(15,3)
        )
        self._etq_sec_opc_grafo.grid(
            row=1, column=0, columnspan=5, sticky="ew", pady=(3,3)
        )
        self._sep_grafo_inf.grid(
            row=2, column=0, columnspan=5, sticky="ew", pady=(3,13)
        )
        # Color fondo
        self._etq_fondo_grafo.grid(
            row=3, column=0, sticky="ew", padx=(10,0),pady=(3,3)
        )
        self._btn_elegir_color_fondo.grid(
            row=3, column=1, padx=(10,10), pady=(3,3)
        )
        # Crecimiento
        self._etq_crecimiento.grid(
            row=4, column=0, sticky="ew", padx=(10,10),  pady=(3,3)
        )
        self._artf_crecimiento.grid(
            row=4, column=1,padx=(10,20),  pady=(3,3)
        )
        # Cota
        self._etq_cota.grid(
            row=3, column=3, sticky="e", padx=(20,10),pady=(3,3)
        )
        self._ingr_cota.grid(
            row=3, column=4, sticky="ew", padx=(0,0), pady=(3,3)
        )
        self._etq_ne_cota.grid(
            row=3, column=5, sticky="w", padx=(0,10), pady=(3,3)
        )
        # Justificado
        self._etq_justificado.grid(
            row=4, column=3, sticky="e",padx=(10,10),  pady=(3,3)
        )
        self._artf_justificado.grid(
            row=4, column=4,padx=(10,20),  pady=(3,3)
        )
