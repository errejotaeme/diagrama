import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
from aplicacion.interfaz import comunes
from aplicacion.interfaz.componentes.elementos import emergente


class AreaDeGrafico:
    """
    Clase encargada de hacer visible el diagrama generado con cada nueva
    proposición.

    :param ancestro: El artefacto que contiene al marco principal del área.
    :type ancestro: PanedWindow
    :param gestor: Gestiona la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor
    """

    def __init__(self, ancestro: tk.PanedWindow, gestor):
        """
        Constructor de la clase AreaDeGrafico.     
        """
        self._gestor = gestor
        self._factor_zoom: float = 1.0  # Permite redimensionar el diagrama
        self._contenedor_cuadro: tk.Frame = tk.Frame(  # Marco principal
            ancestro,  width=200, height=200, **comunes.atrb_contenedor_artf
        )        
        self._cuadro: tk.Canvas = tk.Canvas(
            self._contenedor_cuadro,
            bg=comunes.atrb_grafo["bgcolor"],
            height = 400
        )        
        self._bh: tk.Scrollbar = tk.Scrollbar(
            self._contenedor_cuadro, orient=tk.HORIZONTAL
        )
        self._bh.pack(side=tk.BOTTOM, fill=tk.X)
        self._bh.config(command=self._cuadro.xview)
        self._bv: tk.Scrollbar = tk.Scrollbar(
            self._contenedor_cuadro, orient=tk.VERTICAL
        )
        self._bv.pack(side = tk.RIGHT, fill=tk.Y)
        self._bv.config(command=self._cuadro.yview)
        self._cuadro.config(
            xscrollcommand=self._bh.set, yscrollcommand=self._bv.set
        )
        self._cuadro.pack(fill="both", expand=True)
        self._establecer_atajos()
 
    def artefacto(self) -> tk.Frame:
        """
        Retorna el contenedor principal de la sección.

        :return: El marco principal de la sección.
        :rtype: tk.Frame
        """
        return self._contenedor_cuadro

    def cargar_imagen(self, ruta_img: str) -> None:
        """
        La llama el Gestor para actualizar la imagen del canvas al agregar
        una proposición, al borrar la última o al editar algún atributo del
        diagrama.      

        :param ruta_img: La ubicación del archivo png con el grafo generado por el Diagramador.
        :type ruta_img: str
        """
        self._imagen: Image.Image = Image.open(ruta_img)      
        self._imagen_tk: ImageTk.PhotoImage = ImageTk.PhotoImage(self._imagen)
        ancho_img, alto_img = self._imagen.size
        self._cuadro.config(scrollregion=(0, 0, ancho_img, alto_img))
        self._img_id: int = self._cuadro.create_image(
            0, 0, anchor=tk.NW, image=self._imagen_tk
        )
        self._redimensionar_img(1.0)
        self._cuadro.pack(fill="both", expand=True)

    def actualizar_cuadro(self) -> None:
        """
        Cambia el color de fondo del canvas para que coincida con
        el color de fondo del grafo cuando se editan sus atributos.
        """
        self._cuadro.configure(bg=comunes.atrb_grafo["bgcolor"])
        self._cuadro.pack_forget()
        self._cuadro.pack(fill="both", expand=True)


    def ocultar_cuadro(self) -> None:
        """
        Actuliza el color del fondo del canvas y lo vuelve invisible.
        Además, actualiza el factor de zoom para olvidar el que se aplicó
        previamente.
        """
        self._cuadro.configure(bg=comunes.atrb_grafo["bgcolor"])
        self._cuadro.pack_forget()
        self._factor_zoom = 1.0

    def _redimensionar_img(self, factor: float) -> None:
        """
        Método asociado a atajos de teclado que permite hacer zoom sobre
        la imagen del diagrama.
        
        :param factor: El factor de zoom.
        :type factor: float 
        """
        if self._imagen is None:
            return
        if self._factor_zoom == 1.0 and factor == 1.0:
            return        
        else:
            self._factor_zoom *= factor
            nueva_imagen: Image.Image = self._imagen.resize(
                (int(self._imagen.width * self._factor_zoom),
                 int(self._imagen.height * self._factor_zoom)),
                Image.Resampling.LANCZOS
            )
            self._imagen_tk = ImageTk.PhotoImage(nueva_imagen)
            ancho_img, alto_img = nueva_imagen.size
            self._cuadro.config(scrollregion=(0, 0, ancho_img, alto_img))            
            self._cuadro.itemconfig(self._img_id, image=self._imagen_tk)
            self._contenedor_cuadro.focus()     
        
    def _desplazar(self, señal: str) -> None:
        """
        Método asociado a atajos de teclado para explorar el canvas usando
        las teclas de dirección.
        
        :param señal: El sentido del desplazamiento.
        :type señal: str
        """
        pass
        if señal == "i":
            self._cuadro.xview_scroll(-1, "units")
        elif señal == "d":
            self._cuadro.xview_scroll(1, "units")
        elif señal == "s":
            self._cuadro.yview_scroll(-1, "units")
        elif señal == "b":
            self._cuadro.yview_scroll(1, "units")

    def _enfocar(self) -> None:
        """
        Método asociado a un evento "Enter". Cuando el mouse se posa sobre
        la imagen, pone el foco en el contenedor del canvas para permitir
        explorarla con las teclas de dirección.
        """
        self._contenedor_cuadro.focus()

    def _establecer_atajos(self) -> None:
        """
        Vincula los artefactos con los atajos de teclado.
        """
        self._contenedor_cuadro.bind("<Enter>", lambda e : self._enfocar())
        
        self._contenedor_cuadro.bind_all(
            "<Control-KP_Subtract>", lambda e: self._redimensionar_img(0.9)
        )
        self._contenedor_cuadro.bind_all(
            "<Control-minus>", lambda e: self._redimensionar_img(0.9)
        )
        self._contenedor_cuadro.bind_all(
            "<Control-KP_Add>", lambda e: self._redimensionar_img(1.1)
        )
        self._contenedor_cuadro.bind_all(
            "<Control-plus>", lambda e: self._redimensionar_img(1.1)
        )
        self._contenedor_cuadro.bind("<Left>",lambda e: self._desplazar("i"))
        self._contenedor_cuadro.bind("<Right>",lambda e: self._desplazar("d"))
        self._contenedor_cuadro.bind("<Up>",lambda e: self._desplazar("s"))
        self._contenedor_cuadro.bind("<Down>",lambda e: self._desplazar("b"))
        self._contenedor_cuadro.bind("<Control-a>",lambda e: self._volver(1))
        self._contenedor_cuadro.bind("<Control-s>",lambda e: self._volver(2))
        self._contenedor_cuadro.bind("<Control-d>",lambda e: self._volver(3))
        self._contenedor_cuadro.bind("<Control-f>",lambda e: self._volver(4))
        self._contenedor_cuadro.bind("<Control-u>",lambda e: self._volver(5))
        self._contenedor_cuadro.bind("<Control-w>",lambda e: self._volver(6))
        self._contenedor_cuadro.bind("<Control-W>",lambda e: self._volver(6))        
        self._contenedor_cuadro.bind("<Control-A>",lambda e: self._volver(1))
        self._contenedor_cuadro.bind("<Control-S>",lambda e: self._volver(2))
        self._contenedor_cuadro.bind("<Control-D>",lambda e: self._volver(3))
        self._contenedor_cuadro.bind("<Control-F>",lambda e: self._volver(4))
        self._contenedor_cuadro.bind("<Control-U>",lambda e: self._volver(5))
        self._contenedor_cuadro.bind("<Control-n>",lambda e: self._volver(7))
        self._contenedor_cuadro.bind("<Control-N>",lambda e: self._volver(7))
        self._contenedor_cuadro.bind("<Control-g>",lambda e: self._volver(8))
        self._contenedor_cuadro.bind("<Control-G>",lambda e: self._volver(8))
       
    def _volver(self, señal: int) -> None:
        """
        Método asociado a atajos de teclado. Reenvía al Gestor la señal que
        recibe como argumento, para que la transmita a la sección que
        corresponde.

        :param señal: Un entero que provoca un comportamiento específico en una sección o artefacto.
        :type señal: int
        """
        self._gestor.enfocar_sec_texto(señal)
