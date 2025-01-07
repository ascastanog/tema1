# Escribe un programa que pida al usuario ingresar una frase o párrafo. Luego, el
# programa debe contar cuentas veces aparece cada palabra en el texto y mostrar
# las palabras junto con su frecuencia.
# Requisitos:
# 1. Eliminar los signos de puntuación y convertir todas las palabras a
# minúsculas para evitar diferencias.
# 2. Usar un diccionario donde la clave sea la palabra y el valor sea su
# frecuencia.
# 3. Mostrar las palabras y sus frecuencias de forma ordenada por la palabra
import string

print("Ejercicio 2")


def solicitar_texto():
     texto = input("Introduzca el texto a procesar")
     texto_limpio = texto.translate(str.maketrans("", "", string.punctuation)).lower()
     return texto_limpio.split()

def procesar_texto(texto):
    frecuencia_palabra = {}
    for palabra in texto:
        if palabra in frecuencia_palabra:
            frecuencia_palabra[palabra] += 1
        else:
            frecuencia_palabra[palabra] = 1
    return frecuencia_palabra

palabras = solicitar_texto()
diccionario_palabras = procesar_texto(palabras)
for palabra in sorted(diccionario_palabras):
    print(f"{palabra} : {diccionario_palabras[palabra]}")
