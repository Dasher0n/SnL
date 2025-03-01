import tkinter as tk
from clases import JuegoSerpientesYEscaleras


if __name__ == "__main__":
    tamaño = int(input("Ingrese el tamaño del tablero: "))
    root = tk.Tk()
    juego = JuegoSerpientesYEscaleras(root, tamaño)
    root.mainloop()
