import math
import random
# Función para proteger archivo txt con hamming
def proteger_archivo_txt(archivo, tamaño_bloque):
    # Convertir el contenido del archivo en una secuencia binaria
    secuencia_binaria = ''.join(format(ord(caracter), '08b') for caracter in archivo)

    # Lista para almacenar los bloques protegidos
    bloques_hamming = []

    # Mientras la secuencia binaria no esté vacía
    while secuencia_binaria:
        # Crear un bloque de tamaño especificado con ceros en todas las posiciones
        bloque_aux = ['0'] * (tamaño_bloque + 1)  # Añadimos 1 para tener una posición en bloque_aux correspondiente a 1

        # Llenar el bloque con bits de datos en posiciones que no sean potencia de 2
        for i in range(1, tamaño_bloque + 1):  # Comenzar desde 1 y terminar en tamaño_bloque
            if (i & (i - 1)) != 0:  # Verificar si i no es potencia de 2
                if secuencia_binaria:  # Verificar si hay bits restantes en la secuencia binaria
                    bloque_aux[i] = secuencia_binaria[0]  # Agregar el primer bit de la secuencia binaria
                    secuencia_binaria = secuencia_binaria[1:]  # Eliminar el primer bit de la secuencia binaria

        # Añadir el bloque al conjunto de bloques de Hamming
        bloques_hamming.append(''.join(bloque_aux[1:]))  # Excluir el primer elemento de bloque_aux (índice 0)
        # Iterar sobre cada bloque en bloques_hamming
    for bloque in bloques_hamming:
        # Convertir el bloque de cadena binaria a una lista de enteros
        bloque_enteros = [int(bit) for bit in bloque]

        # Calcular la paridad para cada posición potencia de 2
        for i in range(len(bloque_enteros)-1):
            if i & (i + 1) == 0:  # Verificar si i es potencia de 2
                paridad = 0
                # Calcular la paridad para la posición actual
                for j in range(i, len(bloque_enteros), 2 * (i + 1)):
                    for k in range(j, min(j + (i + 1), len(bloque_enteros))):
                        paridad ^= bloque_enteros[k]

                # Insertar el bit de paridad en la posición correspondiente
                bloque_enteros[i] = paridad
                
        # Convertir la lista de enteros nuevamente a una cadena binaria y actualizar el bloque en bloques_hamming
        bloques_hamming[bloques_hamming.index(bloque)] = ''.join(str(bit) for bit in bloque_enteros)
    return bloques_hamming

def desproteger_archivo_txt(bloques, tamaño_bloque, correccion):
    if correccion:  # Si se requiere corrección de errores
        # Para cada bloque en bloques
        for bloque_idx, bloque in enumerate(bloques):
            control_cod = [] 
            control_decod = []
            # Iterar sobre los bits en el bloque, excepto los bits de control
            for i in range(tamaño_bloque-1):
                # Si el índice es una potencia de 2
                if i & (i + 1) == 0:  # Verificar si i es potencia de 2
                    paridad = 0
                    control_cod.append(int(bloque[i]))
                    # Calcular la paridad para la posición actual
                    for j in range(i, len(bloque), 2 * (i + 1)):
                        for k in range(j, min(j + (i + 1), len(bloque))):
                            paridad ^= int(bloque[k])
                    paridad ^= int(bloque[i])
                    control_decod.append(paridad)

            # Comparar control_cod con control_decod y armar un número binario indicando las diferencias
            error_binario = ""
            for j in range(len(control_cod)):
                if control_cod[j] != control_decod[j]:
                    error_binario = "1" + error_binario
                else:
                    error_binario = "0" + error_binario

            # Convertir el número binario a entero y invertir el bit del bloque en esa posición
            error_entero = int(error_binario, 2)
            if error_entero != 0:
                bloque = bloque[:error_entero - 1] + str(int(bloque[error_entero - 1]) ^ 1) + bloque[error_entero:]
                bloques[bloque_idx] = bloque  # Actualizar el bloque en la lista bloques
        print('Texto corregido: ', blocks_to_text(bloques))
    else:
        print('Texto sin corregir: ', blocks_to_text(bloques))        
    return bloques

def blocks_to_text(bloques):
    binario = ""  # Aquí se guardarán los bits desprotegidos, inicializado como una cadena vacía
    # Para cada bloque en bloques
    for bloque in bloques:
        # Iterar sobre los bits en el bloque, excepto los bits de control
        for i in range(0, len(bloque)):
            # Si el índice no es una potencia de 2, agregar el bit al binario
            if (i+1 & i) != 0:  # Verificar si i no es potencia de 2
                binario += bloque[i]

    texto = ""
    for i in range(0, len(binario), 8):  # Iterar sobre el binario en bloques de 8 bits
        byte = binario[i:i+8]  # Obtener un bloque de 8 bits (un byte)
        if all(bit == "0" for bit in byte):  # Verificar si el byte contiene solo caracteres nulos
            break  # Si es así, detener la iteración
        caracter = chr(int(byte, 2))  # Convertir el byte binario a su correspondiente carácter ASCII
        texto += caracter  # Agregar el carácter al texto
    return texto



def introducir_errores(bloques):
    bloques_con_error = []  # Aquí se guardarán los bloques con errores introducidos

    # Por cada bloque en bloques
    for bloque in bloques:
        # Decidir aleatoriamente si se introducirá error en el bloque con una probabilidad del 10%
        introducir_error = random.random() < 0.5

        if introducir_error:
            # Elegir aleatoriamente un número entre 1 y size(bloque)
            err = random.randint(1, int(len(bloque)))

            contador = 1
            for i in range(len(bloque)-1):
                # Si i no es potencia de 2
                if (i & (i + 1)) != 0:
                    # Si err es igual al contador, invertir el bit y salir del bucle
                    if err == contador:
                        if bloque[i] == '1':
                            bloque = bloque[:i] + '0' + bloque[i + 1:]
                        elif bloque[i] == '0':
                            bloque = bloque[:i] + '1' + bloque[i + 1:]
                        break
                    contador += 1

        # Agregar el bloque (con o sin error) a la lista de bloques con error
        bloques_con_error.append(bloque)

    return bloques_con_error




# Probemos la función proteger_archivo_txt
contenido_ejemplo = "hola manola"
tamaño_bloque_ejemplo = 8
bloques_protegidos = proteger_archivo_txt(contenido_ejemplo, tamaño_bloque_ejemplo)
#print('Bloques protegidos: ',bloques_protegidos)
bloques_error = introducir_errores(bloques_protegidos)
bloques_error_aux = bloques_error
#print('Bloques con error: ',bloques_error)
bloques_error_sin_corregir = desproteger_archivo_txt(bloques_error, tamaño_bloque_ejemplo, False)
bloques_error_corregidos = desproteger_archivo_txt(bloques_error_aux, tamaño_bloque_ejemplo, True)






