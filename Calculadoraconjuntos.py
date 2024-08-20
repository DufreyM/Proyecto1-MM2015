import tkinter as tk
from tkinter import messagebox

class ConjuntosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Operaciones con Conjuntos")
        self.conjuntos = []

        # Configurar el menú principal
        self.label_menu = tk.Label(root, text="Menú Principal", font=('Helvetica', 16))
        self.label_menu.pack(pady=50)

        self.btn_construir = tk.Button(root, text="Construir Conjuntos", command=self.construir_conjuntos)
        self.btn_construir.pack(pady=5)

        self.btn_operar = tk.Button(root, text="Operar Conjuntos", command=self.operar_conjuntos)
        self.btn_operar.pack(pady=5)

        self.btn_finalizar = tk.Button(root, text="Finalizar", command=root.quit)
        self.btn_finalizar.pack(pady=5)

    def construir_conjuntos(self):
        self.construir_ventana = tk.Toplevel(self.root)
        self.construir_ventana.title("Construir Conjuntos")
        
        tk.Label(self.construir_ventana, text="Ingrese los elementos del conjunto (A-Z, 0-9) separados por comas:").pack(pady=10)
        self.entry_conjunto = tk.Entry(self.construir_ventana)
        self.entry_conjunto.pack(pady=5)
        
        tk.Button(self.construir_ventana, text="Agregar Conjunto", command=self.agregar_conjunto).pack(pady=10)
    
    def agregar_conjunto(self):
        conjunto = self.entry_conjunto.get().split(',')
        conjunto = {e.strip() for e in conjunto}  # Elimina espacios adicionales
        conjunto_valido = all(self.validar_entrada(e) for e in conjunto)
        if conjunto_valido:
            self.conjuntos.append(conjunto)
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

        tk.Label(self.operar_ventana, text="Seleccione los conjuntos a operar (haga click encima de los que quiera usar):").pack(pady=10)
        self.listbox_conjuntos = tk.Listbox(self.operar_ventana, selectmode=tk.MULTIPLE)
        for i, conjunto in enumerate(self.conjuntos):
            self.listbox_conjuntos.insert(tk.END, f"Conjunto {i+1}: {', '.join(conjunto)}")
        self.listbox_conjuntos.pack(pady=5)

        tk.Button(self.operar_ventana, text="Realizar Operación", command=self.realizar_operacion).pack(pady=10)
    
    def realizar_operacion(self):
        operacion = self.operacion.get()
        indices = self.listbox_conjuntos.curselection()
        seleccionados = [self.conjuntos[i] for i in indices]

        if not seleccionados:
            messagebox.showwarning("Advertencia", "Debe seleccionar al menos un conjunto para operar.")
            return

        resultado = seleccionados[0]  # Con esto indicamos que empezamos con el primer conjunto seleccionado

        for conjunto in seleccionados[1:]:
            if operacion == "Union":
                resultado = self.union(resultado, conjunto)
            elif operacion == "Interseccion":
                resultado = self.interseccion(resultado, conjunto)
            elif operacion == "Diferencia":
                resultado = self.diferencia(resultado, conjunto)
            elif operacion == "Diferencia Simetrica":
                resultado = self.diferencia_simetrica(resultado, conjunto)
            elif operacion == "Complemento":
                universo = set("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
                resultado = self.complemento(resultado, universo)
        
        messagebox.showinfo("Resultado", f"El resultado de {operacion} es: {', '.join(sorted(resultado))}")
        self.operar_ventana.destroy()

    def validar_entrada(self, elemento):
        return elemento.isalnum() and len(elemento) == 1

    # Métodos para las operaciones entre conjuntos
    def union(self, conjunto1, conjunto2):
        return conjunto1 | conjunto2

    def interseccion(self, conjunto1, conjunto2):
        return conjunto1 & conjunto2

    def diferencia(self, conjunto1, conjunto2):
        return conjunto1 - conjunto2

    def diferencia_simetrica(self, conjunto1, conjunto2):
        return conjunto1 ^ conjunto2

    def complemento(self, conjunto, universo):
        return universo - conjunto

# Ejecutar la aplicación
root = tk.Tk()
app = ConjuntosApp(root)
root.mainloop()
