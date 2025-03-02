import tkinter as tk
from tkinter import messagebox, font
import numpy as np
import random
from PIL import Image, ImageTk
import math

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

        # Mostrar el mapeo de las casillas en el registro
        self.registro = tk.Text(root, width=40, height=15)
        self.registro.pack(side=tk.RIGHT, padx=10, pady=10)
        self.registro.insert(tk.END, f"Mapeo de casillas: {self.tablero.casillas}\n")
        self.registro.see(tk.END)

        self.dibujar_tablero()
        self.actualizar_posiciones()

        # Sección para tirar el dado y mostrar el resultado
        self.lanzamiento_frame = tk.Frame(root)
        self.lanzamiento_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.boton_lanzar = tk.Button(self.lanzamiento_frame, text="Lanzar Dado", command=self.lanzar_dado)
        self.boton_lanzar.pack()

        self.lanzamiento_label = tk.Label(self.lanzamiento_frame, text="Resultado del dado:")
        self.lanzamiento_label.pack()

        self.lanzamiento_display = tk.Label(self.lanzamiento_frame, text="", font=("Helvetica", 24))
        self.lanzamiento_display.pack()

        # Botón para repetir la jugada anterior
        self.boton_repetir = tk.Button(self.lanzamiento_frame, text="Repetir Jugada", command=self.repetir_jugada)
        self.boton_repetir.pack(pady=10)

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

        radio_punto = 3
        self.canvas.create_oval(x1 - radio_punto, y1 - radio_punto, x1 + radio_punto, y1 + radio_punto, fill="black")
        self.canvas.create_oval(x2 - radio_punto, y2 - radio_punto, x2 + radio_punto, y2 + radio_punto, fill="black")

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
                    self.root.after(1000, lambda: self.mover_jugador(jugador, self.tablero.serpientes[nueva_posicion], callback))
                elif nueva_posicion in self.tablero.escaleras:
                    self.root.after(1000, lambda: self.mover_jugador(jugador, self.tablero.escaleras[nueva_posicion], callback))
                else:
                    if callback:
                        callback()

        animar(posiciones)

    def lanzar_dado(self):
        self.boton_lanzar.config(state=tk.DISABLED)  # Deshabilitar el botón
        lanzamiento = self.dado.lanzar()
        self.lanzamiento_display.config(text=str(lanzamiento))
        self.registro.insert(tk.END, f"{self.turno.nombre} lanzó un {lanzamiento}\n")
        self.registro.see(tk.END)
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
        self.registro.see(tk.END)

        if self.turno.puntuacion == self.tablero.tamaño:
            messagebox.showinfo("Juego terminado", f"{self.turno.nombre} ha ganado!")
            self.root.quit()
        else:
            self.turno = self.jugador1 if self.turno == self.jugador2 else self.jugador2
            self.boton_lanzar.config(state=tk.NORMAL)  # Habilitar el botón

    def repetir_jugada(self):
        if self.ultima_jugada:
            jugador, nueva_posicion = self.ultima_jugada
            self.mover_jugador(jugador, nueva_posicion, self.finalizar_turno)


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
        self.factor = max(1, tamaño // 25)  # Ajustar el factor según el tamaño del tablero
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
        num_serpientes = min(random.randint(1, 5) * self.factor, self.tamaño // 2)
        intentos = 0
        while len(serpientes) < num_serpientes and intentos < 100:
            cabeza = random.randint(2, self.tamaño - 1)
            cola = random.randint(1, cabeza - 1)
            if cabeza not in serpientes and cola not in serpientes.values():
                serpientes[cabeza] = cola
            intentos += 1
        return serpientes

    def generar_escaleras(self):
        """
        Genera un diccionario de escaleras aleatorias en el tablero.

        Devuelve:
            dict: Diccionario que mapea el inicio de la escalera a su fin.
        """
        escaleras = {}
        num_escaleras = min(random.randint(1, 5) * self.factor, self.tamaño // 2)
        intentos = 0
        while len(escaleras) < num_escaleras and intentos < 100:
            inicio = random.randint(1, self.tamaño - 2)
            fin = random.randint(inicio + 1, self.tamaño)
            if (inicio not in escaleras and inicio not in self.serpientes and
                fin not in self.serpientes.values() and fin not in escaleras.values() and
                inicio not in self.serpientes.values() and fin not in self.serpientes):
                escaleras[inicio] = fin
            intentos += 1
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

class StartMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Serpientes y Escaleras")

        self.frame = tk.Frame(root)
        self.frame.pack(padx=20, pady=20)

        bold_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.label = tk.Label(self.frame, text="Serpientes y Escaleras", font=bold_font)
        self.label.pack(pady=10)

        integrantes = ["Burciaga Piña Erick Osvaldo", "Camargo Badillo Luis Mauricio", "Gudiño Romero Miguel Ángel"]
        for integrante in integrantes:
            integrante_label = tk.Label(self.frame, text=f"• {integrante}", font=("Helvetica", 11), anchor="center")
            integrante_label.pack(pady=2)

        spacer = tk.Frame(self.frame, height=10)
        spacer.pack()

        self.info_label2 = tk.Label(self.frame, text="Minería de Datos", font=("Helvetica", 11))
        self.info_label2.pack(pady=2)

        self.info_label3 = tk.Label(self.frame, text="Matemáticas Aplicadas y Computación", font=("Helvetica", 11))
        self.info_label3.pack(pady=2)

        spacer = tk.Frame(self.frame, height=10)
        spacer.pack()

        self.tamaño_label = tk.Label(self.frame, text="Ingresa el tamaño del tablero:")
        self.tamaño_label.pack(pady=5)

        self.tamaño_entry = tk.Entry(self.frame)
        self.tamaño_entry.pack(pady=5)
        self.tamaño_entry.bind("<Return>", self.iniciar_juego_event)

        self.start_button = tk.Button(self.frame, text="Iniciar", command=self.iniciar_juego)
        self.start_button.pack(pady=20)

    def iniciar_juego(self):
        tamaño_str = self.tamaño_entry.get()
        try:
            tamaño = int(tamaño_str)
            if tamaño <= 0:
                raise ValueError("El tamaño debe ser un número natural mayor que 0.")
        except ValueError as e:
            messagebox.showerror("Error", f"Por favor, ingresa un número natural válido. ")
            return

        if tamaño > 225:
            messagebox.showerror("Error", "El tamaño máximo permitido es 225.")
            return

        sqrt_tamaño = math.isqrt(tamaño)
        if sqrt_tamaño * sqrt_tamaño != tamaño:
            closest_square = sqrt_tamaño * sqrt_tamaño
            if (sqrt_tamaño + 1) * (sqrt_tamaño + 1) - tamaño < tamaño - closest_square:
                closest_square = (sqrt_tamaño + 1) * (sqrt_tamaño + 1)
            response = messagebox.askyesno("Sugerencia", f"El tamaño ingresado no es un cuadrado perfecto. ¿Quieres usar {closest_square} en su lugar?")
            if not response:
                return
            tamaño = closest_square

        self.frame.destroy()
        JuegoSerpientesYEscaleras(self.root, tamaño)

    def iniciar_juego_event(self, event):
        self.iniciar_juego()
