# Tarea 01: Cruncher Flights :airplane:

## Consideraciones generales :octocat:

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte 1 (Lectura de Archivos): Hecha completa
* Parte 2 (Consultas): Hecha completa
    * Parte 2.1 (Consultas que Retornan Bases de Datos): Hecha completa
    * Parte 2.2 (Consultas que No Retornan Bases de Datos): Hecha completa
* Parte 3 (Interacción con Consola): Hecha completa
* Parte 4 (Archivo Output): Hecha completa
* Parte 5 (Extras): Hecha completa
    * Parte 5.1 (Uso de .gitignore): Hecha completa

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Para correr el programa son además necesarios los siguientes archivos:

### Módulos (se encuentran en la carpeta madre junto al módulo principal):
* ```user.py```
* ```utils.py```
* ```f_queries.py```
* ```iic2233_utils.py```

### Bases de Datos (se deben colocar en las subcarpetas dentro de ```data``` según su tamaño):
Estos archivos .csv se encargan de guardar la información manejada por el programa:
* ```airports.csv```
* ```flights.csv```
* ```flights-passengers2.csv```
* ```passengers.csv```

Además se tienen los siguientes archivos adicionales:

### Archivos de Consultas:
Estos archivos .txt contienen consultas en cada línea, y se pueden leer con el programa utilizando la opción de 'Abrir un archivo con consultas'. Por defecto se incluye uno llamado ```queries.txt```, pero se pueden abrir otros.

### Archivo de Output:
Este archivo llamado ```output.txt``` es generado por el programa al momento de guardar las consultas ingresadas por el usuario. Posteriormente puede ser leído y editado dentro del programa.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente (todas 'built-in'):

1. ```textwrap```-> ```wrap() / Módulos que la usan -> user.py```
2. ```os.path```-> ```exists() / Módulos que la usan -> user.py```
3. ```functools```-> ```reduce() / Módulos que la usan -> user.py```
4. ```collections```-> ```namedtuple(), Counter() / Módulos que la usan -> f_queries.py```
5. ```operator```-> ```lt(), le(), gt(), ge(), eq(), ne() / Módulos que la usan -> f_queries.py```
6. ```datetime```-> ```datetime() / Módulos que la usan -> f_queries.py```
7. ```itertools```-> ```tee() / Módulos que la usan -> f_queries.py```
8. ```math```-> ```radians(), sin(), cos(), asin(), sqrt() / Módulos que la usan -> f_queries.py```
9. ```ast```-> ```literal_eval() / Módulos que la usan -> iic2233_utils.py```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```user.py```-> Se encarga de las funcionalidades asociadas a la interacción con el usuario y sus elecciones.
2. ```utils.py```-> Se encarga de interpretar las consultas ingresadas.
3. ```f_queries.py```-> Se encarga de realizar las consultas directamente en las bases de datos.
4. ```iic2233_utils.py```-> Se encarga de proveer las funciones auxiliares parse() y foreach(). (entregado para su uso en la tarea)

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Se utilizarán los nombres mencionados más arriba para las bases de datos, y éstas se encontrarán en las carpetas respectivas de acuerdo a su tamaño.
2. Las consultas ingresadas directamente por el usuario siempre serán válidas y estarán bien escritas, como se indica en el enunciado.
3. Para seleccionar el tamaño de la base de datos se deberá editar la variable global 'db_size' que se encuentra al comienzo del módulo ```f_queries.py```. Por default está seleccionado el tamaño 'medium' (Issue #339).
4. Todos los id de las bases de datos se van generando como string para mantener consistencia en los datos.
5. Para los casos de 'empate' en las consultas 'favourite_airport', 'popular_airports' y 'furthest_distance' se entrega cualquiera al azar.
6. Para los casos en los que un pasajero no se encuentre entre los viajes (si es que existen estos casos) en las consultas 'favourite_airport' y 'passenger_miles', NO se entregarán dichos pasajeros en los diccionarios con los resultados.
7. En las consultas 'passenger_miles' y 'furthest_distance' se asume que se entregará el generador de aeropuertos 'extra' como segundo parámetro, tal como se indicó en una Issue.
8. Las keys del diccionario retornado por 'passenger_miles' corresponden a los id de cada pasajero, de manera que dicho diccionario sea más accesible en el caso hipotético de que se use posteriormente.
9. La consulta 'popular_airports' retorna una lista.
10. En la consulta 'airport_passengers' se asume que una persona 'viajó' tanto por el aeropuerto de despegue como el de aterrizaje, tal como se indica en el enunciado.
11. Para el funcionamiento correcto de la interfaz del programa se colocaron varias condiciones 'if' y algunas variables mutables dentro del 'while' entregado, con el fin de poder acceder a cada menú y soportar el ingreso de inputs no válidos infinitos sin tener que recurrir al uso de Recursión (el que en este caso no parecía una buena práctica ya que limita el programa).
12. Las fechas se generan y guardan como string (sólo son transformadas a datetime al momento de comparar un par de fechas, por lo que no quedan ocupando espacio en la memoria), por lo que no se utilizaron los 'ticks' en el programa.
13. Al eliminar consultas del archivo 'ouput.txt', las que se conservan cambian sus respectivos números de consulta a los correspondientes según su orden.
14. Al realizar muchas consultas a la vez en las bases de datos de tamaño 'large', puede que se tarde unos segundos en procesarlas (45 segundos aprox. para procesar TODAS las del 'queries.txt' al mismo tiempo) dependiendo de la capacidad de procesamiento del pc.
15. Al eliminar algunas consultas del archivo 'output.txt' (no todas) puede que se tarde un rato si es que posee demasiadas líneas (SOBRE 20 segundos para 'output.txt' con tamaño del orden de megabytes) dependiendo de la capacidad de procesamiento del pc.

## Referencias de código externo :book:

Para realizar mi tarea saqué código de:
1. (https://docs.python.org/3.6/): Se obtuvo información de como usar las librerías 'built-in' (mencionadas más arriba) en la documentación de Python.
2. (https://en.wikipedia.org/wiki/Haversine_formula): Se obtuvieron detalles sobre el uso de la fórmula de Haversine.
