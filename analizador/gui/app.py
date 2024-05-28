import tkinter as tk
from tkinter import scrolledtext, ttk
from collections import defaultdict
from gui.Graficar import generar_automatas
from analizador_lexico.AnalizadorLexico import AnalizadorLexico

class App:

    def __init__(self, root):
        self.root = root
        root.title("My First")

        self.codigo_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=40, height=10)
        self.codigo_text.pack(pady=10)

        self.analizar_button = tk.Button(root, text="Analizar", command=self.analizar)
        self.analizar_button.pack()

        self.tabla_tokens = ttk.Treeview(root, columns=("lexema", "categoria", "posicion"))

        self.tabla_tokens.heading("#1", text="Lexema")
        self.tabla_tokens.heading("#2", text="Categoría")
        self.tabla_tokens.heading("#3", text="Posición")

        self.tabla_tokens.pack(pady=10)

        self.tabla_tokens.column("#1", stretch=tk.YES)
        self.tabla_tokens.column("#2", stretch=tk.YES)
        self.tabla_tokens.column("#3", stretch=tk.YES)

        for col in ("#1", "#2", "#3"):
            self.tabla_tokens.heading(col, anchor=tk.W)

    def analizar(self):
        codigo = self.codigo_text.get("1.0", "end-1c")

        analizador = AnalizadorLexico()

        tokens = analizador.analizar_codigo(codigo)

        self.mostrar_tokens(tokens)
        self.generar_automatas(tokens)

    def mostrar_tokens(self, tokens):
        for item in self.tabla_tokens.get_children():
            self.tabla_tokens.delete(item)

        for token in tokens:
            categoria = token.categoria
            if categoria == 'OPERADOR_INCREMENTO_DECREMENTO':
                categoria = 'OP. INCREMENTO/DECREMENTO'
            elif categoria == 'OPERADOR_COMPARACION':
                categoria = 'OP. COMPARACIÓN'
            elif categoria == 'OPERADOR_ASIGNACION':
                categoria = 'OP. ASIGNACIÓN'
            elif categoria == 'OPERADOR_ARITMETICO':
                categoria = 'OP. ARITMÉTICO'
            elif categoria == 'OPERADOR_LOGICO':
                categoria = 'OP. LÓGICO'
            elif categoria == 'PALABRA_EXCEPCION':
                categoria = 'PALABRA EXCEPCIÓN'
            elif categoria == 'PALABRA_ENTERO':
                categoria = 'PALABRA ENTERO'
            elif categoria == 'PALABRA_REAL':
                categoria = 'PALABRA REAL'
            elif categoria == 'ESPACIO_EN_BLANCO':
                categoria = 'ESPACIO'

            self.tabla_tokens.insert("", "end", values=(token.lexema, categoria, f"({token.linea}, {token.posicion})"))

    def agrupar_tokens_por_categoria(self, tokens):
        tokens_por_categoria = defaultdict(list)

        for token in tokens:
            tokens_por_categoria[token.categoria].append(token)

        return tokens_por_categoria
        
    def generar_automatas(self, tokens):
        tokens_por_categoria = self.agrupar_tokens_por_categoria(tokens)

        for categoria in tokens_por_categoria:
            generar_automatas(tokens_por_categoria[categoria], categoria)
        

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()