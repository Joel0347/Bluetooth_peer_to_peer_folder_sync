import socket
import os
import time
import tkinter as tk
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def send_file(filename, filedata, peer_addr, peer_port, action="CREATE"):
    try:
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as sock:
            sock.connect((peer_addr, peer_port))
            # Enviar datos en formato binario
            sock.send(f"{action}::{filename}::".encode() + filedata)
    except Exception as e:
        print(f"Error al enviar {filename}: {e}")

def delete_file(filename, peer_addr, peer_port):
    try:
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as sock:
            sock.connect((peer_addr, peer_port))
            sock.send(f"DELETE::{filename}".encode())
    except Exception as e:
        print(f"Error al eliminar {filename}: {e}")

def rename_file(old_filename, new_filename, peer_addr, peer_port):
    try:
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as sock:
            sock.connect((peer_addr, peer_port))
            sock.send(f"RENAME::{old_filename}::{new_filename}".encode())
    except Exception as e:
        print(f"Error al renombrar {old_filename}: {e}")

class FileHandler(FileSystemEventHandler):
    def __init__(self, sync_folder, peer_addr, peer_port, listbox):
        self.sync_folder = sync_folder
        self.peer_addr = peer_addr
        self.peer_port = peer_port
        self.listbox = listbox
        self.last_event = None  # Modificado para un manejo adecuado de eventos duplicados

    def on_created(self, event):
        if event.is_directory:
            return
        self.process_event(event, "CREATE")

    def on_deleted(self, event):
        if event.is_directory:
            return
        self.process_event(event, "DELETE")

    def on_modified(self, event):
        if event.is_directory or (self.last_event and self.last_event.src_path == event.src_path):
            return
        self.process_event(event, "MODIFY")  # Aseguramos el procesamiento del evento de modificación

    def on_moved(self, event):
        if event.is_directory:
            return
        old_filename = os.path.relpath(event.src_path, self.sync_folder)
        new_filename = os.path.relpath(event.dest_path, self.sync_folder)
        rename_file(old_filename, new_filename, self.peer_addr, self.peer_port)
        self.update_listbox()

    def process_event(self, event, event_type):
        self.last_event = event
        filepath = event.src_path
        filename = os.path.relpath(filepath, self.sync_folder)
        if event_type in ["CREATE", "MODIFY"]:
            with open(filepath, 'rb') as f:  # Aseguramos la lectura en binario
                filedata = f.read()
            send_file(filename, filedata, self.peer_addr, self.peer_port, action=event_type)
            if event_type == "MODIFY":
                print(f"Archivo {filename} modificado y enviado.")  # Notificación de modificación
        elif event_type == "DELETE":
            delete_file(filename, self.peer_addr, self.peer_port)
        self.update_listbox()

    def update_listbox(self):
        current_files = os.listdir(self.sync_folder)
        self.listbox.delete(0, tk.END)
        self.listbox.insert(tk.END, *current_files)

def watch_folder(sync_folder, listbox, peer_addr, peer_port):
    event_handler = FileHandler(sync_folder, peer_addr, peer_port, listbox)
    observer = Observer()
    observer.schedule(event_handler, sync_folder, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
