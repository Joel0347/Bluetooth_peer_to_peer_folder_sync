import socket
import threading
import os
import time
import tkinter as tk

def start_server(local_addr, port, sync_folder, listbox):
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    sock.bind((local_addr, port))
    sock.listen(1)

    print(f"Servidor escuchando en {local_addr}:{port}")

    while True:
        try:
            client_sock, address = sock.accept()
            data = client_sock.recv(1024)  # Recibir datos binarios

            # Verificar si los datos recibidos cumplen con el formato esperado
            if b'::' in data:
                parts = data.split(b'::', 2)
                if len(parts) >= 2:
                    action = parts[0].decode()
                    filename = parts[1].decode()
                    filedata = parts[2] if len(parts) == 3 else b''  # Solo si hay datos adicionales

                    filepath = os.path.join(sync_folder, filename)
                    
                    if action in ["CREATE", "MODIFY"]:
                        attempts = 5
                        while attempts > 0:
                            try:
                                with open(filepath, 'wb') as f:  # Escribir datos en formato binario
                                    f.write(filedata)
                                print(f"Archivo {action.lower()} recibido y actualizado: {filename} de {address[0]}")
                                break
                            except PermissionError as e:
                                attempts -= 1
                                print(f"Error de permiso al escribir el archivo {filename}: {e}")
                                time.sleep(1)  # Espera antes de reintentar
                    elif action == "DELETE":
                        if os.path.exists(filepath):
                            os.remove(filepath)
                        print(f"Archivo eliminado: {filename} de {address[0]}")
                    elif action == "RENAME":
                        new_filename = filedata.decode()
                        new_filepath = os.path.join(sync_folder, new_filename)
                        if os.path.exists(filepath):
                            os.rename(filepath, new_filepath)
                        print(f"Archivo renombrado de {filename} a {new_filename} de {address[0]}")
                    
                    update_listbox(listbox, sync_folder)
                else:
                    print(f"Error: formato de datos inesperado {data}")
            else:
                print(f"Error: delimitador '::' no encontrado en los datos recibidos {data}")

            client_sock.close()
        except Exception as e:
            print(f"Error al recibir archivo: {e}")

def update_listbox(listbox, sync_folder):
    current_files = os.listdir(sync_folder)
    listbox.delete(0, tk.END)
    listbox.insert(tk.END, *current_files)

def start_sync_service(sync_folder, listbox, local_addr, local_port):
    server_thread = threading.Thread(target=start_server, args=(local_addr, local_port, sync_folder, listbox))
    server_thread.daemon = True
    server_thread.start()
