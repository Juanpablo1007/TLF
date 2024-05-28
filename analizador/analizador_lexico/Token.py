class Token:
    def __init__(self, lexema, categoria, linea, posicion):
        self.lexema = lexema
        self.categoria = categoria
        self.linea = linea
        self.posicion = posicion