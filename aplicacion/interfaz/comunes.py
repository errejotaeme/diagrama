import tkinter as tk

"""
Módulo que contiene las estructuras de datos usadas para dar estilo
a la aplicación y el diagrama, y almacenar las opciones disponibles 
en los menús y los datos requeridos por las áreas y secciones.
"""
      

# DATOS
atajos: dict = { 
    "<Ctrl+o>, <Ctrl+O> :":"Permite elegir un documento (pdf o txt) del cual extraer el texto.",
    "<Ctrl+a>, <Ctrl+A> :":"Vacía la entrada e ingresa el texto seleccionado en el artefacto asociado a la primer entidad.",
    "<Ctrl+s>, <Ctrl+S> :":"Vacía la entrada e ingresa el texto seleccionado en el artefacto asociado al vínculo entre entidades.",
    "<Ctrl+d>, <Ctrl+D> :":"Vacía la entrada e ingresa el texto seleccionado en el artefacto asociado a la segunda entidad.",
    "<Ctrl+w>, <Ctrl+W> :":"Vacía la entrada e ingresa la selección en el artefacto asociado al peso de la relación, que debe ser un entero.",
    "<Ctrl+f>, <Ctrl+F> :":"Grafica la proposición ingresada.",
    "<Ctrl+u>, <Ctrl+U> :":"Borra la última proposición ingresada.",
    "<Ctrl+n>, <Ctrl+N> :":"Permite abrir la pantalla donde se guardan las notas propias.",
    "<Ctrl+g>, <Ctrl+G> :":"Estando en la pantalla de Notas, guarda los cambios y cierra la ventana.",
    "<Ctrl+q>, <Ctrl+Q> :":"Estando en la pantalla de Notas, cierra la ventana sin guardar los cambios.",
    "<Ctrl+g>, <Ctrl+G> :":'Estando en la pestaña de Tareas, guarda el proyecto (previamente activado con la opción "Recordar directorio".',
    "<Ctrl+KP_Subtract>, <Ctrl+minus> :":"Con el foco en la sección del gráfico, aleja la vista del diagrama.",
    "<Ctrl+KP_Add>, <Ctrl+equal> :":"Con el foco en la sección del gráfico, acerca la vista del diagrama.",
    "<Left>, <Right>, <Up>, <Down> :":"Con el foco en la sección del gráfico, permite el desplazamiento sobre la vista del diagrama.",
}

necesarios: list = [
    "nodos.csv",
    "notas_propias.txt",
    "propiedades_n.csv",
    "propiedades_v.csv",
    "proposiciones.csv",
    "vertices.csv",
    "estado_grafo.txt",
    "estado_n_v.txt"
]

formas_nodo: list = [
    "box", "circle", "component", "cylinder", "diamond", "doublecircle",
    "egg", "ellipse", "folder", "house", "invhouse", "invtrapezium",
    "invtriangle", "none", "note", "oval", "parallelogram", "plain",
    "point", "rect", "square", "tab", "trapezium", "triangle", "underline"
]

opc_edicion: list = [
    "Editar grafo",
    "Editar nodo",
    "Editar vértice",
    "Editar relación"
]

tipos_flechas: list = [
    "box", "crow", "diamond", "dot", "inv", "none", "normal", "tee", "vee",
    "odot", "invdot", "invodot", "obox", "odiamond", "ediamond", "open",
    "halfopen", "empty", "invempty"
]

direcciones: list = ["back", "both", "forward", "none"]

crecimiento: list = ["arriba", "abajo", "derecha", "izquierda"]

opciones_parrafo: list = ["centrado", "a la izquierda", "a la derecha"]




