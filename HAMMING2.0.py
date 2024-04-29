import tkinter as tk
from tkinter import filedialog, messagebox
import heapq

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

def construir_arbol_huffman(tabla_frecuencias):
    cola_prioridad = [NodoHuffman(caracter, frecuencia) for caracter, frecuencia in tabla_frecuencias.items()]
    heapq.heapify(cola_prioridad)
    while len(cola_prioridad) > 1:
        izquierda = heapq.heappop(cola_prioridad)
        derecha = heapq.heappop(cola_prioridad)
        nuevo = NodoHuffman(None, izquierda.frecuencia + derecha.frecuencia)
        nuevo.izquierda = izquierda
        nuevo.derecha = derecha
        heapq.heappush(cola_prioridad, nuevo)
    return cola_prioridad[0]

def construir_tabla_frecuencias(texto):
    tabla_frecuencias = {}
    for caracter in texto:
        if caracter in tabla_frecuencias:
            tabla_frecuencias[caracter] += 1
        else:
            tabla_frecuencias[caracter] = 1
    return tabla_frecuencias

def codificar_arbol_huffman(arbol_huffman, codigo='', tabla_codigos={}):
    if arbol_huffman is not None:
        if arbol_huffman.caracter is not None:
            tabla_codigos[arbol_huffman.caracter] = codigo
        codificar_arbol_huffman(arbol_huffman.izquierda, codigo + '0', tabla_codigos)
        codificar_arbol_huffman(arbol_huffman.derecha, codigo + '1', tabla_codigos)
    return tabla_codigos

def comprimir(texto, tabla_frecuencias):
    arbol_huffman = construir_arbol_huffman(tabla_frecuencias)
    tabla_codigos = codificar_arbol_huffman(arbol_huffman)
    datos_comprimidos = ''.join(tabla_codigos[caracter] for caracter in texto)
    return datos_comprimidos

def decodificar_arbol_huffman(texto_comprimido, arbol_huffman):
    texto = ''
    nodo_actual = arbol_huffman
    for bit in texto_comprimido:
        if bit == '0':
            nodo_actual = nodo_actual.izquierda
        else:
            nodo_actual = nodo_actual.derecha
        if nodo_actual.caracter is not None:
            texto += nodo_actual.caracter
            nodo_actual = arbol_huffman
    return texto

def descompactar(texto_comprimido, arbol_huffman):
    texto_descomprimido = decodificar_arbol_huffman(texto_comprimido, arbol_huffman)
    return texto_descomprimido

archivo_cargado = None

def cargar_archivo():
    global archivo_cargado
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    if ruta_archivo:
        with open(ruta_archivo, 'r') as archivo:
            archivo_cargado = archivo.read()
            messagebox.showinfo("Archivo Cargado", "El archivo ha sido cargado exitosamente.")

def guardar_archivo(data, extension):
    ruta_archivo = filedialog.asksaveasfilename(defaultextension=extension)
    if ruta_archivo:
        with open(ruta_archivo, 'w') as archivo:
            archivo.write(data)
            messagebox.showinfo("Guardado Exitoso", "El archivo ha sido guardado exitosamente.")

def compactar_archivo():
    if archivo_cargado:
        tabla_frecuencias = construir_tabla_frecuencias(archivo_cargado)
        datos_comprimidos = comprimir(archivo_cargado, tabla_frecuencias)
        guardar_archivo(datos_comprimidos, ".huf")
        messagebox.showinfo("Compresión Exitosa", "El archivo ha sido compactado exitosamente como .huf.")
    else:
        messagebox.showerror("Error", "No se ha cargado ningún archivo.")

def descompactar_archivo():
    global archivo_cargado
    ruta_archivo = filedialog.askopenfilename(filetypes=[("Archivos Huffman", "*.huf")])
    if ruta_archivo:
        with open(ruta_archivo, 'r') as archivo:
            datos_comprimidos = archivo.read()

        # Construir el árbol de Huffman utilizando las frecuencias del archivo comprimido
        tabla_frecuencias = construir_tabla_frecuencias(archivo_cargado)
        arbol_huffman = construir_arbol_huffman(tabla_frecuencias)

        # Descompactar los datos utilizando el árbol de Huffman
        texto_descomprimido = descompactar(datos_comprimidos, arbol_huffman)

        # Guardar el texto descomprimido en un archivo .dhu
        ruta_guardar = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Archivos de texto", "*.txt")])
        if ruta_guardar:
            with open(ruta_guardar, 'w') as archivo:
                archivo.write(texto_descomprimido)
                messagebox.showinfo("Descompresión Exitosa", "El archivo ha sido descompactado exitosamente.")

def mostrar_archivos():
    ruta_archivo_txt = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])
    ruta_archivo_dhu = filedialog.askopenfilename(filetypes=[("Archivos Descompactados", "*.dhu")])
    if ruta_archivo_txt and ruta_archivo_dhu:
        with open(ruta_archivo_txt, 'r') as archivo_txt, open(ruta_archivo_dhu, 'r') as archivo_dhu:
            contenido_txt = archivo_txt.read()
            contenido_dhu = archivo_dhu.read()
            messagebox.showinfo("Archivos Cargados", f"Contenido del archivo original:\n\n{contenido_txt}\n\nContenido del archivo descompactado:\n\n{contenido_dhu}")

def menu_principal():
    root = tk.Tk()
    root.title("Utilidad de Compresión de Archivos")

    btn_cargar = tk.Button(root, text="1. Cargar Archivo", command=cargar_archivo)
    btn_cargar.pack()

    btn_compactar = tk.Button(root, text="2. Compactar Archivo", command=compactar_archivo)
    btn_compactar.pack()

    btn_descompactar = tk.Button(root, text="3. Descompactar Archivo", command=descompactar_archivo)
    btn_descompactar.pack()

    btn_mostrar_archivos = tk.Button(root, text="4. Mostrar Archivos", command=mostrar_archivos)
    btn_mostrar_archivos.pack()

    root.mainloop()

if __name__ == "__main__":
    menu_principal()

