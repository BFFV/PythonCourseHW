# Tarea 05: DCConnect :oncoming_bus:

## Consideraciones generales :octocat:

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte 1 (Flujo del programa): Hecha Completa
    * Parte 1.1 (Inicio de sesión): Hecha Completa
    * Parte 1.2 (Flujo de la información): Hecha Completa
* Parte 2 (Web services): Hecha Completa
    * Parte 2.1 (Foursquare): Hecha Completa
    * Parte 2.2 (ipstack): Hecha Completa
    * Parte 2.3 (Transantiago): Hecha Completa
* Parte 3 (Expresiones regulares): Hecha Completa
* Parte 4 (Extra): Hecha Completa
    * Parte 4.1 (Uso de .gitignore): Hecha Completa

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Para correr el programa son además necesarios los siguientes archivos:

### Módulos (se encuentran en la carpeta madre junto al módulo principal, excepto credentials):
* ```functionalities.py```
* ```credentials.py```

### Credenciales (se deben utilizar las del corrector):
No se suben al repositorio. Se debe crear un archivo llamado ```credentials.py``` en la carpeta madre (junto a los otros módulos), y dentro se deben definir las siguientes variables (utilizando las credenciales del corrector para las API):

- SQUARE_CLIENT = 'Aquí va el string que representa la credencial del cliente de Foursquare'
- SQUARE_SECRET = 'Aquí va el string que representa la clave secreta de Foursquare'
- STACK_KEY = 'Aquí va el string que representa la clave de acceso de ipstack'

Al definir estas variables en el archivo, se podrán importar y utilizar para las requests. Este paso debe ser realizado antes de probar el programa, de otro modo este no funcionará correctamente.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```requests```-> ```get() / Módulos que la usan -> functionalities.py```
2. ```re```-> ```fullmatch() / Módulos que la usan -> functionalities.py```
3. ```math```-> ```radians(), sin(), cos(), asin(), sqrt() / Módulos que la usan -> functionalities.py```
4. ```datetime```-> ```datetime() / Módulos que la usan -> functionalities.py```
5. ```collections```-> ```deque() / Módulos que la usan -> functionalities.py```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```functionalities.py```-> Se encarga de las funcionalidades del programa.
2. ```credentials.py```-> Contiene las credenciales de las API. (no se sube al repositorio)

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Para la búsqueda de FourSquare se utiliza el límite máximo de 50 resultados, y se muestran el nombre, dirección y categorías (no aparecen más datos relevantes).
2. Al elegir paraderos de destino se utilizan los 3 más cercanos al destino para evitar seleccionar el más cercano y que no se pueda llegar a él.
3. Se buscan los 100 paraderos más cercanos al usuario, y se escoge el más cercano que tenga la misma ruta que el paradero de destino. En caso de que ninguno sirva entre esos 100, se le indica al usuario que no hay paraderos de origen válidos (esto porque con más resultados se vuelve demasiado lento y en un punto la API se sobrecarga).
4. Una vez obtenido el paradero de origen, se muestran todas las micros que están llegando a ese paradero y van en dirección al destino. En caso de que vayan en la otra dirección se ignoran, ya que esto significa que nunca llegarán al destino (utilizan paraderos distintos en cada dirección). En caso de que ninguna micro próxima al paradero sirva, se le indica al usuario que no hay micros disponibles.
5. Por los puntos anteriores, se recomienda probar el programa durante las horas más activas del transporte público, de manera que sean menos los casos en los que no hay micros o paraderos válidos para el usuario (aún así, no existen muchos casos en los que se pueda llegar directamente a un lugar con sólo una micro, por lo que una gran cantidad de resultados entregarán que no hay ruta o micros).
6. Para que el programa funcione correctamente se debe realizar lo explicado anteriormente en la sección de Ejecución, utilizando las credenciales propias del corrector para hacer las requests.
7. Las categorías de FourSquare deben ser ingresadas en inglés (tal como aparecen en la documentación).
8. Cuando la API del Transantiago no responde (error explicado en el enunciado), se muestra un mensaje indicándolo y se vuelve a intentar hasta que funcione (en general no toma muchos intentos).
9. El programa se demora entre 10 segundos y un par de minutos en procesar el flujo necesario para mostrar la información al usuario.
10. Si no se ingresa nada al elegir filtrar por categoría, se muestran resultados cualquiera.

## Referencias de código externo :book:
1. Contenidos semana 14 del curso.
