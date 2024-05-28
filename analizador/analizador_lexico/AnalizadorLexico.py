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
             ('NUMERO_NATURAL', self.es_numero_natural),
            ('NUMERO_HEXADECIMAL', self.es_numero_hexadecimal),
            ('NUMERO_REAL', self.es_numero_real),
            ('PALABRA_RESERVADA', self.es_palabra_reservada),
            ('OPERADOR_INCREMENTO_DECREMENTO', self.es_operador_incremento_decremento),
            ('OPERADOR_COMPARACION', self.es_operador_comparacion),
            ('OPERADOR_ASIGNACION', self.es_operador_asignacion),
            ('OPERADOR_ARITMETICO', self.es_operador_aritmetico),
            ('OPERADOR_LOGICO', self.es_operador_logico),
            ('PALABRA_EXCEPCION', self.es_palabra_excepcion),
            ('PALABRA_ENTERO', self.es_palabra_entero),
            ('PALABRA_REAL', self.es_palabra_real),
            ('IDENTIFICADOR', self.es_identificador),
            ('COMENTARIO_EN_BLOQUE', self.es_comentario_en_bloque),
            ('COMENTARIO_LINEA', self.es_comentario_linea),
            ('PARENTESIS', self.es_parentesis),
            ('LLAVES', self.es_llaves),
            ('TERMINAL', self.es_terminal),
            ('SEPARADOR', self.es_separador),
            ('CADENA_CARACTERES', self.es_cadena_caracteres),
            ('ESPACIO_EN_BLANCO', self.es_espacio_en_blanco),
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
            lexema = None

            for categoria, funcion in patrones:
                match, lexema = funcion(codigo, posicion)
                if match:
                    break

            if match:
                self.tokens.append(Token(lexema, categoria, linea, posicion))
                posicion += len(lexema)
            else:
                error_posicion = codigo.find(' ', posicion)
                lexema = codigo[posicion:error_posicion] if error_posicion != -1 else codigo[posicion:]
                self.tokens.append(Token(lexema, 'TOKEN_NO_RECONOCIDO', linea, posicion))
                posicion += len(lexema)

        return self.tokens
    
    def es_numero_natural(self, codigo, posicion):
        i = posicion
        while i < len(codigo) and codigo[i].isdigit():
            i += 1
        if i < len(codigo) and codigo[i] == '.':
            return False, None
        if i < len(codigo) and codigo[i].isalpha():
            return False, None

        return (i > posicion, codigo[posicion:i]) if i > posicion else (False, None)

    def es_numero_hexadecimal(self, codigo, posicion):
        if codigo[posicion:posicion + 2] in ('0x', '0X'):
            i = posicion + 2
            while i < len(codigo) and (codigo[i].isdigit() or codigo[i].lower() in 'abcdef'):
                i += 1
            return True, codigo[posicion:i] if i > posicion + 2 else (False, None)
        return False, None

    def es_numero_real(self, codigo, posicion):
        i = posicion
        # Primero, verifica si el caracter actual es un dígito.
        if codigo[i].isdigit():
            while i < len(codigo) and codigo[i].isdigit():
                i += 1
            # Si el siguiente caracter es un punto, continúa analizando los dígitos.
            if i < len(codigo) and codigo[i] == '.':
                i += 1
                while i < len(codigo) and codigo[i].isdigit():
                    i += 1
        # Si el caracter actual es un punto, verifica si el siguiente caracter es un dígito.
        elif codigo[i] == '.':
            i += 1
            if i < len(codigo) and codigo[i].isdigit():
                while i < len(codigo) and codigo[i].isdigit():
                    i += 1
            else:
                return False, None
        else:
            return False, None
        return True, codigo[posicion:i]

    

    def es_palabra_reservada(self, codigo, posicion):
        palabras = ['si', 'entonces', 'para', 'mientras', 'function', 'return']
        for palabra in palabras:
            if codigo.startswith(palabra, posicion) and not codigo[posicion + len(palabra)].isalnum():
                return True, palabra
        return False, None

    def es_operador_incremento_decremento(self, codigo, posicion):
        operadores = ['sumsum', 'menmen']
        for op in operadores:
            if codigo.startswith(op, posicion):
                return True, op
        return False, None

    def es_operador_comparacion(self, codigo, posicion):
        operadores = ['same', 'dife', 'may', 'meno', 'menosame', 'maysame']
        for op in operadores:
            if codigo.startswith(op, posicion):
                return True, op
        return False, None

    def es_operador_asignacion(self, codigo, posicion):
        if codigo.startswith('igual', posicion):
            return True, 'igual'
        return False, None

    def es_operador_aritmetico(self, codigo, posicion):
        operadores = ['sum', 'men', 'por', 'div']
        for op in operadores:
            if codigo.startswith(op, posicion):
                return True, op
        return False, None

    def es_operador_logico(self, codigo, posicion):
        operadores = ['AND', 'OR']
        for op in operadores:
            if codigo.startswith(op, posicion):
                return True, op
        return False, None

    def es_palabra_excepcion(self, codigo, posicion):
        palabras = ['intenta', 'atrapa', 'tirarExcepcion']
        for palabra in palabras:
            if codigo.startswith(palabra, posicion):
                return True, palabra
        return False, None

    def es_palabra_entero(self, codigo, posicion):
        if codigo.startswith('entr(', posicion):
            i = posicion + len('entr(')
            while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == '_'):
                i += 1
            if codigo[i] == ')':
                return True, codigo[posicion:i + 1]
        return False, None

    def es_palabra_real(self, codigo, posicion):
        if codigo.startswith('panas(', posicion):
            i = posicion + len('panas(')
            while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == '_'):
                i += 1
            if codigo[i] == ')':
                return True, codigo[posicion:i + 1]
        return False, None

    def es_identificador(self, codigo, posicion):
        if codigo[posicion].isalpha() or codigo[posicion] == '_':
            i = posicion
            while i < len(codigo) and (codigo[i].isalnum() or codigo[i] == '_'):
                i += 1
            return True, codigo[posicion:i]
        return False, None

    def es_comentario_en_bloque(self, codigo, posicion):
        if codigo.startswith('/*', posicion):
            i = posicion + 3  # Avanza el índice para que inicie después de /*! 
            while i < len(codigo) - 1:  # Se asegura de que haya al menos dos caracteres restantes
                if codigo[i:i + 2] == '*/':  # Verifica si se encuentra el final del comentario
                    return True, codigo[posicion:i + 2]  # Retorna el comentario completo
                i += 1
        # Si no se encuentra el final del comentario, se considera un error
            return False, None
        return False, None


    def es_comentario_linea(self, codigo, posicion):
        if codigo[posicion] == '!':
            i = posicion
            while i < len(codigo) and codigo[i] != '\n':
                i += 1
            return True, codigo[posicion:i]
        return False, None

    def es_parentesis(self, codigo, posicion):
        if codigo[posicion] in '()':
            return True, codigo[posicion]
        return False, None

    def es_llaves(self, codigo, posicion):
        if codigo[posicion] in '{}':
            return True, codigo[posicion]
        return False, None

    def es_terminal(self, codigo, posicion):
        if codigo[posicion] == ';':
            return True, codigo[posicion]
        return False, None

    def es_separador(self, codigo, posicion):
        if codigo[posicion] == ',':
            return True, codigo[posicion]
        return False, None

    def es_cadena_caracteres(self, codigo, posicion):
        if codigo[posicion] == '"':
            i = posicion + 1
            while i < len(codigo) and codigo[i] != '"':
                i += 1
            if i < len(codigo) and codigo[i] == '"':
                return True, codigo[posicion:i + 1]
        return False, None

    def es_espacio_en_blanco(self, codigo, posicion):
        if codigo[posicion].isspace():
            return True, codigo[posicion]
        return False, None