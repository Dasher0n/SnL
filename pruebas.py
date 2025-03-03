import math
validacion=False
while validacion == False:
        try:
            user_input=input("Ingresa el numero de casillas del tablero: ")
            casillas=int(user_input)
            if casillas > 8 and casillas < 101:
                sqrt_tamaño = math.isqrt(casillas)
                print(casillas)
                print(sqrt_tamaño)
                if (sqrt_tamaño * sqrt_tamaño) != casillas:
                    closest_square = sqrt_tamaño * sqrt_tamaño
                    if (sqrt_tamaño + 1) * (sqrt_tamaño + 1) - casillas < casillas - closest_square:
                        closest_square = (sqrt_tamaño + 1) * (sqrt_tamaño + 1)
                    print(f"El valor que diste es invalido, se recomienda el {closest_square}")
                if (sqrt_tamaño * sqrt_tamaño) == casillas:
                    validacion = True
                    return casillas
                
                
            else:
                print("Error en dato, solo numeros positivos del 9 al 100")
        except:
            print("Error en dato")