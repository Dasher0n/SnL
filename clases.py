import numpy as np
import random

class Dado:
    """
    Clase que simula el lanzamiento de un dado de n caras con 1<n.

    Atributos:
        lados(int): El número de lados del dado. Por defecto es 6.

    Métodos:
        lanzar(): Devuelve un número aleatorio entre 1 y el número de lados.
    """

    def __init__(self, lados=6):
        """
        Inicializa una instancia de la clase Dado.

        Parámetros:
            lados (int): El número de lados del dado. Debe ser mayor o igual a 2.
                         Por defecto es 6.

        Lanza:
            ValueError: Si el número de lados es menor que 2.
        """
        if lados < 2:
            raise ValueError("El dado debe tener al menos 2 lados.")
        self.lados = lados

    def lanzar(self):
        """
        Devuelve:
            int: Un número aleatorio entre 1 y el número de lados del dado.
        """
        return np.random.randint(1, self.lados + 1)
    

class Jugador:
    """
    Clase que representa a un jugador.

    Atributos:
        nombre (str): El nombre del jugador.
        posición (int): La posición actual del jugador.

    Métodos:
        mover (casilla): Modifica la posición del jugador.
    """

    def __init__(self, nombre):
        """
        Inicializa una instancia de la clase Jugador.

        Parámetros:
            nombre (str): El nombre del jugador.
        """
        self.nombre = nombre
        self.puntuacion = 0

    def mover (self, casilla):
        """
        Modifica la posición del jugador.

        Parámetros:
            casilla (int): La casilla a la que se mueve el jugador.
        """
        self.puntuacion = casilla
    
class Tablero:
    """
    Clase que representa el tablero de juego de Serpientes y Escaleras.

    Atributos:
        tamaño (int): El tamaño del tablero (número de casillas).
        serpientes (dict): Diccionario que mapea la cabeza de la serpiente a su cola.
        escaleras (dict): Diccionario que mapea el inicio de la escalera a su fin.
        casillas (dict): Diccionario que mapea cada casilla a su valor final.

    Métodos:
        verificar_posicion(posicion): Verifica si la posición tiene una serpiente o escalera y devuelve la nueva posición.
    """

    def __init__(self, tamaño):
        """
        Inicializa una instancia de la clase Tablero.

        Parámetros:
            tamaño (int): El tamaño del tablero (número de casillas).
        """
        self.tamaño = tamaño
        self.serpientes = self.generar_serpientes()
        self.escaleras = self.generar_escaleras()
        self.casillas = self.generar_casillas()

    def generar_serpientes(self):
        """
        Genera un diccionario de serpientes aleatorias en el tablero.

        Devuelve:
            dict: Diccionario que mapea la cabeza de la serpiente a su cola.
        """
        serpientes = {}
        for _ in range(random.randint(5, 10)):
            cabeza = random.randint(2, self.tamaño - 1)
            cola = random.randint(1, cabeza - 1)
            serpientes[cabeza] = cola
        return serpientes

    def generar_escaleras(self):
        """
        Genera un diccionario de escaleras aleatorias en el tablero.

        Devuelve:
            dict: Diccionario que mapea el inicio de la escalera a su fin.
        """
        escaleras = {}
        for _ in range(random.randint(5, 10)):
            inicio = random.randint(1, self.tamaño - 2)
            fin = random.randint(inicio + 1, self.tamaño)
            escaleras[inicio] = fin
        return escaleras

    def generar_casillas(self):
        """
        Genera un diccionario de casillas con sus valores finales.

        Devuelve:
            dict: Diccionario que mapea cada casilla a su valor final.
        """
        casillas = {i: i for i in range(1, self.tamaño + 1)}
        casillas.update(self.serpientes)
        casillas.update(self.escaleras)
        return casillas

    def verificar_posicion(self, posicion):
        """
        Verifica si la posición tiene una serpiente o escalera y devuelve la nueva posición.

        Parámetros:
            posicion (int): La posición actual del jugador.

        Devuelve:
            int: La nueva posición del jugador después de verificar serpientes y escaleras.
        """
        if posicion in self.serpientes:
            print("Serpiente")
            return self.serpientes[posicion]
        elif posicion in self.escaleras:
            print("Escalera")
            return self.escaleras[posicion]
        else:
            return posicion