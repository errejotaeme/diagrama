import tkinter as tk
from tkinter import filedialog, ttk
from aplicacion.interfaz import comunes
from aplicacion.interfaz.componentes.elementos import emergente

class PantallaGuardar:
    """
    Clase encargada de construir una ventana independiente que apoya
    la operación de guardar el proyecto actual.

    :param proyecto: La instancia de la clase encargada de permitir guardar, exportar o cargar un proyecto.
    :type proyecto: AreaProyecto
    :param gestor: La instancia de la clase encargada de gestionar la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor 
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk
    :param ancestro: El marco donde se ubica el contenedor principal y/o los artefactos instanciados por la clase.
    :type ancestro: Frame
    """

    def __init__(self, proyecto, gestor, raiz: tk.Tk, ancestro: tk.Frame):
        """
        Constructor de la clase PantallaGuardar.
        """
        self._proyecto = proyecto
        self._ancestro: tk.Frame = ancestro
        self._gestor = gestor
        self._raiz: tk.Tk = raiz    
        self._pantalla_guardar: tk.Toplevel = tk.Toplevel(
            self._ancestro,
            **comunes.atrb_contenedor_artf
        )        
        self._pantalla_guardar.title("Guardar proyecto")
        # Gestiono el cierre de la pantalla
        # por fuera del proceso de guardado
        self._pantalla_guardar.protocol(
            "WM_DELETE_WINDOW", self._cancelar_guardar
        )
        # Obtengo los datos para centrarla en la pantalla
        self._raiz.update_idletasks()
        ancho: int = 500 
        alto: int = 260
        ancho_pantalla: int = self._raiz.winfo_screenwidth()
        alto_pantalla: int = self._raiz.winfo_screenheight()
        x: int = (ancho_pantalla - ancho) // 2
        y: int = (alto_pantalla - alto) // 2
        self._pantalla_guardar.geometry(f"{ancho}x{alto}+{x}+{y}")        
        self._contenedor = tk.Frame(  # Marco principal de la pantalla
            self._pantalla_guardar, **comunes.atrb_contenedor_artf
        )
        self._contenedor.pack()
        self._construir_pantalla(self._contenedor)
        self._crear_notas_emergentes()
        # Guarda los datos del proyecto para restablecerlos
        # si se cancela la operación y vacío las variables
        self._respaldo_recordar: tuple[str, str] = (
            self._proyecto.directorio_activado,
            self._proyecto.nombre_proyecto
        )
        self._proyecto.directorio_activado = ""
        self._proyecto.nombre_proyecto = ""


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
        Oculta el aviso que esté visible.
        """
        self._etq_aviso.config(text="")
        self._etq_aviso.update_idletasks()

    def _activar(self) -> None:
        """
        Alamacena u olvida los datos en las variables que permiten acceder,
        desde el área de tarea, a la operación de guardar el proyecto activado
        con el atajo de teclado.
        """
        if self._var_recordar.get():
            nombre_proyecto: str = self._var_nombre_proyecto.get()
            if nombre_proyecto:
                self._proyecto.nombre_proyecto = nombre_proyecto
                self.ocultar_aviso()
            else:
                aviso: str = "Ingrese un nombre de proyecto para activar esta opción"
                self.mostrar_aviso(aviso)
                self._var_recordar.set(False)
                return
        else:
            self._proyecto.nombre_proyecto = ""
            self._proyecto.directorio_activado = ""
            self._ingr_nombre.delete(0, tk.END)        

    def _cancelar_guardar(self) -> None:
        """
        Recupera los datos respaldados y cierra la ventana.
        """
        self._proyecto.directorio_activado = self._respaldo_recordar[0]
        self._proyecto.nombre_proyecto = self._respaldo_recordar[1]
        self._proyecto.actualizar_etq_proyecto()
        self._pantalla_guardar.destroy()                

    def _confirmar_guardar(self) -> None:
        """
        Verifica que se hayan ingresado los datos necesarios,
        guarda el proyecto y, si fue seleccionada la opción de
        recordar, almacena el nombre y ubicación del mismo.
        Caso contrario, vacía las variables y cierra la ventana.
        """
        self._proyecto.nombre_proyecto = self._var_nombre_proyecto.get()
        sin_nombre: bool = self._proyecto.nombre_proyecto == ""
        sin_ubicacion: bool = self._proyecto.directorio_activado == ""
        if sin_nombre:
            aviso:str = "Ingrese un nombre para su proyecto"
            self.mostrar_aviso(aviso)
            return
        self.ocultar_aviso()
        if sin_ubicacion:
            aviso = "Elija una carpeta donde guardar el proyecto"
            self.mostrar_aviso(aviso)
            return
        self.ocultar_aviso()
        if self._var_recordar.get():
            # Los proximos cambios se guardaran en el directorio activado
            self._gestor.guardar_proyecto(
                self._proyecto.directorio_activado,
                self._proyecto.nombre_proyecto
            )
        else:
            # Se vacian las variables que permiten guardar
            # directamente con el atajo de teclado
            self._gestor.guardar_proyecto(
                self._proyecto.directorio_activado,
                self._proyecto.nombre_proyecto
            )
            self._proyecto.directorio_activado = ""
            self._proyecto.nombre_proyecto = ""
        self._proyecto.actualizar_etq_proyecto()
        self._pantalla_guardar.destroy() 


    def _construir_botonera(self, ancestro: tk.Frame) -> None:
        """
        Construye los botones para guardar o cancelar y al marco que
        los contiene.

        :param ancestro: El marco donde se ubica el contenedor principal y/o los artefactos instanciados por la clase.
        :type ancestro: Frame
        """
        
        self._contenedor_botones: tk.Frame = tk.Frame(
            ancestro, **comunes.atrb_contenedor_artf
        )
        self._contenedor_botones.grid(
            row=4, column=0, padx=(0,0), pady=(30,0), sticky="e"
        )

        self._boton_confirmar: tk.Button = tk.Button(
            self._contenedor_botones,
            text="Confirmar",
            command=self._confirmar_guardar,
            **comunes.atrb_btn_aplicar
        )
        self._boton_confirmar.grid(
            row=0, column=0, sticky="ew", padx=(0,20), pady=(0,0)
        )
        self._boton_cancelar: tk.Button = tk.Button(
            self._contenedor_botones,
            text="Cancelar",
            command=self._cancelar_guardar,
            **comunes.atrb_btn_cancelar
        )
        self._boton_cancelar.grid(
            row=0, column=1, sticky="ew", padx=(0,0), pady=(0,0)
        )
        self._boton_cancelar.focus_set()


    def _construir_pantalla(self, ancestro: tk.Frame)->None:
        """
        Construye y ubica los artefactos necesarios para el proceso
        de guardar el proyecto.

        :param ancestro: El marco donde se ubica el contenedor principal y/o los artefactos instanciados por la clase.
        :type ancestro: Frame
        """
        # Encabezado y notas de aviso
        aux1: str = "La modificación externa del contenido o el nombre de los "
        aux2: str = "archivos .csv\npuede hacer irrecuperable el proyecto"
        aux3: str = aux1 + aux2
        self._etq_indicacion: tk.Label = tk.Label(
            ancestro, text = aux3, **comunes.atrb_etq_adv
        )
        self._etq_indicacion.grid(
            row=0, column=0, padx=(0,0), pady=(10,0), sticky="ew"
        )
        self._sep: ttk.Separator = ttk.Separator(
            ancestro, orient="horizontal"
        )
        self._sep.grid(
            row=1, column=0, columnspan=1, sticky="ew",padx=(15,15), pady=(10,0)
        )
        self._etq_aviso: tk.Label = tk.Label( 
            ancestro, text = "", **comunes.atrb_etq_aviso
        )
        self._etq_aviso.grid(
            row=2, column=0, padx=(0,0), pady=(10,0), sticky="ew"
        )
        # Sección de entradas y opción
        self._marco_nombre: tk.Frame = tk.Frame(
            ancestro, **comunes.atrb_contenedor_artf
        )
        self._marco_nombre.grid(
            row=3, column=0, sticky="ew", padx=(0,0), pady=(10,0)
        )        
        self._etq_nombre: tk.Label = tk.Label(
            self._marco_nombre,
            text = "Nombre del proyecto:",
            **comunes.atrb_etq_ayuda
        )
        self._etq_nombre.grid(
            row=0, column=0, sticky="sw", padx=(0,0), pady=(10,0)
        )
        self._var_nombre_proyecto: tk.StringVar = tk.StringVar()
        self._ingr_nombre: tk.Entry = tk.Entry(
            self._marco_nombre,
            textvariable = self._var_nombre_proyecto,
            **comunes.atrb_entrada
        )
        self._ingr_nombre.grid(
            row=1, column=0, sticky="ew", padx=(0,10), pady=(0,0)
        )
        self._var_recordar: tk.BooleanVar = tk.BooleanVar()
        self._opc_recordar: tk.Checkbutton = tk.Checkbutton(
            self._marco_nombre,
            text="Recordar directorio ",
            variable=self._var_recordar,
            **comunes.atrb_btn_check_np,
            command=self._activar,
        )       
        self._opc_recordar.grid(
            row=1, column=1, sticky="ew", padx=(0,10), pady=(0,0)
        )
        self._btn_seleccionar_directorio: tk.Button = tk.Button(
            self._marco_nombre,
            text="Carpeta",
            command=self._seleccionar_directorio,
            **comunes.atrb_btn_abrir_carpeta
        )
        self._btn_seleccionar_directorio.grid(
            row=1, column=2, sticky="ew", padx=(0,10), pady=(0,0)
        )
        self._construir_botonera(ancestro)

    def _crear_notas_emergentes(self) -> None:
        """
        Construye las notas emergentes asociadas a los artefactos de la pantalla.
        """
        ne_aux:str = "Activarlo para sobrescribir en el directorio seleccionado usando el atajo <Ctrl+g>\n"
        ne_aux = ne_aux + "Desactivarlo para olvidar el directorio seleccionado"
        self._ne_nombre = emergente.NotaEmergente(self._opc_recordar, ne_aux)  
        self._opc_recordar.bind("<Enter>", self._ne_nombre.mostrar)
        self._opc_recordar.bind("<Leave>", self._ne_nombre.ocultar)

    def _seleccionar_directorio(self) -> None:
        """
        Abre una ventana de diálogo que permite elegir la ubicación
        donde se creará la carpeta con los archivos necesarios para
        poder recuperar el proyecto.
        """
        titulo:str = "Se creará una carpeta en esta ubicación"
        directorio = filedialog.askdirectory(
            title=titulo, parent=self._pantalla_guardar
        )
        if directorio:
            nombre: str = self._var_nombre_proyecto.get()
            if nombre:
                if nombre == "__respaldo__":
                    aviso:str = "Palabra reservada: por favor elija otro nombre de proyecto"
                    self.mostrar_aviso(aviso)
                    return
                self._proyecto.directorio_activado = directorio
                self._proyecto.nombre_proyecto = nombre
                self.ocultar_aviso()
            else:
                self.mostrar_aviso("Ingrese un nombre para su proyecto")
        else:
            self.mostrar_aviso("Seleccione una carpeta donde guardar el proyecto")

