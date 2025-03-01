import random

class Jugador:
    def __init__(self, color_ficha, posicion=0):
        self.color_ficha = color_ficha
        self.posicion = posicion

    def tirar_dado(self):
        caradeldado = random.randint(1, 6)
        print(f"{self.color_ficha} sacó un {caradeldado}")
        self.posicion += caradeldado

# Crear varios jugadores y almacenarlos en una lista
jugadores = [
    Jugador("Rojo"),
    Jugador("Azul"),
    Jugador("Verde"),
    Jugador("Amarillo"),
]

# Crear un diccionario para guardar las posiciones de cada ronda
historial_posiciones = {}

# Variable para el número de ronda
numero_ronda = 1

# Hacer que cada jugador tire el dado
def ronda_juego(jugadores, historial_posiciones, numero_ronda):
    print('-' * 10)
    print(f"\nRonda {numero_ronda}")
    
    # Guardar las posiciones de la ronda actual
    posiciones_ronda = {}
    
    for jugador in jugadores:
        jugador.tirar_dado()
        print(f"{jugador.color_ficha} ahora está en la posición {jugador.posicion}\n")
        
        # Guardamos la posición de cada jugador en esta ronda
        posiciones_ronda[jugador.color_ficha] = jugador.posicion
    
    # Añadir las posiciones de esta ronda al historial
    historial_posiciones[numero_ronda] = posiciones_ronda
    
    # Mostrar el historial de posiciones hasta ahora
    print("Posiciones hasta ahora:")
    for ronda, posiciones in historial_posiciones.items():
        print(f"Ronda {ronda}: {posiciones}")
    
    numero_ronda += 1
    print('-' * 10)

    return jugadores, historial_posiciones, numero_ronda

for i in range(2):
    jugadores,historial_posiciones,numero_ronda=ronda_juego(jugadores,historial_posiciones,numero_ronda)