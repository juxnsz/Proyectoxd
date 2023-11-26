import pygame
import tkinter as tk
from tkinter import simpledialog, messagebox, Button
import random
import os

# Inicializar pygame
pygame.init()

# Función para obtener la lista de canciones de una carpeta
def get_song_list(folder_path):
    song_extensions = ['.mp3', '.wav']  # Agrega más formatos si es necesario
    return [os.path.join(folder_path, file) for file in os.listdir(folder_path) if os.path.splitext(file)[1] in song_extensions]

# Carpeta con las canciones
song_folder = 'canciones'  # Cambia esto a la ruta de tu carpeta de canciones
songs = get_song_list(song_folder)

# Asegúrate de que haya canciones disponibles
if not songs:
    raise Exception("No se encontraron canciones en la carpeta especificada.")

# Función para reproducir una canción aleatoria
def play_random_song():
    song = random.choice(songs)
    pygame.mixer.music.load(song)
    pygame.mixer.music.play()
    ask_user_for_song_name(song)

# Función para preguntar al usuario el nombre de la canción y si quiere continuar
def ask_user_for_song_name(song):
    correct = False
    for _ in range(3):  # Tres intentos
        user_guess = simpledialog.askstring("Adivina la canción", "¿Cuál es el nombre de la canción?")
        if user_guess and user_guess.lower() in os.path.basename(song).lower():
            messagebox.showinfo("Correcto", f"¡Correcto! El nombre de la canción es: {os.path.basename(song)}")
            correct = True
            break
        else:
            messagebox.showinfo("Incorrecto", "Intento incorrecto.")

    if not correct:
        messagebox.showinfo("Resultado", f"El nombre de la canción era: {os.path.basename(song)}")

    pygame.mixer.music.stop()

    # Preguntar si quiere intentar con otra canción
    if messagebox.askyesno("Continuar", "¿Quieres intentar con otra canción?"):
        play_random_song()

# Crear ventana principal
root = tk.Tk()
root.title("Juego de Adivinar Canciones")

# Configurar tamaño y posición de la ventana
window_width = 600
window_height = 400
position_x = int(root.winfo_screenwidth()/2 - window_width/2)
position_y = int(root.winfo_screenheight()/2 - window_height/2)
root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")

# Cargar y mostrar la imagen de fondo
background_photo = tk.PhotoImage(file="background.png")  # Asegúrate de que este archivo exista
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# Botón para jugar
play_button = Button(root, text="Comenzar", command=play_random_song,
                     bg="blue", fg="white", font=("Helvetica", 12),
                     relief="groove", padx=10, pady=10)
play_button.pack(pady=20)  # Centrado verticalmente

# Iniciar el bucle principal de Tkinter
root.mainloop()
