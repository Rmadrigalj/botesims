import tkinter as tk
from tkinter import messagebox
import pyperclip
import threading

# Semáforo para controlar el acceso a la generación de E-SIM
semaforo = threading.Semaphore(1)

# Variable para almacenar la última serie generada
ultima_serie_generada = None

def obtener_serie_disponible():
    try:
        with open('almacen.txt', 'r') as archivo_txt:
            lineas = archivo_txt.readlines()
            if lineas:
                serie = lineas[0].strip()  # Lee la primera línea del archivo y elimina los espacios en blanco
                with open('almacen.txt', 'w') as archivo_txt:
                    archivo_txt.writelines(lineas[1:])  # Escribe el resto de las líneas
                return serie
            else:
                return None
    except FileNotFoundError:
        print("El archivo 'almacen.txt' no se encontró.")

def almacenar_serie_usada(serie):
    try:
        with open('e_simusadas.txt', 'a') as archivo_usadas:
            archivo_usadas.write(serie + '\n')
    except FileNotFoundError:
        print("El archivo 'e_simusadas.txt' no se encontró.")

def copiar_al_portapapeles(serie):
    pyperclip.copy(serie)
    # Muestra un mensaje después de copiar al portapapeles
    messagebox.showinfo("Mensaje", "Recuerde pegar la serie de la E-SIM en el pedido de Siebel y darle volver a valorar, cuando esté seguro cierre el generador")

def mostrar_serie(serie):
    global ultima_serie_generada
    if serie != ultima_serie_generada:
        copiar_al_portapapeles(serie)
        almacenar_serie_usada(serie)  # Almacena la serie generada en e_simusadas.txt
        ultima_serie_generada = serie

def solicitar_esim():
    global semaforo
    if semaforo.acquire(blocking=False):
        serie = obtener_serie_disponible()
        if serie:
            resultado_label.config(text=f"Se generó el E-SIM con la serie: {serie}")
            mostrar_serie(serie)
        else:
            resultado_label.config(text="No hay más series disponibles en el almacen.txt")
        semaforo.release()

def main():
    global resultado_label
    ventana = tk.Tk()
    ventana.title("Kolbi ICE - Generador de E-SIM")
    
    # Establece el tamaño de la ventana al abrirse (ancho x alto)
    ventana.geometry("800x600")

    # Configura el fondo
    fondo_label = tk.Label(ventana, background="lightgreen")
    fondo_label.pack(fill="both", expand=True)

    # Configura el logo en el centro de la ventana
    logo_image = tk.PhotoImage(file="kolbi.png")  # Reemplaza "kolbi.png" con el nombre de tu archivo de imagen
    logo_label = tk.Label(fondo_label, image=logo_image, background="lightgreen")
    logo_label.place(relx=0.5, rely=0.5, anchor="center")
    logo_label.image = logo_image

    # Añade un encabezado
    encabezado = tk.Label(ventana, text="Kolbi ICE - Generador de E-SIM", font=("Arial", 20, "bold"), background="lightgreen")
    encabezado.pack(pady=20)

    etiqueta = tk.Label(ventana, text="Presiona el botón para solicitar un E-SIM", font=("Arial", 16), background="lightgreen")
    etiqueta.pack()

    boton = tk.Button(ventana, text="Solicitar E-SIM", command=solicitar_esim, bg="lightgreen", fg="white", font=("Arial", 14), borderwidth=2)
    boton.pack(pady=20)

    resultado_label = tk.Label(ventana, text="", font=("Arial", 14, "bold"), background="lightgreen")
    resultado_label.pack()

    ventana.mainloop()

if __name__ == '__main__':
    main()
