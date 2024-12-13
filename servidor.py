import socket
import threading
import os

# Dirección y puerto del servidor
local_addr = "B4:8C:9D:D4:8E:BA"
port = 30


def start_server(local_addr, port, sync_folder):
    sock = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
    sock.bind((local_addr, port))
    sock.listen(1)

    print(f"Servidor escuchando en {local_addr}:{port}")

    while True:
        try:
            client_sock, address = sock.accept()
            data = client_sock.recv(1024).decode()
            filename, filedata = data.split('::')

            with open(os.path.join(sync_folder, filename), 'w') as f:
                f.write(filedata)

            print(f"Archivo recibido: {filename} de {address[0]}")
            client_sock.close()
        except Exception as e:
            print(f"Error al recibir archivo: {e}")


def start_sync_service(sync_folder):
    server_thread = threading.Thread(target=start_server, args=(local_addr, port, sync_folder))
    server_thread.daemon = True
    server_thread.start()