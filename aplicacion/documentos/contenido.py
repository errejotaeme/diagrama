import fitz  # type: ignore
import re


class Extractor:
    """
    Clase encargada de obtener el texto contenido en un pdf o un txt.
    """
    
    def __init__(self):
        """
        Constructor de la clase Extractor.
        """
        pass
    
    def extraer_contenido(self, ruta: str) -> str:
        """
        Obtiene el texto completo del archivo que recibe como argumento.
        Si no lo obtiene retorna -1.

        :param ruta: Ubicación del archivo.
        :type ruta: str
        :return: El texto contenido en el archivo o -1. 
        :rtype: str
        """
        if ruta.endswith(".pdf"):            
            try:
                with fitz.open(ruta) as pdf:
                    contenido:str = chr(12).join(
                        [pagina.get_text() for pagina in pdf]
                    ) 
                    contenido = self.ordenar_contenido(contenido)
                    return contenido
            except:
                return "-1" 
        elif ruta.endswith(".txt"):
            try:
                with open(ruta,"r") as txt:
                    contenido = "\n".join([linea for linea in txt.readlines()])
                    return contenido
            except:
                return "-1"
        else:  # Extensión no soportada
            return "-1"

    def ordenar_contenido(self, contenido: str) -> str:
        """
        Convierte las líneas extraídas en oraciones.

        :param contenido: El texto del PDF.
        :type ruta_pdf: str
        :return: Las líneas del PDF concatenadas en oraciones.
        :rtype: str
        """
        # Patrones de expresiones regulares
        p1, p2, p3 = "-" + r"\n", r",\n", r";\n"
        # Uno las líneas con palabras cortadas
        lista_aux: list[str] = re.split(p1, contenido)
        contenido = "".join([cadena for cadena in lista_aux])
        # Uno las líneas que terminan en coma
        lista_aux = re.split(p2, contenido)
        contenido = ", ".join([cadena for cadena in lista_aux])
        # Uno las líneas que terminan en punto y coma
        lista_aux = re.split(p3, contenido)
        contenido = "; ".join([cadena.strip() for cadena in lista_aux])

        # Uno las líneas restantes        
        try:
            lista_aux = re.split(r"\n", contenido)
            lista_aux_2: list[str] = []
            i: int = 1
            while i < len(lista_aux):
                # Líneas con caracteres en mayúsculas (posibles títulos)
                if lista_aux[i-1].isupper() and lista_aux[i][0].isupper(): 
                    lista_aux_2.append(lista_aux[i-1] + "\n" + lista_aux[i])
                    i = i+2
                # Líneas que no terminan en punto y aparte    
                elif lista_aux[i-1][-1] != ".": 
                    lista_aux_2.append(lista_aux[i-1] + " " + lista_aux[i])
                    i = i+2
                # Resto de las líneas    
                else:
                    lista_aux_2.append(lista_aux[i-1] + "\n\n" + lista_aux[i])
                    i = i+2                  
            # Agrega el último item si corresponde
            if len(lista_aux) % 2 != 0:
                lista_aux_2.append(lista_aux[-1])
            # Une el texto
            contenido = " ".join([cadena for cadena in lista_aux_2])
        except:
            pass
        # Agrega un indicador al final de cada paǵina extraída
        c_aux:str = "\n\n"+ chr(32)*13 + "----[FIN DE PÁGINA]----\n\n"
        contenido = contenido.replace(chr(12), c_aux)
        # Elimino del texto extraído el caracter reservado
        # para delimitar las tablas
        contenido = contenido.replace(chr(167), "")        
        return contenido       
        

