# UNIVERSIDAD DEL VALLE DE GUATEMALA
# Matemática Discreta
# Descripción: programa que permite crear conjuntos y realizar operaciones con ellos 
# (complemento, union, intersección, diferencia, diferencia simétrica)
# Autores: Leonardo Dufrey Mejía Mejía, Maria José Girón Isidro
# Fecha de creación:  17 de Agosto de 2024
# Fecha de última modificación: 

import tkinter as tk
from tkinter import messagebox

class ConjuntosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Operaciones con Conjuntos")
        self.conjuntos = []

        # Configurar el menú principal
        self.label_menu = tk.Label(root, text="Menú Principal", font=('Helvetica', 16))
        self.label_menu.pack(pady=150)

        self.btn_construir = tk.Button(root, text="Construir Conjuntos", command=self.construir_conjuntos)
        self.btn_construir.pack(pady=50)

        self.btn_operar = tk.Button(root, text="Operar Conjuntos", command=self.operar_conjuntos)
        self.btn_operar.pack(pady=50)

        self.btn_finalizar = tk.Button(root, text="Finalizar", command=root.quit)
        self.btn_finalizar.pack(pady=50)

    def construir_conjuntos(self):
        self.construir_ventana = tk.Toplevel(self.root)
        self.construir_ventana.title("Construir Conjuntos")
        
        tk.Label(self.construir_ventana, text="Ingrese los elementos del conjunto (A-Z, 0-9):").pack(pady=10)
        self.entry_conjunto = tk.Entry(self.construir_ventana)
        self.entry_conjunto.pack(pady=5)
        
        tk.Button(self.construir_ventana, text="Agregar Conjunto", command=self.agregar_conjunto).pack(pady=10)
    
    def agregar_conjunto(self):
        conjunto = self.entry_conjunto.get().split(',')
        conjunto_valido = all(self.validar_entrada(e) for e in conjunto)
        if conjunto_valido:
            self.conjuntos.append(set(conjunto))
            messagebox.showinfo("Éxito", "Conjunto agregado exitosamente.")
            self.construir_ventana.destroy()
        else:
            messagebox.showerror("Error", "Uno o más elementos no son válidos.")

    def operar_conjuntos(self):
        if len(self.conjuntos) < 2:
            messagebox.showwarning("Advertencia", "Debe crear al menos dos conjuntos primero.")
            return
        
        self.operar_ventana = tk.Toplevel(self.root)
        self.operar_ventana.title("Operar Conjuntos")

        tk.Label(self.operar_ventana, text="Seleccione la operación:").pack(pady=10)
        self.operacion = tk.StringVar()
        tk.Radiobutton(self.operar_ventana, text="Complemento", variable=self.operacion, value="Complemento").pack()
        tk.Radiobutton(self.operar_ventana, text="Unión", variable=self.operacion, value="Union").pack()
        tk.Radiobutton(self.operar_ventana, text="Intersección", variable=self.operacion, value="Interseccion").pack()
        tk.Radiobutton(self.operar_ventana, text="Diferencia", variable=self.operacion, value="Diferencia").pack()
        tk.Radiobutton(self.operar_ventana, text="Diferencia Simétrica", variable=self.operacion, value="Diferencia Simetrica").pack()

        tk.Button(self.operar_ventana, text="Realizar Operación", command=self.realizar_operacion).pack(pady=10)
    
    def realizar_operacion(self):
        operacion = self.operacion.get()
        conjunto_1 = self.conjuntos[0]
        conjunto_2 = self.conjuntos[1]

        resultado = set()

        if operacion == "Complemento":
            universo = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
            resultado = universo - conjunto_1
        elif operacion == "Union":
            resultado = conjunto_1 | conjunto_2
        elif operacion == "Interseccion":
            resultado = conjunto_1 & conjunto_2
        elif operacion == "Diferencia":
            resultado = conjunto_1 - conjunto_2
        elif operacion == "Diferencia Simetrica":
            resultado = conjunto_1 ^ conjunto_2
        
        messagebox.showinfo("Resultado", f"El resultado de {operacion} es: {resultado}")
        self.operar_ventana.destroy()

    def validar_entrada(self, elemento):
        return elemento.isalnum() and len(elemento) == 1

# Ejecutar la aplicación
root = tk.Tk()
app = ConjuntosApp(root)
root.mainloop()
