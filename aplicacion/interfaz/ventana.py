import tkinter as tk
from aplicacion.interfaz import diseño
from aplicacion.interfaz import comunes



class Bucle:
    """
    Clase encargada de crear el bucle de la aplicación y gestionar el cambio
    de tema.
    """

    def __init__(self):
        self._tema: str = "oscuro"  # Tema de la aplicación (oscuro por defecto)
        self._cargar_colores()
        self._respaldo_pendiente: bool = False  # Indica si el Gestor debe cargar la carpeta respaldo
        self._diagrama_no_vacio: bool = False  # Indica si se debe modificar el color de fondo del grafo
        self._proyecto_activo: tuple = ()  # Nombre y ubicación del proyecto en el que se está trabajando
        self._texto_respaldo: str = ""  # Contenido del área de texto
    
    def empezar(self) -> None:
        """
        Crea la ventana principal, configura sus dimensiones e instancia
        a la clase encargada de construir y desplegar los elementos de la
        aplicación.
        """
        self._raiz = tk.Tk()  # Ventana principal (controla el bucle de la aplicación)
        ancho: int = self._raiz.winfo_screenwidth()
        alto: int = self._raiz.winfo_screenheight()
        self._raiz.geometry(f"{ancho}x{alto}")    
        self._raiz.resizable(True, True)
        self._x_pantalla = self._raiz.winfo_screenwidth()
        self._y_pantalla = self._raiz.winfo_screenheight()
        self._raiz.maxsize(self._x_pantalla,self._y_pantalla)
        self._raiz.title("Diagrama")
        self._vista: diseño.Interfaz = diseño.Interfaz(
            self,
            self._tema,
            self._respaldo_pendiente,
            self._diagrama_no_vacio,
            self._proyecto_activo,
            self._raiz,
            self._texto_respaldo
        ) 
        self._vista.desplegar()

    def cambiar_tema(
        self,
        diagrama_no_vacio: bool,
        proyecto_activo: tuple[str, str],
        texto_respaldo: str
    ) -> None:
        """
        Alterna entre el tema claro y el oscuro.
        
        :param diagrama_no_vacio: Indica si se debe actualizar el artefacto del área de gráfico para que coincida con el color de fondo del grafo.
        :type diagrama_no_vacio: bool
        :param proyecto_activo: Datos que permiten volver a activar el proyecto que estaba abierto, al reiniciar por cambio en tema.
        :type proyecto_activo: tuple[str, str]
        :param texto_respaldo: Respaldo del contenido del área de texto que se vuelve a cargar cuando se reinicia por cambio de tema.
        :type texto_respaldo: str
        """
        self._diagrama_no_vacio = diagrama_no_vacio
        self._proyecto_activo = proyecto_activo
        self._texto_respaldo = texto_respaldo
        if self._tema == "claro":
            self._tema_oscuro()
            self._tema = "oscuro"
        else:
            self._tema_claro()
            self._tema = "claro"
        self._respaldo_pendiente = True
        self._raiz.destroy()
        self.empezar()

    def _cargar_colores(self) -> None:
        """
        Establece los colores de cada tema.
        """
        # Colores tema claro
        self.color_fondo_grafo_c = "#f3ecec"
        self.color_grafo_c = "#2b2525"
        self.color_tex_grafo_c = "#ffffff"
        self.color_tex_gral_c = "#000000"
        self.color_fondo_gral_c = "#e7baa0" # Predominante
        self.color_tex_mensaje_c = "#000000"
        self.color_tex_etq_ayuda_c = "#141414"
        self.color_fondo_entrada_c = "#f3ecec"
        self.marron_pestaña_a_c = "#f9c7ad"
        self.marron_pestaña_s_c = "#e7baa0"
        self.marron_pestaña_o_c = "#c29b87"
        self.marron_pestaña_c_c = "#a09797"
        self.color_btn_tema_c = "#423b3b" 
        self.color_btn_tema_tex_c = "#ffffff"
        self.color_btn_tema_activo_c = "#5b5151"
        
        # Colores tema oscuro
        self.color_fondo_grafo_o = "#111111"
        self.color_grafo_o = "#f1e5e0"
        self.color_tex_grafo_o = "#000000"
        self.color_tex_gral_o = "#ffffff" 
        self.color_fondo_gral_o = "#111111" # Predominante
        self.color_tex_mensaje_o = "#ffffff"
        self.color_tex_etq_ayuda_o = "#fcfcfc"
        self.color_fondo_entrada_o = "#272727"
        self.marron_pestaña_a_o = "#545454"
        self.marron_pestaña_s_o = "#111111"
        self.marron_pestaña_o_o = "#363636"
        self.marron_pestaña_c_o = "#a09797"
        self.color_btn_tema_o = "#e7b9a0"
        self.color_btn_tema_tex_o = "#000000"
        self.color_btn_tema_activo_o = "#f9c7ad"        

    def _tema_claro(self) -> None:
        """
        Actualiza las entradas de los diccionarios que definen el estilo
        de la aplicación.
        """
        comunes.color_fondo_grafo = self.color_fondo_grafo_c
        comunes.color_grafo = self.color_grafo_c
        comunes.color_tex_grafo = self.color_tex_grafo_c
        comunes.color_tex_gral = self.color_tex_gral_c 
        comunes.color_fondo_gral = self.color_fondo_gral_c
        comunes.color_tex_mensaje = self.color_tex_mensaje_c 
        comunes.color_tex_etq_ayuda = self.color_tex_etq_ayuda_c
        comunes.color_fondo_entrada = self.color_fondo_entrada_c
        comunes.marron_pestaña_a = self.marron_pestaña_a_c
        comunes.marron_pestaña_s = self.marron_pestaña_s_c
        comunes.marron_pestaña_o = self.marron_pestaña_o_c
        comunes.marron_pestaña_c = self.marron_pestaña_c_c
        comunes.color_btn_tema = self.color_btn_tema_c 
        comunes.color_btn_tema_tex = self.color_btn_tema_tex_c
        comunes.color_btn_tema_activo = self.color_btn_tema_activo_c      
        comunes.atrb_color_fondo["background"] = self.color_fondo_gral_c
        comunes.atrb_pestañas_t["background"] = self.marron_pestaña_o_c
        comunes.atrb_pestañas_t["foreground"] = self.color_tex_gral_c
        comunes.atrb_menu_ed["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_menu_ed["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_menu_ed["activebackground"] = self.marron_pestaña_a_c
        comunes.atrb_menu_ed["bg"] = self.marron_pestaña_c_c
        comunes.atrb_menu_opc["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_menu_opc["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_opc["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_opc["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_fuentes["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_fuentes["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_aplicar["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_aplicar["highlightbackground"] = self.color_fondo_gral_c 
        comunes.atrb_btn_restablecer["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_restablecer["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_eliminar_relacion["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_eliminar_relacion["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_filas_vertice["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_filas_vertice["bg"] = self.color_fondo_entrada_c
        comunes.atrb_filas_vertice["highlightcolor"] = self.color_fondo_entrada_c        
        comunes.atrb_filas_vertice["selectforeground"] = self.color_fondo_gral_c
        comunes.atrb_filas_vertice["insertbackground"] = self.color_tex_gral_c
        comunes.atrb_filas_vertice["selectbackground"] = self.color_tex_gral_c                
        comunes.atrb_filas_nodo["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_filas_nodo["selectforeground"] = self.color_fondo_gral_c
        comunes.atrb_filas_nodo["bg"] = self.color_fondo_entrada_c
        comunes.atrb_filas_nodo["highlightbackground"] = self.color_fondo_entrada_c
        comunes.atrb_filas_nodo["insertbackground"] = self.color_tex_gral_c
        comunes.atrb_filas_nodo["selectbackground"] = self.color_tex_gral_c        
        comunes.atrb_filas_relacion["foreground" ] = self. color_tex_gral_c
        comunes.atrb_filas_relacion["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_filas_relacion["selectforeground"] = self.color_fondo_gral_c
        comunes.atrb_filas_relacion["bg"] = self.color_fondo_entrada_c
        comunes.atrb_filas_relacion["highlightcolor"] = self.color_fondo_entrada_c
        comunes.atrb_filas_relacion["insertbackground"] = self.color_tex_gral_c
        comunes.atrb_filas_relacion["selectbackground"] = self.color_tex_gral_c        
        comunes.tag_entidad["selectforeground"] = self.color_fondo_gral_c
        comunes.tag_entidad["foreground"] = self.color_tex_gral_c        
        comunes.tag_relacion["selectforeground"] = self.color_fondo_gral_c
        comunes.tag_relacion["foreground"] = self.color_tex_gral_c        
        comunes.atrb_btn_proyecto_ex["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_proyecto_ex["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_proyecto_g["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_proyecto_g["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_proyecto_ap["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_proyecto_ap["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_proyecto_at["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_proyecto_at["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_radial["selectcolor"] = self.color_fondo_gral_c
        comunes.atrb_btn_radial["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_radial["highlightcolor"] = self.color_fondo_gral_c
        comunes.atrb_btn_radial["bg"] = self.color_fondo_gral_c        
        comunes.atrb_btn_check_np["selectcolor"] = self.color_fondo_gral_c
        comunes.atrb_btn_check_np["bg"] = self.color_fondo_gral_c
        comunes.atrb_btn_check_np["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_check_np["highlightbackground"] = self.color_fondo_gral_c        
        comunes.atrb_contenedor_artf["bg"] = self.color_fondo_gral_c
        comunes.atrb_area_txt["foreground" ] = self. color_tex_gral_c
        comunes.atrb_area_txt["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_area_txt["bg"] = self.color_fondo_entrada_c
        comunes.atrb_area_txt["highlightcolor"] = self.color_fondo_entrada_c        
        comunes.atrb_entrada["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_entrada["selectforeground"] = self.color_fondo_gral_c
        comunes.atrb_entrada["bg"] = self.color_fondo_entrada_c
        comunes.atrb_entrada["highlightcolor"] = self.color_fondo_entrada_c        
        comunes.atrb_entrada_e["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_entrada_e["selectforeground"] = self.color_fondo_gral_c
        comunes.atrb_entrada_e["bg"] = self.color_fondo_entrada_c
        comunes.atrb_entrada_e["highlightcolor"] = self.color_fondo_entrada_c
        comunes.atrb_entrada_e["foreground"] = self.color_tex_gral_c
        comunes.atrb_entrada_e["insertbackground"] = self.color_tex_gral_c
        comunes.atrb_entrada_e["selectbackground"] = self.color_tex_gral_c        
        comunes.atrb_entrada_r["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_entrada_r["selectforeground"] = self.color_fondo_gral_c
        comunes.atrb_entrada_r["bg"] = self.color_fondo_entrada_c
        comunes.atrb_entrada_r["highlightcolor"] = self.color_fondo_entrada_c
        comunes.atrb_entrada_r["foreground"] = self.color_tex_gral_c
        comunes.atrb_entrada_r["insertbackground"] = self.color_tex_gral_c
        comunes.atrb_entrada_r["selectbackground"] = self.color_tex_gral_c      
        comunes.atrb_etq_ent["background"] = self.color_fondo_gral_c        
        comunes.atrb_etq_titulo_a["background"] = self.color_fondo_gral_c
        comunes.atrb_etq_titulo_a["foreground"] = self.color_tex_etq_ayuda_c
        comunes.atrb_etq_tecla["background"] = self.color_fondo_gral_c  
        comunes.atrb_etq_ayuda["background"] = self.color_fondo_gral_c
        comunes.atrb_etq_ayuda["foreground"] = self.color_tex_etq_ayuda_c
        comunes.atrb_etq_adv["background"] = self.color_fondo_gral_c        
        comunes.atrb_etq_aviso["background"] = self.color_fondo_gral_c  
        comunes.atrb_etq_aviso["foreground"] = self.color_tex_mensaje_c
        comunes.atrb_etq_ayuda_mapa["background"] = self.color_fondo_gral_c
        comunes.atrb_etq_ayuda_mapa["foreground"] = self.color_tex_etq_ayuda_c                                  
        comunes.atrb_btn_cargar_texto["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_cargar_texto["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_reiniciar["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_reiniciar["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_abrir_notas["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_abrir_notas["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_abrir_carpeta["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_abrir_carpeta["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_tema["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_tema["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_tema["highlightcolor"] = self.color_btn_tema_activo_c
        comunes.atrb_btn_tema["activebackground"] = self.color_btn_tema_activo_c
        comunes.atrb_btn_tema["activeforeground"] = self.color_btn_tema_tex_c
        comunes.atrb_btn_tema["fg"] = self.color_btn_tema_tex_c
        comunes.atrb_btn_tema["bg"] = self.color_btn_tema_c
        comunes.atrb_btn_cancelar["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_cancelar["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_btn_relacionar["disabledforeground"] = self.color_fondo_gral_c
        comunes.atrb_btn_relacionar["highlightbackground"] = self.color_fondo_gral_c
        comunes.atrb_ne["background"] = self.color_fondo_entrada_c
        comunes.atrb_ne["foreground"] = self.color_tex_gral_c
        comunes.atrb_nodos["color"] = self.color_grafo_c
        comunes.atrb_nodos["fillcolor"] = self.color_grafo_c
        comunes.atrb_nodos["fontcolor"] = self.color_tex_grafo_c
        comunes.atrb_grafo["bgcolor"] = self.color_fondo_gral_c
        comunes.atrb_vertices["color"] = self.color_grafo_c
        comunes.atrb_vertices["fontcolor"] = self.color_grafo_c
        comunes.atrb_grafo["bgcolor"] = self.color_fondo_grafo_c        

    def _tema_oscuro(self) -> None:
        """
        Actualiza las entradas de los diccionarios que definen el estilo
        de la aplicación.
        """
        comunes.color_fondo_grafo = self.color_fondo_grafo_o
        comunes.color_grafo = self.color_grafo_o
        comunes.color_tex_grafo = self.color_tex_grafo_o
        comunes.color_tex_gral = self.color_tex_gral_o
        comunes.color_fondo_gral = self.color_fondo_gral_o
        comunes.color_tex_mensaje = self.color_tex_mensaje_o 
        comunes.color_tex_etq_ayuda = self.color_tex_etq_ayuda_o
        comunes.color_fondo_entrada = self.color_fondo_entrada_o
        comunes.marron_pestaña_a = self.marron_pestaña_a_o
        comunes.marron_pestaña_s = self.marron_pestaña_s_o
        comunes.marron_pestaña_o = self.marron_pestaña_o_o
        comunes.marron_pestaña_c = self.marron_pestaña_c_o
        comunes.color_btn_tema = self.color_btn_tema_o 
        comunes.color_btn_tema_tex = self.color_btn_tema_tex_o
        comunes.color_btn_tema_activo = self.color_btn_tema_activo_o
        comunes.atrb_color_fondo["background"] = self.color_fondo_gral_o
        comunes.atrb_pestañas_t["background"] = self.marron_pestaña_o_o
        comunes.atrb_pestañas_t["foreground"] = self.color_tex_gral_o
        comunes.atrb_menu_ed["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_menu_ed["highlightbackground"] = self.color_fondo_gral_o
        comunes.atrb_menu_ed["activebackground"] = self.marron_pestaña_c_o
        comunes.atrb_menu_ed["bg"] = self.marron_pestaña_a_o        
        comunes.atrb_menu_opc["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_menu_opc["highlightbackground"] = self.color_fondo_gral_o        
        comunes.atrb_btn_opc["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_opc["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_fuentes["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_fuentes["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_aplicar["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_aplicar["highlightbackground"] = self.color_fondo_gral_o  
        comunes.atrb_btn_restablecer["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_restablecer["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_eliminar_relacion["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_eliminar_relacion["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_filas_vertice["highlightbackground"] = self.color_fondo_gral_o
        comunes.atrb_filas_vertice["bg"] = self.color_fondo_entrada_o
        comunes.atrb_filas_vertice["selectforeground"] = self.color_fondo_gral_o
        comunes.atrb_filas_vertice["highlightcolor"] = self.color_fondo_entrada_o
        comunes.atrb_filas_vertice["insertbackground"] = self.color_tex_gral_o
        comunes.atrb_filas_vertice["selectbackground"] = self.color_tex_gral_o
        comunes.atrb_filas_nodo["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_filas_nodo["selectforeground"] = self.color_fondo_gral_o
        comunes.atrb_filas_nodo["bg"] = self.color_fondo_entrada_o
        comunes.atrb_filas_nodo["highlightbackground"] = self.color_fondo_entrada_o
        comunes.atrb_filas_nodo["insertbackground"] = self.color_tex_gral_o
        comunes.atrb_filas_nodo["selectbackground"] = self.color_tex_gral_o
        comunes.atrb_filas_relacion["foreground" ] = self. color_tex_gral_o 
        comunes.atrb_filas_relacion["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_filas_relacion["selectforeground"] = self.color_fondo_gral_o
        comunes.atrb_filas_relacion["bg"] = self.color_fondo_entrada_o
        comunes.atrb_filas_relacion["highlightcolor"] = self.color_fondo_entrada_o
        comunes.atrb_filas_relacion["insertbackground"] = self.color_tex_gral_o
        comunes.atrb_filas_relacion["selectbackground"] = self.color_tex_gral_o
        comunes.tag_entidad["selectforeground"] = self.color_fondo_gral_o
        comunes.tag_entidad["foreground"] = self.color_tex_gral_o    
        comunes.tag_relacion["selectforeground"] = self.color_fondo_gral_o
        comunes.tag_relacion["foreground"] = self.color_tex_gral_o
        comunes.atrb_btn_proyecto_ex["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_proyecto_ex["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_proyecto_g["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_proyecto_g["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_proyecto_ap["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_proyecto_ap["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_proyecto_at["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_proyecto_at["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_radial["selectcolor"] = self.color_fondo_gral_o
        comunes.atrb_btn_radial["disabledforeground"] = self.color_fondo_gral_o
        comunes.atrb_btn_radial["highlightcolor"] = self.color_fondo_gral_o
        comunes.atrb_btn_radial["bg"] = self.color_fondo_gral_o  
        comunes.atrb_btn_check_np["selectcolor"] = self.color_fondo_gral_o
        comunes.atrb_btn_check_np["bg"] = self.color_fondo_gral_o
        comunes.atrb_btn_check_np["disabledforeground"] = self.color_fondo_gral_o
        comunes.atrb_btn_check_np["highlightbackground"] = self.color_fondo_gral_o
        comunes.atrb_contenedor_artf["bg"] = self.color_fondo_gral_o 
        comunes.atrb_area_txt["foreground" ] = self. color_tex_gral_o 
        comunes.atrb_area_txt["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_area_txt["bg"] = self.color_fondo_entrada_o
        comunes.atrb_area_txt["highlightcolor"] = self.color_fondo_entrada_o
        comunes.atrb_entrada["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_entrada["selectforeground"] = self.color_fondo_gral_o
        comunes.atrb_entrada["bg"] = self.color_fondo_entrada_o
        comunes.atrb_entrada["highlightcolor"] = self.color_fondo_entrada_o
        comunes.atrb_entrada_e["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_entrada_e["selectforeground"] = self.color_fondo_gral_o
        comunes.atrb_entrada_e["bg"] = self.color_fondo_entrada_o
        comunes.atrb_entrada_e["highlightcolor"] = self.color_fondo_entrada_o
        comunes.atrb_entrada_e["foreground"] = self.color_tex_gral_o
        comunes.atrb_entrada_e["insertbackground"] = self.color_tex_gral_o
        comunes.atrb_entrada_e["selectbackground"] = self.color_tex_gral_o
        comunes.atrb_entrada_r["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_entrada_r["selectforeground"] = self.color_fondo_gral_o
        comunes.atrb_entrada_r["bg"] = self.color_fondo_entrada_o
        comunes.atrb_entrada_r["highlightcolor"] = self.color_fondo_entrada_o
        comunes.atrb_entrada_r["foreground"] = self.color_tex_gral_o
        comunes.atrb_entrada_r["insertbackground"] = self.color_tex_gral_o
        comunes.atrb_entrada_r["selectbackground"] = self.color_tex_gral_o
        comunes.atrb_etq_ent["background"] = self.color_fondo_gral_o 
        comunes.atrb_etq_titulo_a["background"] = self.color_fondo_gral_o
        comunes.atrb_etq_titulo_a["foreground"] = self.color_tex_etq_ayuda_o
        comunes.atrb_etq_tecla["background"] = self.color_fondo_gral_o   
        comunes.atrb_etq_ayuda["background"] = self.color_fondo_gral_o
        comunes.atrb_etq_ayuda["foreground"] = self.color_tex_etq_ayuda_o
        comunes.atrb_etq_adv["background"] = self.color_fondo_gral_o
        comunes.atrb_etq_aviso["background"] = self.color_fondo_gral_o   
        comunes.atrb_etq_aviso["foreground"] = self.color_tex_mensaje_o 
        comunes.atrb_etq_ayuda_mapa["background"] = self.color_fondo_gral_o
        comunes.atrb_etq_ayuda_mapa["foreground"] = self.color_tex_etq_ayuda_o
        comunes.atrb_btn_cargar_texto["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_cargar_texto["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_reiniciar["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_reiniciar["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_abrir_notas["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_abrir_notas["highlightbackground"] = self.color_fondo_gral_o
        comunes.atrb_btn_abrir_carpeta["disabledforeground"] = self.color_fondo_gral_o
        comunes.atrb_btn_abrir_carpeta["highlightbackground"] = self.color_fondo_gral_o
        comunes.atrb_btn_tema["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_tema["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_tema["highlightcolor"] = self.color_btn_tema_activo_o
        comunes.atrb_btn_tema["activebackground"] = self.color_btn_tema_activo_o
        comunes.atrb_btn_tema["activeforeground"] = self.color_btn_tema_tex_o
        comunes.atrb_btn_tema["fg"] = self.color_btn_tema_tex_o
        comunes.atrb_btn_tema["bg"] = self.color_btn_tema_o
        comunes.atrb_btn_cancelar["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_cancelar["highlightbackground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_relacionar["disabledforeground"] = self.color_fondo_gral_o 
        comunes.atrb_btn_relacionar["highlightbackground"] = self.color_fondo_gral_o
        comunes.atrb_ne["background"] = self.color_fondo_entrada_o
        comunes.atrb_ne["foreground"] = self.color_tex_gral_o
        comunes.atrb_nodos["color"] = self.color_grafo_o 
        comunes.atrb_nodos["fillcolor"] = self.color_grafo_o 
        comunes.atrb_nodos["fontcolor"] = self.color_tex_grafo_o 
        comunes.atrb_grafo["bgcolor"] = self.color_fondo_gral_o 
        comunes.atrb_vertices["color"] = self.color_grafo_o 
        comunes.atrb_vertices["fontcolor"] = self.color_grafo_o
        comunes.atrb_grafo["bgcolor"] = self.color_fondo_grafo_o
        
