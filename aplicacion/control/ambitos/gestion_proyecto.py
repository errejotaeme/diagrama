import ast
import csv
import os
import shutil
from pathlib import Path
from aplicacion.interfaz import comunes
from aplicacion.documentos import diagrama



class GestionProyecto:
    """
    Clase encargada de gestionar las operaciones del área de proyecto.

    :param gestor: Gestiona la comunicación entre los módulos y la interacción con las tablas.
    :type gestor: Gestor 
    :param proposiciones: Ruta a la tabla de proposiciones.
    :type proposiciones: Path
    :param nodos: Ruta a la tabla de nodos.
    :type nodos: Path
    :param vertices: Ruta a la tabla de vértices.
    :type vertices: Path
    :param prop_nodos: Ruta a la tabla con las propiedades de los nodos.
    :type prop_nodos: Path
    :param prop_vertices: Ruta a la tabla con las propiedades de los vértices.
    :type prop_vertices: Path
    """

    def __init__(
        self,
        gestor,
        proposiciones: Path,
        nodos: Path,
        vertices: Path,
        prop_nodos: Path,
        prop_vertices: Path
    ):
        self._gestor = gestor
        self._csv_proposiciones: Path = proposiciones
        self._csv_nodos: Path = nodos
        self._csv_vertices : Path= vertices
        self._csv_prop_nodos: Path = prop_nodos
        self._csv_prop_vertices: Path = prop_vertices  
        self._ruta_recursos: Path = (Path(__file__).parent.parent.parent / "documentos" / "recursos").resolve()
        self._ruta_respaldo: Path = (Path(__file__).parent.parent.parent / "documentos" / "recursos" / "__respaldo__").resolve()
        self._ruta_estado_grafo: Path = (Path(__file__).parent.parent.parent / "documentos" / "recursos" / "estado_grafo.txt").resolve()
        self._ruta_estado_n_v: Path = (Path(__file__).parent.parent.parent / "documentos" / "recursos" / "estado_n_v.txt").resolve()
              

    def cargar_proyecto_guardado(
        self, directorio: Path | str, origen: str
    ) -> None:
        """
        Método llamado al cargar un proyecto, al reiniciar por cambio de tema o
        cuando no se pudo cargar un proyecto guardado y se recupera el respaldo
        con los datos del estado anterior al intento de carga.

        :param directorio: La ubicación del proyecto guardado.
        :type directorio: Path | str
        :param origen: La procedencia de los archivos a cargar.
        :type origen: str
        """
        directorio_path: Path = Path(directorio)
        necesarios: list[str] = comunes.necesarios.copy()
        cant_necesaria: int = len(necesarios)
        conteo: int = 0
        lista_archivos: list[str] = os.listdir(directorio)
        lista_archivos = [  # Excluyo los archivos ocultos
            a for a in lista_archivos if not a.startswith(".")
        ]
        for archivo in lista_archivos:
            if archivo in necesarios:
                recurso: str = str((directorio_path / archivo).resolve())
                if os.path.isfile(recurso):
                    shutil.copy(recurso, self._ruta_recursos)
                    conteo += 1
                    self._eliminar_copiado(necesarios, archivo)
            else:
                aviso: str = "El directorio seleccionado contiene archivos "
                aviso = aviso + "ajenos al proyecto"
                self._proyecto.mostrar_aviso(aviso)
                raise Exception("Archivos ajenos al proyecto")
        if origen == "guardado":  
            if conteo == cant_necesaria:
                # Cargo los atributos del diagrama
                # y elimino los archivos temporales
                self._cargar_estado_grafo(self._ruta_estado_grafo)
                self._cargar_estado_nodos_vertices(self._ruta_estado_n_v)
                os.remove(self._ruta_estado_grafo)
                os.remove(self._ruta_estado_n_v)
                self._grafico.actualizar_cuadro()                          
            else:
                aviso = f"No se encontró: {str(necesarios)}"
                self._proyecto.mostrar_aviso(aviso) 
                raise Exception("Faltan archivos necesarios")            
        try:  # Genero el diagrama
            diagramador = diagrama.Diagramador()
            self._gestor.ruta_png = diagramador.crear_grafo()
            self._grafico.cargar_imagen(self._gestor.ruta_png)
            self._edicion.volver_a_cargar_nodos()
            self._edicion.volver_a_cargar_vertices()
            self._edicion.volver_a_cargar_relaciones()
        except:
            aviso = "Existen inconsistencias en las tablas"
            self._proyecto.mostrar_aviso(aviso)
            raise Exception("Error en las tablas")  
        self._gestion_texto.actualizar_ultimos_ids()
        # Activo la posibilidad de guardar con atajos de teclado
        directorio_activado: str = str(directorio_path.parent)
        nombre_proyecto: str = str(directorio_path.name)
        if origen != "respaldo":
            self._proyecto.directorio_activado = directorio_activado
            self._proyecto.nombre_proyecto = nombre_proyecto     
            self._proyecto.actualizar_etq_proyecto()
        

    def cargar_respaldo_temporal(self, *args) -> None:
        """
        Carga el proyecto anterior, luego de que la operación de abrir uno
        existente no haya sido existosa o al reiniciar por cambio de tema.
        Args captura la tupla vacía que recibe cuando es llamado por el
        gestor para que se ejecute en segundo plano.
        """
        self.cargar_proyecto_guardado(self._ruta_respaldo, "respaldo") 
        self.eliminar_respaldo_temporal()
        
    def crear_respaldo_temporal(self) -> None:
        """
        Registra el estado de la aplicación antes de intentar cargar
        un proyecto o al reiniciar por cambio de tema, copiando los
        archivos a la carpeta respaldo y creando dos archivos extra
        con las propiedades del diagrama. 
        """
        if not os.path.exists(self._ruta_respaldo):
            os.mkdir(self._ruta_respaldo)
        necesarios: list[str] = comunes.necesarios
        lista_archivos: list[str] = os.listdir(self._ruta_recursos)
        lista_archivos = [a for a in lista_archivos if not a.startswith(".")]
        for archivo in lista_archivos:
            if archivo in necesarios:
                recurso :str = str(
                    (self._ruta_recursos / archivo).resolve()
                )
                if os.path.isfile(recurso):
                    shutil.copy(recurso, self._ruta_respaldo)
        estado_grafo: str = str(
            (self._ruta_respaldo / "estado_grafo.txt").resolve()
        )
        estado_n_v: str = str(
            (self._ruta_respaldo / "estado_n_v.txt").resolve()
        )
        self._guardar_estado_grafo(estado_grafo)
        self._guardar_estado_nodos_vertices(estado_n_v)
        
    def eliminar_respaldo_temporal(self, *args) -> None:
        """
        Elimina el directorio de respaldo con las tablas y el estado
        del diagrama, que fué creado antes de cargar un proyecto o al
        cambiar el tema de la aplicación. Args captura la tupla vacía
        que recibe cuando es llamado por el gestor para que se ejecute
        en segundo plano.
        """
        if os.path.exists(self._ruta_respaldo):
            shutil.rmtree(self._ruta_respaldo)
            
    def eliminar_estados_temporales(self) -> None:
        """
        Elimina los archivos de respaldo con las propiedades del diagrama.
        """
        if os.path.isfile(self._ruta_estado_grafo):
            os.remove(self._ruta_estado_grafo)
        if os.path.isfile(self._ruta_estado_n_v):
            os.remove(self._ruta_estado_n_v)
            
    def enlazar_area(self, proyecto, edicion, grafico, gestion_texto) -> None:
        """
        Conecta el ámbito de gestión con otros ámbitos y áreas.

        :param proyecto: La instancia de la clase que gestiona las opciones del proyecto.
        :type proyecto: AreaProyecto
        :param edicion: La instancia de la clase que permite editar el diagrama.
        :type edicion: AreaEdicion
        :param grafico: La instancia de la clase que muestra el diagrama.
        :type grafico: AreaDeGrafico
        :param gestion_texto: La instancia del ámbito de control de las operaciones relacionadas a la carga de textos.
        :type gestion_texto: GestionTexto
        """
        self._proyecto = proyecto
        self._edicion = edicion
        self._grafico = grafico
        self._gestion_texto = gestion_texto

    def exportar_grafico(self, args_exportar: tuple[str, str]) -> None:
        """
        Guarda el diagrama en la ubicación recibida.

        :param args_exportar: Contiene la extensión del archivo y la ruta de salida.
        :type args_exportar: tuple[str, str]
        """
        diagrama_no_vacio:bool = bool(self._gestor.nodos_existentes())
        if diagrama_no_vacio:
            formato: str = args_exportar[0]
            directorio: str = args_exportar[1]
            diagramador = diagrama.Diagramador()
            diagramador.crear_grafo(formato, directorio)
            aviso: str = "El diagrama se exportó correctamente" 
            self._gestor.cola_avisos.put(("img","proyecto", aviso))
            self._gestor.actualizar.set()
        else:
            aviso = "Diagrama vacío: nada que exportar" 
            self._gestor.cola_avisos.put(("img","proyecto", aviso))
            self._gestor.actualizar.set()
            

    def guardar_proyecto_actual(self, args: tuple[str, str]) -> None:
        """
        Guardar las tablas y txt necesarios para poder recuperar el proyecto.

        :param args: Contiene la ruta a la carpeta y el nombre con el que se guardará el proyecto.
        :type args: tuple[str, str]
        """
        directorio: str = args[0]
        nombre_proyecto: str = args[1]
        salida_path: Path = (Path(directorio) / nombre_proyecto).resolve()
        salida: str = str(salida_path)        
        os.makedirs(salida, exist_ok=True)
        # Creo los txt con el estado actual del grafo
        self._guardar_estado_grafo(self._ruta_estado_grafo)
        self._guardar_estado_nodos_vertices(self._ruta_estado_n_v)
        for archivo in os.listdir(self._ruta_recursos):
            recurso: str = str((self._ruta_recursos / archivo).resolve())
            if os.path.isfile(recurso):
                shutil.copy(recurso, salida)
        os.remove(self._ruta_estado_grafo)
        os.remove(self._ruta_estado_n_v)
        aviso: str = "El proyecto se guardó correctamente"
        self._gestor.cola_avisos.put(("img","proyecto", aviso))
        self._gestor.actualizar.set()


    def reinicio_por_tema(self, args: tuple[bool])->None:
        """
        Método encargado de configurar el estilo del gráfico cuando se cambia
        el tema. Si el booleano que recibe como argumento es verdadero,
        recupera el estilo aplicado al diagrama antes del reinicio y los
        carga en los diccionarios de estilo y en el artefacto correspondiente.
        Al final llama al método encargado de cargar los datos respaldados.

        :param args: La indicación de conservar los atributos del grafo o restablecerlos al cambiar entre los temas.
        :type args: tuple[bool]
        """
        diagrama_no_vacio: bool = args[0]
        # Sólo se cargan los atributos del diagrama
        # cuando se ha ingresado alguna proposición
        if diagrama_no_vacio:
            estado_grafo: str = str(
                (self._ruta_respaldo / "estado_grafo.txt").resolve()
            )
            estado_n_v: str = str(
                (self._ruta_respaldo / "estado_n_v.txt").resolve()
            )            
            self._cargar_estado_grafo(estado_grafo)
            self._cargar_estado_nodos_vertices(estado_n_v)
            self._grafico.actualizar_cuadro()
        self.cargar_proyecto_guardado(self._ruta_respaldo, "respaldo")  
        self.eliminar_respaldo_temporal()
        os.remove(self._ruta_estado_grafo)
        os.remove(self._ruta_estado_n_v)

    def _cargar_estado_grafo(self, archivo: str | Path)->None:
        """
        Obtiene los atributos generales del diagrama y actualiza el diccionario
        de estilo del grafo. Se lo llama cuando se guarda un proyecto o cuando
        se reinicia por tema.

        :param archivo: La ubicación del archivo que contiene los artibutos.
        :type archivo: Path | str
        """
        with open(archivo, "r", newline="", encoding="utf-8") as estado:
            contenido = estado.read()
        lista_atributos_g: list[str| int] = ast.literal_eval(contenido)
        comunes.atrb_grafo["bgcolor"] = lista_atributos_g[0]
        comunes.atrb_grafo["rankdir"] = lista_atributos_g[1]
        self._gestor.cota = int(lista_atributos_g[2])
        self._gestor.justificado = lista_atributos_g[3]

    def _cargar_estado_nodos_vertices(self, archivo: str | Path) -> None:
        """
        Obtiene los atributos de nodos y vértices y actualiza sus diccionarios
        de estilo. Se lo llama cuando se guarda un proyecto o cuando se reinicia
        por tema.

        :param archivo: La ubicación del archivo que contiene los atributos.
        :type archivo: Path | str
        """
        with open(archivo, "r", newline="", encoding="utf-8") as estado:
            dicts_n_v: list[str] = estado.readlines()
            comunes.atrb_nodos = ast.literal_eval(dicts_n_v[0])
            comunes.atrb_vertices = ast.literal_eval(dicts_n_v[1])

    def _eliminar_copiado(self, lista: list[str], elem: str) -> None:
        """
        Ayuda a vaciar la copia de la lista de necesarios al cargar un proyecto,
        permitiendo identificar los archivos faltantes en caso de error.

        :param lista: Una lista con los archivos necesarios para cargar un proyecto.
        :type lista: list[str]
        :param elem: Un elemento de la lista.
        :type elem: str
        """
        i:int = 0
        for item in lista:
            if item == elem:
                break
            i += 1
        try:
            del lista[i]
        except:
            pass

    def _guardar_estado_grafo(self, archivo: str | Path)->None:
        """
        Registra los atributos generales del grafo en un archivo cuando
        se guarda un proyecto o al reinicio por cambio tema.

        :param archivo: La ruta al archivo donde guardar los atributos.
        :type archivo: Path | str
        """
        lista_atributos: list[str | int] = []
        lista_atributos.append(comunes.atrb_grafo["bgcolor"])
        lista_atributos.append(comunes.atrb_grafo["rankdir"])
        lista_atributos.append(self._gestor.cota)
        lista_atributos.append(self._gestor.justificado)        
        atributos_grafo: str = str(lista_atributos)        
        with open(archivo, "w",newline="", encoding="utf-8") as estado:
            estado.write(atributos_grafo)

    def _guardar_estado_nodos_vertices(self, archivo: str | Path) -> None:
        """
        Registra los atributos de nodos y vértices en un archivo cuando
        se guarda un proyecto o al reinicio por cambio tema.

        :param archivo: La ruta al archivo donde guardar los atributos.
        :type archivo: Path | str
        """        
        atrb_nodos: str = str(comunes.atrb_nodos)
        atrb_vertices: str = str(comunes.atrb_vertices)
        with open(archivo, "w", newline="", encoding="utf-8") as estado:
            estado.write(atrb_nodos + "\n")
            estado.write(atrb_vertices + "\n")      
