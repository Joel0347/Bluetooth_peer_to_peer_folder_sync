import os
import sys
from servidor import start_sync_service
from cliente import watch_folder

def main():
    # El usuario debe escribir: python sincronizacion.py <ruta_de_la_carpeta>
    if len(sys.argv) != 2:
        print("Uso: python sync_service.py <ruta_de_la_carpeta>")
        sys.exit(1)

    sync_folder = sys.argv[1]

    # Verifica si la carpeta especificada no existe.
    if not os.path.exists(sync_folder):
        os.makedirs(sync_folder)  # Crea la carpeta especificada.

    start_sync_service(sync_folder)
    watch_folder(sync_folder)

if __name__ == "__main__":
    main()

