import csv
import tkinter as tk
from aplicacion.interfaz import comunes
from aplicacion.documentos import contenido, diagrama
from pathlib import Path


class GestionTexto:
    """
    Clase encargada de gestionar las operaciones del área de texto.

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
        self._csv_vertices: Path = vertices
        self._csv_prop_nodos: Path = prop_nodos
        self._csv_prop_vertices: Path = prop_vertices
        self._ultimo_id_nodo:int = 0
        self._ultimo_id_vertice:int = 0
        # Datos para resolver el registro de la proposición
        self._id_ent1: int | str = -1
        self._ent1_defecto: bool = True
        self._id_ent2: int | str = -1
        self._ent2_defecto: bool = True
        self._id_rel: int | str = -1
        self._rel_defecto: bool = True

                
    def enlazar_area(self, grafico, edicion, texto) -> None:
        """
        Conecta la instancia de gestión con las áreas que trabaja.

        :param grafico: La instancia de la clase que muestra el diagrama.
        :type grafico: AreaDeGrafico
        :param edicion: La instancia de la clase que permite editar el diagrama.
        :type edicion: AreaEdicion
        :param texto: La instancia de la clase que permite cargar un texto.
        :type texto: AreaDeTexto      
        """
        self._grafico = grafico
        self._edicion = edicion
        self._texto = texto
            

    def extraer(self, arg_ruta: tuple[str]) -> None:
        """
        Instancia al Extractor de contenido, obtiene y retorna el texto
        del documento (.txt, .pdf) que recibe como argumento.

        :param arg_ruta: La ruta al archivo.
        :type arg_ruta: str
        :return: El texto del documento o "-1". 
        :rtype: str
        """
        res:str = ""
        ruta: str = arg_ruta[0]
        if not isinstance(ruta, tuple):
            extractor = contenido.Extractor()
            texto:str = extractor.extraer_contenido(ruta)
            if texto != "-1":
                res = texto
            else:
                res = "No se seleccionó un archivo válido."
            self._gestor.cola_avisos.put(("txt", res))
            self._gestor.actualizar.set()


    def relacionar(self, arg_proposicion: tuple[list[str]]) -> None:
        """
        Verifica y escribe en las tablas la proposición ingresada. Luego
        actualiza el gráfico.

        :param arg_proposicion: La proposición ingresada.
        :type arg_proposicion: tuple[list[str]]
        """
        # Proceso la proposición
        proposicion: list[str] = arg_proposicion[0]
        proposicion = [self._gestor.eliminar_simbolo(e) for e in proposicion]
        proposicion = [self._gestor.acotar_cadena(e) for e in proposicion]
        proposicion = self._gestionar_justificado(proposicion)
        # Registro nodos y vértices
        self._registrar_nodos(proposicion)
        registrar_proposicion: bool = self._registrar_vertices(proposicion)         
        if registrar_proposicion:
            proposicion_ids: list[int | str] = [
                self._id_ent1, self._id_rel, self._id_ent2, proposicion[3]
            ]
            with open(
                self._csv_proposiciones, "a", newline="", encoding="utf-8"
            ) as proposiciones:
                escritor = csv.writer(proposiciones, delimiter="§")
                escritor.writerow(proposicion_ids)
        else:
            # Si ya existe, restablezco los valores e interrumpo
            aux_aviso:str = "Proposición repetida"
            self._gestor.cola_avisos.put(("img","texto", aux_aviso))
            self._gestor.actualizar.set()            
            self._id_ent1 = -1
            self._ent1_defecto = True
            self._id_ent2 = -1
            self._ent2_defecto = True
            self._id_rel = -1
            self._rel_defecto = True            
            return
        # Registro los atributos de nodos y vértices
        self._registrar_propiedades(proposicion)
        # Obtengo la ruta al grafo generado y el observador actualiza
        diagramador = diagrama.Diagramador()
        self._gestor.ruta_png = diagramador.crear_grafo()
        self._gestor.cola_avisos.put(("img", "texto", ""))
        # Restablezco los valores
        self._id_ent1 = -1
        self._ent1_defecto = True
        self._id_ent2 = -1
        self._ent2_defecto = True
        self._id_rel = -1
        self._rel_defecto = True
        self._gestor.actualizar.set()
        return

    def actualizar_ultimos_ids(self) -> None:
        """
        Obtiene los últimos ids de nodos y vértices cuando se carga un proyecto.
        """
        # Obtengo el último id de los nodos
        with open(
            self._csv_nodos, mode="r", newline="", encoding="utf-8"
        ) as nodos:
            registros = csv.DictReader(nodos, delimiter="§")
            filas: list[dict[str, str]] = list(registros)
        if len(filas) == 0:
            self._ultimo_id_nodo = 0
        else:
            self._ultimo_id_nodo = int(filas[-1]["id"]) + 1
           
        # Obtengo el último id de los vertices
        with open(
            self._csv_vertices, mode="r", newline="", encoding="utf-8"
        ) as vertices:
            registros = csv.DictReader(vertices, delimiter="§")
            filas = list(registros)
        if len(filas) == 0:
            self._ultimo_id_vertice = 0
        else:
            self._ultimo_id_vertice = int(filas[-1]["id"]) + 1

    def _gestionar_justificado(self, proposicion: list[str]) -> list[str]:
        """
        Escapa y agrega el justificado en las entidades y el vínculo para que
        la proposición se escriba sin errores en la tabla.

        :param proposicion: La proposición ingresada.
        :type proposicion: list[str]
        """        
        c_aux:str = "\\" + self._gestor.justificado
        c_aux2:str = proposicion[3]
        if self._gestor.justificado != "n":
            proposicion = [
                e.replace(c_aux, f"\\{self._gestor.justificado}") +
                f"\\{self._gestor.justificado}"
                for e in proposicion[:-1]
            ]
        else:
            proposicion = [
                e.replace(c_aux, f"\\{self._gestor.justificado}")
                for e in proposicion[:-1]
            ]    
        proposicion.append(c_aux2)
        return proposicion
    
    def _registrar_nodos(self, proposicion:list[str]) -> None:
        """
        Registra las entidades ingresadas en la tabla de nodos.
        
        :param proposicion: La proposición ingresada.
        :type proposicion: list[str]
        """
        # Verifico si ya están registrados
        with open(self._csv_nodos, "r", newline="", encoding="utf-8") as nodos:
            registros = csv.DictReader(nodos, delimiter="§")
            for registro in registros:
                # Si la entidad1 ya existe, obtengo su id
                entidad_entrada1:str = self._gestor.eliminar_justificado(proposicion[0])
                entidad_entrada2:str = self._gestor.eliminar_justificado(proposicion[2])
                entidad_en_tabla:str = self._gestor.eliminar_justificado(registro["nodo"])
                if self._id_ent1 == -1 and entidad_en_tabla == entidad_entrada1:
                    self._id_ent1 = registro["id"]
                    # No se le asigna propiedades por defecto 
                    self._ent1_defecto = False                       
                if self._id_ent2 == -1 and entidad_en_tabla == entidad_entrada2:
                    self._id_ent2 = registro["id"]
                    self._ent2_defecto = False
                # Si ambas tienen id salgo del ciclo
                if self._id_ent1 != -1 and self._id_ent2 != -1:
                    break                
        # Si las entidades 1 o 2 no existen las registro en la tabla de nodos        
        with open(self._csv_nodos,"a",newline="",encoding="utf-8") as nodos:
            escritor = csv.writer(nodos, delimiter="§")
            if self._id_ent1 == -1:
                escritor.writerow([self._ultimo_id_nodo, proposicion[0]])
                # Obtengo su id
                self._id_ent1 = self._ultimo_id_nodo
                # Previene que se registre dos veces la misma entidad
                # la primera vez que se escribe
                if proposicion[0] == proposicion[2]:
                    self._id_ent2 = self._id_ent1
                # Actualizo ultimo id nodos
                self._ultimo_id_nodo += 1            
            if self._id_ent2 == -1:
                escritor.writerow([self._ultimo_id_nodo, proposicion[2]])
                self._id_ent2 = self._ultimo_id_nodo
                self._ultimo_id_nodo += 1

    def _registrar_vertices(self, proposicion:list[str]) -> bool:
        """
        Registra el vínculo ingresado en la tabla de vértices y si la
        proposición no existe, la registra en la tabla de proposiciones.
        
        :param proposicion: La proposición ingresada.
        :type proposicion: list[str]
        :return: Indicación sobre la existencia de la proposición.
        :rtype: bool
        """
        # Verifico si el vértice ya está registrado y obtengo su id
        with open(
            self._csv_vertices, "r", newline="", encoding="utf-8"
        ) as vertices:
            registros = csv.DictReader(vertices, delimiter="§")
            for registro in registros:
                relacion_entrada:str = self._gestor.eliminar_justificado(proposicion[1])
                rel_tabla:str = self._gestor.eliminar_justificado(registro["vertice"])
                if rel_tabla == relacion_entrada:
                    self._id_rel = registro["id"] 
                    self._rel_defecto = False
                    break
        # Si no existe
        if self._rel_defecto:            
            # Registro el vértice en la tabla y creo un nuevo id 
            with open(
                self._csv_vertices, "a", newline="", encoding="utf-8"
            ) as vertices:
                escritor = csv.writer(vertices, delimiter="§")
                # El vértice no existe
                if self._id_rel == -1:
                    # Obtengo el últmo id
                    self._id_rel = self._ultimo_id_vertice
                    escritor.writerow([self._id_rel, proposicion[1]])
                    # Actualizo último id vértices
                    self._ultimo_id_vertice += 1
        # El vértice ya existía
        else:        
            # Verifico si existe la proposición      
            prop_aux:dict[str, str] = {
                "ent1" : str(self._id_ent1),
                "rel" : str(self._id_rel),
                "ent2" : str(self._id_ent2),
                "peso" : proposicion[3]
            }        
            with open(
                self._csv_proposiciones, "r", newline="", encoding="utf-8"
            ) as proposiciones:
                registros = csv.DictReader(proposiciones, delimiter="§")
                for registro in registros:
                    if registro == prop_aux:                    
                        # No se agragega porque ya existe
                        return False
        return True

    def _agregar_nodo_a_tabla(self, id_nodo: int | str, valor: str) -> None:
        """
        Antes de escribir, cambia los valores por defecto por los datos ingresados
        y el id generado.

        :param id_nodo: El id del nodo a registrar. 
        :type id_nodo: int | str
        :param valor: El valor del nodo a registrar.
        :type valor: str
        """
        comunes.atrb_nodos["id"] = id_nodo
        comunes.atrb_nodos["label"] = valor
        with open(
            self._csv_prop_nodos, "a", newline="", encoding="utf-8"
        ) as proposiciones:
            escritor = csv.writer(proposiciones, delimiter="§")
            escritor.writerow(comunes.atrb_nodos.values())

    def _registrar_propiedades(self, proposicion:list[str]) -> None:
        """
        Registra en las tablas de propiedades de nodos y vértices los nuevos
        elementos de la proposición ingresada.

        :param proposicion: La proposición ingresada.
        :type proposicion: list[str]
        """
        # Entidad1
        if self._ent1_defecto == True:
            self._agregar_nodo_a_tabla(self._id_ent1, proposicion[0])
        # Entidad2
        if self._ent2_defecto == True:
            self._agregar_nodo_a_tabla(self._id_ent2, proposicion[2])
        # Relación
        if self._rel_defecto == True:
            comunes.atrb_vertices["id"] = self._id_rel
            comunes.atrb_vertices["label"] = proposicion[1]
            with open(
                self._csv_prop_vertices, "a", newline="", encoding="utf-8"
            ) as proposiciones:
                escritor = csv.writer(proposiciones, delimiter="§")    
                escritor.writerow(comunes.atrb_vertices.values())
        # Restablezco valores por defecto en los diccionarios de estilos
        comunes.atrb_nodos["id"] = "-1"
        comunes.atrb_nodos["label"] = ""
        comunes.atrb_vertices["id"] = "-1"
        comunes.atrb_vertices["label"] = ""
