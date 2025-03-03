import tkinter as tk
from tkinter import scrolledtext, ttk
from aplicacion.interfaz import comunes
from aplicacion.interfaz.componentes.elementos import emergente

class PantallaNotas:
    """
    Clase encargada de de construir una ventana independiente en la cual
    guardar notas relacionadas a la tarea en proceso.


    :param gestor: La instancia de la clase encargada de gestionar la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor 
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk
    :param ancestro: El marco donde se ubica el contenedor principal y/o los artefactos instanciados por la clase.
    :type ancestro: Frame
    """

    def __init__(self, gestor, raiz: tk.Tk, ancestro: tk.Frame):
        """
        Constructor de la clase PantallaNotas. 
        """
        self._ancestro: tk.Frame = ancestro
        self._gestor = gestor
        self._raiz: tk.Tk = raiz
        # abro un top level que permita editar todo....
        self._pantalla_notas: tk.Toplevel = tk.Toplevel(
            self._ancestro,
            **comunes.atrb_contenedor_artf
        )        
        self._pantalla_notas.title("Notas propias")        
        # Obtengo los datos para centrarla en la pantalla
        self._raiz.update_idletasks()
        ancho: int = 600 
        alto: int = 480
        ancho_pantalla: int = self._raiz.winfo_screenwidth()
        alto_pantalla: int = self._raiz.winfo_screenheight()
        x: int = (ancho_pantalla - ancho) // 2
        y: int = (alto_pantalla - alto) // 2
        self._pantalla_notas.geometry(f"{ancho}x{alto}+{x}+{y}")
        self._contenedor: tk.Frame = tk.Frame(  # Marco principal de la pantalla
            self._pantalla_notas, **comunes.atrb_contenedor_artf
        )
        self._contenedor.pack()
        self._contenedor.grid_rowconfigure(0, weight=1)
        self._contenedor.grid_columnconfigure(0, weight=1)
        self._crear_texto_desplazable()
        self._crear_botonera()
        self._cargar_notas()
        self._establecer_atajos()

    def _establecer_atajos(self) -> None:
        """
        Asocia los artefactos con atajos de teclados que efectúan llamadas
        a los métodos correspondientes.
        """
        self._pantalla_notas.bind("<Control-g>", self._guardar)
        self._pantalla_notas.bind("<Control-G>", self._guardar)
        self._area_texto.bind("<Control-g>", self._guardar)
        self._area_texto.bind("<Control-G>", self._guardar)
        self._btn_guardar.bind("<Return>", self._guardar)
        self._pantalla_notas.bind("<Control-q>", self._salir)
        self._pantalla_notas.bind("<Control-Q>", self._salir)
        self._area_texto.bind("<Control-q>", self._salir)
        self._area_texto.bind("<Control-Q>", self._salir)
        

    def _crear_texto_desplazable(self) -> None:
        """
        Crea el artefacto donde apuntar las notas.
        """
        self._area_texto = scrolledtext.ScrolledText(
            self._contenedor,
            wrap=tk.WORD,
            state=tk.NORMAL,
            undo=True,
            maxundo=50,
            **comunes.atrb_area_txt
        )        
        self._area_texto.tag_configure(
            "formato", spacing1=1, spacing2=3 , spacing3=1
        )        
        self._area_texto.grid(
            row=0, column=0, padx=(20,20), pady=(20,10), sticky="nsew"
        )

    def _crear_botonera(self) -> None:
        """
        Crea el marco que contiene al botón de guardado.
        """
        self._marco_botonera: tk.Frame = tk.Frame(
            self._contenedor, **comunes.atrb_contenedor_artf
        )
        self._marco_botonera.grid(
            row=1, column=0, padx=(0,35), pady=(0,20), sticky="e"
        )
        self._btn_guardar: tk.Button = tk.Button(
            self._marco_botonera,
            text="Guardar",
            command=self._guardar,
            **comunes.atrb_btn_cargar_texto
        )
        self._btn_guardar.grid(
            row=0, column=0, padx=(0, 0), pady=(10,0), sticky="ew"
        )

    def _cargar_notas(self) -> None:
        """
        Obtiene del gestor las notas que se hayan registrado cuando se
        guardó el proyecto. Cuando se empieza de cero, éstas son una cadena
        vacía.
        """
        notas: str = self._gestor.obtener_notas()
        self._area_texto.delete(1.0, tk.END)
        self._area_texto.insert(tk.END, notas)
        self._area_texto.tag_add("formato", "1.0", "end")  
        self._area_texto.update_idletasks()    
        self._area_texto.focus()               

    def _guardar(self, *args) -> None:
        """
        Obtiene el texto del ScrolledText y lo guardo en un txt para poder
        recuperarlo al cargar un proyecto. Args captura los eventos
        vinculados a los artefactos que llaman a éste método
        """        
        notas: str = str(self._area_texto.get("1.0", tk.END))
        self._gestor.guardar_notas(notas)
        self._pantalla_notas.destroy()

    def _salir(self, *args) -> None:
        """
        Cierra la ventana que contiene a la pantalla de notas. Args captura
        los eventos vinculados a los artefactos que llaman a éste método
        """
        self._pantalla_notas.destroy()    
