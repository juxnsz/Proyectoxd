import tkinter as tk
import random
import pygame
import time
import threading
import cod_game
from pygame import mixer
from tkinter import font, messagebox
from PIL import Image, ImageTk

# Funciones de utilidad

def leer_imagen(path, size):
    return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ADAPTIVE))

def centrar_ventana(ventana,aplicacion_ancho,aplicacion_largo):    
    pantall_ancho = ventana.winfo_screenwidth()
    pantall_largo = ventana.winfo_screenheight()
    x = int((pantall_ancho/2) - (aplicacion_ancho/2))
    y = int((pantall_largo/2) - (aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")

def botonjugar():
    # Ocultar o destruir el cuerpo principal
    cuerpo_principal.pack_forget()

    # Crear y configurar el nuevo Frame
    inner_frame = tk.Frame(root)
    inner_frame.pack(side="top", expand=True, fill=tk.BOTH)

    # Agregar contenido al nuevo Frame
    label = tk.Label(inner_frame, text="imagen")
    label.pack(expand=True)
    start_game_button = tk.Button(inner_frame, text="Iniciar Juego", command=iniciar_juego)
    start_game_button.pack()

def iniciar_juego():
    cancion_elegida = random.choice(cod_game.canciones)
    ruta_cancion = cancion_elegida[2]

    # Inicia la reproducción de la canción en un hilo separado
    hilo_reproduccion = threading.Thread(target=cod_game.reproducir_cancion, args=(ruta_cancion,))
    hilo_reproduccion.start()


def show_about_text():
    # Limpiar el cuerpo principal antes de agregar nuevos elementos
    limpiar_cuerpo_principal()

    # Cargar la imagen de fondo
    background_image = leer_imagen("./imagenes/background.jpg", (1920, 1080))

    # Crear una etiqueta para la imagen de fondo
    background_label = tk.Label(cuerpo_principal, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # Añadir texto encima de la imagen de fondo
    about_text = "Este es un juego musical basado en las canciones más famosas. Tendrás que adivinar cada una de ellas. ¡Diviértete!"
    about_label = tk.Label(cuerpo_principal, text=about_text, font=("Roboto", 16), bg='cyan')
    about_label.place(relx=0.5, rely=0.5, anchor='n')

    # Mantener una referencia a la imagen para evitar que sea eliminada por el recolector de basura
    about_label.image = background_image

def limpiar_cuerpo_principal():
    # Limpiar el cuerpo principal antes de agregar nuevos elementos
    for widget in cuerpo_principal.winfo_children():
        widget.destroy()

def configurar_boton_menu(button, text, image_path, font_awesome, ancho_menu, alto_menu):
    img = leer_imagen(image_path, (ancho_menu, alto_menu))
    button.config(image=img, compound=tk.LEFT,
                  bd=0, bg=COLOR_MENU_LATERAL, fg="white", width=ancho_menu, height=alto_menu)
    button.img = img
    button.pack(side=tk.TOP)
    bind_hover_events(button)

def bind_hover_events(button):
    # Asociar eventos Enter y Leave con la función dinámica
    button.bind("<Enter>", lambda event: on_enter(event, button))
    button.bind("<Leave>", lambda event: on_leave(event, button))

def on_enter(event, button):
    # Cambiar estilo al pasar el ratón por encima
    button.config(bg=COLOR_MENU_CURSOR_ENCIMA, fg='white')

def on_leave(event, button):
    # Restaurar estilo al salir el ratón
    button.config(bg=COLOR_MENU_LATERAL, fg='white')

def toggle_panel():
    # Alternar visibilidad del menú lateral
    if menu_lateral.winfo_ismapped():
        menu_lateral.pack_forget()
    else:
        menu_lateral.pack(side=tk.LEFT, fill='y')

# Configuración de la ventana principal
root = tk.Tk()
root.title('Juego de adivinanzas musicales')
root.iconbitmap("./imagenes/tryingiconlol.ico")
w, h = 1024, 600
centrar_ventana(root, w, h)

# Colores y otras constantes
COLOR_BARRA_SUPERIOR = "#1f2329"
COLOR_MENU_LATERAL = "#2a3138"
COLOR_CUERPO_PRINCIPAL = "#f1faff"
COLOR_MENU_CURSOR_ENCIMA = "#2f88c5"

# Creación de los paneles
barra_superior = tk.Frame(root, bg=COLOR_BARRA_SUPERIOR, height=50)
barra_superior.pack(side=tk.TOP, fill='both')

menu_lateral = tk.Frame(root, bg=COLOR_MENU_LATERAL, width=150)
menu_lateral.pack(side=tk.LEFT, fill='both', expand=False)

cuerpo_principal = tk.Frame(root, bg=COLOR_CUERPO_PRINCIPAL)
cuerpo_principal.pack(side=tk.RIGHT, fill='both', expand=True)

# Controles en la barra superior
font_awesome = font.Font(family='FontAwesome', size=12)

labelTitulo = tk.Label(barra_superior, text="Musical Riddle")
labelTitulo.config(fg="#fff", font=("Roboto", 15), bg=COLOR_BARRA_SUPERIOR, pady=10, width=20)
labelTitulo.pack(side=tk.LEFT)

buttonMenuLateral = tk.Button(barra_superior, text="≡", font=font_awesome,
                               command=toggle_panel, bd=0, bg=COLOR_BARRA_SUPERIOR, fg="white")
buttonMenuLateral.pack(side=tk.LEFT)

# Controles en el menú lateral
ancho_menu = 210
alto_menu = 70

imagen2 = leer_imagen("./imagenes/imagen2.png", (100, 100))
labellogo = tk.Label(menu_lateral, image=imagen2, bg=COLOR_MENU_LATERAL)
labellogo.pack(side=tk.TOP, pady=10)

buttons_info = [
    ("Jugar", "./imagenes/play.png", tk.Button(menu_lateral, command=botonjugar)),
    ("Acerca De", "./imagenes/about.png", tk.Button(menu_lateral, command=show_about_text)),
    ("Salir", "./imagenes/exitlol.png", tk.Button(menu_lateral, command=root.quit))
]

for text, image_path, button in buttons_info:
    configurar_boton_menu(button, text, image_path, font_awesome, ancho_menu, alto_menu)

root.mainloop()