# ESTILOS
# Colores de ambos temas
B_OPCION_FONDO = "#82ac9a"    #
B_OPCION_ACTIVO = "#95c6b2"
B_OPCION_TEX = "#050605"
B_FUENTES_FONDO = "#f97d5e"    #
B_FUENTES_ACTIVO = "#ff8b6e"
B_FUENTES_TEX = "#070403"
M_OPCION_FONDO = "#007d75"    #
M_OPCION_ACTIVO = "#00958b"
M_OPCION_TEX = "#000807"
RELACIONAR_FONDO = "#f97d5e"    #
RELACIONAR_ACTIVO = "#ff8b6e"
RELACIONAR_TEX = "#070403"
RELACIONAR_BORDE = "#ff8b6e"
GRIS_O_ETQ_PROP = "#454545"
ATAJOS_FONDO = "#00a477"        #
ATAJOS_ACTIVO = "#00be88"
ATAJOS_TEX = "#000705"
ATAJOS_BORDE = "#00be88"
ADVERTENCIA_FONDO = "#00a477"   #
ADVERTENCIA_ACTIVO = "#00be88"
ADVERTENCIA_TEX = "#000705"
NEGRO_TEX = "#000000"
EXPORTAR_FONDO = "#007d75"      #
EXPORTAR_ACTIVO = "#00958b"
EXPORTAR_TEX = "#000807"
EXPORTAR_BORDE = "#00958b"
CARGAR_FONDO = "#5ce0a3"        #
CARGAR_ACTIVO = "#68fdb8"
CARGAR_TEX = "#030705"
CARGAR_BORDE = "#68fdb8"
CARGAR_RESALTADO = "#68fdb8"
GUARDAR_FONDO = "#82ac9a"       #
GUARDAR_ACTIVO = "#95c6b2"
GUARDAR_TEX = "#050605"
GUARDAR_BORDE = "#95c6b2"
NOTAS_FONDO = "#82ac9a"         #
NOTAS_ACTIVO = "#95c6b2"      
NOTAS_TEX = "#050605"
NOTAS_BORDE = "#95c6b2"
ABRIR_FONDO = "#f97d5e"         #
ABRIR_ACTIVO = "#ff8b6e"
ABRIR_BORDE = "#ff8b6e"
ABRIR_TEX = "#070403"
TEX_ENTRADA = "#00958b"

# Colores de tema oscuro (por defecto)
color_fondo_grafo = "#111111"
color_grafo = "#f1e5e0"
color_tex_grafo = "#000000"
color_tex_gral = "#ffffff"
color_fondo_gral = "#111111"
color_tex_mensaje = "#ffffff"
color_tex_etq_ayuda = "#fcfcfc"
color_fondo_entrada = "#272727"
marron_pestaña_a = "#545454"
marron_pestaña_s = "#111111"
marron_pestaña_o = "#363636"
marron_pestaña_c = "#a09797"
color_btn_tema = "#e7b9a0"
color_btn_tema_tex = "#000000"
color_btn_tema_activo = "#f9c7ad"



# ATRIBUTOS DE ARTEFACTOS
atrb_color_fondo: dict = {"background":color_fondo_gral}

atrb_pestañas_t: dict = {
    "background":marron_pestaña_o,
    "foreground":color_tex_gral,
    "font":"Arial 8 bold",
    "padding":[14,6,14,4],
}

atrb_menu_ed: dict = {
    "activebackground":marron_pestaña_c,
    "activeforeground":NEGRO_TEX,
    "anchor":"center",
    "bd":4,
    "bg":marron_pestaña_a,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral,
    "fg":NEGRO_TEX, 
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral,
    "highlightthickness":2,
    "justify":"center",
    "padx":10,
    "pady":5,
    "width":10,
    "wraplength":100,
    "relief":tk.RIDGE,
}

atrb_menu_opc: dict = {
    "activebackground":M_OPCION_ACTIVO,
    "activeforeground":M_OPCION_TEX,
    "anchor":"center",
    "bd":4,
    "bg":M_OPCION_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral, 
    "fg":M_OPCION_TEX,
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral, 
    "highlightthickness":2,
    "justify":"center",
    "padx":10,
    "pady":5,
    "width":10,
    "wraplength":100,
    "relief":tk.RIDGE,  
}



