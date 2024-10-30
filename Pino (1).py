import tkinter as tk
from tkinter import messagebox

class Tablero:
    def __init__(self, root):  
        # Creamos un tablero de 3x3 como lista de listas.
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]
        self.botones = [[None for _ in range(3)] for _ in range(3)]
        self.jugador_actual = "X"
        self.root = root
        self.crear_interfaz()

    def crear_interfaz(self):
        # Creamos botones para cada celda del tablero.
        for i in range(3):
            for j in range(3):
                boton = tk.Button(self.root, text=" ", font=('Arial', 24), width=5, height=2,
                                  command=lambda i=i, j=j: self.colocar_jugada(i, j))
                boton.grid(row=i, column=j)
                self.botones[i][j] = boton

    def lugar_disponible(self, fila, columna):
        # Revisa si una posición está disponible.
        return self.tablero[fila][columna] == " "

    def colocar_jugada(self, fila, columna):
        # Coloca la jugada del jugador actual en el tablero.
        if self.lugar_disponible(fila, columna):
            self.tablero[fila][columna] = self.jugador_actual
            self.botones[fila][columna].config(text=self.jugador_actual)
            
            # Verificar si hay un ganador
            if self.verificar_ganador(self.jugador_actual):
                messagebox.showinfo("Ganador", f"¡El jugador {self.jugador_actual} ha ganado!")
                self.reiniciar_juego()
            elif self.tablero_lleno():
                messagebox.showinfo("Empate", "¡El juego ha terminado en empate!")
                self.reiniciar_juego()
            else:
                # Cambiar de jugador
                self.cambiar_jugador()
        else:
            messagebox.showwarning("Posición ocupada", "Esa posición ya está ocupada. Elige otra.")

    def cambiar_jugador(self):
        # Cambia de jugador 'X' a 'O' o de 'O' a 'X'.
        self.jugador_actual = "O" if self.jugador_actual == "X" else "X"

    def verificar_ganador(self, jugador):
        # Verifica si el jugador dado ha ganado.
        for i in range(3):
            if all(self.tablero[i][j] == jugador for j in range(3)):  # Filas
                return True
            if all(self.tablero[j][i] == jugador for j in range(3)):  # Columnas
                return True

        # Verificamos las diagonales
        if all(self.tablero[i][i] == jugador for i in range(3)):  # Diagonal principal
            return True
        if all(self.tablero[i][2 - i] == jugador for i in range(3)):  # Diagonal inversa
            return True

        return False

    def tablero_lleno(self):
        # Verifica si ya no hay espacios vacíos.
        return all(self.tablero[i][j] != " " for i in range(3) for j in range(3))

    def reiniciar_juego(self):
        # Reinicia el tablero para un nuevo juego.
        self.tablero = [[" " for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                self.botones[i][j].config(text=" ")
        self.jugador_actual = "X"

if __name__ == "__main__":  # Iniciar juego 
    root = tk.Tk()
    root.title("Juego Triki")
    juego = Tablero(root)
    root.mainloop()
