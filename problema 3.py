# Escribe un programa que permita al usuario crear dos conjuntos de números
# enteros. Luego, el programa debe calcular y mostrar:
# 1. La intersección de ambos conjuntos (elementos comunes).
# 2. La unión de ambos conjuntos (todos los elementos sin duplicados).
# 3. La diferencia simétrica (elementos que están en uno u otro conjunto,
# pero no en ambos).


def definir_conjunto():
    control = True
    conjunto = []
    print(
        "Ingrese numeros que quiera introducir en el conjunto y pulse enter. cuando quiera parar introduzca otra cosa")
    while control:
        try:
            valor = float(input())
            conjunto.append(valor)
        except ValueError:
            print("Conjunto definido")
            control = False
    return conjunto

def comprobar_interseccion(conjunto1, conjunto2):
    interseccion = set(conjunto1) & set(conjunto2)
    return interseccion
def comprobar_union(lista1, lista2):
    interseccion =set(lista1+lista2)
    return list(interseccion)

def comprobar_diferencia(conjunto1, conjunto2):
    interseccion = set(conjunto1) ^ set(conjunto2)
    return interseccion


print("Defininiendo conjunto 1:")
conjunto1 = definir_conjunto()
print("Defininiendo conjunto 2:")
conjunto2 = definir_conjunto()


print("El resultado de la interseccion es: ",comprobar_interseccion(conjunto1, conjunto2))
print("El resultado de la union es: ",comprobar_union(conjunto1, conjunto2))
print("El resultado de la diferencia es: ",comprobar_diferencia(conjunto1, conjunto2))