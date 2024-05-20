import tkinter as tk
from tkinter import scrolledtext, ttk
from analizador_lexico.AnalizadorLexico import AnalizadorLexico


# Clase principal de la interfaz
class App:

    def __init__(self, root):
        self.root = root
        root.title("My First")  # Título de la ventana

        # Área de texto para código fuente
        self.codigo_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.codigo_text.pack(pady=10)

        # Botón para ejecutar análisis
        self.analizar_button = tk.Button(root, text="Analizar", command=self.analizar)
        self.analizar_button.pack()

        # Tabla para mostrar tokens
        self.tabla_tokens = ttk.Treeview(root, columns=("lexema", "categoria", "posicion"))

        # Encabezados de columnas
        self.tabla_tokens.heading("#1", text="Lexema")
        self.tabla_tokens.heading("#2", text="Categoría")
        self.tabla_tokens.heading("#3", text="Posición")

        self.tabla_tokens.pack(pady=10)

        # Ajustar anchos de columna
        self.tabla_tokens.column("#1", stretch=tk.YES)
        self.tabla_tokens.column("#2", stretch=tk.YES)
        self.tabla_tokens.column("#3", stretch=tk.YES)

        # Ajustar encabezados al contenido
        for col in ("#1", "#2", "#3"):
            self.tabla_tokens.heading(col, anchor=tk.W)

    # Método para ejecutar análisis léxico
    def analizar(self):

        # Obtiene código fuente
        codigo = self.codigo_text.get("1.0", "end-1c")

        # Crea analizador léxico
        analizador = AnalizadorLexico()

        # Analiza y obtiene tokens
        tokens = analizador.analizar_codigo(codigo)

        # Muestra tokens en tabla
        self.mostrar_tokens(tokens)

    # Método para mostrar tokens en tabla
    def mostrar_tokens(self, tokens):

        # Limpia tabla
        for item in self.tabla_tokens.get_children():
            self.tabla_tokens.delete(item)

        # Inserta fila por token
        for token in tokens:
            self.tabla_tokens.insert("", "end", values=(token.lexema, token.categoria, f"({token.linea}, {token.posicion})"))


if __name__ == "__main__":

    # Crea ventana principal
    root = tk.Tk()

    # Crea objeto de la app
    app = App(root)

    # Bucle principal
    root.mainloop()

# Ejemplo código prueba
codigo_de_prueba = """
! Esto es un comentario de línea
if lexema == '\n':
    linea += 1
"""

'''
! Este es un comentario en línea 
!*
Este es un comentario en bloque
Puede incluir múltiples líneas.  
*!

print("Hola, mundo!")

!judfhsf'''

# Código para GUI con Tkinter que permite ingresar código, analizarlo léxicamente y mostrar tokens resultantes en tabla.