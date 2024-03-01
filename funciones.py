def comparador_min_max( valores: list):
    min = sum(valores)
    max = 0
    for _ in range(len(valores)):
        if valores[_] < min:
            min = valores[_]    
        if valores[_] > max:
            max = valores[_]
    return min, max

def sumatoria(valores: list):
    return sum(valores), "Hola Mundo"

def mostrar_resultado(resultado: tuple) -> None:
    print(f"================== Comparador Minimo-Maximo =========================")
    print(f"El valor minimo es: {resultado[0]}\nEl valor maximo es: {resultado[1]}")
    print(f"=====================================================================")


"""
Fibonacci:

1. Pedir un rango especifico de numeros de la serie a mostrar. :)
2. Dentro de la funcion: :)
    2.0 Declarar una variable 'resultado' que almacene la lista que se va generando. :) 
    2.1 Declarar dos variables a y b con los valores iniciales. :)
    2.2 Declarar un bucle que en cada iteracion haga lo siguiente: :)
        2.2.1 Sumar los dos valores. :)
        2.2.2 Agregar la suma de los valores a la variable resultado. :)
        2.2.3 Actualizar los valores iniciales de las variables a y b. :)
3. Mostrar el resultado. :)

"""


def fibonacci(rango) -> list:
    resultado = []
    a = 1
    b = 0
    for i in range(rango):
        c = a + b
        resultado.append(c)
        a = b
        b = c
    return resultado


rango = int(input("Ingrese el rango de la serie Fibonacci: "))
resultado = fibonacci(rango)
print(f'======================== Serie Fibonacci ==============================')
print(f'Los primeeros {rango} valores de la serie Fibonacci son:\n{resultado}')
print(f'=======================================================================')
