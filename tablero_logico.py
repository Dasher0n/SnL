import numpy as np
from  clases import Jugador
import clases
def generar_tablero(n):
    '''
    Generamos un arreglo con posibles escaleras que tendrian un valor positivo (+) y
    las serpientes con valor negativo (-).
    '''
    escalerasyserpientes = np.arange(-10,11,1)
    '''
    Se genera un arreglo de la misma dimension que las serpientes y escales con la probabilidad que
    salga en nuestro tablero, con probabilidades igualitarias para numeros diferentes del 0
    '''
    probabilidades = np.where(escalerasyserpientes == 0,0.5,0.025)
    '''
    Generamos nuestro tablero con los valores de serpientes y escaleras de tamano n*n, y usando
    el arreglo de probabilidades
    '''
    tablero = np.random.choice(escalerasyserpientes, size=(n*n),p=probabilidades)
    '''
    Puesto que en este tablero las escaleres o serpientes pueden tener valores que nos "sacarian del
    tablero" ajustamos esos valores a sus limites
    '''
    for i in range(len(tablero)):
        '''
        En la primera casilla no habra ni escalera ni serpiente porque es la inicial
        '''
        if i== 0:
            tablero[i] = 0
        '''
        tampoco en la ultima
        '''
        if i==len(tablero):
            tablero[i]=0
        
        '''
        Este es el caso en que una serpientes rebasa nuestro limite inferior del tablero
        '''
        if tablero[i] + i < 0:      
            tablero[i] = -i
        '''
        Este es el caso donde una escalera rebase nuestro limite superior del tablero
        '''
        if tablero[i] + i >= len(tablero):
            tablero[i] = len(tablero) - i -1
        '''
        Condicionales para no tener bucles
        '''
        if tablero[i] > 0 :
            if tablero[tablero[i]+i] != 0:
                tablero[[tablero[i]+i]] = 0

        if tablero[len(tablero)-i-1] < 0:
            if tablero[(tablero[len(tablero)-i-1])+len(tablero)-i-1] != 0:
                tablero[(tablero[len(tablero)-i-1])+len(tablero)-i-1] = 0    
    return tablero

def mover_jugador(posicion_jugador, tablero):
    if tablero[posicion_jugador] < 0:
        print("Serpientes, bajaras escaleras")
        posicion_jugador = posicion_jugador+tablero[posicion_jugador]
    elif tablero[posicion_jugador] > 0:
        print("Escalera, subes casillas")
        posicion_jugador = posicion_jugador+tablero[posicion_jugador]
    else:
        print("Avanzas casillas")

    if posicion_jugador > len(tablero):
        posicion_jugador=len(tablero)
    return posicion_jugador
        
def clasificar_efectos(tablero):
    efectos = {"serpientes": {}, "escaleras": {}}
    for i, valor in enumerate(tablero):
        if valor < 0:
            efectos["serpientes"][i + 1] = i+valor+1  # Guardamos solo las serpientes
        elif valor > 0:
            efectos["escaleras"][i + 1] = valor  # Guardamos solo las escaleras

    return efectos
