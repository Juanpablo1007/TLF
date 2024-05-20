import tkinter as tk
from tkinter import ttk
from analizador_lexico.AnalizadorLexico import AnalizadorLexico



class Interface:
    """
    Clase que representa la interfaz gráfica del analizador léxico.
    """
    
    def __init__(self, master):
        self.master = master
        master.title("Analizador Lexico - MyFirst")

        self.analizador = AnalizadorLexico()

        self.create_ui()

    def create_ui(self):
        """
        Crea la interfaz de usuario.
        """
        # Crear la sección de entrada
        self.create_input_section()
        # Crear la sección de resultados
        self.create_results_section()
        # Crear los botones
        self.create_buttons()

    def create_input_section(self):
        """
        Crea la sección de entrada de código.
        """
        # Crear un marco para la sección de entrada
        input_frame = ttk.LabelFrame(self.master, text="Entrada")
        input_frame.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # Crear un campo de texto para el código de entrada
        self.codigo_text = tk.Text(input_frame, width=40, height=10)
        self.codigo_text.grid(row=0, column=0, padx=10, pady=5)

    def create_results_section(self):
        """
        Crea la sección de resultados.
        """
        # Crear un marco para la sección de resultados
        results_frame = ttk.LabelFrame(self.master, text="Resultados")
        results_frame.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        # Crear un campo de texto para mostrar los resultados
        self.resultados_text = tk.Text(results_frame, width=40, height=10)
        self.resultados_text.grid(row=0, column=0, padx=10, pady=5)

    def create_buttons(self):
        """
        Crea los botones de la interfaz.
        """
        # Crear un marco para los botones
        button_frame = ttk.Frame(self.master)
        button_frame.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        # Crear un botón para analizar el código
        self.analizar_button = ttk.Button(button_frame, text="Analizar", command=self.analizar)
        self.analizar_button.grid(row=0, column=0, padx=5)

        # Crear un botón para borrar los resultados
        self.borrar_button = ttk.Button(button_frame, text="Borrar Resultados", command=self.borrar_resultados)
        self.borrar_button.grid(row=0, column=1, padx=5)

    def analizar(self):
        """
        Analiza el código de entrada y muestra los resultados.
        """
        # Obtener el código de entrada del campo de texto
        codigo = self.codigo_text.get("1.0", "end-1c")
        # Analizar el código utilizando el analizador léxico
        tokens = self.analizador.analizar_codigo(codigo)
        # Mostrar los resultados en el campo de texto de resultados
        self.mostrar_resultados(tokens)

    def borrar_resultados(self):
        """
        Borra los resultados mostrados en el campo de texto.
        """
        # Borrar el contenido del campo de texto de resultados
        self.resultados_text.delete("1.0", "end")

    def mostrar_resultados(self, tokens):
        """
        Muestra los resultados en el campo de texto de resultados.
        """
        # Borrar el contenido actual del campo de texto de resultados
        self.resultados_text.delete("1.0", "end")
        # Mostrar cada token en el campo de texto de resultados
        for token in tokens:
            self.resultados_text.insert("end", f'Lexema: {token.lexema}, Categoría: {token.categoria}, '
                                               f'Posición: ({token.linea}, {token.posicion})\n')
