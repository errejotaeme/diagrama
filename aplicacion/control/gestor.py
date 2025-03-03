import copy
import csv
import os
import queue
import sys
import platform
import threading
import tkinter as tk
from pathlib import Path
from typing import Callable, Any
from aplicacion.interfaz import comunes
from aplicacion.documentos import diagrama
from aplicacion.control.ambitos import gestion_edicion, gestion_texto, gestion_proyecto
from aplicacion.interfaz.componentes.areas import edicion, grafico, proyecto, texto


class Gestor:
    """
    Clase encargada de coordinar la comunicación entre los módulos,
    trabajar con las tablas y distribuir las tareas de las distintas
    divisiones entre los ámbitos de gestión. Su constructor genera 
    las rutas a los recursos, los valores por defectos de los atributos 
    del diagrama y las estructuras de datos que permiten ordenar la 
    ejecución de tareas en segundo plano.

    :param raiz: Ventana principal que controla el bucle de la aplicación.
    :type raiz: Tk
    :param tema: El tema actual de la aplicación.
    :type tema: str
    """

    def __init__(self, raiz: tk.Tk, tema: str):
        self._raiz: tk.Tk = raiz
        self._tema: str = tema
        # Áreas
        self._grafico: grafico.AreaDeGrafico = None  # type: ignore
        self._texto: texto.AreaDeTexto = None  # type: ignore
        self._edicion: edicion.AreaEdicion = None  # type: ignore
        self._proyecto: proyecto.AreaProyecto = None  # type: ignore
        # Rutas a recursos
        self._ruta_csv_proposiciones: Path = (Path(__file__).parent.parent / "documentos" / "recursos" / "proposiciones.csv").resolve()
        self._ruta_csv_propiedades_n: Path = (Path(__file__).parent.parent / "documentos" / "recursos" / "propiedades_n.csv").resolve()
        self._ruta_csv_propiedades_v: Path = (Path(__file__).parent.parent / "documentos" / "recursos" / "propiedades_v.csv").resolve()
        self._ruta_csv_vertices: Path = (Path(__file__).parent.parent / "documentos" / "recursos" / "vertices.csv").resolve()
        self._ruta_notas: Path = (Path(__file__).parent.parent / "documentos" / "recursos" / "notas_propias.txt").resolve()
        self._ruta_csv_nodos: Path = (Path(__file__).parent.parent / "documentos" / "recursos" / "nodos.csv").resolve()
        self._ruta_resultados: Path = (Path(__file__).parent.parent / "resultados").resolve()
        # Atributos generales del grafo
        self.cota: int = 25  # Long. máx. aprox. de líneas
        self.justificado: str = "n"  # Centrado
        # Ambitos de gestión
        self._gestion_texto: gestion_texto.GestionTexto = gestion_texto.GestionTexto(
            self,
            self._ruta_csv_proposiciones,
            self._ruta_csv_nodos,
            self._ruta_csv_vertices,
            self._ruta_csv_propiedades_n,
            self._ruta_csv_propiedades_v    
        )
        self._gestion_edicion: gestion_edicion.GestionEdicion = gestion_edicion.GestionEdicion(
            self,
            self._ruta_csv_proposiciones,
            self._ruta_csv_nodos,
            self._ruta_csv_vertices,
            self._ruta_csv_propiedades_n,
            self._ruta_csv_propiedades_v    
        )
        self._gestion_proyecto: gestion_proyecto.GestionProyecto  = gestion_proyecto.GestionProyecto(
            self,
            self._ruta_csv_proposiciones,
            self._ruta_csv_nodos,
            self._ruta_csv_vertices,
            self._ruta_csv_propiedades_n,
            self._ruta_csv_propiedades_v    
        )
        # Valores por defecto del diagrama
        val_def_nodos: dict[str, str] = copy.deepcopy(comunes.atrb_nodos)
        val_def_vertices:  dict[str, str] = copy.deepcopy(comunes.atrb_vertices)
        val_def_grafo: dict[str, str] = copy.deepcopy(comunes.atrb_grafo)
        self._valores_por_defecto: list[dict[str, str]] = [
            val_def_nodos, val_def_vertices, val_def_grafo
        ]
        self.ruta_png: str = ""
        # Colas para almacenar las tareas pendientes
        self._cola_texto: queue.Queue = queue.Queue()
        self._cola_grafico: queue.Queue = queue.Queue()
        self._cola_edicion: queue.Queue = queue.Queue()
        self._cola_proyecto: queue.Queue = queue.Queue()
        # Variables de control para saber si hay una tarea en ejecución
        self._tarea_texto: list[bool] = [False]
        self._tarea_grafico: list[bool] = [False]
        self._tarea_edicion: list[bool] = [False]
        self._tarea_proyecto: list[bool] = [False]
        # Comunicacion entre hilo principal y tareas en segundo plano
        self.actualizar: threading.Event = threading.Event()
        self.cola_avisos: queue.Queue = queue.Queue()
        self._id_tarea_pendiente: str | None = None
        self._id_ocultar_avisos: str | None = None
        self._observador()
        self._ocultar_avisos()




    def acotar_cadena(self, cadena: str) -> str:
        """
        Separa la cadena en líneas de longitud aproximada (por arriba)
        a la cota.
        
        :param cadena: La cadena a separar.
        :type cadena: str
        :return: La cadena en líneas acotadas.
        :rtype: str 
        """
        cadena = cadena.strip()
        if len(cadena) < self.cota:
            return cadena
        else:
            res: str = cadena[:self.cota]
            indice: int = self.cota    
            while indice < len(cadena) and cadena[indice] != " ":
                indice += 1    
            if indice == len(cadena):
                return cadena            
            else:
                res = res+cadena[self.cota:indice]+f"\\{self.justificado}"
                return res+self.acotar_cadena(cadena[indice:].strip())
            
    def actualizar_elemento(
        self, tipo: str, id_elem: str, cambios: dict[str, str]
    ) -> bool: 
        """
        Delega la operación al ámbito que gestiona las tareas de edición.
        
        :param tipo: Un indicador del tipo de elemento.
        :type tipo: str
        :param id_elem: El id del elemento.
        :type id_elem: str
        :param cambios: Las modificaciones en los atributos del elemento.
        :type cambios: dict[str, str]
        :return: La confirmación de que se inició la tarea.
        :rtype: bool
        """
        if tipo == "nodo":
            aux_aviso: str = f"Aplicando los cambios al nodo con ID: {id_elem}..."
            self._edicion.mostrar_aviso_nodo(aux_aviso)
        else:
            aux_aviso = f"Aplicando los cambios al vértice con ID: {id_elem}..."
            self._edicion.mostrar_aviso_vertice(aux_aviso)
        self._encolar_tarea(
            self._gestion_edicion.modificar_elemento,
            self._cola_grafico,
            self._tarea_grafico,
            tipo,
            id_elem,
            cambios
        )
        return True
    
    def actualizar_grafo(self, cambios: list[dict[str, str]]) -> bool:  
        """
        Delega la operación al ámbito que gestiona las tareas de edición.

        :param cambios: Las modifcaciones en los atributos del diagrama.
        :type cambios: list[dict[str, str]]
        :return: La confirmación de que se inició la tarea, cuando existen elementos que actualizar.
        :rtype: bool
        """
        if self._existen_proposiciones():
            self._edicion.mostrar_aviso_grafo("Aplicando los cambios al grafo...")
            self._encolar_tarea(
                self._gestion_edicion.modificar_grafo,
                self._cola_grafico,
                self._tarea_grafico,
                cambios
            )
            return True
        else:
            return False

    def borrar_de_tabla(self, ruta_tabla: Path, id_elemento: str) -> None:
        """
        Elimina el elemento indicado de la tabla recibida.
            
        :param ruta_tabla: La ruta a la tabla.
        :type ruta_tabla: Path
        :param id_elemento: El id del elemento
        :type id_elemento: str         
        """
        # Obtengo el índice de la fila del registro a borrar
        with open(ruta_tabla, "r", newline="", encoding="utf-8") as tabla:
            registros = tabla.readlines()
            indice_fila: int = 1        
            for registro in registros[1:]:
                l_aux: list[str] = registro.split(chr(167))
                if l_aux[0] == id_elemento:
                    break
                indice_fila += 1
        del registros[indice_fila]
        # Escribo todas menos la fila eliminada
        with open(ruta_tabla, "w", newline="", encoding="utf-8") as archivo:
            archivo.writelines(registros)

    def borrar_ultimo_ingreso(self) -> None:
        """
        Agrega la tarea a la cola de pendientes.
        """
        self._texto.mostrar_aviso("Borrando la última proposición...")
        self._encolar_tarea(
            self._borrar_ultima_proposicion,
            self._cola_grafico,
            self._tarea_grafico
        )

    def cancelar_pendientes(self) -> None:
        """
        Cancela las tareas pendientes, frenando la ejecución del observador
        y del método encargado de ocultar los avisos visibles, a fin de evitar
        errores al reiniciar la aplicación.        
        """
        if not self._id_tarea_pendiente is None:
            self._raiz.after_cancel(self._id_tarea_pendiente)
        if not self._id_ocultar_avisos is None:
            self._raiz.after_cancel(self._id_ocultar_avisos)   
        
    
    def cargar_proyecto(self, directorio: str, origen: str) -> None:
        """
        Delega la operación al ámbito que gestiona las tareas del proyecto.

        :param directorio: La ruta a la carpeta con los archivos del proyecto.
        :type directorio: str
        :param origen: La indicación de si es un respaldo temporal o un proyecto guardado.
        :type origen: str
        """
        return self._gestion_proyecto.cargar_proyecto_guardado(
            directorio, origen
        ) 

    def cargar_respaldo(self) -> None:
        """
        Delega en el ámbito que gestiona las tareas del proyecto el volver el
        programa al estado previo a intentar abrir un proyecto, cuando éste
        intento falla.
        """
        self._proyecto.mostrar_aviso("Algo salió mal: cargando los datos anteriores...")
        self._encolar_tarea(
            self._gestion_proyecto.cargar_respaldo_temporal,
            self._cola_proyecto,
            self._tarea_proyecto
        )

    def datos_proyecto_activo(self) -> tuple[str, str] | tuple[()]:
        """
        Retorna la ubicacion y el nombre del proyecto que se encuentra activado
        (abierto y que permite guardar los cambios con atajo de teclado).

        :return: Los datos del proyecto.
        :rtype: tuple[str, str]
        """
        return self._proyecto.obtener_proyecto_activo()

    def editar_relacion(self, cambios: dict[str, tuple[str, str]]) -> None:
        """
        Delega la operación al ámbito que gestiona las tareas de edición.

        :param cambios: Las modficaciones a la proposición.
        :type cambios: dict[str, tuple[str, str]]
        """        
        self._edicion.mostrar_aviso_relacion("Aplicando las modificaciones...")
        self._encolar_tarea(
            self._gestion_edicion.modificar_registros,
            self._cola_edicion,
            self._tarea_edicion,
            cambios
        )

    def eliminar_justificado(self, cadena: str) -> str:
        """
        Remueve de la cadena que recibe los todo los caractéres escapados que
        se usan para alinear el texto.

        :param cadena: La cadena a limpiar.
        :type cadena: str
        :return: La cadena limpia.
        :rtype:
        """
        res = cadena.replace("\\n", " ")
        res = res.replace("\\l", " ")
        res = res.replace("\\r", " ")
        return res

    def eliminar_relacion(self, id_rel: str) -> None:
        """
        Delega la operación al ámbito que gestiona las tareas de edición.

        :param id_rel: El índice de la fila a eliminar de la tabla de proposiciones.
        :type id_rel: str
        """
        self._edicion.mostrar_aviso_relacion("Actualizando relaciones...")
        self._encolar_tarea(
            self._gestion_edicion.borrar_relacion,
            self._cola_edicion,
            self._tarea_edicion,
            id_rel
        )

    def eliminar_respaldo(self) -> None: 
        """
        Cuando se abre correctamente un proyecto guardado o luego de reiniciar
        por cambio de tema, borra la carpeta de respaldo con los archivos que
        permiten restaurar el estado de la aplicación. Delega la operación al
        ámbito que gestiona las tareas del proyecto
        """
        self._encolar_tarea(
            self._gestion_proyecto.eliminar_respaldo_temporal,
            self._cola_proyecto,
            self._tarea_proyecto
        )

    def eliminar_simbolo(self, cadena: str) -> str:
        """
        Para prevenir errores al ingresar proposiciones, elimina de la cadena
        el símbolo utilizado como delimitador en las tablas y los saltos de línea.

        :param cadena: La cadena a limpiar.
        :type cadena: str
        :return: La cadena limpia.
        :rtype: str        
        """
        cadena = cadena.replace("\n", " ")
        return cadena.replace(chr(167), "")
        
    def enfocar_sec_texto(self, señal:int) -> None:
        """
        Envía al área de texto la señal con el atajo de teclado ingresado,
        cuando el foco está puesto en el área de gráfico. 
        """
        self._texto.atajo(señal)

    def enlazar(
        self,
        texto: texto.AreaDeTexto,
        edicion: edicion.AreaEdicion,
        proyecto: proyecto.AreaProyecto,
        grafico: grafico.AreaDeGrafico,
        respaldo_pendiente: bool,
        diagrama_no_vacio: bool,
        proyecto_activo: tuple[str, str]
    )->None:
        """
        Conecta el Gestor con las instancias de las áreas de la aplicación.

        :param texto: La instancia de la clase que permite cargar un texto.
        :type texto: AreaDeTexto
        :param edicion: La instancia de la clase que permite editar el diagrama.
        :type edicion: AreaEdicion
        :param proyecto: La instancia de la clase que gestiona las opciones del proyecto.
        :type proyecto: AreaProyecto
        :param grafico: La instancia de la clase que muestra el diagrama.
        :type grafico: AreaDeGrafico
        :param respaldo_pendiente: Indica si se debe cargar el respaldo temporal guardado antes del reinicio por cambio de tema.
        :type respaldo_pendiente: bool
        :param diagrama_no_vacio: Indica si se debe actualizar el artefacto del área de gráfico para que coincida con el color de fondo del grafo.
        :type diagrama_no_vacio: bool
        :param proyecto_activo: Datos que permiten volver a activar el proyecto que estaba abierto, al reiniciar por cambio en tema.
        :type proyecto_activo: tuple[str, str]
        """
        self._texto = texto
        self._edicion = edicion
        self._proyecto = proyecto
        self._grafico = grafico
        if not self._gestion_texto is None:
            self._gestion_texto.enlazar_area(grafico, edicion, texto)
        if not self._gestion_edicion is None:
            self._gestion_edicion.enlazar_area(edicion)
        if not self._gestion_proyecto is None:
            self._gestion_proyecto.enlazar_area(
                proyecto, edicion, grafico, self._gestion_texto
            )
        if respaldo_pendiente:
            self._inicio_por_cambio_en_tema(diagrama_no_vacio)
        if proyecto_activo:
            self._proyecto.restaurar_proyecto_activo(proyecto_activo)
            
    def enrutar(self, mensaje: list[str]) -> None:
        """
        Permite la comunicación entre los OptionMenus del area de edición,
        y los artefactos de las secciones y subsecciones con los que trabajan.
        Delega la operación al ámbito que gestiona las tareas de edición.
        """
        self._gestion_edicion.enviar(mensaje)
    
    def exportar_diagrama(self, formato: str, directorio: str) -> None:
        """
        Delega la operación al ámbito que gestiona las tareas del proyecto.

        :param formato: La extensión del archivo con el diagrama.
        :type formato: str
        :param directorio: La ruta de salida.
        :type directorio: str
        """
        self._proyecto.mostrar_aviso("Exportando el diagrama...")
        self._encolar_tarea(
            self._gestion_proyecto.exportar_grafico,
            self._cola_proyecto,
            self._tarea_proyecto,
            formato,
            directorio
        )

    def guardar_notas(self, texto: str) -> None:
        """
        Escribe el contenido de las notas tomadas eun un txt, permitiendo
        recuperarlas cuando se abra el proyecto guardado.

        :param texto: El contenido de las notas
        :type texto: str
        """
        with open(self._ruta_notas, "w", newline="",encoding="utf-8") as notas:
            notas.write(texto)    
        
    def guardar_proyecto(self, directorio: str, nombre: str) -> None:
        """
        Delega la operación al ámbito que gestiona las tareas del proyecto.

        :param directorio: La carpeta donde se guardará.
        :type directorio: str
        :param nombre: El nombre de la carpeta que contiene los archivos.
        :type nombre: str
        """
        self._proyecto.mostrar_aviso("Guardando el proyecto...")
        self._encolar_tarea(
            self._gestion_proyecto.guardar_proyecto_actual,
            self._cola_proyecto,
            self._tarea_proyecto,
            directorio,
            nombre
        )

    def guardar_proyecto_desde_atajo(self) -> None:
        """
        Ejecuta en segundo plano la operación de guardar los cambios del proyecto.
        """        
        self._encolar_tarea(
            self._guardar_en_segundo_plano,
            self._cola_proyecto,
            self._tarea_proyecto,
        )

    def lista_ids(self, elem: str) -> list[str]:
        """
        Retorna una lista con los id de los elementos registrados, ayudando
        a prevenir que, al deshacer cambios en Edición, se produzca un error
        al intentar restablecer los atributos de un elemento que no existe.
        Delega la operación al ámbito que gestiona las tareas de edición.

        :param elem: El tipo de los elementos (nodo o vértice).
        :type elem: str
        :return: La lista de ids de los elementos registrados.
        :rtye: list[str]
        """
        return self._gestion_edicion.ids_registrados(elem)

    def lista_valores(self, tipo: str) -> list[str]:
        """
        Retorna una lista con los valores de todos los elementos registrados,
        del tipo (nodo o vértice) que recibe como argumento.
            
        :param tipo: El tipo de los elementos.
        :type tipo: str
        :return: La lista de valores de los elementos registrados.
        :rtype: list[str]
        """
        res: list[str] = []
        if tipo == "nodo":
            tabla = self._ruta_csv_nodos
        else:
            tabla = self._ruta_csv_vertices            
        with open(tabla, "r", newline="", encoding="utf-8") as archivo:
            registros = csv.DictReader(archivo, delimiter="§")
            for registro in registros:
                res.append(registro[tipo])
        return res

    def nodos_existentes(self) -> dict[str, str | None]:
        """
        Retorna el id y valor de los nodos registrados en la tabla.
        Delega la operación al ámbito que gestiona las tareas de edición.

        :return: Los nodos registrados.
        :rtype: dict[str, str | None]
        """
        return self._gestion_edicion.nodos_registrados()

    def obtener_atributos(self, tipo: str, id_elem: str) -> tuple[str, dict[str, str]]:
        """
        Retorna los atributos del elemento solicitado. Delega la operación
        al ámbito que gestiona las tareas de edición.

        :param tipo: El tipo de elemento (nodo o vértice).
        :type tipo: str
        :param id_elem: El id del elemento.
        :type id_elem: str
        :return: Los atributos del elemento.
        :rtype: tuple[str, dict[str, str]]        
        """
        return self._gestion_edicion.atributos_de_elemento(tipo, id_elem)

    def obtener_notas(self) -> str:
        """
        Retorna el contenido de las notas de un proyecto guardado.

        :return: El contenido de las notas.
        :rtype: str
        """
        with open(self._ruta_notas, "r", newline="", encoding="utf-8") as notas:
            contenido = notas.read()
        return contenido
            
    def obtener_texto(self, ruta: str) -> str:   
        """
        Extrae el texto del archivo cuya recibe como argumento. Delega la
        operación al ámbito que gestiona las tareas de texto.

        :param ruta:
        :type ruta:
        :return: El contenido del texto.
        :rtype: str
        """
        self._encolar_tarea(
            self._gestion_texto.extraer,
            self._cola_texto,
            self._tarea_texto,
            ruta
        )
        if ruta:
            return "Cargando texto..."
        else:
            return ""

    def reiniciar(self) -> None:
        """
        Reinicia la aplicación.
        """
        self.cancelar_pendientes()  
        if platform.system() == "Windows":
            python_exe = sys.executable  
            os.execv(python_exe, [python_exe] + sys.argv)  
        else:
            os.execv(sys.executable, ["python"] + sys.argv)

    def relacionar_entidades(self, proposicion: list[str]) -> bool:  
        """
        Agrega la proposición al diagrama. Delega la operación al ámbito
        que gestiona las tareas de texto.

        :param proposicion: La proposición a registrar.
        :type proposicion: list[str]
        :return: Confirmación del inicio de la operación.
        :rtype: bool
        """
        self._texto.mostrar_aviso("Actualizando el diagrama...")
        self._encolar_tarea(
            self._gestion_texto.relacionar,
            self._cola_grafico,
            self._tarea_grafico,
            proposicion
        )
        return True          

    def relaciones_existentes(self) -> dict[int, list[tuple[str, str]]]:
        """
        Devuelve las proposiciones registradas. Delega la operación al ámbito
        que gestiona las tareas de edición.

        :return: Las proposiciones registradas.
        :rtype: dict[int, list[tuple[str, str]]]
        """
        return self._gestion_edicion.relaciones_registradas()

    def respaldo_temporal(self) -> None:
        """
        Delega la operación al ámbito que gestiona las tareas del proyecto.
        """
        self._gestion_proyecto.crear_respaldo_temporal()

    def restablecer_todo(self) -> None:
        """
        Vacía el contenido de las tablas y las notas, y  elimina el gráfico
        generado.
        """
        with open(self._ruta_notas, "w", newline="", encoding="utf-8") as notas:
            pass
        with open(
            self._ruta_csv_proposiciones, "w", newline="", encoding="utf-8"
        ) as proposiciones:
            escritor = csv.writer(proposiciones, delimiter="§")
            escritor.writerow(["ent1", "rel", "ent2", "peso"])    
        with open(self._ruta_csv_nodos, "w", newline="", encoding="utf-8") as nodos:
            escritor = csv.writer(nodos, delimiter="§")
            escritor.writerow(["id", "nodo"])
        with open(
            self._ruta_csv_vertices, "w", newline="", encoding="utf-8"
        ) as vertices:
            escritor = csv.writer(vertices, delimiter="§")
            escritor.writerow(["id", "vertice"])
        with open(
            self._ruta_csv_propiedades_n, "w", newline="", encoding="utf-8"
        ) as propiedades_n:
            escritor = csv.writer(propiedades_n, delimiter="§")
            encabezado = list(comunes.atrb_nodos.keys())
            escritor.writerow(encabezado)
        with open(
            self._ruta_csv_propiedades_v, "w", newline="", encoding="utf-8"
        ) as propiedades_v:
            escritor = csv.writer(propiedades_v, delimiter="§")
            encabezado = list(comunes.atrb_vertices.keys())
            escritor.writerow(encabezado)
        for archivo in os.listdir(self._ruta_resultados):
            ruta_archivo = os.path.join(self._ruta_resultados, archivo)
            if os.path.isfile(ruta_archivo):
                os.remove(ruta_archivo)
        self._gestion_proyecto.eliminar_estados_temporales()

    def vertices_existentes(self) -> dict[str, list[list[str | None]]]:
        """
        Retorna las proposiciones agrupadas por el vértice que las vincula.
        Delega la operación al ámbito que gestiona las tareas de edición.

        :return: Los vértices registrados y las proposiciones de las que son parte.
        :rtype: dict[str, list[list[str | None]]]
        """
        return self._gestion_edicion.vertices_registrados()
        
    def _actualizar_imagen(self, area:str, aviso:str) -> None:
        """
        Actualiza el artefacto que muestra el diagrama y oculta
        los avisos que indicaban el inicio de las operaciones que
        modifican al diagrama, o avisa cuando no es necesario volver
        a generar el gráfico.
        
        :param area: El área de los avisos a mostrar u ocultar.
        :type area: str
        :param aviso: El contenido del aviso.
        :type aviso: str
        """
        if area == "texto":
            if aviso:
                self._texto.mostrar_aviso(aviso)
            else:
                # Solo se actualiza la imagen cuando el aviso es vacío
                self._grafico.cargar_imagen(self.ruta_png)
                self._edicion.volver_a_cargar_nodos()
                self._edicion.volver_a_cargar_vertices()
                self._edicion.volver_a_cargar_relaciones()
                self._texto.ocultar_aviso()
        elif area.startswith("e"):
            self._grafico.actualizar_cuadro()
            self._grafico.cargar_imagen(self.ruta_png)
            if area.endswith("g"):
                self._edicion.ocultar_aviso_grafo()
            elif area.endswith("r"):    
                self._edicion.volver_a_cargar_relaciones()
                self._edicion.ocultar_aviso_relacion()
            elif area.endswith("v"):
                self._edicion.ocultar_aviso_nodo()
                self._edicion.ocultar_aviso_vertice()
        elif area.startswith("p"):
            if aviso:
                self._proyecto.mostrar_aviso(aviso)
            else:
                self._proyecto.ocultar_aviso()

    def _actualizar_texto(self, texto: str) -> None:
        """
        Ubica el contenido extraído en el artefacto de texto desplazable.
        """
        self._texto.cargar_texto_retornado(texto)

    def _borrar_ultima_proposicion(self, *args) -> None:
        """
        Elimina de la tabla de proposiciones el último ingreso y remueve
        de las otras tablas los elementos que quedaron sin relación. Args
        captura la tupla vacía que recibe cuando es llamado para que se
        ejecute en segundo plano.
        """
        # Borra la última fila de la tabla de proposiciones       
        with open(
            self._ruta_csv_proposiciones, "r", newline="", encoding="utf-8"
        ) as proposiciones:
            registros = proposiciones.readlines()
            # Previene que se borre el encabezado
            if len(registros) == 1:
                self.cola_avisos.put(("img","texto","No hay más proposiciones"))
                self.actualizar.set()
                return
        # Escribir todas menos la última
        with open(
            self._ruta_csv_proposiciones, "w", newline="", encoding="utf-8"
        ) as archivo:
            archivo.writelines(registros[:-1])
        # Obtengo los ids
        l_aux: list[str] = registros[-1].split(chr(167))
        ids: dict={}
        ids["ent1"] = l_aux[0]
        ids["rel"] = l_aux[1]      
        ids["ent2"] = l_aux[2].replace("\r\n", "")            
        # Identifico los elementos a borrar
        borrar_ent1: bool = True
        borrar_rel: bool = True
        borrar_ent2: bool = True
        for registro in registros[1:-1]:
            salir: bool = (
                not borrar_ent1 and not borrar_rel and not borrar_ent2
            )
            if salir:
                break
            l_aux = registro.split(chr(167))
            cond: bool = False
            if borrar_ent1:
                cond = (ids["ent1"] in l_aux[0] or ids["ent1"] in l_aux[2])
                if cond:
                    borrar_ent1 = False
            if borrar_rel:
                cond = ids["rel"] in l_aux[1]
                if cond:
                    borrar_rel = False
            if borrar_ent2:
                cond = (ids["ent2"] in l_aux[0] or ids["ent2"] in l_aux[2])
                if cond:
                    borrar_ent2 = False
        # Borro los nodos y/o relaciones aisladas
        if borrar_ent1:
            self.borrar_de_tabla(self._ruta_csv_nodos, ids["ent1"])
            self.borrar_de_tabla(self._ruta_csv_propiedades_n, ids["ent1"])
        if borrar_rel:
            self.borrar_de_tabla(self._ruta_csv_vertices, ids["rel"])
            self.borrar_de_tabla(self._ruta_csv_propiedades_v, ids["rel"])
        if borrar_ent2:
            if ids["ent2"] != ids["ent1"]:
                self.borrar_de_tabla(self._ruta_csv_nodos, ids["ent2"])
                self.borrar_de_tabla(self._ruta_csv_propiedades_n, ids["ent2"])           
        # Obtengo la ruta al grafo generado
        diagramador = diagrama.Diagramador()
        self.ruta_png = diagramador.crear_grafo()
        self.cola_avisos.put(("img","texto",""))
        self.actualizar.set()

    def _encolar_tarea(
        self,
        llamada: Callable,
        cola: queue.Queue,
        var_control: list[bool],
        *args: Any
    ):
        """
        Encola una tarea para que se ejecute en segundo plano. Si no hay nada
        en ejecución, inicia la operación.

        :param llamada: La tarea a ejecutar.
        :param type: Callable
        :param cola: La cola de tareas.
        :param type: queue.Queue
        :param var_control: Una variable de control mutable.
        :param type: list[bool]
        :param args: Los argumentos de los métodos llamados.
        """
        cola.put((llamada, args))
        if not var_control[0]:
            var_control[0] = True
            threading.Thread(
                target = self._procesar_tareas,
                args = (cola, var_control),
                daemon = True
            ).start()

    def _existen_proposiciones(self) -> bool:
        """
        Verifica si la tabla de proposiciones está vacía.

        :return: El resultado de la verificación.
        :rtype: bool
        """      
        with open(
            self._ruta_csv_proposiciones, "r", newline="", encoding="utf-8"
        ) as proposiciones:
            registros = proposiciones.readlines()
            if len(registros) == 1:
                return False
            else:
                return True

    def _guardar_en_segundo_plano(self, *args) -> None:
        """
        Guarda los cambios en el proyecto activo, cuando se usan el atajo
        de teclado. Args captura la tupla vacía que recibe cuando es llamado
        para que se ejecute en segundo plano.
        """
        ubicacion = self._proyecto.directorio_activado
        nombre = self._proyecto.nombre_proyecto        
        if ubicacion and nombre:
            aviso = "Guardando los cambios..."
            self.cola_avisos.put(("img", "texto", aviso))
            self.actualizar.set()
            self.guardar_proyecto(ubicacion, nombre)
        else:
            aviso = "No hay un proyecto activo"
            self.cola_avisos.put(("img", "texto", aviso))
            self.actualizar.set()

    def _inicio_por_cambio_en_tema(self, conservar_fondo: bool) -> None:
        """
        Delega la operación al ámbito que gestiona las tareas del proyecto.      
        
        :param conservar_fondo: Indicación de actualizar o no el color de fondo del grafo.
        :type conservar_fondo: bool
        """
        self._texto.mostrar_aviso(f"Aplicando el tema {self._tema}...")
        self._encolar_tarea(
            self._gestion_proyecto.reinicio_por_tema,
            self._cola_proyecto,
            self._tarea_proyecto,
            conservar_fondo
        )

    def _observador(self) -> None:
        """
        Llama a la actulización de las áreas y/o artefactos correspondientes,
        cada vez que detecta que una tarea en segundo plano dió el aviso de
        haber concluido la operación.
        """
        if self.actualizar.is_set():
            try:
                while True:
                    señal = self.cola_avisos.get_nowait()
                    if señal[0] == "img":
                        self._actualizar_imagen(señal[1], señal[2])
                    if señal[0] == "txt":
                        self._actualizar_texto(señal[1])
            except queue.Empty:
                self.actualizar.clear()
        # Programo la próxima verificación
        self._id_tarea_pendiente = self._raiz.after(1000, self._observador)
                               # reducir a medio segundo

    def _ocultar_avisos(self) -> None:
        """
        Se encarga de ocultar las notificaciones que puedan estar visibles.
        """
        if not self._texto is None:
            self._texto.ocultar_aviso()
##        if not self._edicion is None:
##            self._edicion.ocultar_aviso_relacion()
##            self._edicion.ocultar_aviso_nodo()
##            self._edicion.ocultar_aviso_vertice()
##            self._edicion.ocultar_aviso_grafo()
        if not self._proyecto is None:
            self._proyecto.ocultar_aviso()
        self._id_ocultar_avisos = self._raiz.after(3000, self._ocultar_avisos)
      
    def _procesar_tareas(self, cola: queue.Queue, var_control: list[bool]) -> None:
        """
        Procesa las tareas que fueron encoladas para ser ejecutadas en segundo
        plano.
        
        :param cola: La cola de tareas a procesar.
        :type cola: queue.Queue
        :param var_control: Una variable de control mutable.
        :type var_control: list[bool]
        """
        while not cola.empty():
            try:
                tarea: tuple[Callable, Any] = cola.get()
                metodo: Callable = tarea[0]
                argumentos: Any = tarea[1]
                metodo(argumentos)
                cola.task_done()
            except Exception as e:
                print(f"Error en la tarea: {e}")
        var_control[0] = False
