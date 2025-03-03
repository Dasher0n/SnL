from graphics import *
import time
from PIL import Image as PILImage

def draw_board(window, rows, cols, size, board_effects):
    '''
    Colores del tablero
    '''
    colors = ["Yellow", "Cyan", "Green", "Magenta", "White", "Orange", 
              "Pink", "Purple", "Light Blue", "Light Green"]  # Secuencia de 10 colores
    '''
    Primero dibujamos nuestros círculos blancos
    '''
    positions = {}
    number = 1  # Empezamos la numeración desde 1
    for i in range(rows - 1, -1, -1):  # Comienza desde la fila inferior
        if (rows - 1 - i) % 2 == 0:
            col_range = range(cols)  # Izquierda a derecha
        else:
            col_range = range(cols - 1, -1, -1)  # Derecha a izquierda

        for j in col_range:
            x1, y1 = j * size, i * size
            x2, y2 = x1 + size, y1 + size

            # Dibujar el círculo con borde exterior blanco
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            radius = size / 1.9  # Ajusta el tamaño del círculo

            # Círculo con borde blanco
            circle_outer = Circle(Point(center_x, center_y), radius)
            circle_outer.setOutline("white")  # Borde exterior blanco
            circle_outer.setFill("white")
            circle_outer.draw(window)

            # Dibujar el círculo de colores
            circle_inner = Circle(Point(center_x, center_y), radius / 1.15)
            color_index = (j + i) % len(colors)
            circle_inner.setFill(colors[color_index])  # Color del círculo
            circle_inner.draw(window)

            # Dibujar el número de la casilla
            text = Text(Point(center_x, center_y), str(number))
            text.setSize(int(radius // 3.2))  # Ajusta el tamaño del número
            text.setTextColor("black")  # Color del texto (número)
            text.draw(window)
            
            positions[number] = (center_x, center_y)
            number += 1

    '''
    Dibujar serpientes y escaleras
    '''
    for i in range(len(board_effects)):
        if board_effects[i] != 0:
            start_pos = i + 1
            end_pos = start_pos + board_effects[i]
            if end_pos in positions:
                start_x, start_y = positions[start_pos]
                end_x, end_y = positions[end_pos]
                
                if board_effects[i] > 0:
                    # Ajuste para las escaleras: mover la línea hacia arriba
                    start_y -= 10  # Mueve el inicio hacia arriba
                    end_y -= 10    # Mueve el final hacia arriba

                    # Dibujar la línea exterior de la escalera (azul más gruesa)
                    ladder_outer = Line(Point(start_x, start_y), Point(end_x, end_y))
                    ladder_outer.setOutline("black")
                    ladder_outer.setWidth(8)  # Línea exterior más gruesa
                    ladder_outer.draw(window)

                    # Dibujar la escalera (línea azul)
                    ladder = Line(Point(start_x, start_y), Point(end_x, end_y))
                    ladder.setOutline("blue")
                    ladder.setWidth(5)  # Línea más delgada para la escalera
                    ladder.draw(window)

                    # Dibujar el punto de inicio y fin de la escalera (color azul) con borde negro
                    start_point = Circle(Point(start_x, start_y), 5)
                    start_point.setFill("blue")
                    start_point.setOutline("black")  # Borde negro
                    start_point.draw(window)

                    end_point = Circle(Point(end_x, end_y), 5)
                    end_point.setFill("blue")
                    end_point.setOutline("black")  # Borde negro
                    end_point.draw(window)

                else:
                    # Ajuste para las serpientes: mover la línea hacia abajo
                    start_y += 10  # Mueve el inicio hacia abajo
                    end_y += 10    # Mueve el final hacia abajo

                    # Dibujar la línea exterior de la serpiente (roja más gruesa)
                    snake_outer = Line(Point(start_x, start_y), Point(end_x, end_y))
                    snake_outer.setOutline("black")
                    snake_outer.setWidth(8)  # Línea exterior más gruesa
                    snake_outer.draw(window)

                    # Dibujar la serpiente (línea roja)
                    snake = Line(Point(start_x, start_y), Point(end_x, end_y))
                    snake.setOutline("red")
                    snake.setWidth(5)  # Línea más delgada para la serpiente
                    snake.draw(window)

                    # Dibujar el punto de inicio y fin de la serpiente (color rojo) con borde negro
                    start_point = Circle(Point(start_x, start_y), 5)
                    start_point.setFill("red")
                    start_point.setOutline("black")  # Borde negro
                    start_point.draw(window)

                    end_point = Circle(Point(end_x, end_y), 5)
                    end_point.setFill("red")
                    end_point.setOutline("black")  # Borde negro
                    end_point.draw(window)

    return positions  # Devuelve las posiciones


def mover_imagen(window,imagen_jugador,posicion_inicial, posicion_final, pasos=20, tiempo_por_casilla=2):
    """
    Mueve una imagen desde la casilla inicial hasta la casilla final.

    :param window: ventana de gráficos.
    :param posicion_inicial: posición inicial en el tablero.
    :param posicion_final: posición final en el tablero.
    :param pasos: número de pasos para mover la imagen.
    :param tiempo_por_casilla: tiempo en segundos por casilla.
    """
    # Coordenadas de las casillas (de la función `draw_board`)
    x1, y1 = posicion_inicial
    x2, y2 = posicion_final
    
    # Cargar la imagen del jugador usando PIL
    pil_image = PILImage.open(imagen_jugador)
    
    # Redimensionar la imagen según el factor de escala
    width, height = pil_image.size
    pil_image = pil_image.resize((int(width * 0.15), int(height * 0.15)))  # Cambia el tamaño aquí si es necesario
    
    # Guardar la imagen redimensionada en un archivo temporal
    pil_image.save("jugador1_resized.png")
    
    # Si ya existe una imagen en la ventana, borrarla
    if hasattr(mover_imagen, 'imagen_jugador'):
        mover_imagen.imagen_jugador.undraw()  # Borra la imagen anterior

    # Cargar la imagen redimensionada en graphics.py
    imagen_jugador = Image(Point(x1, y1), "jugador1_resized.png")
    imagen_jugador.draw(window)
    
    # Guardar la referencia para la próxima ronda
    mover_imagen.imagen_jugador = imagen_jugador
    
    # Desplazamiento: número de pasos entre las casillas
    delta_x = (x2 - x1) / pasos
    delta_y = (y2 - y1) / pasos
    
    # Movimiento de la imagen
    for paso in range(pasos):
        imagen_jugador.move(delta_x, delta_y)
        time.sleep(tiempo_por_casilla / pasos)  # Controla la velocidad de la animación, dividiendo el tiempo entre los pasos

    # Asegurarse de que la imagen esté exactamente en la posición final
    imagen_jugador.move(x2 - (x1 + delta_x * pasos), y2 - (y1 + delta_y * pasos))



def graficar_juego(numero_filas, tablero):
    rows, cols, size = numero_filas, numero_filas, 75
    board_effects = tablero
    win = GraphWin("Serpientes y Escaleras", cols * size, rows * size)
    win.setBackground("lightgreen")
    
    # Obtener las posiciones del tablero
    positions = draw_board(win, rows, cols, size, board_effects)
    return win, positions
