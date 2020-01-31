# Tarea 02: DCCasino :moneybag:

## Consideraciones generales :octocat:

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte 1 (Entidades): Hecha completa
    * Parte 1.1 (Clientes): Hecha completa
    * Parte 1.2 (Personal del Casino): Hecha completa
    * Parte 1.3 (Juegos): Hecha completa
    * Parte 1.4 (Instalaciones): Hecha completa
* Parte 2 (Actividades): Hecha completa
* Parte 3 (Interfaz Gráfica): Hecha completa
* Parte 4 (Simulación): Hecha completa
    * Parte 4.1 (Estadísticas): Hecha completa
    * Parte 4.2 (Parámetros): Hecha completa
* Parte 5 (Diagrama de Clases): Hecha completa
* Parte 6 (Extra): Hecha completa
    * Parte 6.1 (Uso de .gitignore): Hecha completa

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Para correr el programa son además necesarios los siguientes archivos:

### Módulos (se encuentran en la carpeta madre junto al módulo principal):
* ```parameters.py```
* ```people.py```
* ```services.py```
* ```simulation.py```

### Carpeta gui:
No se sube al repositorio. Contiene todos los archivos necesarios para el funcionamiento de la interfaz gráfica.

Además se tienen los siguientes archivos adicionales:

### Archivo de Estadísticas:
Este archivo llamado ```Statistics.txt``` es generado por el programa al momento de guardar las estadísticas de la simulación.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```random```-> ```choice(), choices(), randint(), normalvariate(), triangular(), uniform() / Módulos que la usan -> people.py, services.py, simulation.py```
2. ```sys```-> ```exit() / Módulos que la usan -> simulation.py```
3. ```statistics```-> ```mean() / Módulos que la usan -> simulation.py```
4. ```math```-> ```pi(), sqrt() / Módulos que la usan -> people.py```
5. ```collections```-> ```deque() / Módulos que la usan -> services.py```
6. ```names```-> ```get_full_name() / Módulos que la usan -> people.py``` (Debe Instalarse)

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```parameters.py```-> Contiene los distintos parámetros externos a la simulación y permite ajustarlos.
2. ```people.py```-> Contiene las clases que modelan a los clientes y al personal del casino.
3. ```services.py```-> Contiene las clases que modelan a los juegos e instalaciones del casino.
4. ```simulation.py```-> Contiene a la clase que modela la simulación del casino.
5. ```gui```-> Se encarga del funcionamiento de la interfaz gráfica. (entregado para su uso en la tarea)

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Los clientes que se retiran o son expulsados del casino no volverán a entrar durante el resto de la simulación.
2. Al aumentar la probabilidad p de que llegue un cliente el casino podría quedar muy saturado y la simulación se ralentizaría.
3. Los atributos Dinero (representación de la riqueza, no dinero actual) y Sociabilidad no son considerados Properties, ya que no varían durante la simulación.
4. El aumento de la ansiedad al tener más del doble o menos de la quinta parte del dinero inicial solo está presente mientras el cliente se encuentre en dichos rangos de dinero, es decir, no es permanente.
5. Si el cliente queda con el dinero menor a 1 (solo podría ir al baño), se considera que lo perdió todo y su stamina baja a 0 (Issue #430).
6. Los clientes solo pueden realizar una cierta acción (por ejemplo apostar) si es que tienen la cantidad necesaria de dinero para ello.
7. Cuando un kibitzer termina de estudiar la ruleta y decide ir a predecir resultados, esta será su única decisión posible hasta que hayan pasado las 'v' rondas o bien lo hayan expulsado.
8. Los juegos requieren de al menos 1 dealer para funcionar, pero no hay un límite para estos.
9. La jornada de trabajo del personal se calculó obteniendo los tiempos de trabajo y descanso con las distribuciones indicadas, SIN considerar que estos podrían entrar a trabajar más de una vez por día si es que el tiempo de descanso es muy corto (Issue #427).
10. Basta con que 1 dealer mafioso esté presente en una ruleta para que aumente la probabilidad de ganar de un cliente coludido con la mafia. Por otro lado, la probabilidad de sorprender a un cliente haciendo trampa es mayor mientras más dealers haya en la ruleta.
11. El tarot tiene una probabilidad del 50% de aumentar la suerte en 0.2, o disminuir la stamina en 0.2.
12. Al apostar en la ruleta y ganar, se obtiene la apuesta multiplicada por el factor indicado SIN descontar la apuesta original realizada (si apuesta 1 al color verde y gana, obtiene 5 y NO pierde la apuesta de 1). 
13. Las filas de espera tienen una capacidad máxima, la que se puede modificar en el módulo ```parameters.py```, aunque no es recomendable aumentarla demasiado.
14. El costo de hablar con Tini no cuenta para las ganancias del casino, pero sí para las pérdidas de los clientes.
15. Los clientes se colocarán en el borde de las instalaciones/juegos que estén ocupando (también para los que estén en la fila).
16. Cuando quieran conversar, los clientes se colocarán o en la zona central (sobre las ruletas y bajo el restobar), o en la pequeña zona un poco más abajo de la entrada.
17. Para hablar con Tini, los clientes se dirigen al extremo derecho central del casino (sobre el tragamonedas).
18. Se utilizaron un par de veces los métodos updatePixmap() y setFixedSize(x, y) que venían con la interfaz para arreglar el tamaño de las entidades y sus bordes.
19. Para las ganancias del casino se cuentan las ganancias directas de los juegos, los pozos FINALES de los tragamonedas y los costos de las instalaciones.
20. Algunas clases en el diagrama de la tarea están vacías, esto es debido a que sólo se utilizan para facilitar la creación de entidades en la interfaz sin añadir ningún atributo o método nuevo (por ejemplo Building), o bien sólo hacen Overriding de métodos de la SuperClase (por ejemplo Bar).
21. Cuando un cliente gana en el tragamonedas y vacía el pozo, esto no cuenta como pérdida para el casino (ya que el dinero nunca perteneció originalmente a este).
22. Se pueden seleccionar 3 velocidades distintas para la simulación (5, 1 y 0.1 milisegundos de delay por cada tick). Al utilizar la más lenta la simulación tarda entre 7-8 minutos para 1 día. Para la velocidad media tarda entre 5-6 minutos para 2 días. Finalmente para la más alta tarda alrededor de 6 minutos para 3 días (estos valores pueden cambiar dependiendo del pc utilizado).
23. Los horarios de entrada iniciales del personal son escogidos de manera semi-aleatoria (algunos fijos, otros no).

## Referencias de código externo :book:
No se utilizó código externo en este programa.
