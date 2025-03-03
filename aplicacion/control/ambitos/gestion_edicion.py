import csv
from aplicacion.interfaz import comunes
from aplicacion.documentos import diagrama
from pathlib import Path


class GestionEdicion:
    """
    Clase encargada de gestionar las operaciones del área de edición.

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
        self._edicion = None
        self._gestor = gestor
        self._csv_proposiciones: Path = proposiciones
        self._csv_nodos: Path = nodos
        self._csv_vertices: Path = vertices
        self._csv_prop_nodos: Path = prop_nodos
        self._csv_prop_vertices: Path = prop_vertices

    def atributos_de_elemento(self, tipo: str, id_elem: str) -> tuple[str, dict[str, str]]:
        """
        Retorna los atributos del nodo o vértice cuyo id recibe como argumento.
        
        :param tipo: El tipo de elemento (nodo o vértice).
        :type tipo: str
        :param id_elem: El id del elemento.
        :type id_elem: str
        :return: Los atributos del elemento.
        :rtype: tuple[str, dict[str, str]]
        """
        res_fila: dict[str, str] = {}       
        if tipo == "nodo":
            with open(
                self._csv_prop_nodos, "r", newline="",  encoding="utf-8"
            ) as propiedades:
                registros = csv.DictReader(propiedades, delimiter="§")
                for fila in registros:
                    if fila["id"] == id_elem:
                        res_fila = fila
                        break
        else:
            fila_res:dict = {}
            with open(
                self._csv_prop_vertices, "r", newline="", encoding="utf-8"
            ) as propiedades:
                registros = csv.DictReader(propiedades, delimiter="§")
                for fila in registros:
                    if fila["id"] == id_elem:
                        res_fila = fila
                        break
            with open(
                self._csv_proposiciones, "r", newline="", encoding="utf-8"
            ) as proposiciones:
                registros = csv.DictReader(proposiciones, delimiter="§")
                filas = list(registros)
            for fila in filas:
                if fila["rel"] == id_elem:
                    res_fila["peso"] = fila["peso"]
                    break
        return id_elem, res_fila

    def borrar_relacion(self, arg_id: tuple[str]) -> None:
        """
        Elimina la proposición indicada de la tabla de proposiciones,  y de
        la tabla de nodos, vértices y propiedades cuando corresponde. Luego
        actualiza la vista.

        :param arg_id: El id de la proposición a eliminar.
        :type arg_id: tuple[str]
        """
        id_rel: str = arg_id[0]
        ids_a_borrar: list[str] = self._borrar_fila_proposicion(id_rel)        
        self._borrar_elementos_aislados(ids_a_borrar)       
        diagramador = diagrama.Diagramador()
        self._gestor.ruta_png = diagramador.crear_grafo()
        self._gestor.cola_avisos.put(("img", "edición_r", ""))
        self._gestor.actualizar.set()      
                
    def enlazar_area(self, edicion) -> None:
        """
        Conecta la instancia de gestión con el área que trabaja.

        :param edicion: La instancia de la clase que permite editar el diagrama.
        :type edicion: AreaEdicion 
        """
        self._edicion = edicion

    def enviar(self, mensaje: list[str]) -> None:
        """
        Envía el mensaje recibido desde los OptionMenu al área correspondiente.

        :param mensaje: Una lista con la referencia de la instancia y la opción elegida.
        :type mensaje: list[str]
        """
        if mensaje[0] == "opc_edicion":
            if not self._edicion is None:
                self._edicion.cambio_en_opc(mensaje[1])
        elif mensaje[0] == "opc_forma_nodo":
            if not self._edicion is None:
                self._edicion.cambio_en_forma_nodo(mensaje[1])
        elif mensaje[0] == "opc_tipo_flecha_d":
            if not self._edicion is None:
                self._edicion.cambio_en_flecha_d(mensaje[1])
        elif mensaje[0] == "opc_tipo_flecha_t":
            if not self._edicion is None:
                self._edicion.cambio_en_flecha_t(mensaje[1])
        elif mensaje[0] == "opc_direccion":
            if not self._edicion is None:
                self._edicion.cambio_en_direccion(mensaje[1])
        elif mensaje[0] == "opc_crecimiento":
            if not self._edicion is None:
                self._edicion.cambio_en_crecimiento(mensaje[1])
        elif mensaje[0] == "opc_justificado":
            if not self._edicion is None:
                self._edicion.cambio_en_justificado(mensaje[1])

    def ids_registrados(self, elem: str) -> list[str]:
        """
        Retorna una lista con los ids registrados en la tabla de nodos o
        de vértices.

        :param elem: El tipo de los elementos.
        :type elem: str
        """        
        if elem == "vértice":
            res:list = self._obtener_ids(self._csv_vertices)
        else:
            res = self._obtener_ids(self._csv_nodos)
        return res

    def modificar_grafo(self, arg_cambios: tuple[list[dict[str, str]]]) -> None:
        """
        Escribe las modificaciones en la tabla y aplica los cambios al
        diccionario de estilos para que los nuevos ingresos tengan los
        atributos definidos.

        :param arg_cambios: Los cambios en los atributos del grafo.
        :type arg_cambios: tuple[dict[str, str]]
        """
        cambios: list[dict[str, str]] = arg_cambios[0]
        if cambios[0]:
            self._actualizar_propiedades(
                self._csv_prop_nodos, cambios[0]
            )            
            for clave in cambios[0]:
                comunes.atrb_nodos[clave] = cambios[0][clave]
        if cambios[1]:
            self._actualizar_propiedades(
                self._csv_prop_vertices, cambios[1]
            )
            for clave in cambios[1]:
                comunes.atrb_vertices[clave] = cambios[1][clave]
        if cambios[2]:
            self._actualizar_atributos_grafo(cambios[2])
        # Obtengo la ruta al grafo generado
        diagramador = diagrama.Diagramador()
        self._gestor.ruta_png = diagramador.crear_grafo()
        self._gestor.cola_avisos.put(("img", "edición_g", ""))
        self._gestor.actualizar.set()

    def modificar_elemento(
        self, arg_elem: tuple[str, str, dict[str, str]]
    ) -> None:
        """
        Actualiza los atributos de nodos y vértices con los ingresados
        en la sección edición.
        
        :param arg_elem: Los cambios en el elemento.
        :type arg_elem: tuple[str, str, dict[str, str]]
        """
        tipo: str = arg_elem[0]
        id_elem: str = arg_elem[1]
        cambios: dict[str, str] = arg_elem[2]
        if tipo == "nodo":
            self._actualizar_fila(
                self._csv_prop_nodos, id_elem, cambios
            )
        else:
            self._actualizar_fila(
                self._csv_prop_vertices, id_elem, cambios
            )
        diagramador = diagrama.Diagramador()
        self._gestor.ruta_png = diagramador.crear_grafo()
        self._gestor.cola_avisos.put(("img", "edición_v", ""))
        self._gestor.actualizar.set()  

    def modificar_registros(
        self, arg_cambios: tuple[dict[str, tuple[str, str]]]
    ) -> None:
        """
        Registra las modificaciones realizadas en la sección relación
        a los elementos de una proposición específica. Actuliza en las
        tablas los registros de los que forman parte los elementos
        modificados.

        :param arg_cambios: Los cambios en el elemento.
        :type arg_cambios: tuple[dict[str, tuple[str, str]]]        
        """
        cambios: dict[str, tuple[str, str]] = arg_cambios[0]
        # Proceso las cadenas ingresadas
        if not cambios["ent2"]:
            del cambios["ent2"]
        valores: list[str] = [cambios[c][1] for c in cambios.keys()]
        valores = [self._gestor.eliminar_simbolo(v) for v in valores]
        valores = [self._gestor.acotar_cadena(v) for v in valores]
        valores = self._gestionar_justificado(valores)
        # Actualizo las tablas correspondientes
        self._escribir_en_tablas(valores, cambios)
        # Actualizo la vista
        diagramador = diagrama.Diagramador()
        self._gestor.ruta_png = diagramador.crear_grafo()
        self._gestor.cola_avisos.put(("img", "edición_r", ""))
        self._gestor.actualizar.set()  

    def nodos_registrados(self) -> dict[str, str | None]:
        """
        Retorna los nodos registrados en la tabla.

        :return: Los nodos registrados.
        :rtype: dict[str, str | None]
        """
        res: dict[str, str | None] = {}
        with open(self._csv_nodos, "r", newline="", encoding="utf-8") as nodos:
            registros = csv.DictReader(nodos, delimiter="§")
            for registro in registros:
                res[registro["id"]] = registro["nodo"]
        return res

    def relaciones_registradas(self) -> dict[int, list[tuple[str, str]]]:
        """
        Retorna el número de fila y el registro correspondiente de las
        proposiciones en la tabla junto con el valor de cada id.

        :return: Las proposiciones registradas.
        :rtype: dict[int, list[tuple[str, str]]]
        """
        res: dict[int, list[tuple[str, str]]] = {} 
        with open(
            self._csv_proposiciones, "r", newline="", encoding="utf-8"
        ) as proposiciones:
            registros = csv.DictReader(proposiciones, delimiter="§")
            id_prop: int = 1
            for fila in registros:
                l_aux: list = []
                id_ent1, id_rel, id_ent2 = (
                    fila["ent1"], fila["rel"], fila["ent2"]
                )               
                val_ent1: str = self._valor_entidad(self._csv_nodos, id_ent1)
                val_rel: str = self._valor_entidad(self._csv_vertices, id_rel)
                val_ent2: str = self._valor_entidad(self._csv_nodos, id_ent2)
                t_ent1: tuple[str, str] = (id_ent1, val_ent1)
                t_rel: tuple[str, str] = (id_rel, val_rel)
                t_ent2: tuple[str, str] = (id_ent2, val_ent2)
                l_aux.append(t_ent1)
                l_aux.append(t_rel)
                l_aux.append(t_ent2)
                res[id_prop] = l_aux
                id_prop += 1
        return res

    def vertices_registrados(self) -> dict[str, list[list[str | None]]]:
        """
        Retorna, para cada vértice registrado en la tabla, una lista de las
        proposiciones de las que forma parte.
            
        :return: Los vértices registrados.
        :rtype: dict[str, list[list[str | None]]]
        """
        # creo el diccionadior de ids de vertices con listas vacias como valores
        ids_vertices: dict[str, list[list[str | None]]] = {}
        with open(
            self._csv_vertices, "r", newline="", encoding="utf-8"
        ) as vertices:
            registros = csv.DictReader(vertices, delimiter="§")
            for registro in registros:
                id_actual:str = registro["id"]
                ids_vertices[id_actual] = []
                with open(
                    self._csv_proposiciones, "r", newline="", encoding="utf-8"
                ) as proposiciones:
                    filas = csv.DictReader(proposiciones, delimiter="§")
                    for fila in filas:
                        if fila["rel"] == id_actual:
                            ent1: str = self._valor_entidad(
                                self._csv_nodos, fila["ent1"]
                            )
                            ent2: str = self._valor_entidad(
                                self._csv_nodos, fila["ent2"]
                            )
                            c_aux: str = self._gestor.eliminar_justificado(
                                registro["vertice"]
                            )                                
                            ids_vertices[id_actual].append(
                                [ent1, c_aux, ent2]
                            )
        return ids_vertices

    def _actualizar_atributos_grafo(self, cambios_grafo: dict[str, str]) -> None:
        """
        Actualiza las entradas del diccionario con los atributos del grafo.
        Algunas claves pueden no existir. Utiliza un indicador que previene
        realizar la gestión del justificado en los valores de nodos y vértices.

        :param cambios_grafo: Las modificaciones ingresadas en edición de grafo.
        :type cambios_grafo: dict[str, str]
        """
        justificado_aplicado: bool = False
        try:
            color_bg_grafo: str = cambios_grafo["fondo"]
            if color_bg_grafo:
                comunes.atrb_grafo["bgcolor"] = color_bg_grafo
        except:
            pass
        try:
            direccion: str = cambios_grafo["crecimiento"]
            if direccion:
                comunes.atrb_grafo["rankdir"] = direccion
        except:
            pass
        try:
            cota: str = cambios_grafo["cota"]
            if cota:
                self._gestor.cota = int(cota)
                justificado: str = ""
                try:
                    if cambios_grafo["justificado"] != self._gestor.justificado:
                        self._gestor.justificado = cambios_grafo["justificado"]
                    else:
                        pass                        
                except:
                    pass
                self._normalizar_tablas()
                justificado_aplicado = True
        except:
            pass
        if not justificado_aplicado:            
            try:
                justificado = cambios_grafo["justificado"]
                if justificado:
                    if justificado != self._gestor.justificado:
                        self._gestor.justificado = justificado
                        self._normalizar_tablas()
            except:
                pass

    def _actualizar_fila(
        self, tabla:Path, id_elem: str, cambios: dict[str, str]
    ) -> None:
        """
        Reemplaza en la tabla correspondiente, la fila del elemento cuyo id
        recibe como argumento, con los cambios contenidos en el diccionario.

        :param tabla: La ruta a la tabla.
        :type tabla: Path
        :param id_elem: El id del elemento a modificar.
        :type id_elem: str
        :param cambios: Los nuevos valores.
        :type cambios: dict[str. str]
        """
        peso: str = ""
        if str(tabla).endswith("v.csv"):
            try:
                peso = cambios["peso"]
                del cambios["peso"]
            except:
                pass
        with open(tabla, "r", newline="", encoding="utf-8") as propiedades:
            registros = csv.DictReader(propiedades, delimiter="§")
            filas: list[dict[str, str]] = list(registros)                
        encabezado:list[str] = list(filas[0].keys())
        indice_fila_editada:int  = -1
        for dicc_fila in filas:
            indice_fila_editada += 1
            if dicc_fila["id"] == id_elem:
                break
        # Actualizo los valores
        for atributo in cambios.keys():
            filas[indice_fila_editada][atributo] = cambios[atributo]
        # Preparo las filas y luego las escribo              
        filas_actualizadas:list[list[str]] = [
            list(fila.values()) for fila in filas
        ]
        with open(tabla, "w", newline="", encoding="utf-8") as propiedades:
            escritor = csv.writer(propiedades, delimiter="§")
            escritor.writerow(encabezado)
            for fila in filas_actualizadas:
                escritor.writerow(fila)
        # Actualizo los pesos
        if peso:
            self._actualizar_peso(id_elem, peso)          


    def _actualizar_peso(self, id_vertice: str, peso: str) -> None:
        """
        Modifica en la tabla de proposiciones el peso de las relaciones que
        incluyen al vértice cuyo id recibe como argumento.
        
        :param id_vertice: El id del vértice.
        :type id_vertice: str
        :param peso: El nuevo peso de la relación.
        :type peso: str
        """
        with open(
            self._csv_proposiciones, "r", newline="", encoding="utf-8"
        ) as proposiciones:
            registros = csv.DictReader(proposiciones, delimiter="§")
            filas: list[dict[str, str]] = list(registros)                
        encabezado:list[str] = list(filas[0].keys())
        for dicc_fila in filas:
            if dicc_fila["rel"] == id_vertice:
                dicc_fila["peso"] = str(peso)
        filas_actualizadas:list[list[str]] = [
            list(fila.values()) for fila in filas
        ]
        with open(
            self._csv_proposiciones, "w", newline="", encoding="utf-8"
        ) as proposiciones:
            escritor = csv.writer(proposiciones, delimiter="§")
            escritor.writerow(encabezado)
            for fila in filas_actualizadas:
                escritor.writerow(fila)  

    def _actualizar_propiedades(
        self, tabla: Path, cambios: dict[str, str]
    ) -> None:
        """
        Actualiza todos los registros de la tabla que recibe como argumento,
        con los cambios almacenados en el diccionario.

        :param tabla: La ruta a la tabla de propiedades a modificar.
        :type tabla: Path
        :param cambios: Los nuevos valores.
        :type cambios: dict[str, str]
        """
        filas: list[dict[str, str]] = [{}]
        with open(tabla, "r", newline="", encoding="utf-8") as propiedades:
            registros = csv.DictReader(propiedades, delimiter="§")
            filas = list(registros)
        # Actulizo los valores
        for clave in cambios.keys():
            for dicc_fila in filas:
                dicc_fila[clave] = cambios[clave]
        # Preparo los datos para escribirlos
        encabezado:list[str] = list(filas[0].keys())
        filas_actualizadas:list[list[str]] = [
            list(fila.values()) for fila in filas
        ]
        # Escribo los cambios en la tabla
        with open(tabla, "w", newline="", encoding="utf-8") as propiedades:
            escritor = csv.writer(propiedades, delimiter="§")
            escritor.writerow(encabezado)
            for fila in filas_actualizadas:
                escritor.writerow(fila)

    def _borrar_elementos_aislados(self, ids_a_borrar: list[str]) -> None:
        """
        Encuentra y elimina los elementos no incluidos en alguna proposición
        de las tablas de nodos, vertices y propiedades.

        :param ids_a_borrar: Los candidatos a ser borrados.
        :type ids_a_borrar: list[str]
        """
        borrar_ent1: bool = True
        borrar_rel: bool = True
        borrar_ent2: bool = True
        seguir_buscando: bool = borrar_ent1 or borrar_rel or borrar_ent2
        ent1: str = ids_a_borrar[0]
        rel: str = ids_a_borrar[1]
        ent2: str = ids_a_borrar[2]
        with open(
            self._csv_proposiciones, "r", newline="", encoding="utf-8"
        ) as proposiciones:
            registros = csv.DictReader(proposiciones, delimiter="§")
            for registro in registros:
                if not seguir_buscando:
                    break
                if borrar_ent1:
                    if registro["ent1"] == ent1 or registro["ent2"] == ent1:
                        borrar_ent1 = False
                if borrar_ent2:
                    if registro["ent1"] == ent2 or registro["ent2"] == ent2:
                        borrar_ent2 = False                
                if borrar_rel:
                    if registro["rel"] == rel:
                        borrar_rel = False
        if borrar_ent1:
            self._gestor.borrar_de_tabla(self._csv_nodos, ent1)
            self._gestor.borrar_de_tabla(self._csv_prop_nodos, ent1)
        if borrar_rel:
            self._gestor.borrar_de_tabla(self._csv_vertices, rel)
            self._gestor.borrar_de_tabla(self._csv_prop_vertices, rel)
        if borrar_ent2:
            if ent2 != ent1:
                self._gestor.borrar_de_tabla(self._csv_nodos, ent2)
                self._gestor.borrar_de_tabla(self._csv_prop_nodos, ent2)
                    

    def _borrar_fila_proposicion(self, indice: str) -> list[str]:
        """
        Borra la fila indicada por el índice y devuelve los ids de los
        elementos de la proposición eliminada.

        :param indice: El índice de la fila a borrar.
        :type indice: str
        """
        with open(
            self._csv_proposiciones, "r", newline="", encoding="utf-8"
        ) as proposiciones:
            registros = proposiciones.readlines()
        indice_fila:int = int(indice)
        ids_a_borrar:list[str] = registros[indice_fila].split(chr(167))
        del ids_a_borrar[3] # Elimino el campo de peso
        del registros[indice_fila] # Elimino la fila
        with open(
            self._csv_proposiciones, "w", newline="", encoding="utf-8"
        ) as archivo:
            archivo.writelines(registros)
        return ids_a_borrar


    def _editar_campo(
        self, tabla: Path, campo: str, id_elem: str, valor: str
    ) -> None:
        """
        Modifica el campo de la tabla con el valor recibido, del elemento
        cuyo id también recibe como argumento.

        :param tabla: La ruta a la tabla a modificar.
        :type tabla: Path
        :param campo: El campo que se debe modificar.
        :type campo: str
        :param id_elem: El id del elemento.
        :type id_elem: str
        :param valor: El nuevo valor.
        :type valor: str
        """
        indice: int = self._obtener_indice_registro(tabla, id_elem)
        indice -= 1
        with open(tabla, "r", newline="", encoding="utf-8") as archivo:
            registros = csv.DictReader(archivo, delimiter="§")
            filas: list[dict[str, str]] = list(registros)
        encabezado:str = chr(167).join(filas[0].keys())
        encabezado = encabezado + "\r\n"
        # Modifico el campo deseado
        filas[indice][campo] = valor
        nuevos_registros = []
        nuevos_registros.append(encabezado)
        for fila in filas:
            c_aux:str = chr(167).join([fila[c] for c in fila.keys()])
            c_aux = c_aux + "\r\n"
            nuevos_registros.append(c_aux)
        with open(tabla, "w", newline="",encoding="utf-8") as archivo:
            archivo.writelines(nuevos_registros)  

                    
    def _editar_registro(self, tabla: Path, id_elem: str, valor: str) -> None:
        """
        Modifica un registro de la tabla de nodos o vértices.

        :param tabla: La ruta a la tabla a modificar.
        :type tabla: Path
        :param id_elem: El id del elemento.
        :type id_elem: str
        :param valor: El nuevo valor.
        :type valor: str
        """
        indice: int = self._obtener_indice_registro(tabla, id_elem)
        with open(tabla, "r", newline="", encoding="utf-8") as archivo:
            registros = archivo.readlines()
        nueva_fila: str = id_elem + chr(167) + valor + "\r\n"
        registros[indice] = nueva_fila
        with open(tabla, "w", newline="",encoding="utf-8") as archivo:
            archivo.writelines(registros) 


    def _escribir_en_tablas(
        self, valores: list[str], cambios: dict[str, tuple[str, str]]
    ) -> None:
        """
        Actualiza las tablas de nodos, vértices y propiedades con los valores
        ingresados al modificar una relación.

        :param valores: Los nuevos valores de nodos y/o vértices.
        :type valores: list[str]
        :param cambios: Los cambios en los atributos de los elementos.
        :type cambios: dict[str, tuple[str, str]]
        """
        # Entidad1
        id_ent1: str = cambios["ent1"][0]
        val_ent1: str = valores[0]
        self._editar_registro(self._csv_nodos, id_ent1, val_ent1)
        self._editar_campo(self._csv_prop_nodos, "label", id_ent1, val_ent1)
        # Relacion
        id_rel: str = cambios["rel"][0]
        val_rel: str = valores[1]
        self._editar_registro(self._csv_vertices, id_rel, val_rel)
        self._editar_campo(self._csv_prop_vertices, "label", id_rel, val_rel)
        # Entidad2
        try:
            if cambios["ent2"]:
                id_ent2: str = cambios["ent2"][0]
                val_ent2: str = valores[2]
                self._editar_registro(self._csv_nodos, id_ent2, val_ent2)
                self._editar_campo(
                    self._csv_prop_nodos, "label", id_ent2, val_ent2
                )
        except:
            pass

    def _gestionar_justificado(self, valores: list[str]) -> list[str]:
        """
        Alinea la modificación ingresada según los valores establecidos.

        :param valores: La modificación ingresada.
        :type valores: list[str]
        :return: Las cadenas de texto alineadas según el criterio existente.
        :rtype: list[str]
        """
        c_aux:str = "\\" + self._gestor.justificado
        if self._gestor.justificado != "n":
            valores = [
                v.replace(c_aux, f"\\{self._gestor.justificado}") +
                f"\\{self._gestor.justificado}"
                for v in valores
            ]
        else:
            valores = [
                v.replace(c_aux, f"\\{self._gestor.justificado}")
                for v in valores
            ]    
        return valores            
        
                    

    def _normalizar_tablas(self) -> None:
        """
        Envía cada una de las tablas a un método que les aplica el criterio
        existente.
        """
        self._ordenar(self._csv_nodos, "nodo")
        self._ordenar(self._csv_vertices, "vertice")
        self._ordenar(self._csv_prop_nodos, "label")
        self._ordenar(self._csv_prop_vertices, "label")

    def _obtener_ids(self, tabla: Path) -> list[str]:
        """
        Retorna una lista con los ids de la tabla de nodos o vértices.
        
        :param tabla: La ruta a la tabla.
        :type tabla: Path
        :return: La lista de ids.
        :rtype: list[str]
        """
        res:list[str] = []
        with open(tabla, "r", newline="", encoding="utf-8") as archivo:
            registros = csv.DictReader(archivo, delimiter="§")
            for registro in registros:
                res.append(registro["id"])
        return res

    def _obtener_indice_registro(self, tabla: Path, id_elem: str) -> int:
        """
        Retorna el índice de la fila de la tabla que coincide con el id
        recibido como argumento.
        
        :param tabla: La ruta a la tabla donde buscar.
        :type tabla: Path
        :param id_elem: El id del elemento.
        :type id_elem: str
        :return: El índice de la fila.
        :rtype: int
        """
        with open(tabla, "r", newline="", encoding="utf-8") as archivo:
            registros = archivo.readlines()
        indice: int = 1
        for registro in registros[1:]:
            l_aux = registro.split(chr(167))
            if l_aux[0] == id_elem:
                break
            indice += 1
        return indice

    def _ordenar(self, tabla: Path, columna: str) -> None:
        """
        Aplica el justificado existente a los campos de texto de cada fila
        de la tabla recibida.

        :param tabla: La ruta a la tabla a ordenar.
        :type tabla: Path
        :param columna: Un indicador que permite aplicar un proceso diferente según la estructura de la tabla.
        :type columna: str
        """
        if columna == "nodo" or columna == "vertice":
            registros_aux: list[str] = []
            with open(tabla, "r", newline="", encoding="utf-8") as archivo:
                registros = archivo.readlines()
            registros_aux.append(registros[0])            
            agregar_justificado: bool = False
            if self._gestor.justificado != "n":
                agregar_justificado = True
            for registro in registros[1:]:                
                l_aux: list[str] = registro.split(chr(167))
                c_aux: str = l_aux[1]
                # Remuevo justificados anteriores
                c_aux = self._gestor.eliminar_justificado(c_aux)
                c_aux = self._gestor.acotar_cadena(c_aux)
                if agregar_justificado:
                    c_aux = (
                        l_aux[0] + chr(167) + c_aux +
                        f"\\{self._gestor.justificado}" + "\r\n"
                    )
                else:
                    c_aux = l_aux[0] + chr(167) + c_aux + "\r\n"
                registros_aux.append(c_aux)
            with open(tabla, "w", newline="", encoding="utf-8") as archivo:
                archivo.writelines(registros_aux)
        # Tablas de propiedades, mismo procedimiento, otra estructura
        else:
            registros_aux = []
            with open(tabla, "r", newline="", encoding="utf-8") as archivo:
                registros = archivo.readlines()
            registros_aux.append(registros[0])
            agregar_justificado = False
            if self._gestor.justificado != "n":
                agregar_justificado = True
            for registro in registros[1:]:
                l_aux = registro.split(chr(167))
                c_aux = l_aux[10]
                c_aux = self._gestor.eliminar_justificado(c_aux)
                c_aux = self._gestor.acotar_cadena(c_aux)
                # Obtengo las columnas anteriores a "label"
                anteriores:str = chr(167).join([col for col in l_aux[:10]])
                if agregar_justificado:
                    # Tabla propiedades vértices
                    if str(tabla).endswith("v.csv"):
                        siguiente: str = l_aux[11]
                        c_aux = (
                            anteriores + chr(167) + c_aux +
                            f"\\{self._gestor.justificado}" + chr(167) + siguiente
                        )
                    # Tabla propiedades nodos
                    else:
                        c_aux = (
                            anteriores + chr(167) + c_aux +
                            f"\\{self._gestor.justificado}" + "\r\n"
                        )
                else:
                    if str(tabla).endswith("v.csv"):
                        siguiente = l_aux[11]
                        c_aux = (
                            anteriores + chr(167) + c_aux + chr(167) + siguiente
                        )
                    else:
                        c_aux = anteriores + chr(167) + c_aux + "\r\n"                    
                registros_aux.append(c_aux)
            with open(tabla, "w", newline="", encoding="utf-8") as archivo:
                archivo.writelines(registros_aux)

    def _valor_entidad(self, tabla: Path, id_entidad: str) -> str:
        """
        Retorna el valor de texto del elemento cuyo id recibe como argumento,
        sin el justificado. Esto permite comparar realmente los cambios
        ingresados con los valores existentes.

        :param tabla: La tabla en la cual buscar.
        :type tabla: Path
        :param id_entidad: El id del elemento.
        :type id_entidad: str
        :return: El valor de texto del elemento.
        :rtype: str
        """        
        res: str = ""
        # obtengo en la tabla su valor le quito el justificado y lo retorno
        with open(tabla, "r", newline="", encoding="utf-8") as archivo:
            registros = csv.DictReader(archivo, delimiter="§")
            for registro in registros:
                if registro["id"] == id_entidad:
                    if str(tabla).endswith("nodos.csv"):
                        res = self._gestor.eliminar_justificado(
                            registro["nodo"]
                        )
                        break
                    else:
                        res = self._gestor.eliminar_justificado(
                            registro["vertice"]
                        )
                        break
        return res


