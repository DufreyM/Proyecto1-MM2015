import tkinter as tk
from tkinter import messagebox

class ConjuntosApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Operaciones con Conjuntos")
        self.conjuntos = []
        self.seleccionados = []

        # Configurar el menú principal
        self.label_menu = tk.Label(root, text="Menú Principal", font=('Helvetica', 16))
        self.label_menu.pack(pady=50)

        self.btn_construir = tk.Button(root, text="Construir Conjuntos", command=self.construir_conjuntos)
        self.btn_construir.pack(pady=5)

        self.btn_operar = tk.Button(root, text="Operar Conjuntos", command=self.operar_conjuntos)
        self.btn_operar.pack(pady=5)
        
        self.btn_editar = tk.Button(root, text="Editar Conjuntos", command=self.editar_conjuntos)
        self.btn_editar.pack(pady=5)

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
        conjunto = [e.strip() for e in conjunto]  # Elimina espacios adicionales
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
        self.listbox_conjuntos = tk.Listbox(self.operar_ventana, selectmode=tk.SINGLE)
        self.listbox_conjuntos.bind('<<ListboxSelect>>', self.agregar_a_seleccionados)
        for i, conjunto in enumerate(self.conjuntos):
            self.listbox_conjuntos.insert(tk.END, f"Conjunto {i+1}: {', '.join(conjunto)}")
        self.listbox_conjuntos.pack(pady=5)

        tk.Button(self.operar_ventana, text="Realizar Operación", command=self.realizar_operacion).pack(pady=10)
    
    def agregar_a_seleccionados(self, event):
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = selection[0]
            self.seleccionados.append(self.conjuntos[index])

    def realizar_operacion(self):
        operacion = self.operacion.get()
        if len(self.seleccionados) < 2:
            messagebox.showwarning("Advertencia", "Debe seleccionar al menos dos conjuntos para operar.")
            return

        resultado = self.seleccionados[0]  # Empezamos con el primer conjunto seleccionado

        for conjunto in self.seleccionados[1:]:
            if operacion == "Union":
                resultado = self.union(resultado, conjunto)
            elif operacion == "Interseccion":
                resultado = self.interseccion(resultado, conjunto)
            elif operacion == "Diferencia":
                resultado = self.diferencia(resultado, conjunto)  # Resta del conjunto actual
            elif operacion == "Diferencia Simetrica":
                resultado = self.diferencia_simetrica(resultado, conjunto)
            elif operacion == "Complemento":
                universo = [chr(i) for i in range(ord('A'), ord('Z')+1)] + [str(i) for i in range(0, 10)]
                resultado = self.complemento(resultado, universo)

        messagebox.showinfo("Resultado", f"El resultado de {operacion} es: {', '.join(sorted(resultado))}")
        
        # Limpiar los conjuntos seleccionados después de la operación
        self.seleccionados.clear()
        self.operar_ventana.destroy()

    def editar_conjuntos(self):
        if len(self.conjuntos) == 0:
            messagebox.showwarning("Advertencia", "No hay conjuntos disponibles para editar.")
            return
        
        self.editar_ventana = tk.Toplevel(self.root)
        self.editar_ventana.title("Editar Conjuntos")

        tk.Label(self.editar_ventana, text="Seleccione el conjunto a editar:").pack(pady=10)
        self.listbox_editar = tk.Listbox(self.editar_ventana)
        for i, conjunto in enumerate(self.conjuntos):
            self.listbox_editar.insert(tk.END, f"Conjunto {i+1}: {', '.join(conjunto)}")
        self.listbox_editar.pack(pady=5)

        tk.Button(self.editar_ventana, text="Editar", command=self.seleccionar_conjunto_para_editar).pack(pady=10)
    
    def seleccionar_conjunto_para_editar(self):
        selection = self.listbox_editar.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Debe seleccionar un conjunto para editar.")
            return
        
        index = selection[0]
        self.conjunto_a_editar = index
        conjunto = self.conjuntos[index]
        
        # Abrir ventana de edición
        self.ventana_edicion = tk.Toplevel(self.root)
        self.ventana_edicion.title(f"Editar Conjunto {index+1}")

        tk.Label(self.ventana_edicion, text=f"Editando Conjunto {index+1}:").pack(pady=10)
        self.entry_editar = tk.Entry(self.ventana_edicion)
        self.entry_editar.insert(0, ', '.join(conjunto))
        self.entry_editar.pack(pady=5)

        tk.Button(self.ventana_edicion, text="Guardar Cambios", command=self.guardar_cambios).pack(pady=10)

    def guardar_cambios(self):
        conjunto_editado = self.entry_editar.get().split(',')
        conjunto_editado = [e.strip() for e in conjunto_editado]  # Elimina espacios adicionales
        conjunto_valido = all(self.validar_entrada(e) for e in conjunto_editado)
        if conjunto_valido:
            self.conjuntos[self.conjunto_a_editar] = conjunto_editado
            messagebox.showinfo("Éxito", "Conjunto editado exitosamente.")
            self.ventana_edicion.destroy()
            self.editar_ventana.destroy()
        else:
            messagebox.showerror("Error", "Uno o más elementos no son válidos.")

    def validar_entrada(self, elemento):
        return elemento.isalnum() and len(elemento) == 1

    # Métodos para las operaciones entre conjuntos sin usar 'set'
    def union(self, conjunto1, conjunto2):
        resultado = conjunto1[:]
        for elemento in conjunto2:
            if elemento not in resultado:
                resultado.append(elemento)
        return resultado

    def interseccion(self, conjunto1, conjunto2):
        resultado = []
        for elemento in conjunto1:
            if elemento in conjunto2 and elemento not in resultado:
                resultado.append(elemento)
        return resultado

    def diferencia(self, conjunto1, conjunto2):
        resultado = []
        for elemento in conjunto1:
            if elemento not in conjunto2:
                resultado.append(elemento)
        return resultado

    def diferencia_simetrica(self, conjunto1, conjunto2):
        resultado = []
        for elemento in conjunto1:
            if elemento not in conjunto2:
                resultado.append(elemento)
        for elemento in conjunto2:
            if elemento not in conjunto1:
                resultado.append(elemento)
        return resultado

    def complemento(self, conjunto, universo):
        resultado = []
        for elemento in universo:
            if elemento not in conjunto:
                resultado.append(elemento)
        return resultado

# Ejecutar la aplicación
root = tk.Tk()
app = ConjuntosApp(root)
root.mainloop()
