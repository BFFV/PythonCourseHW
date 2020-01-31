# Tarea 00: DCCorreos :school_satchel:

## Consideraciones generales :octocat:

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte 1 (Registro e inicio de sesión): Hecha completa
* Parte 2 (Correos): Hecha completa
* Parte 3 (Bandeja de entrada): Hecha completa
* Parte 4 (Calendario): Hecha completa
    * Parte 4.1 (Eventos): Hecha completa
    * Parte 4.2 (Acciones Disponibles): Hecha completa
* Parte 5 (Encriptación): Hecha completa 
* Parte 6 (Bases de Datos): Hecha completa

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Para correr el programa son además necesarios los siguientes archivos:

### Módulos (se encuentran en la carpeta madre junto al módulo principal):
* ```user.py```
* ```mails.py```
* ```events.py```

### Bases de Datos (se encuentran en la carpeta ```datos```):
Estos archivos .csv se encargan de guardar la información manejada por el programa:
* ```db_emails.csv```
* ```db_users.csv```
* ```db_events.csv```
* ```old_db_emails.csv``` (sólo para testear)

Además se tienen los siguientes archivos no necesarios para la ejecución del programa:

### Bases de Datos de Respaldo (se encuentran en la carpeta ```datos_originales```):
Estos archivos .csv representan las bases de datos entregadas originalmente, y se pueden usar para reemplazar los archivos de la carpeta 'datos' en caso que se desee 'reiniciar' las bases de datos a su estado original:
* ```db_emails.csv```
* ```db_users.csv```
* ```db_events.csv```
* ```old_db_emails.csv``` (sólo para testear)

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente (todas 'built-in'):

1. ```datetime```-> ```datetime(), timedelta() / user.py, events.py```
2. ```textwrap```-> ```wrap() / mails.py, events.py```
3. ```random```-> ```randint() / mails.py```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```user.py```-> Contiene a la clase ```User``` y se encarga de las funcionalidades que involucran directamente al usuario.
2. ```mails.py```-> Contiene a la clase ```Mail``` y se encarga del envío, lectura y manejo de los correos.
2. ```events.py```-> Contiene a la clase ```Event``` y se encarga de las funcionalidades del calendario y los eventos.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Los correos guardados en la base de datos están ordenados descendientemente por fecha de envío (el más reciente es el de más abajo), esto se consideró así ya que los correos no llevan fecha de envío para poder ordenarlos.
2. Los nombres de usuario deben cumplir con el formato usuario@proveedor.dominio, donde además se cumplen las especificaciones del enunciado. Esto se hizo para que los nombres elegidos tuvieran algo de sentido y semejanza a los utilizados en internet.
3. Los textos que se guardan entre comillas simples en el .csv no pueden contener comillas simples, ya que se perdería el sentido de utilizarlas para diferenciar los caracteres literales de los de separación.
4. No se consideran los años bisiestos al momento de manejar las fechas, tal como se indicó en las Issues.
5. Para filtrar los eventos por fecha se consideró un rango delimitado por una fecha mínima y una máxima, mostrando los eventos que comiencen y terminen dentro de dicho rango, ya que esto me hacía mas sentido al momento de buscar eventos a los que se pudiera asistir dentro de un período en específico.
6. Los textos tipo etiquetas que se guardan en el .csv usando ';' para separar datos no pueden contener ';' en dichos datos, ya que se perdería el sentido de utilizarlas para separar distintos elementos.
7. Los usuarios que se inviten a los eventos o a los que se les envíen correos pueden no estar registrados en el programa, pero deben cumplir con el formato de nombre de usuario mencionado anteriormente.


## Referencias de código externo :book:
No se utilizó código externo en este programa.
