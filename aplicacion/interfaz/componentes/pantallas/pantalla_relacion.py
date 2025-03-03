import tkinter as tk
from tkinter import ttk
from aplicacion.interfaz import comunes


class PantallaRelacion:
    """
    Clase encargada de construir una ventana independiente en la que
    editar la relación seleccionada.

    :param gestor: La instancia de la clase encargada de gestionar la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor 
    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk
    :param ancestro: El marco donde se ubica el contenedor principal y/o los artefactos instanciados por la clase.
    :type ancestro: Frame
    :param valores: El id y valor de cada elemento implicado en la relación entidad->vinculo->entidad.
    :type valores: list[tuple[str, str]]
    """
    
    def __init__(
        self,
        gestor,
        raiz: tk.Tk,
        ancestro: tk.Frame,
        valores: list[tuple[str, str]]
    ):
        """
        Constructor de la clase PantallaRelación. Recibe la instancia del
        Gestor, de la ventana principal, del artefacto en el que se ubica y
        una lista de tuplas con los ids y valores de los nodos y el vértice
        que están implicados en la relación.
        """
        self._ancestro: tk.Frame = ancestro
        self._gestor = gestor
        self._raiz: tk.Tk = raiz
        self._valores: list[tuple[str, str]] = valores

        self._pantalla_relacion: tk.Toplevel = tk.Toplevel(
            self._ancestro, **comunes.atrb_contenedor_artf
        )        
        self._pantalla_relacion.title("Editar relación")        
        # Obtengo los datos para centrarla en la pantalla
        self._raiz.update_idletasks()
        ancho:int = 500 
        alto:int = 300
        ancho_pantalla:int = self._raiz.winfo_screenwidth()
        alto_pantalla:int = self._raiz.winfo_screenheight()
        x:int = (ancho_pantalla - ancho) // 2
        y:int = (alto_pantalla - alto) // 2
        self._pantalla_relacion.geometry(f"{ancho}x{alto}+{x}+{y}")
        self._contenedor: tk.Frame = tk.Frame(  # Marco principal de la pantalla
            self._pantalla_relacion, **comunes.atrb_contenedor_artf
        )
        self._contenedor.pack()
        self._etq_aviso: tk.Label = tk.Label( 
            self._contenedor, text = "", **comunes.atrb_etq_aviso
        )
        self._etq_aviso.grid(
            row=0, column=0, padx=(0,0), pady=(10,0), sticky="ew"
        )
        self._construir_entradas(self._contenedor, valores)
        self._construir_botonera(self._contenedor)
        self._establecer_atajos()

    def mostrar_aviso(self, aviso:str) -> None:
        """
        Actualiza la etiqueta de avisos con el texto recibido.
        
        :param aviso: El texto a mostrar.
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
        
    def _establecer_atajos(self) -> None:
        """
        Asocia el presionar "Enter" en los artefactos con una llamada al
        método correspondiente.
        """
        self._boton_cancelar.bind("<Return>", self._cancelar_edicion)
        self._boton_confirmar.bind("<Return>", self._confirmar_edicion)
        self._ingr_entidad1.bind("<Return>", self._confirmar_edicion)
        self._ingr_relacion.bind("<Return>", self._confirmar_edicion)
        if self._valores[0][0] != self._valores[2][0]:
            self._ingr_entidad2.bind("<Return>", self._confirmar_edicion) 

    def _construir_botonera(self, ancestro: tk.Frame) -> None:
        """
        Construye el marco y los artefactos que permiten confirmar o cancelar
        la edición.

        :param ancestro: El marco donde se ubica el contenedor principal y/o los artefactos instanciados por la clase.
        :type ancestro: Frame
        """
        self._contenedor_botones: tk.Frame = tk.Frame(
            ancestro, **comunes.atrb_contenedor_artf
        )
        self._contenedor_botones.grid(
            row=2, column=0, padx=(70,70), sticky="ew"
        )
        self._boton_confirmar: tk.Button = tk.Button(
            self._contenedor_botones,
            text="Confirmar",
            command=self._confirmar_edicion,
            **comunes.atrb_btn_aplicar
        )
        self._boton_confirmar.grid(
            row=0, column=0, sticky="ew", padx=(20,20), pady=(10,0)
        )
        self._boton_cancelar: tk.Button = tk.Button(
            self._contenedor_botones,
            text="Cancelar",
            command=self._cancelar_edicion,
            **comunes.atrb_btn_cancelar
        )
        self._boton_cancelar.grid(
            row=0, column=1, sticky="ew", padx=(20,20), pady=(10,0)
        )
        self._boton_cancelar.focus_set()


    def _cancelar_edicion(self, *args) -> None:
        """
        Destruye el Toplevel que permite editar la relación seleccionada.
        Args captura los eventos vinculados a los artefactos de ingreso
        que llaman a éste método.
        """
        self._pantalla_relacion.destroy()        


    def _confirmar_edicion(self, *args) -> None:
        """
        Verifica que las modificaciones realizadas sean procesables y
        envía al gestor los cambios a registrar. Args captura los eventos
        vinculados a los artefactos de ingreso que llaman a éste método.
        """
        cambios: dict[str, tuple[()] | tuple[str, str]] = {}
        edicion_ok: bool = self._comprobar_ingresos()
        if edicion_ok:
            self.ocultar_aviso()
            cambios["ent1"] = (self._valores[0][0], self._ent1.get())
            cambios["rel"] = (self._valores[1][0], self._rel.get())
            if self._valores[0][0] != self._valores[2][0]:
                cambios["ent2"] = (self._valores[2][0], self._ent2.get())
            else:
                cambios["ent2"] = ()
            self._gestor.editar_relacion(cambios)
            self._pantalla_relacion.destroy()

    def _comprobar_ingresos(self) -> bool:
        """
        Verifica que las modificaciones ingresadas sean válidas.

        :return: El resultado de la verificación.
        :rtype: bool
        """
        self.mostrar_aviso("Comprobando...")
        valores_nodos: list[str] = self._gestor.lista_valores("nodo")
        valores_vertices: list[str] = self._gestor.lista_valores("vertice")
        e1_distinta_original:bool = (
            self._ent1.get().strip() != self._valores[0][1]
        )
        if self._ent1.get() in valores_nodos and e1_distinta_original:
            self.mostrar_aviso("La entidad ingresada ya existe")
            self._ingr_entidad1.focus_set()
            self._ingr_entidad1.select_range(0, tk.END)
            return False
        r_distinta_original: bool = (
            self._rel.get().strip() != self._valores[1][1]
        )
        if self._rel.get() in valores_vertices and r_distinta_original:
            self.mostrar_aviso("El vínculo ingresado ya existe")
            self._ingr_relacion.focus_set()
            self._ingr_relacion.select_range(0, tk.END)
            return False
        if self._valores[0][0] != self._valores[2][0]:
            e2_distinta_original: bool = (
                self._ent2.get().strip() != self._valores[2][1]
            )
            if self._ent2.get() in valores_nodos and e2_distinta_original:
                self.mostrar_aviso("La entidad ingresada ya existe")
                self._ingr_entidad2.focus_set()
                self._ingr_entidad2.select_range(0, tk.END)
                return False
            una_distinta: bool = (
                e1_distinta_original or r_distinta_original or e2_distinta_original
            )
            if not una_distinta:
                self.mostrar_aviso("La proposición ingresada ya existe")
                return False
            else:
                return True
        else:
            una_distinta = e1_distinta_original or r_distinta_original
            if not una_distinta:
                self.mostrar_aviso("La proposición ingresada ya existe")
                return False
            else:
                return True

    def _construir_entradas(
        self, ancestro: tk.Frame, valores: list[tuple[str, str]]
    ) -> None:
        """
        Crea los artefactos que permiten modificar los valores de
        los elementos de la relación.
        
        :param ancestro: El marco donde se ubica el contenedor principal y/o los artefactos instanciados por la clase.
        :type ancestro: Frame
        :param valores: El id y valor de cada elemento implicado en la relación entidad->vinculo->entidad.
        :type valores: list[tuple[str, str]]
        """
        self._contenedor_entradas = tk.Frame(
            ancestro, **comunes.atrb_contenedor_artf
        )
        self._contenedor_entradas.grid(row=1, column=0, sticky="ew")
        # Variables de almacenamiento
        self._ent1: tk.StringVar = tk.StringVar()
        self._rel: tk.StringVar = tk.StringVar()
        self._ent2: tk.StringVar = tk.StringVar()
        # Entidad1
        self._etq_entidad1: tk.Label = tk.Label(
            self._contenedor_entradas,
            text = "Entidad:",
            **comunes.atrb_etq_ayuda
        )
        self._etq_entidad1.grid(row=0, column=0, sticky="w", pady=(20,0))       
        self._ingr_entidad1: tk.Entry = tk.Entry(
            self._contenedor_entradas,
            textvariable = self._ent1,
            width=60,
            **comunes.atrb_entrada_e
        )
        self._ingr_entidad1.grid(row=1, column=0, sticky="ew", pady=(0,20))
        self._ingr_entidad1.insert(0, valores[0][1])
        # Relación entre entidades
        self._etq_relacion: tk.Label = tk.Label(
            self._contenedor_entradas,
            text = "Vínculo:",
            **comunes.atrb_etq_ayuda
        )
        self._etq_relacion.grid(row=2, column=0, sticky="w")
        self._ingr_relacion: tk.Entry = tk.Entry(
            self._contenedor_entradas,
            textvariable = self._rel,
            width=60,
            **comunes.atrb_entrada_r
        )
        self._ingr_relacion.grid(row=3, column=0, sticky="ew", pady=(0,20))
        self._ingr_relacion.insert(0, valores[1][1])
        # A Entidad2 la creo solo si la relación no es un bucle
        if valores[0][0] != valores[2][0]:            
            self._etq_entidad2: tk.Label = tk.Label(
                self._contenedor_entradas,
                text = "Entidad:",
                **comunes.atrb_etq_ayuda)
            self._etq_entidad2.grid(row=4,column=0,sticky="w")
            self._ingr_entidad2: tk.Entry = tk.Entry(
                self._contenedor_entradas,
                textvariable = self._ent2,
                width=60,
                **comunes.atrb_entrada_e)
            self._ingr_entidad2.grid(row=5,column=0,sticky="ew",pady=(0,20))
            self._ingr_entidad2.insert(0, valores[2][1])
            
