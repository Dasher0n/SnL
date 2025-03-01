import tkinter as tk
from tkinter import messagebox
from clases import Dado, Jugador, Tablero
import numpy as np
from PIL import Image, ImageTk

class JuegoSerpientesYEscaleras:
    def __init__(self, root, tamaño):
        self.root = root
        self.root.title("Serpientes y Escaleras")
        self.tablero = Tablero(tamaño)
        self.jugador1 = Jugador("Jugador 1")
        self.jugador2 = Jugador("Jugador 2")
        self.dado = Dado()
        self.turno = self.jugador1
        self.ultima_jugada = None

        self.canvas = tk.Canvas(root, width=600, height=600)
        self.canvas.pack(side=tk.LEFT)

        # Cargar y redimensionar imágenes de jugadores
        self.img_jugador1 = self.cargar_imagen("assets/jugador1.png", 30, 30)
        self.img_jugador2 = self.cargar_imagen("assets/jugador2.png", 30, 30)

        self.dibujar_tablero()
        self.actualizar_posiciones()

        # Sección para tirar el dado y mostrar el resultado
        self.lanzamiento_frame = tk.Frame(root)
        self.lanzamiento_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.boton_lanzar = tk.Button(self.lanzamiento_frame, text="Lanzar Dado", command=self.lanzar_dado)
        self.boton_lanzar.pack()

        self.lanzamiento_label = tk.Label(self.lanzamiento_frame, text="Lanzamiento del dado:")
        self.lanzamiento_label.pack()

        self.lanzamiento_display = tk.Label(self.lanzamiento_frame, text="", font=("Helvetica", 24))
        self.lanzamiento_display.pack()

        # Botón para repetir la jugada anterior
        self.boton_repetir = tk.Button(self.lanzamiento_frame, text="Repetir Jugada", command=self.repetir_jugada)
        self.boton_repetir.pack(pady=10)

        # Registro de movimientos
        self.registro = tk.Text(root, width=40, height=15)
        self.registro.pack(side=tk.RIGHT, padx=10, pady=10)

    def cargar_imagen(self, path, width, height):
        imagen = Image.open(path)
        imagen = imagen.resize((width, height), Image.LANCZOS)
        return ImageTk.PhotoImage(imagen)

    def dibujar_tablero(self):
        tamaño = self.tablero.tamaño
        casillas_por_fila = int(np.ceil(tamaño ** 0.5))
        tamaño_casilla = 600 // casillas_por_fila

        for i in range(tamaño):
            fila = i // casillas_por_fila
            columna = i % casillas_por_fila
            x1 = columna * tamaño_casilla
            y1 = fila * tamaño_casilla
            x2 = x1 + tamaño_casilla
            y2 = y1 + tamaño_casilla
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")
            self.canvas.create_text(x1 + tamaño_casilla // 2, y1 + tamaño_casilla // 2, text=str(i + 1))

        for cabeza, cola in self.tablero.serpientes.items():
            self.dibujar_linea(cabeza, cola, "green")

        for inicio, fin in self.tablero.escaleras.items():
            self.dibujar_linea(inicio, fin, "orange")

    def dibujar_linea(self, inicio, fin, color):
        tamaño = self.tablero.tamaño
        casillas_por_fila = int(np.ceil(tamaño ** 0.5))
        tamaño_casilla = 600 // casillas_por_fila

        fila_inicio = (inicio - 1) // casillas_por_fila
        columna_inicio = (inicio - 1) % casillas_por_fila
        x1 = columna_inicio * tamaño_casilla + tamaño_casilla // 2
        y1 = fila_inicio * tamaño_casilla + tamaño_casilla // 2

        fila_fin = (fin - 1) // casillas_por_fila
        columna_fin = (fin - 1) % casillas_por_fila
        x2 = columna_fin * tamaño_casilla + tamaño_casilla // 2
        y2 = fila_fin * tamaño_casilla + tamaño_casilla // 2

        self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

    def actualizar_posiciones(self):
        self.canvas.delete("jugador")
        self.dibujar_jugador(self.jugador1, self.img_jugador1)
        self.dibujar_jugador(self.jugador2, self.img_jugador2)

    def dibujar_jugador(self, jugador, imagen):
        tamaño = self.tablero.tamaño
        casillas_por_fila = int(np.ceil(tamaño ** 0.5))
        tamaño_casilla = 600 // casillas_por_fila

        fila = (jugador.puntuacion - 1) // casillas_por_fila
        columna = (jugador.puntuacion - 1) % casillas_por_fila
        x = columna * tamaño_casilla + tamaño_casilla // 2
        y = fila * tamaño_casilla + tamaño_casilla // 2

        jugador.imagen_id = self.canvas.create_image(x, y, image=imagen, tags="jugador")

    def mover_jugador(self, jugador, nueva_posicion, callback=None):
        tamaño = self.tablero.tamaño
        casillas_por_fila = int(np.ceil(tamaño ** 0.5))
        tamaño_casilla = 600 // casillas_por_fila

        posiciones = list(range(jugador.puntuacion + 1, nueva_posicion + 1))
        if nueva_posicion < jugador.puntuacion:
            posiciones = list(range(jugador.puntuacion - 1, nueva_posicion - 1, -1))

        def animar(posiciones):
            if posiciones:
                pos = posiciones.pop(0)
                fila = (pos - 1) // casillas_por_fila
                columna = (pos - 1) % casillas_por_fila
                x = columna * tamaño_casilla + tamaño_casilla // 2
                y = fila * tamaño_casilla + tamaño_casilla // 2
                self.canvas.coords(jugador.imagen_id, x, y)
                self.root.after(100, animar, posiciones)
            else:
                jugador.mover(nueva_posicion)
                self.actualizar_posiciones()
                if nueva_posicion in self.tablero.serpientes:
                    self.root.after(1000, lambda: self.mover_jugador(jugador, self.tablero.serpientes[nueva_posicion]))
                elif nueva_posicion in self.tablero.escaleras:
                    self.root.after(1000, lambda: self.mover_jugador(jugador, self.tablero.escaleras[nueva_posicion]))
                elif callback:
                    callback()

        animar(posiciones)

    def lanzar_dado(self):
        lanzamiento = self.dado.lanzar()
        self.lanzamiento_display.config(text=str(lanzamiento))
        self.registro.insert(tk.END, f"{self.turno.nombre} lanzó un {lanzamiento}\n")
        nueva_posicion = self.turno.puntuacion + lanzamiento
        if nueva_posicion > self.tablero.tamaño:
            nueva_posicion = self.tablero.tamaño
        self.ultima_jugada = (self.turno, nueva_posicion)
        self.mover_jugador(self.turno, nueva_posicion, self.finalizar_turno)

    def finalizar_turno(self):
        nueva_posicion = self.turno.puntuacion
        if nueva_posicion in self.tablero.serpientes:
            self.registro.insert(tk.END, f"{self.turno.nombre} cayó en una serpiente y bajó a la casilla {nueva_posicion}\n")
        elif nueva_posicion in self.tablero.escaleras:
            self.registro.insert(tk.END, f"{self.turno.nombre} subió una escalera a la casilla {nueva_posicion}\n")
        self.registro.insert(tk.END, f"{self.turno.nombre} está en la casilla {self.turno.puntuacion}\n")

        if self.turno.puntuacion == self.tablero.tamaño:
            messagebox.showinfo("Juego terminado", f"{self.turno.nombre} ha ganado!")
            self.root.quit()
        else:
            self.turno = self.jugador1 if self.turno == self.jugador2 else self.jugador2

    def repetir_jugada(self):
        if self.ultima_jugada:
            jugador, nueva_posicion = self.ultima_jugada
            self.mover_jugador(jugador, nueva_posicion, callback=None)

if __name__ == "__main__":
    tamaño = int(input("Ingrese el tamaño del tablero: "))
    root = tk.Tk()
    juego = JuegoSerpientesYEscaleras(root, tamaño)
    root.mainloop()
