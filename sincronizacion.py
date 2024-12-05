import os
import sys

def main():
    # El usuario debe escribir: python sincronizacion.py <ruta_de_la_carpeta>
    if len(sys.argv) != 2:
        print("Uso: python sync_service.py <ruta_de_la_carpeta>")
        sys.exit(1)

    sync_folder = sys.argv[1]

    # Verifica si la carpeta especificada no existe.
    if not os.path.exists(sync_folder):
        os.makedirs(sync_folder)  # Crea la carpeta especificada.

if __name__ == "__main__":
    main()

