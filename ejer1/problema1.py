def Ordenar_listas(lista):
    lista_positivos = []
    lista_negativos = []
    for num in lista:
        if num >= 0 :
            lista_positivos.append(num)
        else:
            lista_negativos.append(num)
    lista_positivos.sort()
    lista_negativos.sort()
    return lista_positivos, lista_negativos

lista = [3,1,2,3,4,-2,-5]
positivos, negativos =Ordenar_listas(lista)
print("positivos: ",positivos)
print("negativos: ",negativos)