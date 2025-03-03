from clases import Jugador
import clases
import tablero_logico
import tablero_grafico
from graphics import *
import math

def num_jugadores():
    while True:
        try:
            user_input=input("Ingreso el numero de jugadores (1-4): ")
            numero=int(user_input)
            if numero > 0 and numero < 5:
                break
            else:
                print("Error en dato, solo es posible de 1 a 4 jugadores")
        except:
            print("Error en dato")
  
    # Definir los colores disponibles
    colores = ["Rojo", "Azul", "Verde", "Amarillo"]
    imagenes = ["jugador1.png","jugador2.png","jugador3.png","jugador4.png"]
    # Crear la lista de jugadores con base en el número indicado
    jugadores = []
    for i in range(numero):
        jugadores.append(Jugador(colores[i],imagenes[i]))
    return jugadores


def validacion_numero_casillas():
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
                        return sqrt_tamaño
                    
                else:
                    print("Error en dato, solo numeros positivos del 9 al 100")
            except:
                print("Error en dato")


def juego():

    jugadores = num_jugadores()
    numero_casillas = validacion_numero_casillas()
    # Crear un diccionario para guardar las posiciones
    historial_posiciones = {}
    # Generamos nuestros valores de serpientes y escaleras
    tablero = tablero_logico.generar_tablero(numero_casillas)

    # Agregamos en un diccionario las serpientes y escaleras del tablero
    efectos = tablero_logico.clasificar_efectos(tablero)

    # Antes de comenzar el juego, debemos imprimir nuestro tablero y nuestras serpientes y escaleras
    print(efectos)

    # Graficamos el tablero
    win, positions = tablero_grafico.graficar_juego(numero_casillas, tablero)

    # Función para crear el menú de inicio y botones
    def crear_menu(win):
        # Ajustar las dimensiones del botón en relación con el tamaño de la ventana
        ancho_ventana = win.getWidth()
        alto_ventana = win.getHeight()
        
        # Definir las proporciones de los botones
        ancho_boton = ancho_ventana * 0.70  # 40% del ancho de la ventana
        alto_boton = alto_ventana * 0.3    # 10% del alto de la ventana
        x_boton = (ancho_ventana - ancho_boton) / 2  # Centrar horizontalmente
        y_boton = alto_ventana * 0.3      # 30% de la altura de la ventana

        # Crear el botón de "Comenzar juego"
        boton_comenzar = Rectangle(Point(x_boton, y_boton), Point(x_boton + ancho_boton, y_boton + alto_boton))
        boton_comenzar.setFill("lightblue")
        boton_comenzar.draw(win)
        texto_comenzar = Text(Point(x_boton + ancho_boton / 2, y_boton + alto_boton / 2), "Comenzar Juego")
        texto_comenzar.setSize(15)
        texto_comenzar.draw(win)

        # Esperar un clic en el botón para iniciar el juego
        while True:
            click = win.getMouse()
            if (x_boton <= click.getX() <= x_boton + ancho_boton) and (y_boton <= click.getY() <= y_boton + alto_boton):
                break

        boton_comenzar.undraw()
        texto_comenzar.undraw()

    # Función para crear el botón de "Tirar Dado"
    def crear_boton_tirar_dado(win):
        # Ajustar las dimensiones del botón en relación con el tamaño de la ventana
        ancho_ventana = win.getWidth()
        alto_ventana = win.getHeight()

        # Definir las proporciones de los botones
        ancho_boton = ancho_ventana * 0.2  # 40% del ancho de la ventana
        alto_boton = alto_ventana * 0.05    # 10% del alto de la ventana
        x_boton = (ancho_ventana - ancho_boton) / 2  # Centrar horizontalmente
        y_boton = alto_ventana * 0.5      # 50% de la altura de la ventana

        # Crear el botón de "Tirar dado"
        boton_tirar = Rectangle(Point(x_boton, y_boton), Point(x_boton + ancho_boton, y_boton + alto_boton))
        boton_tirar.setFill("lightgreen")
        boton_tirar.draw(win)
        texto_tirar = Text(Point(x_boton + ancho_boton / 2, y_boton + alto_boton / 2), "Tirar Dado")
        texto_tirar.setSize(15)
        texto_tirar.draw(win)

        # Esperar un clic en el botón para tirar el dado
        while True:
            click = win.getMouse()
            if (x_boton <= click.getX() <= x_boton + ancho_boton) and (y_boton <= click.getY() <= y_boton + alto_boton):
                return True  # Retorna True para indicar que se ha tirado el dado

    # Menú de inicio
    crear_menu(win)
    numero_ronda=0
    ganador=False
    # Rondas del juego
    while ganador==False:
        print(f"Ronda {numero_ronda+1}")
        for jugador in jugadores:
            # Mostrar el botón para tirar el dado
            if crear_boton_tirar_dado(win):
                posicion_actual = jugador.posicion
                jugador.tirar_dado()
                posicion_nueva = jugador.posicion
                if (jugador.posicion+1) >= len(tablero)+1:
                    jugador.posicion = len(tablero) - 1
                    posicion_nueva = jugador.posicion
                
                # Mover imagen en el gráfico
                tablero_grafico.mover_imagen(win,jugador.imagen, positions[posicion_actual + 1], positions[posicion_nueva + 1])
                posicion_actual = posicion_nueva
                jugador.posicion = tablero_logico.mover_jugador(jugador.posicion, tablero)
                posicion_nueva = jugador.posicion
                if posicion_nueva != posicion_actual:
                    tablero_grafico.mover_imagen(win,jugador.imagen, positions[posicion_actual + 1], positions[posicion_nueva + 1])
                # Guardar los resultados de la ronda
            clases.posiciones_del_juego(jugadores, historial_posiciones, numero_ronda + 1)
            
            if (jugador.posicion + 1) == len(tablero):
                ganador = True
                print(f"EL JUGADOR {jugador.color_ficha} HA GANADO!!!!")
                break
            numero_ronda+=numero_ronda+1
    # Mostrar el resumen del juego
    clases.mostrar_posiciones_del_juego(historial_posiciones)
    win.close()

juego()