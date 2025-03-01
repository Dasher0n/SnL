import numpy as np

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

# Tamaño de la matriz
n = 5  # Cambia esto por el tamaño que desees

# Generar y mostrar la matriz
for i in range(10):
    tablero = generar_tablero(n)
    print(tablero)
