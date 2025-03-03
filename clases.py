import random
'''
Nuestra primera clase es de nuestros jugadores, se le asigna un color, y todos comienzan en la posicion
0, ademas les agregaremos un metodo que en el juego de la vida real solo tiran el dado y el tablero es
el que los avanza o los retrocede con escaleras o serpientes, pero el jugador solo tira el dado
'''
class Jugador:
    def __init__(self, color_ficha,imagen, posicion=0):
        self.color_ficha = color_ficha
        self.posicion = posicion
        self.imagen = imagen

    def tirar_dado(self):
        caradeldado = random.randint(1, 6)
        print(f"{self.color_ficha} sacó un {caradeldado}")
        self.posicion += caradeldado

'''
Esta es una funcion que nos ayudara a hacer un resumen del juego completo
'''
# Hacer que cada jugador tire el dado
def posiciones_del_juego(jugadores, historial_posiciones, posiciones_numero_ronda):
    # Guardar las posiciones de la ronda actual
    posiciones_ronda = {}
    for jugador in jugadores:
        posiciones_ronda[jugador.color_ficha] = jugador.posicion
    # Añadir las posiciones de esta ronda al historial
    historial_posiciones[posiciones_numero_ronda] = posiciones_ronda
    return jugadores, historial_posiciones
''''
Esta funcion imprime el resumen del juego
'''
def mostrar_posiciones_del_juego(historial_posiciones):
    for ronda, posiciones in historial_posiciones.items():
        print(f"Ronda {ronda}: {posiciones}")