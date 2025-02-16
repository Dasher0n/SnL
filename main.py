import numpy as np
import sphinx

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

d6=Dado()

print("Tiro de Dado:", d6.lanzar())
