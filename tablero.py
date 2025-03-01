from graphics import *

def draw_board(window, rows, cols, size):
    '''
    Colores del tablero
    '''
    colors = ["Yellow", "Red", "Green", "Blue", "White", "Orange", 
              "Pink", "Purple", "Light Blue", "Light Green"]  # Secuencia de 10 colores
    '''
    Primero dibujamos nuestros círculos blancos
    '''
    for i in range(rows):
        for j in range(cols):
            x1, y1 = j * size, i * size
            x2, y2 = x1 + size, y1 + size

            # Dibujar el círculo con borde exterior blanco
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            radius = size / 1.8  # Ajusta el tamaño del círculo

            # Círculo con borde blanco
            circle_outer = Circle(Point(center_x, center_y), radius)  # Hacemos el radio un poco más grande
            circle_outer.setOutline("white")  # Borde exterior blanco
            circle_outer.setFill("white")
            circle_outer.draw(window)

    '''
    Luego los círculos de colores y los números
    '''
    number = 1  # Empezamos la numeración desde 1
    for i in range(rows - 1, -1, -1):  # Comienza desde la fila inferior
        for j in range(cols):
            x1, y1 = j * size, i * size
            x2, y2 = x1 + size, y1 + size
            # Dibujar el círculo en el centro de la casilla
            center_x = (x1 + x2) / 2
            center_y = (y1 + y2) / 2
            radius = size / 2  # Ajusta el tamaño del círculo
            circle_inner = Circle(Point(center_x, center_y), radius)
            color_index = (j + i) % len(colors)
            circle_inner.setFill(colors[color_index])  # Puedes cambiar el color del círculo
            circle_inner.draw(window)

            label_circle = Circle(Point(center_x, center_y - radius / 1.5), radius/2.9)
            label_circle.setFill("white")
            label_circle.draw(window)

            # Dibujar el número de la casilla
            text = Text(Point(center_x, center_y - radius / 1.5), str(number))
            text.setSize(int(radius//3.5))  # Ajusta el tamaño del número
            text.setTextColor("black")  # Color del texto (número)
            text.draw(window)

            # Incrementar el número para la siguiente casilla
            number += 1

def main():
    rows, cols, size = 10, 15, 50
    win = GraphWin("Serpientes y Escaleras", cols * size, rows * size)
    win.setBackground("lightgreen")
    draw_board(win, rows, cols, size)
    
    win.getMouse()  # Espera un clic antes de cerrar
    win.close()

if __name__ == "__main__":
    main()
