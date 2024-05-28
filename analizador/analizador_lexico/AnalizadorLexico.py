import re
from .Token import Token

class AnalizadorLexico:
    def __init__(self):
        self.tokens = []

    def analizar_codigo(self, codigo):
        self.tokens = []
        posicion = 0
        linea = 1

        patrones = [
            # Número hexadecimal
            (r'0[xX][0-9a-fA-F]+', 'NUMERO_HEXADECIMAL'),
            # Número real
            (r'\d+\.\d*|\.\d+', 'NUMERO_REAL'),
            # Número natural
            (r'\d+', 'NUMERO_NATURAL'),
            # Palabras reservadas
            (r'\b(si|entonces|para|mientras|function|return)\b', 'PALABRA_RESERVADA'),
            # Operadores de incremento/decremento
            (r'(sumsum|menmen)', 'OPERADOR_INCREMENTO_DECREMENTO'),
            # Operadores de comparación
            (r'(same|dife|may|meno|menosame|maysame)', 'OPERADOR_COMPARACION'),
            # Operador de asignación
            (r'igual', 'OPERADOR_ASIGNACION'),
            # Operadores aritméticos
            (r'(sum|men|por|div)', 'OPERADOR_ARITMETICO'),
            # Operadores lógicos
            (r'(AND|OR)', 'OPERADOR_LOGICO'),
            # Palabra para excepciones
            (r'\b(intenta|atrapa|tirarExcepcion)\b', 'PALABRA_EXCEPCION'),
            # Palabra para enteros
            (r'\b(entr)\b\([\w\d]*\)', 'PALABRA_ENTERO'),
            # Palabra para reales
            (r'\b(panas)\b\([\w\d]*\)', 'PALABRA_REAL'),
            # Identificador
            (r'\b[a-zA-Z_]\w*\b', 'IDENTIFICADOR'),
            # Comentario de múltiples líneas
            (r'!\*[\s\S]*?\*!', 'COMENTARIO_EN_BLOQUE'),
            # Comentario de línea
            (r'!.*', 'COMENTARIO_LINEA'),
            # Paréntesis
            (r'(\(|\))', 'PARENTESIS'),
            # Llaves
            (r'(\{|})', 'LLAVES'),
            # Punto y coma
            (r';', 'TERMINAL'),
            # Coma
            (r',', 'SEPARADOR'),
            # Cadena de caracteres
            (r'"[^"]*"', 'CADENA_CARACTERES'),
            # Espacios en blanco
            (r'\s+', 'ESPACIO_EN_BLANCO'),
        ]

        while posicion < len(codigo):
            if codigo[posicion].isspace():
                if codigo[posicion] == '\n':
                    linea += 1
                lexema = codigo[posicion]
                self.tokens.append(Token(lexema, 'ESPACIO_EN_BLANCO', linea, posicion))
                posicion += 1
                continue

            match = None

            for patron, categoria in patrones:
                regex = re.compile(patron)
                match = regex.match(codigo, posicion)
                if match:
                    break

            if match:
                lexema = match.group(0)
                self.tokens.append(Token(lexema, categoria, linea, match.start()))
                posicion = match.end()
            else:
                error_posicion = codigo.find(' ', posicion)
                lexema = codigo[posicion:error_posicion] if error_posicion != -1 else codigo[posicion:]
                self.tokens.append(Token(lexema, 'TOKEN_NO_RECONOCIDO', linea, posicion))
                posicion += len(lexema)

        return self.tokens