import socket

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