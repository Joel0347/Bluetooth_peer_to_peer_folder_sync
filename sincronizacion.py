import os

def main():

    sync_folder = "" # aqui pondremos la direccion de la carpeta para sincronizar

    # Verifica si la carpeta especificada no existe.
    if not os.path.exists(sync_folder):
        os.makedirs(sync_folder)  # Crea la carpeta especificada.

if __name__ == "__main__":
    main()