atrb_btn_opc: dict = {
    "activebackground":B_OPCION_ACTIVO,
    "activeforeground":B_OPCION_TEX,
    "anchor":"center",
    "bd":4,
    "bg":B_OPCION_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral, 
    "fg":B_OPCION_TEX,
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":B_OPCION_ACTIVO,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":10,
    "pady":5,
    "width":5,
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_btn_fuentes: dict = {
    "activebackground":B_FUENTES_ACTIVO,
    "activeforeground":B_FUENTES_TEX,
    "anchor":"center",
    "bd":4,
    "bg":B_FUENTES_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral, 
    "fg":B_FUENTES_TEX,
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":B_FUENTES_ACTIVO,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":10,
    "pady":5,
    "width":10,
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_btn_aplicar: dict = {
    "activebackground":CARGAR_ACTIVO,
    "activeforeground":CARGAR_TEX,
    "anchor":"center",
    "bd":4,
    "bg":CARGAR_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral,
    "fg":CARGAR_TEX,
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":CARGAR_BORDE,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":10,
    "pady":5,
    "width":10,
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_btn_restablecer: dict = {
    "activebackground":ADVERTENCIA_ACTIVO,
    "activeforeground":ADVERTENCIA_TEX,
    "anchor":"center",
    "bd":4,
    "bg":ADVERTENCIA_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral, 
    "fg":ADVERTENCIA_TEX,
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":ADVERTENCIA_ACTIVO,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":10,
    "pady":5,
    "width":15,
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_btn_eliminar_relacion: dict = {
    "activebackground":ADVERTENCIA_ACTIVO,
    "activeforeground":ADVERTENCIA_TEX,
    "anchor":"center",
    "bd":4,
    "bg":ADVERTENCIA_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral,
    "fg":ADVERTENCIA_TEX,
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral, 
    "highlightcolor":ADVERTENCIA_ACTIVO,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":10,
    "pady":5,
    "width":15,
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_filas_vertice: dict = {
    "height":"1",
    "width":"7",
    "wrap":"none",
    "bd":"1",
    "bg":color_fondo_entrada,
    "font":"Arial 10 normal", 
    "highlightcolor":color_fondo_entrada,
    "highlightbackground":color_fondo_gral,
    "insertbackground":color_tex_gral, 
    "selectbackground":color_tex_gral,
    "selectforeground":color_fondo_gral,
    "relief":tk.SUNKEN
}

atrb_filas_nodo: dict = {
    "height":"1",
    "width":"17",
    "wrap":"none",
    "bd":"1",
    "bg":color_fondo_entrada,
    "font":"Arial 10 normal", 
    "highlightcolor":color_fondo_entrada,
    "highlightbackground":color_fondo_gral,
    "insertbackground":color_tex_gral,
    "selectbackground":color_tex_gral,
    "selectforeground":color_fondo_gral,
    "relief":tk.SUNKEN
}

atrb_filas_relacion: dict = {
    "height":"1",
    "width":"30",
    "wrap":"none",
    "bd":"1",
    "bg":color_fondo_entrada,
    "foreground" : color_tex_gral,
    "font":"Arial 10 normal", 
    "highlightcolor":color_fondo_entrada,
    "highlightbackground":color_fondo_gral,
    "insertbackground":color_tex_gral,
    "selectbackground":color_tex_gral,
    "selectforeground":color_fondo_gral,
    "relief":tk.SUNKEN
}


tag_entidad = {
    "foreground":color_tex_gral,
    "font":"Arial 9 bold",
    "selectforeground":color_fondo_gral,
}

tag_relacion = {
    "foreground":color_tex_gral,
    "font":"Arial 9 italic",
    "selectforeground":color_fondo_gral,
}

atrb_btn_proyecto_ex: dict = {
    "activebackground":EXPORTAR_ACTIVO,
    "activeforeground":EXPORTAR_TEX,
    "anchor":"center",
    "bd":4,
    "bg":EXPORTAR_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral,
    "fg":EXPORTAR_TEX,
    "font":"Arial 8 bold",
    "height":2,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":EXPORTAR_BORDE,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":9,
    "pady":5,
    "width":14,
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_btn_proyecto_g: dict = {
    "activebackground":GUARDAR_ACTIVO,
    "activeforeground":GUARDAR_TEX,
    "anchor":"center",
    "bd":4,
    "bg":GUARDAR_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral,
    "fg":GUARDAR_TEX,
    "font":"Arial 8 bold",
    "height":2,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":GUARDAR_BORDE,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":9,
    "pady":5,
    "width":15,
    "wraplength":100,
    "relief":tk.RAISED
}


atrb_btn_proyecto_ap: dict = {
    "activebackground":ABRIR_ACTIVO,
    "activeforeground":ABRIR_TEX,
    "anchor":"center",
    "bd":4,
    "bg":ABRIR_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral,
    "fg":ABRIR_TEX,
    "font":"Arial 8 bold",
    "height":2,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":ABRIR_ACTIVO,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":9,
    "pady":5,
    "width":13,
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_btn_proyecto_at: dict = {
    "activebackground":ATAJOS_ACTIVO,
    "activeforeground":ATAJOS_TEX,
    "anchor":"center",
    "bd":4,
    "bg":ATAJOS_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral,
    "fg":ATAJOS_TEX,
    "font":"Arial 8 bold",
    "height":2,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":ATAJOS_BORDE,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":9,
    "pady":5,
    "width":15,
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_btn_radial: dict = {
    "bg":color_fondo_gral,
    "fg":EXPORTAR_FONDO,
    "activebackground":EXPORTAR_ACTIVO,
    "activeforeground":EXPORTAR_TEX,
    "disabledforeground":color_fondo_gral,    
    "font":"Arial 8 bold",
    "highlightbackground":color_fondo_gral,
    "highlightcolor":EXPORTAR_BORDE,
    "relief":"flat",
    "selectcolor":color_fondo_gral,
    "highlightthickness":0,
}

atrb_btn_check_np: dict = { 
    "bg":color_fondo_gral,
    "fg":GUARDAR_FONDO,
    "activebackground":GUARDAR_FONDO,
    "activeforeground":GUARDAR_TEX,
    "disabledforeground":color_fondo_gral, 
    "font":"Arial 8 bold",
    "highlightbackground":color_fondo_gral,  
    "highlightcolor":GUARDAR_BORDE,
    "relief":"flat",
    "selectcolor":color_fondo_gral,
    "highlightthickness":0,
}

atrb_contenedor_artf: dict = { 
    "bg":color_fondo_gral,
    "relief":tk.SUNKEN,
}

atrb_area_txt: dict = {
    "bg":color_fondo_entrada,
    "foreground" : color_tex_gral, 
    "font":"Arial 10", 
    "highlightcolor":color_fondo_entrada,
    "highlightbackground":color_fondo_gral,
    "insertbackground":CARGAR_RESALTADO,
    "selectbackground":CARGAR_RESALTADO, 
    "selectforeground":NEGRO_TEX,
}

atrb_entrada: dict = {
    "bg":color_fondo_entrada,
    "bd":2,
    "foreground":TEX_ENTRADA, 
    "font":"Arial 10 normal", 
    "highlightcolor":color_fondo_entrada,
    "highlightbackground":color_fondo_gral,
    "insertbackground":TEX_ENTRADA, 
    "selectbackground":TEX_ENTRADA,
    "selectforeground":color_fondo_gral,
    "relief":tk.SUNKEN
}

atrb_entrada_e: dict = { 
    "bg":color_fondo_entrada,
    "bd":2,
    "foreground":color_tex_gral,
    "font":"Arial 9 bold", 
    "highlightcolor":color_fondo_entrada,
    "highlightbackground":color_fondo_gral,
    "insertbackground":color_tex_gral,
    "selectbackground":color_tex_gral,
    "selectforeground":color_fondo_gral,
    "relief":tk.SUNKEN
}

atrb_entrada_r: dict = {
    "bg":color_fondo_entrada,
    "bd":2,
    "foreground":color_tex_gral,
    "font":"Arial 9 italic", 
    "highlightcolor":color_fondo_entrada,
    "highlightbackground":color_fondo_gral,
    "insertbackground":color_tex_gral,
    "selectbackground":color_tex_gral,
    "selectforeground":color_fondo_gral,
    "relief":tk.SUNKEN
}

atrb_etq_ent: dict = {
    "background":color_fondo_gral,  
    "foreground":GRIS_O_ETQ_PROP,
    "font":"Arial 8 bold",
}

atrb_etq_titulo_a: dict = {
    "background":color_fondo_gral,  
    "foreground":color_tex_etq_ayuda,
    "font":"Arial 14 bold",
}

atrb_etq_tecla: dict = {
    "background":color_fondo_gral,  
    "foreground":ATAJOS_FONDO,
    "font":"Arial 8 bold",
}

atrb_etq_ayuda: dict = {
    "background":color_fondo_gral,  
    "foreground":color_tex_etq_ayuda,
    "font":"Arial 8 bold",
}

atrb_etq_adv: dict = {
    "background":color_fondo_gral,  
    "foreground":ADVERTENCIA_FONDO,
    "font":"Arial 8 bold",
}

atrb_etq_aviso: dict = {
    "background":color_fondo_gral,  
    "foreground":color_tex_mensaje,
    "font":"Arial 8 bold italic",
}

atrb_etq_ayuda_mapa: dict = {
    "background":color_fondo_gral,  
    "foreground":color_tex_etq_ayuda,
    "font":"Arial 8 normal",
    "height":3,
}

atrb_btn_cargar_texto: dict = {
    "activebackground":CARGAR_ACTIVO, 
    "activeforeground":CARGAR_TEX, 
    "anchor":"center",
    "bd":4,
    "bg":CARGAR_FONDO, 
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral, 
    "fg":CARGAR_TEX, 
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":CARGAR_BORDE, 
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":9,
    "pady":5,
    "width":10,
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_btn_reiniciar: dict = {
    "activebackground":ADVERTENCIA_ACTIVO,
    "activeforeground":ADVERTENCIA_TEX,
    "anchor":"center",
    "bd":4,
    "bg":ADVERTENCIA_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral,
    "fg":ADVERTENCIA_TEX,
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":ADVERTENCIA_ACTIVO,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":10,
    "pady":5,
    "width":7, 
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_btn_abrir_notas: dict = {
    "activebackground":NOTAS_ACTIVO,
    "activeforeground":NOTAS_TEX,
    "anchor":"center",
    "bd":4,
    "bg":NOTAS_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral,
    "fg":NOTAS_TEX,
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":NOTAS_BORDE,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":10,
    "pady":5,
    "width":5,
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_btn_abrir_carpeta: dict = {
    "activebackground":GUARDAR_ACTIVO,
    "activeforeground":GUARDAR_TEX,
    "anchor":"center",
    "bd":4,
    "bg":GUARDAR_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral,
    "fg":GUARDAR_TEX,
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":GUARDAR_BORDE,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":10,
    "pady":5,
    "width":5,
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_btn_tema: dict = {
    "activebackground":color_btn_tema_activo,
    "activeforeground":color_btn_tema_tex,
    "anchor":"center",
    "bd":4,
    "bg":color_btn_tema,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral,
    "fg":color_btn_tema_tex,
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":color_btn_tema_activo,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":10,
    "pady":5,
    "width":10, 
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_btn_cancelar: dict = {
    "activebackground":ADVERTENCIA_ACTIVO,
    "activeforeground":ADVERTENCIA_TEX,
    "anchor":"center",
    "bd":4,
    "bg":ADVERTENCIA_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral, 
    "fg":ADVERTENCIA_TEX,
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":ADVERTENCIA_ACTIVO,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":10,
    "pady":5,
    "width":10,
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_btn_relacionar: dict = {
    "activebackground":RELACIONAR_ACTIVO,
    "activeforeground":RELACIONAR_TEX,
    "anchor":"center",
    "bd":4,
    "bg":RELACIONAR_FONDO,
    "cursor":"hand2",
    "disabledforeground":color_fondo_gral, 
    "fg":RELACIONAR_TEX,
    "font":"Arial 8 bold",
    "height":1,
    "highlightbackground":color_fondo_gral,
    "highlightcolor":RELACIONAR_BORDE,
    "highlightthickness":2,
    "justify":"center",
    "overrelief":"raised",
    "padx":10,
    "pady":5,
    "width":8,
    "wraplength":100,
    "relief":tk.RAISED
}

atrb_ne: dict = {
    "background":color_fondo_entrada, 
    "relief":"solid",
    "justify":"left",
    "borderwidth":"0",
    "foreground":color_tex_gral,
    "font":"Arial 9 normal",
}




# GRAFO
atrb_nodos: dict = {
    "id":"-1",
    "color":color_grafo, # color del borde de los nodos
    "fillcolor":color_grafo, # color de relleno de los nodos
    "fixedsize":"false", # todos los nodos del mismo tamaño
    "fontcolor":color_tex_grafo, # color del texto de los nodos
    "fontsize":"9", # tamaño de fuente de los nodos
    "fontname":"Sans",
    "nojustify":"true",
    "shape": "circle", # forma de los nodos
    "style":"filled", # nodo relleno
    "label":"",
}

atrb_grafo: dict = {"bgcolor":color_fondo_grafo, "rankdir": "TB",}

atrb_vertices: dict = {
    "id":"-1",
    "arrowhead":"normal",
    "arrowtail":"normal",
    "arrowsize":"0.75",
    "color":color_grafo, 
    "decorate":"false", # unir la etiqueta al vértice con una línea
    "dir":"forward", 
    "fontsize":"9", 
    "fontcolor":color_grafo, 
    "fontname":"Sans", 
    "label":"",
    "nojustify":"true",
}
