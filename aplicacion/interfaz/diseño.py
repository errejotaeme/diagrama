import tkinter as tk
from aplicacion.control import gestor
from aplicacion.interfaz.componentes.areas import edicion, grafico, proyecto, texto
from aplicacion.interfaz.componentes.elementos import emergente
from aplicacion.interfaz import comunes
from tkinter import ttk


class Interfaz:
    """
    Clase encargada de construir los componentes básicos de la aplicación.

    :param bucle: Instancia de la clase encargada de crear el bucle de la aplicación y gestionar el cambio de tema.
    :type bucle: Bucle
    :param tema: El tema actual de la aplicacion.
    :type tema: str
    :param respaldo_pendiente: Indica si se debe cargar el respaldo temporal guardado antes del reinicio por cambio de tema.
    :type respaldo_pendiente: bool
    :param diagrama_no_vacio: Indica si se debe actualizar el artefacto del área de gráfico para que coincida con el color de fondo del grafo.
    :type diagrama_no_vacio: bool
    :param proyecto_activo: Datos que permiten volver a activar el proyecto que estaba abierto, al reiniciar por cambio en tema.
    :type proyecto_activo: tuple[str, str]
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk
    :param texto_respaldo: Respaldo del contenido del área de texto que se vuelve a cargar cuando se reinicia por cambio de tema.
    :type texto_respaldo: str
    """

    def __init__(
        self,
        bucle,
        tema: str,
        respaldo_pendiente: bool,
        diagrama_no_vacio: bool,
        proyecto_activo: tuple[str, str],
        raiz: tk.Tk,
        texto_respaldo: str
    ):
        """
        Constructor de la clase Interfaz.
        """
        self._ventana_raiz: tk.Tk = raiz
        self._bucle = bucle
        self._tema: str = tema
        self._respaldo_pendiente: bool = respaldo_pendiente
        self._proyecto_activo: tuple[str, str] = proyecto_activo
        self._diagrama_no_vacio: bool = diagrama_no_vacio
        self._texto_respaldo: str = texto_respaldo
    
    def desplegar(self) -> None:
        """
        Instancia y ordena los elementos en la ventana principal.
        Da inicio al bucle de la aplicación.
        """
        instancia_gestor = gestor.Gestor(self._ventana_raiz, self._tema)
        # Restablece los recursos en caso de que se haya modificado 
        # la estructura de las tablas
        instancia_gestor.restablecer_todo()        
        # Panel principal
        estructura: tk.PanedWindow = tk.PanedWindow(
            self._ventana_raiz, orient=tk.HORIZONTAL
        )
        estructura.pack(fill=tk.BOTH, expand=True)
        # Pestañas
        estilo_pestaña: ttk.Style = ttk.Style()
        estilo_pestaña.theme_use("default")
        estilo_pestaña.configure("TNotebook", **comunes.atrb_color_fondo)
        estilo_pestaña.configure("TNotebook.Tab", **comunes.atrb_pestañas_t)
        estilo_pestaña.map(
            "TNotebook.Tab",
            background = [
                ("active", comunes.marron_pestaña_a),
                ("selected", comunes.marron_pestaña_s)
            ],
            foreground = [("selected", comunes.color_tex_gral)]
                )
        pestañas: ttk.Notebook = ttk.Notebook(estructura, style="TNotebook")
        estructura.add(pestañas)
        
        area_texto: texto.AreaDeTexto = texto.AreaDeTexto(
            pestañas,
            instancia_gestor,
            self._ventana_raiz,
            self._bucle,
            self._tema,
            self._texto_respaldo
        )
        p_texto: tk.Frame = area_texto.artefacto()
        pestañas.add(p_texto, text = "Tarea")

        area_edicion: edicion.AreaEdicion = edicion.AreaEdicion(
            pestañas, instancia_gestor, self._ventana_raiz
        )
        p_edicion:tk.Frame = area_edicion.artefacto()
        pestañas.add(p_edicion, text = "Edición")

        area_proyecto: proyecto.AreaProyecto = proyecto.AreaProyecto(
            pestañas, instancia_gestor, self._ventana_raiz
        )
        p_proyecto: tk.Frame = area_proyecto.artefacto()       
        pestañas.add(p_proyecto, text = "Proyecto")       
        
        # Panel interior derecho
        contenedor_seccion_grafico: tk.PanedWindow = tk.PanedWindow(
            estructura, orient=tk.VERTICAL
        )
        estructura.add(contenedor_seccion_grafico)    

        area_grafico: grafico.AreaDeGrafico = grafico.AreaDeGrafico(
            contenedor_seccion_grafico,  instancia_gestor
        )
        artf_grafico: tk.Frame = area_grafico.artefacto()
        contenedor_seccion_grafico.add(artf_grafico)
        
        # Enlazo el gestor con las secciones
        instancia_gestor.enlazar(
            area_texto,
            area_edicion,
            area_proyecto,
            area_grafico,
            self._respaldo_pendiente,
            self._diagrama_no_vacio,
            self._proyecto_activo
        )

        # Inicio el bucle de la aplicación
        self._ventana_raiz.mainloop()
        # Vacío las tablas y archivos cuando se cierra la aplicación
        instancia_gestor.restablecer_todo()
        
