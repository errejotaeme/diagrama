import os
import tkinter as tk
from tkinter import filedialog, ttk
from aplicacion.interfaz import comunes
from aplicacion.interfaz.componentes.elementos import emergente
from aplicacion.interfaz.componentes.pantallas import pantalla_guardar

class AreaProyecto:
    """
    Clase encargada de permitir guardar, exportar o cargar un proyecto.

    :param ancestro: El artefacto que contiene al marco principal del área. 
    :type ancestro: ttk.Notebook
    :param gestor: Gestiona la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk
    """

    def __init__(self, ancestro: ttk.Notebook, gestor, raiz: tk.Tk):
        """
        Constructor de la clase AreaProyecto.
        """
        self._gestor = gestor
        self._raiz: tk.Tk = raiz
        self.directorio_activado: str = ""
        self.nombre_proyecto: str = ""
        self._atajos_visibles: bool = False
        self._atajos_ubicados: dict[str, tk.Frame | None] = {}
        self._contenedor_artf: tk.Frame = tk.Frame(  # Marco principal
            ancestro, **comunes.atrb_contenedor_artf) 
        self._etq_aviso = tk.Label(
            self._contenedor_artf, text="", **comunes.atrb_etq_aviso
        )
        self._etq_aviso.grid(
            row=0, column=1, columnspan=4, padx=(0,0), pady=(20,10), sticky="n"
        )
        self._crear_botonera()
        self._crear_notas_emergentes()
        self._crear_seccion_atajos()
        tex_aux: str = "No hay un proyecto activo"
        self.etq_proyecto_activo = tk.Label( 
            self._contenedor_artf, text=tex_aux, **comunes.atrb_etq_adv
        )
        self.etq_proyecto_activo.grid(
            row=2, column=0, columnspan=2, padx=(35,0), pady=(15,0), sticky="w"
        )        

    def artefacto(self) -> tk.Frame:
        """
        Retorna el contenedor principal de la sección.

        :return: El marco principal de la sección.
        :rtype: tk.Frame
        """
        return self._contenedor_artf

    def actualizar_etq_proyecto(self) -> None:
        """
        Actualiza la etiqueta que muestra el proyecto que está activo.
        """
        nombre: str = self.nombre_proyecto
        if nombre:
            self.etq_proyecto_activo.config(
                text=f"Proyecto activo: {nombre}"
            )
        else:
            self.etq_proyecto_activo.config(
                text=f"No hay un proyecto activo"
            )
        self.etq_proyecto_activo.update_idletasks() 

    def mostrar_aviso(self, aviso: str) -> None:
        """
        Actualiza la etiqueta de avisos con el texto recibido.

        :param aviso: La notificación a mostrar.
        :type aviso: str
        """
        self._etq_aviso.config(text=aviso)
        self._etq_aviso.update_idletasks()

    def obtener_proyecto_activo(self) -> tuple[str, str] | tuple[()]:
        """
        Devuelve los datos del proyecto activo o una tupla vacía. Se utiliza
        al reiniciar por cambio de tema.

        :rteurn: Los datos del proyecto activo.
        :rtype: tuple[str, str] | tuple[()]
        """
        if self.directorio_activado and self.nombre_proyecto:
            return self.directorio_activado, self.nombre_proyecto
        else:
            return ()
            

    def ocultar_aviso(self) -> None:
        """
        Oculta el aviso que esté visible.
        """
        self._etq_aviso.config(text="")
        self._etq_aviso.update_idletasks()

    def restaurar_proyecto_activo(self, proyecto: tuple[str, str]) -> None:
        """
        Si el Gestor detectó que había un proyecto activo al reinicio por cambio
        de tema, llama al método para que carge los datos y muestre la notificación

        :param proyecto: Los datos del proyecto activo.
        :type proyecto: tuple[str, str] | tuple[()]
        """
        directorio: str = proyecto[0]
        nombre: str = proyecto[1] 
        self.directorio_activado = directorio
        self.nombre_proyecto = nombre
        self.actualizar_etq_proyecto()
        
    def _crear_botonera(self) -> None:
        """
        Crea los artefactos que habilitan las opciones de proyecto.
        """
        self._marco_botonera: tk.Frame = tk.Frame(
            self._contenedor_artf, **comunes.atrb_contenedor_artf
        )
        self._marco_botonera.grid(
            row=1, column=0, sticky="ew", padx=(20,10), pady=(10,0)
        )
        self._sep1: ttk.Separator = ttk.Separator(
            self._marco_botonera, orient="horizontal"
        )
        self._sep1.grid(
            row=1, column=0, columnspan=1, sticky="ew",padx=(15,15), pady=(10,0)
        )
        # Exportar diagrama
        self._btn_exportar_diagrama: tk.Button = tk.Button(
            self._marco_botonera,
            text="Exportar diagrama",
            command=self._exportar_diagrama,
            **comunes.atrb_btn_proyecto_ex
        )
        self._btn_exportar_diagrama.grid(
            row=2, column=0, sticky="ew", padx=(15,15), pady=(15,0)
        )
        self._var_btn_radial: tk.StringVar = tk.StringVar()
        self._opc_pdf: tk.Radiobutton = tk.Radiobutton(
            self._marco_botonera,
            text=".pdf ",
            variable=self._var_btn_radial,
            value="pdf",
            **comunes.atrb_btn_radial
        )
        self._opc_pdf.grid(
            row=3, column=0, sticky="n", padx=(15,15), pady=(10,5)
        )
        self._opc_png: tk.Radiobutton = tk.Radiobutton(
            self._marco_botonera,
            text=".png ",
            variable=self._var_btn_radial,
            value="png",
            **comunes.atrb_btn_radial
        )
        self._opc_png.grid(
            row=4, column=0, sticky="n", padx=(15,15), pady=(0,0)
        )
        # Guardar proyecto
        self._btn_guardar_proyecto: tk.Button = tk.Button(
            self._marco_botonera,
            text="Guardar proyecto",
            command=self._pantalla_guardar,
            **comunes.atrb_btn_proyecto_g
        )
        self._btn_guardar_proyecto.grid(
            row=5, column=0, sticky="ew", padx=(15,15), pady=(13,15)
        )
        # Abrir proyecto
        self._btn_cargar_proyecto: tk.Button = tk.Button(
            self._marco_botonera,
            text="Abrir proyecto",
            command=self._cargar_proyecto,
            **comunes.atrb_btn_proyecto_ap
        )
        self._btn_cargar_proyecto.grid(
            row=6, column=0, sticky="ew", padx=(15,15), pady=(15,15)
        )
        self._btn_cargar_proyecto.focus_set()
        # Atajos
        self._btn_atajos: tk.Button = tk.Button(
            self._marco_botonera,
            text="Atajos de teclado",
            command=self._cargar_atajos,
            **comunes.atrb_btn_proyecto_at
        )
        self._btn_atajos.grid(
            row=7, column=0, sticky="ew", padx=(15,15), pady=(15,0)
        )
        self._sep2: ttk.Separator = ttk.Separator(
            self._marco_botonera, orient="horizontal"
        )
        self._sep2.grid(
            row=8, column=0, columnspan=1, sticky="ew", padx=(15,15), pady=(15,0)
        )


    def _crear_notas_emergentes(self) -> None:
        """
        Crea las notas emergentes del área.
        """
        # Exportar diagrama
        tex_ne1: str = "Seleccione un formato antes de elegir el directorio"
        self._ne_btn_exportar_diagrama: emergente.NotaEmergente = emergente.NotaEmergente(
            self._btn_exportar_diagrama, tex_ne1            
        ) 
        self._btn_exportar_diagrama.bind(
            "<Enter>", self._ne_btn_exportar_diagrama.mostrar
        )
        self._btn_exportar_diagrama.bind(
            "<Leave>", self._ne_btn_exportar_diagrama.ocultar
        )
        # Cargar proyecto
        tex_ne2: str ="Se reemplazarán los datos actuales: guarde el proyecto "
        tex_ne2 = tex_ne2 + "para no perder los cambios"
        self._ne_btn_cargar_proyecto: emergente.NotaEmergente = emergente.NotaEmergente(
            self._btn_cargar_proyecto, tex_ne2            
        ) 
        self._btn_cargar_proyecto.bind(
            "<Enter>", self._ne_btn_cargar_proyecto.mostrar
        )
        self._btn_cargar_proyecto.bind(
            "<Leave>", self._ne_btn_cargar_proyecto.ocultar
        )

    def _crear_seccion_atajos(self) -> None:
        """
        Construye la sección con los datos de los atajos de teclado.
        """
        self._contenedor_atajos: tk.Frame = tk.Frame(
            self._contenedor_artf, **comunes.atrb_contenedor_artf
        )
        self._estilo_lista_a: ttk.Style = ttk.Style()
        self._estilo_lista_a.configure("TFrame")
        self._estilo_lista_a.configure(
            "ListaA.TFrame", background=comunes.color_fondo_gral
        )
        self._lista_atajos: ttk.Frame = ttk.Frame(
            self._contenedor_atajos, style="ListaA.TFrame"
        )
        self._lista_atajos.grid(
            row=1, column=0, sticky="n", pady=(0,0)
        )
        self._cv_atajos: tk.Canvas = tk.Canvas( 
            self._lista_atajos,
            width=370,
            height=345,
            highlightthickness=0,
            **comunes.atrb_contenedor_artf
        )
        self._barra_v: ttk.Scrollbar = ttk.Scrollbar(
            self._lista_atajos, orient="vertical",
            command=self._cv_atajos.yview
        )  
        self._barra_h: ttk.Scrollbar = ttk.Scrollbar(
            self._lista_atajos, orient="horizontal",
            command=self._cv_atajos.xview
        )        
        self._marco_desplazable_a: ttk.Frame = ttk.Frame(
            self._cv_atajos, style="ListaA.TFrame"
        )
        self._marco_desplazable_a.bind(
            "<Configure>",
            lambda e: self._cv_atajos.configure(
                scrollregion=self._cv_atajos.bbox("all")
            )
        )
        self._cv_atajos.create_window(
            (0, 0), window=self._marco_desplazable_a, anchor="nw"
        )
        aux_titulo: str = "Atajos de teclado"
        self._etq_titulo_atajos: tk.Label = tk.Label(
            self._marco_desplazable_a, text=aux_titulo,
            **comunes.atrb_etq_titulo_a
        )
        self._etq_titulo_atajos.grid(row=0, column=0, sticky="w", pady=(0,5))
        self._sep_atajos: ttk.Separator = ttk.Separator(
            self._marco_desplazable_a, orient="horizontal"
        )
        self._sep_atajos.grid(
            row=1, column=0, columnspan=1, sticky="ew", padx=(0,0), pady=(0,15)
        )
        
        fila: int = 2
        for clave, valor in comunes.atajos.items():
            marco: tk.Frame = tk.Frame(
                self._marco_desplazable_a, **comunes.atrb_contenedor_artf
            )
            etq_tecla: tk.Label = tk.Label(
                marco, text=clave, **comunes.atrb_etq_tecla
            )
            etq_tecla.grid(row=0, column=0, sticky="w", pady=(0,5))
            etq_descripcion: tk.Label = tk.Label(
                marco, text=valor, **comunes.atrb_etq_ayuda
            )
            etq_descripcion.grid(row=0, column=1, sticky="w", pady=(0,5))
            sep: ttk.Separator = ttk.Separator(
                self._marco_desplazable_a, orient="horizontal"
            )
            fila_sep: int = fila + 1
            sep.grid(
                row=fila_sep, column=0, columnspan=1, sticky="ew", padx=(0,0), pady=(10,12)
            )
            marco.grid(row=fila, column=0, sticky="ew", padx=(0,0), pady=(0,0))
            self._atajos_ubicados[clave] = marco
            fila += 2
            
        self._cv_atajos.grid(row=0, column=0, sticky="ew", padx=(5,5))
        self._cv_atajos.configure(yscrollcommand=self._barra_v.set)
        self._cv_atajos.configure(xscrollcommand=self._barra_h.set)
        self._barra_v.grid(row=0, column=1, sticky="ns")
        self._barra_h.grid(row=1, column=0, sticky="ew")

    def _cargar_atajos(self) -> None:
        """
        Muestra u oculta la sección de atajos de teclado.
        """
        if not self._atajos_visibles:
            self._contenedor_atajos.grid(
                row=1, column=1, padx=(10,0), pady=(0,0), sticky="ew"
            )
            self._atajos_visibles = True
        else:
            self._contenedor_atajos.grid_forget()
            self._atajos_visibles = False
        

    def _exportar_diagrama(self) -> None:
        """
        Abre una ventana de dialogo que permite obtener la ubicacion donde
        guardar el diagrama. Luego capura la extensión seleccionada y envía
        los datos al gestor.
        """
        titulo: str = "Se guardará en esta ubicación"
        directorio: str | None = filedialog.askdirectory(title=titulo)
        if directorio:
            formato: str = self._var_btn_radial.get()
            if formato:
                self._gestor.exportar_diagrama(formato, directorio)
            else:
                self.mostrar_aviso("Seleccione un formato")
        else:
            self.mostrar_aviso("Seleccione un directorio")          

    def _cargar_proyecto(self) -> None:
        """
        Abre un proyecto guardado. Si la operación falla, restaura los datos
        previos al intento de carga.
        """
        titulo: str = "Ingrese a la carpeta del proyecto a cargar"
        directorio: str | None = filedialog.askdirectory(title=titulo)
        if directorio:
            self._gestor.respaldo_temporal()
            try:
                self._gestor.cargar_proyecto(directorio, "guardado")
                self.mostrar_aviso("El proyecto se cargó correctamente")
            except Exception as e:
                print(e)
                self._gestor.cargar_respaldo()
            self._gestor.eliminar_respaldo()

    def _pantalla_guardar(self) -> None:
        """
        Abre la pantalla con las opciones para guardar el proyecto.
        """
        pantalla = pantalla_guardar.PantallaGuardar(
            self, self._gestor, self._raiz, self._contenedor_artf
        )
