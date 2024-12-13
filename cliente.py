import socket
import os
import time

# Dirección del dispositivo Bluetooth del peer al que se desea conectar
peer_addr = "B4:8C:9D:D4:8E:BA"
# Puerto de comunicación Bluetooth
port = 30

def send_file(filename, filedata, peer_addr, port):
    try:
        # establece un canal de comunicación mediante Bluetooth utilizando el protocolo RFCOMM
        # (Radio Frequency Communication)
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as sock:
            # Conectar al dispositivo Bluetooth con la dirección y puerto especificados
            sock.connect((peer_addr, port))
            # Enviar el nombre del archivo y sus datos concatenados y codificados en bytes
            sock.send(f"{filename}::{filedata}".encode())
    except Exception as e:
        # Imprimir un mensaje de error en caso de que ocurra una excepción
        print(f"Error al enviar {filename}: {e}")

def watch_folder(sync_folder):
    # Obtener el conjunto inicial de archivos en la carpeta de sincronización
    watched_files = set(os.listdir(sync_folder))
    
    while True:
        # Obtener el conjunto actual de archivos en la carpeta de sincronización
        current_files = set(os.listdir(sync_folder))
        # Determinar los nuevos archivos agregados
        new_files = current_files - watched_files

        # Filtrar archivos temporales y añadir un retraso
        time.sleep(1)
        current_files = set(os.listdir(sync_folder))
        new_files = current_files - watched_files

        for file in new_files:
            # Ignorar archivos temporales que empiezan con "~$" o terminan en ".tmp"
            if file.startswith("~$") or file.endswith(".tmp"):
                continue  # Continuar con el siguiente archivo

            try:
                # Leer el contenido del nuevo archivo
                with open(os.path.join(sync_folder, file), 'r') as f:
                    filedata = f.read()
                # Enviar el archivo a una dirección de par y puerto especificados
                send_file(file, filedata, peer_addr, port)
                print(f"Archivo enviado: {file}")
            except PermissionError as e:
                # Manejar errores de permisos al acceder al archivo
                print(f"Error de permisos al acceder al archivo {file}: {e}")
            except Exception as e:
                # Manejar cualquier otro error al acceder al archivo
                print(f"Error al acceder al archivo {file}: {e}")

        # Actualizar el conjunto de archivos observados
        watched_files = current_files