"""
Logica de Negocio:
1. Pedir al usuario los valores a comparar.  :)
2. Comparar los valores dados por el usuario para extraer el mínimo y el máximo. :)
3. Mostrar el resultado de la comparación. :)

"""

def comparador(valores : list) -> None:
    min = sum(valores)
    max = 0
    for i in range(len(valores)):
        if valores[i] > max:
            max = valores[i]
        if valores[i] < min:
            min = valores[i]
    return min, max


if __name__=="__main__":
    try:
        valores = [ int(input(f"Ingrese el valor en la posición { _ + 1 }: ")) for _ in range(6) ]
    except ValueError as e:
        print(f'Error: Debes incluir valores enteros... {e}')

    resultados = comparador(valores)

    print(f"======================= COMPARADOR DE VALORES ========================")
    print(f"El valor mínimo es: {resultados[0]}\nEl valor máximo es: {resultados[1]}")
    print(f"======================================================================")




 
