# Tarea 04: DCCurve :video_game:

## Consideraciones generales :octocat:

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte 1 (Juego): Hecha en su mayoría
    * Parte 1.1 (Repartición de Puntaje): Faltó arreglar errores en la determinación de la victoria y puntajes (explicados en los supuestos), la eliminación simultánea sí está implementada
    * Parte 1.2 (Inicialización de la Partida y Rondas): Hecha completa
    * Parte 1.3 (Movimiento Continuo): Hecha completa
    * Parte 1.4 (Un Rastro Peligroso): Hecha completa
    * Parte 1.5 (Poderes): Hecha completa
* Parte 2 (Funcionalidades): Hecha completa
    * Parte 2.1 (Sistema de Autentificación): Hecha completa
    * Parte 2.2 (Sala de Espera): Hecha completa
* Parte 3 (Interfaz Gráfica): Hecha en su mayoría
    * Parte 3.1 (Ventana de Inicio): Hecha completa
    * Parte 3.2 (Sala de Espera): Faltó corregir un error con la cuenta regresiva (explicado en los supuestos), lo demás está implementado
    * Parte 3.3 (Sala de Juego): Faltó mostrar el puntaje necesario para la victoria y los puntajes de cada jugador (explicado en los supuestos)
* Parte 4 (Networking): Hecha completa
* Parte 5 (Bonus): Hecha parcialmente
    * Parte 5.1 (Tres Poderes Más): Hecha completa
    * Parte 5.2 (Modo Multijugador): No se implementó
* Parte 6 (Entregable): Hecha completa
* Parte 7 (Extra): Hecha completa
    * Parte 7.1 (Uso de .gitignore): Hecha completa

## Ejecución :computer:
Los módulos principales de la tarea a ejecutar son  ```server.py``` (carpeta server) y ```frontend.py``` (carpeta client), los que deben ser ejecutados en dicho orden. Para correr el programa son además necesarios los siguientes archivos:

### Módulos (se encuentran en la carpeta client):
* ```client.py```
* ```backend.py```

### IP y Puerto:
Para hacer host de las salas del juego se utilizó la IP del 'localhost' (127.0.0.1) y el puerto 8000.

### Sprites (carpeta dentro de client):
Contiene a los sprites utilizados en la interfaz gráfica.

### Windows (carpeta dentro de client):
Contiene a las ventanas hechas en QtDesigner utilizadas en la interfaz gráfica.

### Base de Datos (archivo dentro de server):
Este archivo llamado ```database.json``` es generado por el programa al momento de registrar al primer usuario. Posteriormente es utilizado como base de datos del programa.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```json```-> ```dumps(), loads(), dump(), load() / Módulos que la usan -> client.py, server.py```
2. ```pickle```-> ```dumps(), loads(), UnpicklingError, HIGHEST_PROTOCOL / Módulos que la usan -> client.py, server.py```
3. ```binascii```-> ```hexlify(), unhexlify() / Módulos que la usan -> server.py```
4. ```hashlib```-> ```sha256() / Módulos que la usan -> server.py```
5. ```os```-> ```urandom() / Módulos que la usan -> server.py```
6. ```os.path```-> ```exists() / Módulos que la usan -> server.py```
7. ```math```-> ```sqrt(), cos(), sin(), radians() / Módulos que la usan -> server.py, backend.py```
8. ```time```-> ```sleep() / Módulos que la usan -> server.py, backend.py```
9. ```socket```-> ```socket(), AF_INET, SOCK_STREAM / Módulos que la usan -> server.py, client.py```
10. ```threading```-> ```Thread() / Módulos que la usan -> server.py, client.py```
11. ```random```-> ```uniform(), choice(), randint() / Módulos que la usan -> server.py, backend.py```
12. ```collections```-> ```deque() / Módulos que la usan -> client.py, backend.py```
13. ```sys```-> ```exit() / Módulos que la usan -> frontend.py```
14. ```PyQt5```-> ```Módulos que la usan -> server.py, backend.py, frontend.py```


### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```backend.py```-> Se encarga de la lógica del juego y ventanas, así como también de hacer de puente entre el frontend y cliente.
2. ```frontend.py```-> Se encarga de la visualización del programa, comunicándose periódicamente con el backend.
3. ```client.py```-> Se encarga de la comunicación con el servidor.
4. ```server.py```-> Se encarga de conectar a los clientes que estén usando el programa, además de realizar operaciones lógicas.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Para testear el juego en sí (y la mayor parte de la tarea) se recomienda comentar en el archivo 'server.py' lo que está en las líneas 161 a 174 (y borrar el 'else' que viene justo después, corriendo lo que estaba indentado dentro de este para que se ejecute siempre), para así evitar los errores mencionados en los siguientes puntos y poder jugar rondas indefinidamente.
2. Para las asignaciones de puntaje faltó corregir que se sumaran bien los puntos, además se genera la lista con cada [usuario, color, puntaje] en la línea 156 del archivo 'server.py', pero no se envía para ser mostrada en la interfaz.
3. Para la determinación de la victoria se incluyeron las condiciones en las líneas 162 y 164 del archivo 'server.py', pero tampoco se alcanzó a corregir el error que daba al determinar el fin de una partida. También se incluyeron los labels que iban a indicar la victoria en la interfaz de la sala de juego (QtDesigner).
4. No alcancé a corregir un error que causaba que no se viera el label con los números de la cuenta regresiva, pero los 10 segundos si pasan por detrás, solo que no se ve.
5. Para ponerle pausa al juego se debe utilizar el botón de pausa, y no la barra de espacio, la que se ocupa para comenzar cada ronda del juego. (Issue #775)
6. El juego funciona bien mediante networking, excepto cuando la velocidad llega a niveles demasiado altos (bastante improbable), donde podría ocurrir lag con respecto a los demás.
7. Se utiliza una base de datos en formato 'json'.
8. El jefe de la sala de espera es demarcado con la corona que aparece a su derecha.
9. Para el poder 'Fernando Atraviessa' se escogió una duración de 8 segundos. Además, si al momento de desactivar el poder el jugador queda entre medio de la zona del juego y la pared que está atravesando, entonces es eliminado.
10. Si un jugador pausa el juego y luego otro presiona el botón de pausa, entonces se resume el juego. (Issue #775)
11. No alcancé a utilizar el método 'disconnect' de la clase Client, el que se encargaría de cerrar el socket al cerrar las ventanas de PyQt, por esto mismo se recomienda volver a iniciar el servidor cada vez que se cierre alguna ventana.
12. Los nombres de objetos PyQt se colocaron con Mayúsculas en varios casos para poder mantener la consistencia con dicha librería (que utiliza así los nombres a diferencia del snake_case de Python).

## Referencias de código externo :book:
1. Contenidos semanas 9 a 13 del curso.
