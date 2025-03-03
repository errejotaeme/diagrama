import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from aplicacion.interfaz import comunes
from aplicacion.interfaz.componentes.elementos import emergente
from aplicacion.interfaz.componentes.pantallas import pantalla_notas



class AreaDeTexto:
    """
    Clase encargada de cargar un texto e ingresar las proposiciones
    que constituyen el diagrama.

    :param ancestro: El artefacto que contiene al marco principal del área. 
    :type ancestro: ttk.Notebook
    :param gestor: La instancia de la clase encargada de gestionar la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor 
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk
    :param bucle: Instancia de la clase encargada de crear el bucle de la aplicación y gestionar el cambio de tema.
    :type bucle: Bucle
    :param tema: El tema actual de la aplicacion.
    :type tema: str
    :param texto_respaldo: Respaldo del contenido del área de texto que se vuelve a cargar cuando se reinicia por cambio de tema.
    :type texto_respaldo: str   
    """  

    def __init__(
        self,
        ancestro: ttk.Notebook,
        gestor,
        raiz: tk.Tk,
        bucle,
        tema: str,
        texto_respaldo: str
    ):
        """
        Constructor de la clase AreaDeTexto.   
        """
        self._raiz: tk.Tk = raiz
        self._gestor = gestor  # type: ignore
        self._bucle = bucle
        self._tema: str = tema
        self._texto_respaldo: str = texto_respaldo
        self._contenedor_artf: tk.Frame = tk.Frame(  # Marco principal
            ancestro, **comunes.atrb_contenedor_artf
        )
        # Permite que el texto desplazable ocupe todo el espacio disponible
        self._contenedor_artf.grid_rowconfigure(1, weight=1)
        self._contenedor_artf.grid_columnconfigure(0, weight=1)        
        self._crear_botonera() 
        self._crear_texto_desplazable() 
        self._crear_subsec_proposicion()     
        self._crear_notas_emergentes()
        self._establecer_atajos() 

    def artefacto(self) -> tk.Frame:
        """
        Retorna el contenedor principal de la sección.

        :return: El marco principal de la sección.
        :rtype: tk.Frame
        """
        return self._contenedor_artf
    

    def atajo(self, señal: int) -> str:
        """
        Asocia cada señal con un artefacto y comportamiento específico.

        :param señal: Un entero indicando la entrada a modificar o el botón activado.
        :type señal: int 
        :return: Una cadena que previene que el evento se propage a través de la jerarquía de artefactos.
        :rtype: str
        """
        self._area_texto.focus()
        seleccion: str = ""
        try:
            seleccion = self._area_texto.get("sel.first", "sel.last")
        except:
            pass
        # Entidad1
        if señal == 1:
            self._ingr_entidad1.delete(0, tk.END)
            self._ingr_entidad1.insert(0, seleccion)
            self._ingr_entidad1.focus()
        # Relacion
        elif señal == 2:
            self._ingr_relacion.delete(0, tk.END)
            self._ingr_relacion.insert(0, seleccion)
            self._ingr_relacion.focus()
        # Entidad2
        elif señal == 3:
            self._ingr_entidad2.delete(0, tk.END)
            self._ingr_entidad2.insert(0, seleccion)
            self._ingr_entidad2.focus()
        # Relacionar entidades
        elif señal == 4:
            self._btn_confirmar_relacion.focus()
            self._actualizar_diagrama()            
        # Borrar lo último que se graficó
        elif señal == 5:
            self._gestor.borrar_ultimo_ingreso()
            self._area_texto.focus()
        # Peso relación
        elif señal == 6:
            self._ingr_peso_rel.delete(0, tk.END)
            self._ingr_peso_rel.insert(0, seleccion)
            self._ingr_peso_rel.focus()
        # Peso relación
        elif señal == 7:
            self._abrir_notas()
        elif señal == 8:
            self._gestor.guardar_proyecto_desde_atajo()
        return "break"

    def cargar_texto_retornado(self, texto: str) -> None:
        """
        Recibe desde el Gestor la indicación para actualizar el área de texto,
        cuando el contenido se terminó de extraer.

        :param texto: El contenido a cargar.
        :type texto: str
        """
        self._area_texto.delete(1.0, tk.END)
        self._area_texto.insert(tk.END, texto)
        self._area_texto.tag_add("formato", "1.0", "end")
        self._area_texto.focus()

    def mostrar_aviso(self, aviso: str) -> None:
        """
        Actualiza la etiqueta de avisos con el texto recibido.

        :param aviso: La notificación a mostrar.
        :type aviso: str
        """
        self._etq_aviso.config(text=aviso)
        self._etq_aviso.update_idletasks()

    def ocultar_aviso(self) -> None:
        """
        Oculta el aviso que esté activo.
        """
        self._etq_aviso.config(text="")
        self._etq_aviso.update_idletasks()


    def _abrir_notas(self) -> None:
        """
        Habilita la pantalla que permite tomar notas personales del proyecto.
        """
        pantalla = pantalla_notas.PantallaNotas(
            self._gestor, self._raiz, self._contenedor_artf
        )

    def _actualizar_diagrama(self, *args) -> None:
        """
        Obtiene el texto ingresado y llama al Gestor para que actualice
        la vista del diagrama. Args captura el evento producido al presionar
        el botón relacionar.
        """
        proposicion: list[str] = []
        ent1: str = self._ent1.get().strip()
        if ent1:
            proposicion.append(ent1)
        else:
            self._ingr_entidad1.focus()
            return
        proposicion.append(self._rel.get().strip())  # Si es vacío lo maneja el gestor
        ent2: str = self._ent2.get().strip()
        if ent2:
            proposicion.append(ent2)
        else:
            self._ingr_entidad2.focus()
            return
        peso: str = self._peso.get().strip() 
        if peso:
            cond1: bool = False
            cond2: bool = False
            try:
                cond1 = type(int(peso)) is int
                cond_aux: bool = int(peso) > 0
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
                proposicion.append(peso)
            else:
                self._ingr_peso_rel.focus()
                return
        else:
            self._ingr_peso_rel.focus()
            return
        
        # Envía al gestor la proposición para que actualice el mapa
        respuesta: bool = self._gestor.relacionar_entidades(proposicion)
        if respuesta:
            # Vacía los artefactos
            self._ingr_entidad1.delete(0, tk.END)
            self._ingr_relacion.delete(0, tk.END)
            self._ingr_peso_rel.delete(0, tk.END)
            self._ingr_peso_rel.insert(0, "1")
            self._ingr_entidad2.delete(0, tk.END)
            self._area_texto.focus()

    def _cambiar_tema(self) -> None:
        """
        Obtiene los datos necesarios previo al reinicio que permite cambiar
        el tema de la aplicación.
        """
        self._gestor.cancelar_pendientes()
        self._gestor.respaldo_temporal()
        proyecto_activo: tuple[str, str] = self._gestor.datos_proyecto_activo()
        diagrama_no_vacio: bool = bool(self._gestor.nodos_existentes())
        texto_actual: str = self._area_texto.get(1.0, tk.END)
        self._bucle.cambiar_tema(
            diagrama_no_vacio, proyecto_activo, texto_actual
        )

    def _cargar_texto(self) -> None:
        """
        Carga en el área de texto desplazable el contenido extraído del
        documento seleccionado.
        """
        ruta: str | None = filedialog.askopenfilename(
            filetypes=[
                ("Archivos de texto plano", "*.txt"),
                ("Documentos PDF", "*.pdf")
            ]
        )
        if ruta:
            texto: str = self._gestor.obtener_texto(ruta)
            # Define el estilo de aviso, vacía y escribe en el área de texto
            self._area_texto.delete(1.0, tk.END)
            self._area_texto.insert(tk.END, texto)
            self._area_texto.tag_add("aviso", "1.0", "end")  
            self._area_texto.tag_config(
                "aviso", foreground=comunes.color_tex_mensaje,
                font=("Arial", 10, "bold italic")
            )
            self._area_texto.update_idletasks()    
            self._area_texto.focus()

    def _cadena_tema(self) -> str:
        """
        Devuelve una cadena con el tema a aplicar.
        """
        return "claro" if self._tema == "oscuro" else "oscuro"


    def _crear_botonera(self) -> None:
        """
        Construye la botonera del área de texto.
        """
        self._botonera_sup: tk.Frame = tk.Frame(
            self._contenedor_artf, **comunes.atrb_contenedor_artf
        )        
        self._botonera_sup.grid(
            row=0, column=0, padx=(0,0), pady=(0,0), sticky="ew"
        )
        self._btn_cargar_texto: tk.Button = tk.Button(
            self._botonera_sup,
            text="Cargar texto",
            command=self._cargar_texto,
            **comunes.atrb_btn_cargar_texto
        )
        self._btn_cargar_texto.grid(
            row=0, column=0, padx=(20, 0), pady=(20,10), sticky="ew"
        )
        self._btn_notas: tk.Button = tk.Button(
            self._botonera_sup,
            text="Notas",
            command=self._abrir_notas,
            **comunes.atrb_btn_abrir_notas
        )        
        self._btn_notas.grid(
            row=0, column=1, padx=(20, 0), pady=(20,10), sticky="ew"  
        )
        self._btn_reiniciar: tk.Button = tk.Button(
            self._botonera_sup,
            text="Reiniciar",
            command=self._reiniciar,
            **comunes.atrb_btn_reiniciar
        )        
        self._btn_reiniciar.grid(
            row=0, column=2, padx=(20,0), pady=(20,10), sticky="ew"
        )
        tema: str = self._cadena_tema()
        tex_boton_tema: str = f"Tema {tema}"
        self._btn_tema: tk.Button = tk.Button(
            self._botonera_sup,
            text=tex_boton_tema,
            command=self._cambiar_tema,
            **comunes.atrb_btn_tema
        )        
        self._btn_tema.grid(
            row=0, column=3, padx=(20,0), pady=(20,10), sticky="ew"
        )
        self._etq_aviso: tk.Label = tk.Label( # Etiqueta estado
            self._botonera_sup, text = "", **comunes.atrb_etq_aviso
        )
        self._etq_aviso.grid(
            row=0, column=4, padx=(10, 0), pady=(20,10), sticky="w"
        )

    def _crear_texto_desplazable(self) -> None:
        """
        Construye el artefacto donde se carga el texto extraído
        de los documentos seleccionados.
        """
        self._area_texto: scrolledtext.ScrolledText = scrolledtext.ScrolledText(
            self._contenedor_artf,
            wrap=tk.WORD,
            state=tk.NORMAL,
            undo=True,
            maxundo=25,
            **comunes.atrb_area_txt
        )        
        self._area_texto.tag_configure(
            "formato", spacing1=1, spacing2=3 , spacing3=1
        )        
        self._area_texto.grid(
            row=1, column=0, padx=(20,20), pady=(10,10), sticky="nsew"
        )
        self._area_texto.insert(tk.END, self._texto_respaldo)
        self._area_texto.tag_add("formato", "1.0", "end")
        

    def _crear_subsec_proposicion(self) -> None:
        """
        Construye los artefactos que permiten el ingreso
        de proposiciones.
        """
        self._subseccion_ingresos: tk.Frame = tk.Frame(
            self._contenedor_artf, **comunes.atrb_color_fondo
        )
        self._subseccion_ingresos.grid(
            row=2, column=0, sticky="s", pady=(0,25)
        )            
        self._botonera_mapa: tk.Frame = tk.Frame(
            self._subseccion_ingresos, **comunes.atrb_color_fondo
        )
        self._botonera_mapa.grid(row=0, column=0)
        # Separador
        self._sep_prop_izq: ttk.Separator = ttk.Separator(
            self._botonera_mapa, orient="horizontal"
        )
        self._sep_prop_der: ttk.Separator = ttk.Separator(
            self._botonera_mapa, orient="horizontal"
        )
        self._etq_prop_titulo: tk.Label = tk.Label(
            self._botonera_mapa,
            text = "P R O P O S I C I Ó N",
            **comunes.atrb_etq_ayuda
        )        
        # Variables de almacenamiento
        self._ent1: tk.StringVar = tk.StringVar()
        self._rel: tk.StringVar = tk.StringVar()
        self._ent2: tk.StringVar = tk.StringVar()
        self._peso: tk.StringVar = tk.StringVar()        
        # Etiqueta con nota emergente
        self._etq_proposicion: tk.Label = tk.Label(
            self._botonera_mapa, text="( ? )", **comunes.atrb_etq_ayuda
        )
        # Entidad1
        self._etq_entidad1: tk.Label = tk.Label(
            self._botonera_mapa, text="Entidad", **comunes.atrb_etq_ent)
        self._ingr_entidad1: tk.Entry = tk.Entry(
            self._botonera_mapa, textvariable=self._ent1, **comunes.atrb_entrada_e
        ) 
        # Relación entre entidades
        self._etq_relacion: tk.Label = tk.Label( 
            self._botonera_mapa, text="Vínculo", **comunes.atrb_etq_ent
        ) 
        self._ingr_relacion: tk.Entry = tk.Entry(
            self._botonera_mapa, textvariable=self._rel, **comunes.atrb_entrada_r
        )
        # Peso de la relación entre entidades
        self._etq_peso_rel: tk.Label = tk.Label( 
            self._botonera_mapa, text="Peso", **comunes.atrb_etq_ent
        ) 
        self._ingr_peso_rel: tk.Entry = tk.Entry( 
            self._botonera_mapa,
            width = 5,
            textvariable = self._peso,
            **comunes.atrb_entrada
        )
        self._ingr_peso_rel.insert(0, "1")
        # Entidad2
        self._etq_entidad2: tk.Label = tk.Label( 
            self._botonera_mapa, text="Entidad", **comunes.atrb_etq_ent
        )
        self._ingr_entidad2: tk.Entry = tk.Entry( 
            self._botonera_mapa, textvariable=self._ent2, **comunes.atrb_entrada_e
        ) 
        # Boton confirmar relación
        self._btn_confirmar_relacion: tk.Button = tk.Button(
            self._botonera_mapa, text="Relacionar", **comunes.atrb_btn_relacionar
        )
        self._btn_confirmar_relacion.config(command=self._actualizar_diagrama)
        
        # Ubicacion de los elementos en la botonera mapa        
        # Fila 1
        self._sep_prop_izq.grid(
            row=0, column=0, columnspan=1, sticky="ew", pady=(10,5)
        )
        self._etq_prop_titulo.grid(row=0, column=1, pady=(10,5))
        self._sep_prop_der.grid(
            row=0, column=2, columnspan=6, sticky="ew", pady=(10,5)
        )
        # Fila 2
        self._etq_entidad1.grid(row=1, column=1,sticky="ew")
        self._etq_relacion.grid(row=1, column=2,sticky="ew")
        self._etq_peso_rel.grid(row=1, column=3,sticky="ew")
        self._etq_entidad2.grid(row=1, column=4,sticky="ew")        
        # Fila 3
        self._etq_proposicion.grid(row=2, column=0, padx=(9, 9))
        self._ingr_entidad1.grid(row=2, column=1, padx=(0, 9))
        self._ingr_relacion.grid(row=2, column=2, padx=(0, 9))
        self._ingr_peso_rel.grid(row=2, column=3, padx=(0, 9))
        self._ingr_entidad2.grid(row=2, column=4, padx=(0, 9))
        self._btn_confirmar_relacion.grid(row=2, column=5, sticky="w", padx=(0,9))

    def _crear_notas_emergentes(self) -> None:
        """
        Construye las notas que se mostrarán al posar el cursor sobre ciertos
        artefactos.
        """
        # Nota emergente sobre botón cargar-texto
        ne1: str = 'Archivos con extensión ".pdf" o ".txt"'
        self._ne_btn_cargar = emergente.NotaEmergente(
            self._btn_cargar_texto, ne1
        )  
        self._btn_cargar_texto.bind("<Enter>", self._ne_btn_cargar.mostrar)
        self._btn_cargar_texto.bind("<Leave>", self._ne_btn_cargar.ocultar)
        # Nota emergente sobre etiqueta de ayuda a proposición
        ne2: str = '"Relacionar" graficará la proposición:  [ Entidad_1 ]----'
        ne2 = ne2 + "[ Vínculo ]---->[ Entidad_2 ]"
        self._ne_proposicion = emergente.NotaEmergente(
            self._etq_proposicion, ne2
        )
        self._etq_proposicion.bind("<Enter>", self._ne_proposicion.mostrar)
        self._etq_proposicion.bind("<Leave>", self._ne_proposicion.ocultar)
        # Nota emergente sobre etiqueta Entidad1
        self._ne_ent1 = emergente.NotaEmergente(
            self._etq_entidad1,
            "<Ctrl+a> ingresa automáticamente el texto seleccionado") # Enviar a un diccionario  
        self._etq_entidad1.bind("<Enter>", self._ne_ent1.mostrar)
        self._etq_entidad1.bind("<Leave>", self._ne_ent1.ocultar)
        # Nota emergente sobre etiqueta Relación
        ne3:str =  "<Ctrl+s> ingresa automáticamente el texto seleccionado"
        self._ne_rel = emergente.NotaEmergente( self._etq_relacion, ne3)
        self._etq_relacion.bind("<Enter>", self._ne_rel.mostrar)
        self._etq_relacion.bind("<Leave>", self._ne_rel.ocultar)
        # Nota emergente sobre etiqueta Peso de relación
        ne4: str = "Ingresar un número entero o decimal > 0 (valor por "
        ne4 = ne4 + "defecto = 1).\nA mayor peso, mayor proximidad "
        ne4 = ne4 + "relativa entre las entidades relacionadas."
        ne4 = ne4 + "\nAtajo de teclado: <Ctrl+w>"
        self._ne_peso = emergente.NotaEmergente(self._etq_peso_rel, ne4)
        self._etq_peso_rel.bind("<Enter>", self._ne_peso.mostrar)
        self._etq_peso_rel.bind("<Leave>", self._ne_peso.ocultar)
        # Nota emergente sobre etiqueta Entidad2
        ne5: str ="<Ctrl+d> ingresa automáticamente el texto seleccionado"
        self._ne_ent2 = emergente.NotaEmergente(self._etq_entidad2, ne5)  
        self._etq_entidad2.bind("<Enter>", self._ne_ent2.mostrar)
        self._etq_entidad2.bind("<Leave>", self._ne_ent2.ocultar)
        # Nota emergente sobre boton Relacionar
        self._ne_btn_relacionar = emergente.NotaEmergente(
            self._btn_confirmar_relacion, "<Ctrl+f>"
        )
        self._btn_confirmar_relacion.bind("<Enter>", self._ne_btn_relacionar.mostrar)
        self._btn_confirmar_relacion.bind("<Leave>", self._ne_btn_relacionar.ocultar)
  
    def _establecer_atajos(self) -> None:
        """
        Vincula algunos artefactos y sus operaciones con atajos de teclado.
        """
        self._btn_notas.bind("<Return>",lambda e: self._abrir_notas())
        self._btn_reiniciar.bind("<Return>",lambda e: self._reiniciar())
        self._btn_tema.bind("<Return>",lambda e: self._cambiar_tema())
        self._btn_cargar_texto.bind("<Return>",lambda e: self._cargar_texto())
        # Cargar texto        
        self._btn_cargar_texto.bind_all("<Control-o>", lambda e: self._cargar_texto())
        self._btn_cargar_texto.bind_all("<Control-O>", lambda e: self._cargar_texto())
        # Ingresar entidad1
        self._area_texto.bind("<Control-a>", lambda e: self.atajo(1))
        self._area_texto.bind("<Control-A>", lambda e: self.atajo(1))
        self._ingr_entidad1.bind("<Control-a>", lambda e: self.atajo(1))
        self._ingr_entidad1.bind("<Control-A>", lambda e: self.atajo(1))
        self._ingr_relacion.bind("<Control-a>", lambda e: self.atajo(1))
        self._ingr_relacion.bind("<Control-A>", lambda e: self.atajo(1))
        self._ingr_entidad2.bind("<Control-a>", lambda e: self.atajo(1))
        self._ingr_entidad2.bind("<Control-A>", lambda e: self.atajo(1))        
        self._btn_confirmar_relacion.bind("<Control-a>", lambda e: self.atajo(1))
        self._btn_confirmar_relacion.bind("<Control-A>", lambda e: self.atajo(1))
        self._ingr_peso_rel.bind("<Control-a>", lambda e: self.atajo(1))
        self._ingr_peso_rel.bind("<Control-A>", lambda e: self.atajo(1))
        # Ingresar relación
        self._area_texto.bind("<Control-s>", lambda e: self.atajo(2))
        self._area_texto.bind("<Control-S>", lambda e: self.atajo(2))
        self._ingr_entidad1.bind("<Control-s>", lambda e: self.atajo(2))
        self._ingr_entidad1.bind("<Control-S>", lambda e: self.atajo(2))
        self._ingr_relacion.bind("<Control-s>", lambda e: self.atajo(2))
        self._ingr_relacion.bind("<Control-S>", lambda e: self.atajo(2))
        self._ingr_entidad2.bind("<Control-s>", lambda e: self.atajo(2))
        self._ingr_entidad2.bind("<Control-S>", lambda e: self.atajo(2))        
        self._btn_confirmar_relacion.bind("<Control-s>", lambda e: self.atajo(2))
        self._btn_confirmar_relacion.bind("<Control-S>", lambda e: self.atajo(2))
        self._ingr_peso_rel.bind("<Control-s>", lambda e: self.atajo(2))
        self._ingr_peso_rel.bind("<Control-S>", lambda e: self.atajo(2))
        # Ingresar peso
        self._area_texto.bind("<Control-w>", lambda e: self.atajo(6))
        self._area_texto.bind("<Control-W>", lambda e: self.atajo(6))
        self._ingr_entidad1.bind("<Control-w>", lambda e: self.atajo(6))
        self._ingr_entidad1.bind("<Control-W>", lambda e: self.atajo(6))
        self._ingr_relacion.bind("<Control-w>", lambda e: self.atajo(6))
        self._ingr_relacion.bind("<Control-W>", lambda e: self.atajo(6))
        self._ingr_entidad2.bind("<Control-w>", lambda e: self.atajo(6))
        self._ingr_entidad2.bind("<Control-W>", lambda e: self.atajo(6))        
        self._btn_confirmar_relacion.bind("<Control-w>", lambda e: self.atajo(6))
        self._btn_confirmar_relacion.bind("<Control-w>", lambda e: self.atajo(6))
        self._ingr_peso_rel.bind("<Control-w>", lambda e: self.atajo(6))
        self._ingr_peso_rel.bind("<Control-W>", lambda e: self.atajo(6))
        # Ingresa entidad2
        self._area_texto.bind("<Control-d>", lambda e: self.atajo(3))
        self._area_texto.bind("<Control-D>", lambda e: self.atajo(3))
        self._ingr_entidad1.bind("<Control-d>", lambda e: self.atajo(3))
        self._ingr_entidad1.bind("<Control-D>", lambda e: self.atajo(3))
        self._ingr_relacion.bind("<Control-d>", lambda e: self.atajo(3))
        self._ingr_relacion.bind("<Control-D>", lambda e: self.atajo(3))
        self._ingr_entidad2.bind("<Control-d>", lambda e: self.atajo(3))
        self._ingr_entidad2.bind("<Control-D>", lambda e: self.atajo(3))        
        self._btn_confirmar_relacion.bind("<Control-d>", lambda e: self.atajo(3))
        self._btn_confirmar_relacion.bind("<Control-D>", lambda e: self.atajo(3))
        self._ingr_peso_rel.bind("<Control-d>", lambda e: self.atajo(3))
        self._ingr_peso_rel.bind("<Control-D>", lambda e: self.atajo(3))
        # Relacionar entidades
        self._area_texto.bind("<Control-f>",lambda e: self.atajo(4))
        self._area_texto.bind("<Control-F>",lambda e: self.atajo(4))
        self._ingr_entidad1.bind("<Return>", lambda e: self.atajo(4))
        self._ingr_relacion.bind("<Return>", lambda e: self.atajo(4))
        self._ingr_peso_rel.bind("<Return>", lambda e: self.atajo(4))
        self._ingr_entidad2.bind("<Return>", lambda e: self.atajo(4))
        self._btn_confirmar_relacion.bind("<Return>",lambda e: self.atajo(4))
        self._ingr_entidad1.bind("<Control-f>", lambda e: self.atajo(4))
        self._ingr_entidad1.bind("<Control-F>", lambda e: self.atajo(4))
        self._ingr_relacion.bind("<Control-f>", lambda e: self.atajo(4))
        self._ingr_relacion.bind("<Control-F>", lambda e: self.atajo(4))
        self._ingr_entidad2.bind("<Control-f>", lambda e: self.atajo(4))
        self._ingr_entidad2.bind("<Control-F>", lambda e: self.atajo(4))        
        self._btn_confirmar_relacion.bind("<Control-f>", lambda e: self.atajo(4))
        self._btn_confirmar_relacion.bind("<Control-F>", lambda e: self.atajo(4))
        self._ingr_peso_rel.bind("<Control-f>", lambda e: self.atajo(4))
        self._ingr_peso_rel.bind("<Control-F>", lambda e: self.atajo(4))
        # Borrar ultimo ingreso
        self._area_texto.bind("<Control-u>",lambda e: self.atajo(5))
        self._area_texto.bind("<Control-U>",lambda e: self.atajo(5))
        self._ingr_entidad1.bind("<Control-u>", lambda e: self.atajo(5))
        self._ingr_entidad1.bind("<Control-U>", lambda e: self.atajo(5))
        self._ingr_relacion.bind("<Control-u>", lambda e: self.atajo(5))
        self._ingr_relacion.bind("<Control-U>", lambda e: self.atajo(5))
        self._ingr_entidad2.bind("<Control-u>", lambda e: self.atajo(5))
        self._ingr_entidad2.bind("<Control-U>", lambda e: self.atajo(5))        
        self._btn_confirmar_relacion.bind("<Control-u>", lambda e: self.atajo(5))
        self._btn_confirmar_relacion.bind("<Control-U>", lambda e: self.atajo(5))
        self._ingr_peso_rel.bind("<Control-u>", lambda e: self.atajo(5))
        self._ingr_peso_rel.bind("<Control-U>", lambda e: self.atajo(5))
        # Abrir notas
        self._area_texto.bind("<Control-n>",lambda e: self.atajo(7))
        self._area_texto.bind("<Control-N>",lambda e: self.atajo(7))
        self._ingr_entidad1.bind("<Control-n>", lambda e: self.atajo(7))
        self._ingr_entidad1.bind("<Control-N>", lambda e: self.atajo(7))
        self._ingr_relacion.bind("<Control-n>", lambda e: self.atajo(7))
        self._ingr_relacion.bind("<Control-N>", lambda e: self.atajo(7))
        self._ingr_entidad2.bind("<Control-n>", lambda e: self.atajo(7))
        self._ingr_entidad2.bind("<Control-N>", lambda e: self.atajo(7))        
        self._btn_confirmar_relacion.bind("<Control-n>", lambda e: self.atajo(7))
        self._btn_confirmar_relacion.bind("<Control-N>", lambda e: self.atajo(7))
        self._ingr_peso_rel.bind("<Control-n>", lambda e: self.atajo(7))
        self._ingr_peso_rel.bind("<Control-N>", lambda e: self.atajo(7))
        # Guardar proyecto
        self._area_texto.bind("<Control-g>",lambda e: self.atajo(8))
        self._area_texto.bind("<Control-G>",lambda e: self.atajo(8))
        self._ingr_entidad1.bind("<Control-g>", lambda e: self.atajo(8))
        self._ingr_entidad1.bind("<Control-G>", lambda e: self.atajo(8))
        self._ingr_relacion.bind("<Control-g>", lambda e: self.atajo(8))
        self._ingr_relacion.bind("<Control-G>", lambda e: self.atajo(8))
        self._ingr_entidad2.bind("<Control-g>", lambda e: self.atajo(8))
        self._ingr_entidad2.bind("<Control-G>", lambda e: self.atajo(8))        
        self._btn_confirmar_relacion.bind("<Control-g>", lambda e: self.atajo(8))
        self._btn_confirmar_relacion.bind("<Control-G>", lambda e: self.atajo(8))
        self._ingr_peso_rel.bind("<Control-g>", lambda e: self.atajo(8))
        self._ingr_peso_rel.bind("<Control-G>", lambda e: self.atajo(8))
        
    def _reiniciar(self) -> None:
        """
        Recibe la orden de reinicio y activa la ventana de dialogo.
        """
        mensaje: str = "Se eliminarán todos los datos registrados. "
        mensaje = mensaje + "Esta acción no se puede revertir."
        self._ventana_dialogo(mensaje, "Confirmar reinicio")            

    def _ventana_dialogo(self, contenido: str, titulo_ventana: str) -> None:
        """
        Construye la ventana de confirmación de reinicio.

        :param contenido: Mensaje a notificar.
        :type contenido: str
        :param titulo_ventana: Título de la ventana.
        :type titulo_ventana: str
        """
        self._dialogo: tk.Toplevel = tk.Toplevel(
            self._contenedor_artf, **comunes.atrb_contenedor_artf
        )
        self._dialogo.title(titulo_ventana)        
        self._etiqueta_mensaje: tk.Label = tk.Label(
            self._dialogo,
            text=contenido,
            justify="left",
            **comunes.atrb_etq_ayuda
        )
        if titulo_ventana == "Confirmar reinicio":
            # La centor en la pantalla
            self._raiz.update_idletasks()
            ancho: int = 600 
            alto: int = 140 
            ancho_pantalla: int = self._raiz.winfo_screenwidth()
            alto_pantalla: int = self._raiz.winfo_screenheight()
            x: int = (ancho_pantalla - ancho) // 2
            y: int = (alto_pantalla - alto) // 2
            self._dialogo.geometry(f"{ancho}x{alto}+{x}+{y}")
            
            self._boton_confirmar: tk.Button = tk.Button(
                self._dialogo,
                text="Confirmar",
                command=self._confirmar_reinicio,
                **comunes.atrb_btn_aplicar
            )
            self._boton_cancelar: tk.Button = tk.Button(
                self._dialogo,
                text="Cancelar",
                command=self._cancelar_reinicio,
                **comunes.atrb_btn_cancelar
            )
            # Ubicación de los elementos
            self._etiqueta_mensaje.grid(
                row=0, column=0, columnspan=2, sticky="ew", padx=(100,10), pady=(30,10)
            )
            self._boton_confirmar.grid(row=1, column=0, padx=(100,10), pady=(10,30))
            self._boton_cancelar.grid(row=1, column=1, padx=(10,10), pady=(10,30))
            self._boton_cancelar.focus_set()
            # Atajos de teclado
            self._boton_cancelar.bind("<Return>", self._cancelar_reinicio)
            self._boton_confirmar.bind("<Return>", self._confirmar_reinicio)
        else:
            self._dialogo.destroy()
            self._etiqueta_mensaje.destroy()            

    def _confirmar_reinicio(self, *args) -> None:
        """
        Destruye la ventana y envia al gestor la orden de reinicio.
        Args captura el evento producido al presionar el botón.
        """
        self._dialogo.destroy()
        self._area_texto.delete(1.0, tk.END)
        self._gestor.reiniciar()

    def _cancelar_reinicio(self, *args) -> None:
        """
        Destruye la ventana. Args captura el evento producido al presionar
        el botón.
        """
        self._dialogo.destroy()
        
