from clases import Jugador
import clases
import tablero_logico
import tablero_grafico

'''
PRERONDA
'''
# Crear varios jugadores y almacenarlos en una lista
jugadores = [
    Jugador("Rojo"),
    Jugador("Azul"),
    Jugador("Verde"),
    Jugador("Amarillo"),
]
# Crear un diccionario para guardar las posiciones
historial_posiciones = {}
# Variable para el número de ronda
numero_ronda = 1
'''
pedir al usuario el numero de casillas, la raiz de este numero tiene que ser un entero sin decimales
'''
numero_casillas = 7
'''
Generamos nuestros valores de serpientes y escaleras
'''
tablero = tablero_logico.generar_tablero(numero_casillas)
'''
Agremos en un diccionario las serpientes y escaleras del tablero
'''
efectos=tablero_logico.clasificar_efectos(tablero)
'''
Antes de comenzar el juego debemos imprimir nuestro tablero y nuestras serpientes y escaleras
'''
print(efectos)
'''
Graficamos el tablero
'''
win, positions = tablero_grafico.graficar_juego(numero_casillas,tablero)



'''
RONDA

Cambia el for por un boton que diga comenzar juego
'''
for i in range(5):
    print(f"ronda {i}")
    for jugador in jugadores:
        '''
        antes debe aparecer un boton de tirar dado para que se ejecute esto
        '''
        posicion_actual = jugador.posicion
        jugador.tirar_dado()
        posicion_nueva=jugador.posicion
        tablero_grafico.mover_imagen(win, positions[posicion_actual+1], positions[posicion_nueva+1])
        posicion_actual=posicion_nueva
        jugador.posicion= tablero_logico.mover_jugador(jugador.posicion,tablero)
        posicion_nueva=jugador.posicion
        if posicion_nueva != posicion_actual:
            tablero_grafico.mover_imagen(win, positions[posicion_actual+1], positions[posicion_nueva+1])
    '''
    Guardamos los resultados
    '''
    clases.posiciones_del_juego(jugadores, historial_posiciones,i+1)


'''
Esto imprime el resumen del juego
'''
clases.mostrar_posiciones_del_juego(historial_posiciones)