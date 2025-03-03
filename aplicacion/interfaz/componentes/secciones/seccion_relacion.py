import tkinter as tk
from tkinter import ttk
from aplicacion.interfaz import comunes
from aplicacion.interfaz.componentes.pantallas import pantalla_relacion


class EdicionRelacion:
    """
    Clase encargada de construir los artefactos que permiten editar
    las relaciones del diagrama.

    :param ancestro: El artefacto que contiene al marco principal del área. 
    :type ancestro: tk.Frame
    :param gestor: La instancia de la clase encargada de gestionar la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor 
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk
    """ 

    def __init__(self, ancestro: tk. Frame, gestor, raiz: tk.Tk):
        """
        Constructor de la clase EdicionRelacion.
        """
        self._gestor = gestor
        self._raiz: tk.Tk = raiz
        self._ancestro: tk.Frame = ancestro
        self._relaciones_existentes: dict[int, list[tuple[str, str]]] = {}  # Contiene las relaciones ingresadas
        self._relaciones_ubicadas:dict[int, tk.Frame] = {}  # Contiene a los marcos generados dinámicamente
        self._contenedor_sec_relacion = tk.Frame(  # Se ubica con una señal del ancestro
            ancestro, **comunes.atrb_contenedor_artf
        ) 
        self._construir_encabezado(self._contenedor_sec_relacion)
        self._construir_lista_relaciones(self._contenedor_sec_relacion)
        
    def activar_seccion(self) -> None:
        """
        Obtiene las relaciones existentes y los ubica en el contenedor.
        """
        self._eliminar_relaciones_existentes()
        self._relaciones_existentes = self._obtener_relaciones()
        if not self._contenedor_lista_relaciones is None:
            self._contenedor_lista_relaciones.destroy()            
        self._construir_lista_relaciones(self._contenedor_sec_relacion)
        self._cargar_relaciones()
        self._cargar_de_nuevo()
        
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

    def olvidar_ubicacion(self) -> None:
        """
        Oculta el módulo cuando es seleccionado otro modo de edición.
        """
        self._contenedor_sec_relacion.grid_forget()

    def ubicar(self) -> None:
        """
        Hace visible el módulo cuando se lo selecciona como modo de edición.
        """
        self._contenedor_sec_relacion.grid(
            row=1, column=0, sticky="ew",padx=(140,0), pady=(10,10)
        )

    def _cargar_relaciones(self) -> None:
        """
        Ubica las relaciones existentes en el contenedor de la lista de relacioens.
        """    
        fila:int = 0
        for id_prop, valores in self._relaciones_existentes.items():
            marco:tk.Frame = tk.Frame(
                self._marco_desplazable_r, **comunes.atrb_contenedor_artf
            )
            t_aux:str = "ID : " + str(id_prop)
            etq_id: tk.Label = tk.Label(marco, text=t_aux, **comunes.atrb_etq_ayuda)
            etq_id.grid(row=fila, column=0, sticky="w", pady=(0,5))
            rel: tk.Text = tk.Text(marco, **comunes.atrb_filas_relacion)
            self._insertar_texto(rel, valores)
            rel.config(state=tk.DISABLED)
            rel.grid(row=fila, column=1, padx=(5,5), pady=(0,5))
            boton: tk.Button = tk.Button(
                marco,
                text="Editar",
                command=lambda val=valores:self._pantalla_edicion(val),  # type: ignore
                **comunes.atrb_btn_abrir_notas
            )
            boton.grid(row=fila, column=2, padx=(5,0), pady=(0,5))
            marco.grid(row=fila, column=0, sticky="ew", padx=(5,5), pady=(0,5))
            self._relaciones_ubicadas[id_prop] = marco
            fila += 1

    def _cargar_de_nuevo(self) -> None:
        """
        Vuelve visible la barra de desplazamiento vertical cuando la lista
        de relaciones es demasiado grande.
        """
        self._marco_desplazable_r.update_idletasks()
        alto: int = self._marco_desplazable_r.winfo_height()
        if alto > 295:
            self._barra_r.grid(row=0, column=1, sticky="ns")
        else:
            self._barra_r.grid_forget()
            
    def _comprobar_id(self, id_rel:str) -> bool:
        """
        Verifica que el id ingresado sea válido.

        :return: El resultado de la verificación.
        :rtype: bool
        """
        res: bool = False
        self._obtener_relaciones()
        if self._relaciones_existentes:
            try:
                if int(id_rel) in self._relaciones_existentes.keys():
                    res = True
            except:
                pass
        return res

    def _construir_encabezado(self, ancestro: tk.Frame) -> None:
        """
        Construye el encabezado de la sección.

        :param ancestro: El artefacto que contiene al encabezado.
        :type ancestro: tk.Frame
        """
        self._contenedor_encabezado: tk.Frame = tk.Frame( 
            ancestro, **comunes.atrb_contenedor_artf
        )
        self._contenedor_encabezado.grid(
            row=0, column=0, sticky="w", padx=(0,28), pady=(0,0)
        )
        # Id a borrar
        self._etq_id_borrar: tk.Label = tk.Label( 
            self._contenedor_encabezado, text="ID: ", **comunes.atrb_etq_ayuda
        )
        self._etq_id_borrar.grid(
            row=0, column=0, sticky="w", padx=(5,0), pady=(0,0)
        )
        self._id_borrar: tk.StringVar = tk.StringVar()
        self._ingr_id_borrar: tk.Entry = tk.Entry( 
            self._contenedor_encabezado,
            textvariable=self._id_borrar,
            width=3,
            **comunes.atrb_entrada
        )
        self._ingr_id_borrar.grid(
            row=0, column=1, sticky="w", padx=(0,10), pady=(0,0)
        )
        self._btn_borrar_relacion: tk.Button = tk.Button(
            self._contenedor_encabezado,
            text="Eliminar",
            command=self._eliminar_relacion,
            **comunes.atrb_btn_restablecer
        )
        self._btn_borrar_relacion.grid(
            row=0, column=2, sticky="w", padx=(0,10), pady=(0,0)
        )
        self._etq_aviso: tk.Label = tk.Label(  # Notificaciones
            self._contenedor_encabezado, text="", **comunes.atrb_etq_aviso
        )
        self._etq_aviso.grid(
            row=0, column=3, padx=(0,0), pady=(0,0), sticky="w"
        )

    def _construir_lista_relaciones(self, ancestro: tk.Frame) -> None:
        """
        Construye el contenedor donde se cargan dinámicamente
        las relaciones existentes.

        :param ancestro: El artefacto que contiene a la lista de relaciones.
        :type ancestro: tk.Frame
        """
        self._contenedor_lista_relaciones: tk.Frame = tk.Frame(
           ancestro,**comunes.atrb_contenedor_artf
        )
        self._contenedor_lista_relaciones.grid(
            row=1, column=0, sticky="n", padx=(0, 20), pady=(10,10)
        )
        self._estilo_lista_r: ttk.Style = ttk.Style()
        self._estilo_lista_r.configure("TFrame")
        self._estilo_lista_r.configure(
            "ListaR.TFrame", background=comunes.color_fondo_gral
        )
        self._lista_relaciones: ttk.Frame = ttk.Frame(
            self._contenedor_lista_relaciones,
            style="ListaR.TFrame"
        )
        self._lista_relaciones.grid(
            row=0, column=0, sticky="n", pady=(0,0)
        )
        self._cv_relaciones: tk.Canvas = tk.Canvas(
            self._lista_relaciones,
            width=350,
            height=300,
            highlightthickness=0,
            **comunes.atrb_contenedor_artf
        )
        self._barra_r: ttk.Scrollbar = ttk.Scrollbar(
            self._lista_relaciones, orient="vertical", command=self._cv_relaciones.yview
        )        
        self._marco_desplazable_r: ttk.Frame = ttk.Frame(
            self._cv_relaciones, style="ListaR.TFrame"
        )
        self._marco_desplazable_r.bind(
            "<Configure>",
            lambda e: self._cv_relaciones.configure(
                scrollregion=self._cv_relaciones.bbox("all")
            )
        )
        self._cv_relaciones.create_window(
            (0, 0), window=self._marco_desplazable_r, anchor="nw"
        )
        self._cv_relaciones.grid(row=0, column=0, sticky="ew", padx=(5,5))
        self._cv_relaciones.configure(yscrollcommand=self._barra_r.set)


    def _insertar_texto(
        self, artefacto: tk.Text, valores: list[tuple[str, str]]
    ) -> None:
        """
        Aplica formato a cada elemento de la relación antes de insertarlo. 

        :param artefacto: El artefacto de texto.
        :type artefacto: tk.Text
        :param valores: Los elementos de la relación.
        :type valores: list[tuple[str, str]]]
        """
        # Configuro los estilos
        artefacto.tag_config("entidad", **comunes.tag_entidad)
        artefacto.tag_config("relacion", **comunes.tag_relacion)
        # Inserto y formateo cada texto
        tex_ent1 = valores[0][1]
        artefacto.insert(tk.END, tex_ent1)
        artefacto.tag_add("entidad", "1.0", "end")
        # Posición antes de insertar (último carácter)
        pos_inicio = artefacto.index("end-1c")  
        tex_rel = " " + valores[1][1]
        artefacto.insert(tk.END, tex_rel)
         # Posición después de insertar (último carácter)
        pos_fin = artefacto.index("end-1c") 
        artefacto.tag_add("relacion", pos_inicio, pos_fin)
        pos_inicio = artefacto.index("end-1c")  
        tex_ent2 = " " + valores[2][1]
        artefacto.insert(tk.END, tex_ent2)
        pos_fin = artefacto.index("end-1c") 
        artefacto.tag_add("entidad", pos_inicio, pos_fin)

    def _eliminar_relacion(self) -> None:
        """
        Elimina la relación cuyo id fue ingresado.
        """
        id_borrar: str = self._id_borrar.get()
        id_ok: bool = self._comprobar_id(id_borrar)
        if id_ok:
            self._gestor.eliminar_relacion(id_borrar)
            self._ingr_id_borrar.delete(0, tk.END)
        else:
            self._ingr_id_borrar.focus_set()
            self._ingr_id_borrar.select_range(0, tk.END)

    def _eliminar_relaciones_existentes(self) -> None:
        """
        Vacía las entradas con las relaciones generadas dinámicamente.
        """
        for marco in self._relaciones_ubicadas.values():
            marco.destroy()
        self._relaciones_ubicadas.clear()
    
    def _obtener_relaciones(self) -> dict[int, list[tuple[str, str]]]:
        """
        Devuelve las relaciones registrados hasta el momento.
        """
        return self._gestor.relaciones_existentes()
  
    def _pantalla_edicion(self, valores: list[tuple[str, str]]) -> None:
        """
        Crea la pantalla que permite editar cada proposición.

        :param valores:
        :type valores: list[tuple[str, str]]
        """       
        pantalla = pantalla_relacion.PantallaRelacion(
            self._gestor, self._raiz, self._ancestro, valores
        )       
