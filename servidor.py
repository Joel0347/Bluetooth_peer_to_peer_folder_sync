import os

# Dirección y puerto del servidor
local_addr = "B4:8C:9D:D4:8E:BA"
port = 30

#iniciar servidor
def start_server(local_addr, port, sync_folder):
    print(f"Servidor escuchando en {local_addr}:{port}")

    while True:
        try:
            filename = "hello_world"
            address = [local_addr]
            print(f"Archivo recibido: {filename} de {address[0]}")
        except Exception as e:
            print(f"Error al recibir archivo: {e}")

#iniciar servicio de sincronización
def start_sync_service(sync_folder):
    print("")