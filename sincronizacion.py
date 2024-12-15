import os
import threading
from tkinter import Listbox, ttk, messagebox
import tkinter as tk
import re

from cliente import watch_folder
from servidor import start_sync_service

def es_direccion_mac_valida(mac):
    patron_mac = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    return bool(patron_mac.match(mac))

def set_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(foreground='grey')
    entry.bind("<FocusIn>", lambda e: clear_placeholder(entry, placeholder))
    entry.bind("<FocusOut>", lambda e: add_placeholder(entry, placeholder))
    
def clear_placeholder(entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(foreground='black')
        
def add_placeholder(entry, placeholder):
    if entry.get() == '': 
        entry.insert(0, placeholder)
        entry.config(foreground='grey')

def start_monitoring():
    try: 
        sync_folder = folder_entry.get()
        local_addr = local_addr_entry.get()
        peer_addr = peer_addr_entry.get()
        
        if not es_direccion_mac_valida(local_addr):
            messagebox.showerror("Error", "La dirección MAC local no es válida.")
            return
        
        if not es_direccion_mac_valida(peer_addr):
            messagebox.showerror("Error", "La dirección MAC de tu pareja no es válida.")
            return
        
        local_port = int(local_port_entry.get())
        peer_port = int(peer_port_entry.get())
        
        if not os.path.exists(sync_folder):
            os.makedirs(sync_folder)
    
        start_sync_service(sync_folder, file_listbox, local_addr, local_port)
        threading.Thread(target=watch_folder, args=(sync_folder, file_listbox, peer_addr, peer_port), daemon=True).start()
        messagebox.showinfo("Información", "Monitoreo iniciado.")        
    except ValueError:
        messagebox.showerror("Error", "Falta por entrar algún dato o no es correcto.")
    

# Configurar la ventana principal
root = tk.Tk()
root.title("Chat Bluetooth")

# Configurar el marco principal
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Etiqueta y campo de entrada para el directorio a monitorear
ttk.Label(frame, text="Directorio a Monitorear:").grid(column=1, row=1, sticky=tk.W)
folder_entry = ttk.Entry(frame, width=50)
folder_entry.grid(column=2, row=1, sticky=(tk.W, tk.E))

# Etiqueta y campo de entrada para la dirección local 
ttk.Label(frame, text="Dirección Local:").grid(column=1, row=2, sticky=tk.W)
local_addr_entry = ttk.Entry(frame, width=50)
local_addr_entry.grid(column=2, row=2, sticky=(tk.W, tk.E))
set_placeholder(local_addr_entry, "B4:B5:B6:DA:55:9C")

# Etiqueta y campo de entrada para la dirección del par
ttk.Label(frame, text="Dirección del Par:").grid(column=1, row=3, sticky=tk.W)
peer_addr_entry = ttk.Entry(frame, width=50)
peer_addr_entry.grid(column=2, row=3, sticky=(tk.W, tk.E)) 
set_placeholder(peer_addr_entry, "B4:8C:9D:D4:8E:BA")

# Etiqueta y campo de entrada para el puerto local
ttk.Label(frame, text="Puerto Local:").grid(column=1, row=4, sticky=tk.W)
local_port_entry = ttk.Entry(frame, width=50)
local_port_entry.grid(column=2, row=4, sticky=(tk.W, tk.E))
set_placeholder(local_port_entry, "30")

# Etiqueta y campo de entrada para el puerto del par 
ttk.Label(frame, text="Puerto del Par:").grid(column=1, row=5, sticky=tk.W)
peer_port_entry = ttk.Entry(frame, width=50)
peer_port_entry.grid(column=2, row=5, sticky=(tk.W, tk.E))
set_placeholder(peer_port_entry, "30")

# Listbox para mostrar los archivos en la carpeta sincronizada
file_listbox = Listbox(frame, width=50, height=20)
file_listbox.grid(column=1, row=6, columnspan=2, sticky=(tk.W, tk.E))

# Botón para iniciar el monitoreo
ttk.Button(frame, text="Iniciar Monitoreo", command=start_monitoring).grid(column=2, row=7, sticky=tk.W)

# Configurar padding y expandir
for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

# Capturar el evento de cierre de la ventana
def on_closing():
    print("La ventana se ha cerrado.")
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)

# Iniciar el bucle principal de la interfaz
root.mainloop()
