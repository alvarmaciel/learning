"""
Realizá un programa que permita ingresar 3 notas pertenecientes a tres trimestres distintos
para cierto alumno de nivel secundario.
Debe calcularse y mostrarse la nota promedio

leer 3 numeros
    leer numero
    leer numero
    leer numero
calcular promedio
mostrar resultado

"""

numero1 = input("Ingrese un numero: ")
numero1 = int(numero1)

numero2 = input("Ingrese un numero: ")
numero2 = int(numero2)

numero3 = int(input("Ingrese un numero: "))

promedio = (numero1 + numero2 + numero3) / 3


print("Notas:",numero1,numero2,numero3," Promedio:",promedio)

cadena_formato = f"Notas: [{numero1},{numero2},{numero3}] ==> Promedio:  {promedio:8.2}"

print(cadena_formato)



