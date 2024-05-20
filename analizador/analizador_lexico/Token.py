
class Token:
    def __init__(self, lexema, categoria, linea, posicion):
        """
        Clase que representa un token en el analizador léxico.

        Args:
            lexema (str): El lexema del token.
            categoria (str): La categoría del token.
            linea (int): El número de línea donde se encuentra el token.
            posicion (int): La posición del token dentro de la línea.

        Attributes:
            lexema (str): El lexema del token.
            categoria (str): La categoría del token.
            linea (int): El número de línea donde se encuentra el token.
            posicion (int): La posición del token dentro de la línea.
        """
        self.lexema = lexema
        self.categoria = categoria
        self.linea = linea
        self.posicion = posicion









        