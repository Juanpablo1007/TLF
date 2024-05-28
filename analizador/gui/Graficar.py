from graphviz import Digraph

def generar_automatas(tokens, categoria):
    
    if categoria == 'NUMERO_NATURAL':
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')  # Nodo inicial

        for i, token in enumerate(tokens):
            numero = token.lexema

            # Agregar nodo para el token
            dot.node('q'+str(i), 'q'+str(i))

            # Agregar transiciones
            dot.edge('start', 'q'+str(i))  # Desde el nodo inicial al nodo del token
            if len(numero) > 1:
                dot.edge('q'+str(i), 'q'+str(i), label=','.join(numero[:-1]))  # Desde el nodo del token a sí mismo
            dot.edge('q'+str(i), 'q'+str(len(tokens)), label=numero[-1])  # Desde el nodo del token al nodo final

        # Nodo final
        dot.node('q'+str(len(tokens)), 'q'+str(len(tokens)), shape='doublecircle')

        # Renderizar el gráfico
        dot.render('Automata_Numeros_Naturales', view=False)
    
    elif categoria == 'COMENTARIO_LINEA':
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')  # Nodo inicial

        dot.node('q1', 'q1')
        dot.node('q2', 'q2')
        dot.node('q3', 'q3',shape='doublecircle')

        # Agregar transiciones
        dot.edge('start', 'q1')
        dot.edge('q1', 'q2', label='!')
        dot.edge('q2', 'q2', label='C.O.S')
        dot.edge('q2', 'q3', label='C.O.S')

        # Agregar texto adicional
        dot.attr(label='Cantidad de comentarios de línea en el código = {}'.format(len(tokens)))

        # Renderizar el gráfico
        dot.render('Automata_Comentarios_Linea', view=False)
        
    elif categoria == 'COMENTARIO_EN_BLOQUE':
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')  # Nodo inicial

        dot.node('q1', 'q1')
        dot.node('q2', 'q2')
        dot.node('q3', 'q3')
        dot.node('q4', 'q4',shape='doublecircle')

        # Agregar transiciones
        dot.edge('start', 'q1')
        dot.edge('q1', 'q2', label='!*')
        dot.edge('q2', 'q2', label='C.O.S')
        dot.edge('q2', 'q3', label='C.O.S')
        dot.edge('q3', 'q4', label='*!')

        # Agregar texto adicional
        dot.attr(label='Cantidad de comentarios de bloque en el código = {}'.format(len(tokens)))

        # Renderizar el gráfico
        dot.render('Automata_Comentarios_Bloque', view=False)
        
    elif categoria == 'NUMERO_HEXADECIMAL':
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')  # Nodo inicial
        dot.node('q0', 'q0')
        dot.node('q1', 'q1')
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='0')
        
        for i, token in enumerate(tokens, 2):
            numero = token.lexema

            # Agregar nodo para el token
            dot.node('q'+str(i), 'q'+str(i))

            # Agregar transiciones
            dot.edge('q1', 'q'+str(i), label='x')  # Desde el nodo inicial al nodo del token
            if len(numero) > 1:
                dot.edge('q'+str(i), 'q'+str(i), label=','.join(numero[2:-1]))  # Desde el nodo del token a sí mismo
            dot.edge('q'+str(i), 'q'+str(len(tokens)+2), label=numero[-1])  # Desde el nodo del token al nodo final

        # Nodo final
        dot.node('q'+str(len(tokens)+2), 'q'+str(len(tokens)+2), shape='doublecircle')

        # Renderizar el gráfico
        dot.render('Automata_Numeros_Hexadecimales', view=False)
        
    elif categoria == 'NUMERO_REAL':
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')  # Nodo inicial
        dot.node("q0", "q0")
        dot.edge('start', 'q0')

        i = 0
        j = 1
        final_node = 'qf'  # Nodo final único

        while i < len(tokens):
            token = tokens[i]
            numero = token.lexema

            dot.node('q'+str(j), 'q'+str(j))
            
            if numero[0] == '.':  # Si el número empieza con un punto
                # Agregar transiciones
                dot.edge('q0', 'q'+str(j), label='.')  # Desde el nodo inicial al nodo del token

                if len(numero) > 2:
                    dot.edge('q'+str(j), 'q'+str(j), label=','.join(numero[1:-1]))  # Desde el nodo del token a sí mismo
                dot.edge('q'+str(j), final_node, label=numero[-1])  # Desde el nodo del token al nodo final
                j += 1
                
            else:
                # Agregar transiciones
                partes = numero.split('.')
                parte_entera = partes[0]
                parte_decimal = partes[1]
                dot.edge('q0', 'q'+str(j), label=numero[0])
                if len(parte_entera) > 1:
                    dot.edge('q'+str(j), 'q'+str(j), label=','.join(parte_entera[1:]))
                dot.node('q'+str(j+1), 'q'+str(j+1))
                dot.edge('q'+str(j), 'q'+str(j+1), label='.')
                if len(parte_decimal) > 1:
                    dot.edge('q'+str(j+1), 'q'+str(j+1), label=','.join(parte_decimal[:-1]))
                dot.edge('q'+str(j+1), final_node, label=numero[-1])  # Desde el nodo del token al nodo final
                j += 2

            i += 1

        # Nodo final
        dot.node(final_node, final_node, shape='doublecircle')

        # Renderizar el gráfico
        dot.render('Automata_Numeros_Reales', view=False)
        
    elif categoria == 'PALABRA_RESERVADA':
        
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')  # Nodo inicial
        dot.node("q0", "q0")
        dot.node("q1", "q1", shape='doublecircle')
        dot.edge('start', 'q0')
        
        palabras_procesadas = set()

        # Crear un diccionario para contar las ocurrencias de cada palabra reservada
        palabras_reservadas = {"si": 0, "entonces": 0, "para": 0, "mientras": 0, "function": 0, "return": 0}
        
        for i, token in enumerate(tokens, 1):
            palabra = token.lexema

            # Solo procesar la palabra si no ha sido procesada antes
            if palabra not in palabras_procesadas:
                dot.edge('q0', 'q1', label=palabra)
                palabras_procesadas.add(palabra)  # Agregar la palabra al conjunto de palabras procesadas
                
            
            # Incrementar el contador de la palabra reservada
            palabras_reservadas[palabra] += 1
        
        
        # Crear una lista para almacenar las etiquetas
        etiquetas = []

        for palabra, cantidad in palabras_reservadas.items():
            if cantidad > 0:  # Solo crear la etiqueta si la palabra reservada está presente
                etiquetas.append('Cantidad de {} en el codigo = {}'.format(palabra, cantidad))

        # Unir todas las etiquetas en una cadena, separadas por '\n' para que aparezcan en líneas separadas
        etiquetas_str = '\n'.join(etiquetas)

        # Establecer la cadena de etiquetas como la etiqueta del gráfico
        dot.attr(label=etiquetas_str)

        # Renderizar el gráfico
        dot.render('Automata_Palabras_Reservadas', view=False)
        
    elif categoria == 'IDENTIFICADOR':
            
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')
    
        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')

        for i, token in enumerate(tokens):
            identificador = token.lexema

            # Agregar nodo para el token
            dot.node('q'+str(i), 'q'+str(i))

            # Agregar transiciones
            dot.edge('start', 'q'+str(i))  # Desde el nodo inicial al nodo del token
            if len(identificador) > 1:
                dot.edge('q'+str(i), 'q'+str(i), label=','.join(identificador[:-1]))  # Desde el nodo del token a sí mismo
            dot.edge('q'+str(i), 'q'+str(len(tokens)), label=identificador[-1])  # Desde el nodo del token al nodo final

        # Nodo final
        dot.node('q'+str(len(tokens)), 'q'+str(len(tokens)), shape='doublecircle')

        # Renderizar el gráfico
        dot.render('Automata_Identificadores', view=False)
        
    
    elif categoria == 'OPERADOR_INCREMENTO_DECREMENTO':
        
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')  # Nodo inicial

        dot.node('q0', 'q0')
        dot.node('q1', 'q1')
        dot.node('q2', 'q2',shape='doublecircle')

        # Agregar transiciones
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='sum')
        dot.edge('q1', 'q2', label='sum')

        dot.edge('q0', 'q1', label='men')
        dot.edge('q1', 'q2', label='men')
        
        # Agregar texto adicional
        dot.attr(label='Cantidad de incrementos/decrementos en el codigo = {}'.format(len(tokens)))

        # Renderizar el gráfico
        dot.render('Automata_Incrementos_Decrementos', view=False)
        
    elif categoria == 'OPERADOR_COMPARACION':
        
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')  # Nodo inicial

        dot.node('q0', 'q0')
        dot.node('q1', 'q1',shape='doublecircle')

        # Agregar transiciones
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='same')
        dot.edge('q0', 'q1', label='dife')
        dot.edge('q0', 'q1', label='may')
        dot.edge('q0', 'q1', label='meno')
        dot.edge('q0', 'q1', label='menosame')
        dot.edge('q0', 'q1', label='maysame')
        
        
        # Agregar texto adicional
        dot.attr(label='Cantidad de same/dife/may/meno/menosame/maysame en el codigo = {}'.format(len(tokens)))

        # Renderizar el gráfico
        dot.render('Automata_Operadores_Comparacion', view=False)
        
    elif categoria == 'OPERADOR_ASIGNACION':
        
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')  # Nodo inicial

        dot.node('q0', 'q0')
        dot.node('q1', 'q1',shape='doublecircle')

        # Agregar transiciones
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='igual')

        
        
        # Agregar texto adicional
        dot.attr(label='Cantidad de igual en el codigo = {}'.format(len(tokens)))

        # Renderizar el gráfico
        dot.render('Automata_Operadores_Comparacion', view=False)
        
    elif categoria == 'OPERADOR_ARITMETICO':
        
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')
        
        dot.node('q0', 'q0')
        dot.node('q1', 'q1', shape='doublecircle')
        
        # Agregar transiciones
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='sum')
        dot.edge('q0', 'q1', label='men')
        dot.edge('q0', 'q1', label='por')
        dot.edge('q0', 'q1', label='div')
        
        # Agregar texto adicional
        dot.attr(label='Cantidad de sum/men/por/div en el codigo = {}'.format(len(tokens)))
        
        # Renderizar el gráfico
        dot.render('Automata_Operadores_Aritmeticos', view=False)
        
    elif categoria == 'OPERADOR_LOGICO':
        
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')
        
        dot.node('q0', 'q0')
        dot.node('q1', 'q1', shape='doublecircle')
        
        # Agregar transiciones
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='AND')
        dot.edge('q0', 'q1', label='OR')
        
        # Agregar texto adicional
        dot.attr(label='Cantidad de AND/OR en el codigo = {}'.format(len(tokens)))
        
        # Renderizar el gráfico
        dot.render('Automata_Operadores_Logicos', view=False)
        
    elif categoria == 'PARENTESIS':
        
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')
        
        dot.node('q0', 'q0')
        dot.node('q1', 'q1')
        dot.node('q2', 'q2', shape='doublecircle')
        
        # Agregar transiciones
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='(')
        dot.edge('q1', 'q1', label='C.O.S')
        dot.edge('q1', 'q2', label=')')
        
        # Agregar texto adicional
        dot.attr(label='Cantidad de parentesis en el codigo = {}'.format(len(tokens)))
        
        # Renderizar el gráfico
        dot.render('Automata_Parentesis', view=False)
        
    elif categoria == 'LLAVES':
        
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')
        
        dot.node('q0', 'q0')
        dot.node('q1', 'q1')
        dot.node('q2', 'q2', shape='doublecircle')
        
        # Agregar transiciones
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='{')
        dot.edge('q1', 'q1', label='C.O.S')
        dot.edge('q1', 'q2', label='}')
        
        # Agregar texto adicional
        dot.attr(label='Cantidad de llaves en el codigo = {}'.format(len(tokens)))
        
        # Renderizar el gráfico
        dot.render('Automata_Llaves', view=False)
        
    elif categoria == 'TERMINAL':
        
        dot = Digraph()
        dot.attr('node', shape='circle')
        
        #Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')
        
        dot.node('q0', 'q0')
        dot.node('q1', 'q1')
        dot.node('q2', 'q2', shape='doublecircle')
        
        #Agregar transiciones
        
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='C.O.S')
        dot.edge('q1', 'q2', label=';')
        dot.edge('q1', 'q1', label='C.O.S')
        
        #Agregar texto adicional
        dot.attr(label='Cantidad de ; en el codigo = {}'.format(len(tokens)))
        
        #Renderizar el grafico
        dot.render('Automata_Terminal', view=False)
        
    elif categoria == 'SEPARADOR':
        
        dot = Digraph()
        dot.attr('node', shape='circle')
        
        #Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')
        
        dot.node('q0', 'q0')
        dot.node('q1', 'q1')
        dot.node('q2', 'q2', shape='doublecircle')
        
        #Agregar transiciones
        
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='C.O.S')
        dot.edge('q1', 'q2', label=',')
        dot.edge('q1', 'q1', label='C.O.S')
        
        #Agregar texto adicional
        dot.attr(label='Cantidad de , en el codigo = {}'.format(len(tokens)))
        
        #Renderizar el grafico
        dot.render('Automata_Separador', view=False)
        
    elif categoria == 'CADENA_CARACTERES':
        
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')
        
        dot.node('q0', 'q0')
        dot.node('qf', 'qf', shape='doublecircle')
        
        # Agregar transiciones
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='"')
        
        for i, token in enumerate(tokens, 1):
            cadena = token.lexema

            # Agregar nodo para el token
            dot.node('q'+str(i), 'q'+str(i))

            if len(cadena) > 3:
                dot.edge('q'+str(i), 'q'+str(i), label=','.join(cadena[1:-2]))  # Desde el nodo del token a sí mismo
            dot.edge('q'+str(i), 'q'+str(len(tokens)+1), label=cadena[-2])  # Desde el nodo del token al nodo final

        dot.node('q'+str(len(tokens)+1), 'q'+str(len(tokens)+1))
        dot.edge('q'+str(len(tokens)+1), 'qf', label='"')
        
        # Renderizar el gráfico
        dot.render('Automata_Cadena_Caracteres', view=False)
        
    elif categoria == 'PALABRA_EXCEPCION':
        
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')
        
        dot.node('q0', 'q0')
        dot.node('q1', 'q1', shape='doublecircle')
        
        # Agregar transiciones
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='intenta')
        dot.edge('q0', 'q1', label='atrapa')
        dot.edge('q0', 'q1', label='tirarExcepcion')
        
        # Agregar texto adicional
        dot.attr(label='Cantidad de palabras de excepcion en el codigo = {}'.format(len(tokens)))
        
        # Renderizar el gráfico
        dot.render('Automata_Excepciones', view=False)
        
    elif categoria == 'PALABRA_ENTERO':
        
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')
        
        dot.node('q0', 'q0')
        dot.node('q1', 'q1')
        dot.node('q2', 'q2')
        dot.node('q3', 'q3', shape='doublecircle')
        
        # Agregar transiciones
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='entr') 
        dot.edge('q1', 'q2', label='(')
        dot.edge('q2', 'q2', label='C.O.S')
        dot.edge('q2', 'q3', label=')')
        
        # Agregar texto adicional
        dot.attr(label='Cantidad de palabras de entero en el codigo = {}'.format(len(tokens)))
        
        # Renderizar el gráfico
        dot.render('Automata_Palabras_Entero', view=False)
        
    elif categoria == 'PALABRA_REAL':
        
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')
        
        dot.node('q0', 'q0')
        dot.node('q1', 'q1')
        dot.node('q2', 'q2')
        dot.node('q3', 'q3', shape='doublecircle')
        
        # Agregar transiciones
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='panas') 
        dot.edge('q1', 'q2', label='(')
        dot.edge('q2', 'q2', label='C.O.S')
        dot.edge('q2', 'q3', label=')')
        
        # Agregar texto adicional
        dot.attr(label='Cantidad de palabras de real en el codigo = {}'.format(len(tokens)))
        
        # Renderizar el gráfico
        dot.render('Automata_Palabras_Real', view=False)
        
    elif categoria == 'ESPACIO_EN_BLANCO':
        
        # Crear un objeto Digraph
        dot = Digraph()
        dot.attr('node', shape='circle')

        # Agregar nodos
        dot.node('start', '', shape='circle', color='black', fillcolor='black', style='filled', width='0.1')
        
        dot.node('q0', 'q0')
        dot.node('q1', 'q1', shape='doublecircle')
        
        # Agregar transiciones
        dot.edge('start', 'q0')
        dot.edge('q0', 'q1', label='\\nlinea') 
        dot.edge('q0', 'q1', label='\\tlinea')
        dot.edge('q1', 'q1', label='C.O.S, \\nlinea, \\tlinea')
        
        # Agregar texto adicional
        dot.attr(label='Cantidad de espacios en blanco en el codigo = {}'.format(len(tokens)))
        
        # Renderizar el gráfico
        dot.render('Automata_Espacios_Blanco', view=False)
        
    else:
        print('Categoria no reconocida')
        return None
        
        
        
        
        
        

        