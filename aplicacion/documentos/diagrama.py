import csv, graphviz  # type: ignore
import platform
from pathlib import Path
from typing import Any
from aplicacion.interfaz import comunes


class Diagramador:
    """
    Clase encargada de generar el diagrama. Su constructor genera 
    las rutas a los archivos necesarios para construir el diagrama.
    """
    
    def __init__(self):
        """
        Constructor de la clase Diagramador. 
        """
        self._ruta_salida: Path = (Path(__file__).parent.parent / "resultados").resolve()
        self._ruta_csv_proposiciones: Path = (Path(__file__).parent / "recursos" / "proposiciones.csv").resolve()
        self._ruta_csv_propiedades_n: Path = (Path(__file__).parent / "recursos" / "propiedades_n.csv").resolve()
        self._ruta_csv_propiedades_v: Path = (Path(__file__).parent / "recursos" / "propiedades_v.csv").resolve()
        self._ruta_csv_nodos: Path = (Path(__file__).parent / "recursos" / "nodos.csv").resolve()
        self._ruta_csv_vertices: Path = (Path(__file__).parent / "recursos" / "vertices.csv").resolve()
        self._nombre_png: str = "grafo_proposiciones"    
    
    def crear_grafo(
        self, formato: str = "png", directorio: str | Path = ""
    ) -> str:
        """
        Genera un archivo png o pdf a partir de las tablas.

        :param formato: La extensión deseada del archivo con el diagrama.
        :type formato: str
        :param directorio: La ubicación donde guardar el diagrama.
        :type directorio: str | Path
        :return: La ruta al archivo con el diagrama generado. 
        :rtype: str
        """
        if not directorio:
            directorio = self._ruta_salida
        grafo = graphviz.Digraph(
            self._nombre_png, graph_attr=comunes.atrb_grafo
        )
        # Cargo los nodos
        with open(
            self._ruta_csv_nodos, "r", newline="", encoding="utf-8"
        ) as nodos:
            registros = csv.DictReader(nodos, delimiter="§")
            for registro in registros:
                atributos: list[str | Any] = self._atributos(
                    registro["id"], self._ruta_csv_propiedades_n
                )
                grafo.node(registro["id"], **atributos[0])
        # Cargo los vertices
        with open(
            self._ruta_csv_proposiciones, "r", newline="", encoding="utf-8"
        ) as proposiciones:
            registros = csv.DictReader(proposiciones, delimiter="§")
            for registro in registros:
                atributos = self._atributos(
                    registro["rel"], self._ruta_csv_propiedades_v
                )
                grafo.edge(
                    registro["ent1"],         # Id nodo1
                    registro["ent2"],         # Id nodo2
                    f" {atributos[0]}",       # Texto de relación
                    weight=registro["peso"],  # Peso de la relación
                    **atributos[1]            # Propiedades del vértice
                )           
        grafo.render(directory=directorio, format=formato)
        res: Path = (self._ruta_salida / f"{self._nombre_png}.gv.{formato}").resolve()
        return str(res)

    def _atributos(
        self, id_elem : str, tabla_propiedades : Path
    ) -> list[str | Any]:
        """
        Obtiene los atributos de estilo de nodos y vértices.

        :param id_elem: El id del elemento.
        :type id_elem: str
        :param tabla_prop: La tabla en la que se encuentran los datos. 
        :type tabla_prop: Path
        :return: Los atributos del elemento.
        :rtype: list[str | Any]
        """
        res: list[str | Any] = []
        with open(
            tabla_propiedades, "r", newline="", encoding="utf-8"
        ) as tabla:
            registros = csv.DictReader(tabla, delimiter="§")
            for registro in registros:
                if registro["id"] == id_elem:
                    # Obtengo la etiqueta aparte para separarla del vértice
                    if str(tabla_propiedades).endswith("v.csv"):
                        res.append(registro["label"])
                        del registro["id"]
                        del registro["label"]
                        res.append(registro)                        
                    else:
                        del registro["id"]
                        res.append(registro) 
                    break                        
        return res
        
