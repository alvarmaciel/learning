"""
Realizá un programa que permita ingresar valores del mismo tipo para las variables num1 y
num2. Una vez cargadas, mostrar ambas variables por pantalla, intercambiá sus valores (que
lo cargado en num1 quede en num2, y viceversa) y volvé a mostrarlas actualizadas

leer num1 y num2

mostrar num1 num2

swap num1 num2

mostrar num1 num2

"""
num1 = 25
num2 = 33

print(f"{num1}   <======>   {num2}")

auxiliar = num1
num1 = num2
num2 = auxiliar

print(f"{num1}   <======>   {num2}")

num1,num2 = num2,num1  #TUPLAS

print(f"{num1}   <======>   {num2}")
