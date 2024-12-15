# Bluetooth_peer_to_peer_folder_sync
 
> Claudia Hernáandez Pérez C-312

> Joel Aparicio Tamayo C-312


Para probar el código de sincronización de carpetas en dos laptops utilizando Bluetooth, sigue estos pasos:

### Preparativos Iniciales

1. **Empareja ambas laptops** a través de Bluetooth a nivel de sistema operativo.
2. **Obtén las direcciones MAC** de ambas laptops.
3. **Navega por la consola** a la carpeta del proyecto.
4. **Ejecuta el comando** `python syncronizacion.py`.
5. Rellena los campos superiores en la ventana con el nombre de la **carpeta de sincronización** (deben tener el mismo nombre en ambas laptops, en caso de no existir serán creadas), las **MAC** y los **puertos**.
6. Presiona el botón **Iniciar monitoreo** y cierra la ventana emergente


### Ejemplo de Ejecución

> Crear archivos en ambas laptops:

En Laptop 1: Crear archivo **hola.txt**. Verificar que se haya creado en la Laptop 2. Debe notificarse en la consola, además de aparecer los archivos de la carpeta de sincronización en la ventana de la app.


En Laptop 2: Crear archivo **hello.txt**. Verificar lo mismo en la Laptop 1.

> Modificar archivos en ambas laptops:

En Laptop 1: Modificar el archivo **hola.txt** escribiendo `hola mundo`. Verificar que se haya modificado en la Laptop 2. Debe notificarse en la consola.


En Laptop 2: Modificar el archivo **hello.txt** escribiendo `hello world`. Verificar lo mismo en la Laptop 1.

En Laptop 1: Modificar el archivo **hola.txt** renombrándolo a **mundo.txt**. Verificar que se haya modificado en la Laptop 2. Debe notificarse en la consola, además de aparecer modificado en la ventana de la app.


En Laptop 2: Modificar el archivo **hello.txt** renombrándolo a **world.txt**. Verificar lo mismo en la Laptop 1.

> Borrar archivos en ambas laptops:

En Laptop 1: Borrar el archivo **mundo.txt**. Verificar que se haya borrado en la Laptop 2. Debe notificarse en la consola, y debe desaparecer de la ventana de la app.


En Laptop 2: Borrar el archivo **world.txt**. Verificar lo mismo en la Laptop 1.


### Con estos pasos, deberías poder probar y verificar la funcionalidad del servicio de sincronización de carpetas entre dos laptops utilizando Bluetooth.