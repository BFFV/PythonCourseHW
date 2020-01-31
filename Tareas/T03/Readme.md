# Tarea 03: Electromatic :zap:

## Consideraciones generales :octocat:

### Cosas implementadas y no implementadas :white_check_mark: :x:

* Parte 1 (Red Eléctrica): Hecha completa
    * Parte 1.1 (Cálculo de la Demanda): Hecha completa
    * Parte 1.2 (Flujo de Potencia): Hecha completa
* Parte 2 (Modificación de la Red): Hecha completa
    * Parte 2.1 (Agregar y Remover Aristas): Hecha completa
    * Parte 2.2 (Agregar Nodos): Hecha completa
    * Parte 2.3 (Remover Nodos): Hecha completa
* Parte 3 (Consultas): Hecha completa
* Parte 4 (Excepciones): Hecha completa
* Parte 5 (Testing): Hecha completa
* Parte 6 (Interacción con Consola): Hecha completa
* Parte 7 (Bases de Datos): Hecha completa
* Parte 8 (Entregable): Hecha completa
* Parte 9 (Extra): Hecha completa
    * Parte 9.1 (Uso de .gitignore): Hecha completa

## Ejecución :computer:
El módulo principal de la tarea a ejecutar es  ```main.py```. Para correr el programa son además necesarios los siguientes archivos:

### Módulos (se encuentran en la carpeta madre junto al módulo principal):
* ```entities.py```
* ```functionalities.py```
* ```structures.py```
* ```testing.py```

### Bases de Datos (se deben colocar en las subcarpetas dentro de ```bd```):
No se suben al repositorio. Contienen todos los datos de la red eléctrica inicial del programa.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. ```csv```-> ```reader() / Módulos que la usan -> structures.py```
2. ```textwrap```-> ```indent(), wrap() / Módulos que la usan -> structures.py```
3. ```unittest```-> ```TestCase, TestLoader(), TextTestRunner() / Módulos que la usan -> testing.py```

### Librerías propias
Por otro lado, los módulos que fueron creados fueron los siguientes:

1. ```entities.py```-> Contiene las clases que modelan a las distintas entidades de la red y a las excepciones.
2. ```functionalities.py```-> Se encarga de las funcionalidades del programa (modificar red y consultas).
3. ```structures.py```-> Contiene las clases que modelan a las estructuras de datos propias.
4. ```testing.py```-> Se utiliza para realizar tests unitarios sobre el programa.

## Supuestos y consideraciones adicionales :thinking:
Los supuestos que realicé durante la tarea son los siguientes:

1. Se asume que se utilizarán los mismos nombres para las distintas columnas de las bases de datos (aunque no es necesario que estén en el mismo orden).
2. Se asume que los nombres de los sistemas serán los mismos en la base de datos ('SING', 'SIC', 'AYSEN', 'MAGALLANES').
3. Puede haber cualquier cantidad de Subestaciones Elevadoras en un sistema (incluso 0).
4. Al calcular la demanda de la red, primero se obtiene la demanda de cada Elevadora utilizando un algoritmo DFS que se guía por los cálculos del enunciado. A continuación se suman estas demandas solamente para las Elevadoras que están conectadas con alguna Central Generadora (de otra manera estarían aisladas). Finalmente se distribuye la demanda de estas Elevadoras de manera equitativa entre las Centrales que les proveen la energía y se suman a la demanda las pérdidas que ocurren por la resistencia de los cables entre cada Central y Elevadora (se consideran estas pérdidas con respecto a la energía REAL que les pueden mandar las Centrales a cada Elevadora, ya que en realidad no son 'parte' de la demanda de la red, sino un efecto 'colateral' al transmitir la energía hacia la red).
5. Está controlado que no se puedan formar ciclos dirigidos en la red, aunque no es necesario.
6. La resistencia siempre será positiva y como máximo será igual a 0,999.
7. Para el flujo de potencia, cada Central proporcionará la cantidad de energía exacta demandada por cada una de las Elevadoras conectadas, y en caso de que no genere lo suficiente para satisfacerlas todas, repartirá su máxima capacidad de producción de manera proporcional a la demanda de cada Elevadora conectada.
8. Se controla en las conexiones que no puedan haber Casas recibiendo de una Subestación de Distribución y de otra Casa a la vez, y pueden estar conectadas a más de una Subestación de Distribución siempre y cuando pertenezcan a la misma comuna.
9. Se asume que no se realizarán consultas con 'strings' que incluyan caracteres como los tildes (ya que el csv reader no es capaz de decodificar dichos caracteres correctamente al cargar la base de datos, y los guarda en el programa con caracteres 'raros'), tal como se indicó en una Issue.
10. Cada vez que se realiza una modificación a la red se recalcula la demanda y el flujo de potencia.
11. Pueden existir nodos aislados en la red, que pertenezcan a un sistema pero no estén conectados a la red en ese momento.
12. Al remover un nodo, la energía que le llegaba 'desaparece' de la red debido a que se vuelve a calcular la demanda y el flujo, en los que ya no se considera al nodo eliminado.
13. Para la consulta 'Energía Total Consumida en una Comuna' no se consideran las pérdidas por la resistencia, ya que se habla del consumo REAL de cada Casa y Subestación de Distribución de dicha comuna.
14. Para las consultas de mayor y menor consumidor, en el caso de que hayan múltiples Casas con el mismo consumo, se elige cualquiera (una sola). Además, se consideran las Casas aisladas mencionadas anteriormente para estas consultas.
15. Para el testing se asume que se utilizarán las bases de datos 'large' entregadas, ya que en caso contrario todos los resultados de los test podrían cambiar y causar que estos fallen.
16. Se crearon unas versiones 'adaptadas' de las consultas y funcionalidades del programa para su uso en el testing, ya que las originales están pensadas para interactuar directamente con el usuario y obtener los parámetros por medio de inputs.
17. La función que se utiliza para hacer el testing de la excepción ElectricalOverload es una combinación entre las funciones de agregar nodo y agregar arista (ya que la única manera de generar el error rápidamente en la base de datos era agregando un consumidor con una gran demanda y conectándolo a un sistema que posea la energía suficiente para que ocurra la sobrecarga, en este caso se utilizó el sistema 'AYSEN').
18. En el módulo ```structures.py``` se puede editar el nombre de la variable db_size (está al comienzo) para cambiar la carpeta de las bases de datos (debe estar dentro de la carpeta bd).
19. Al momento de cargar las bases de datos, se desempaquetan las estructuras prohibidas retornadas por el csv reader dentro del ```__init__``` de las estructuras propias (como se mencionó en las Issues).
20. Los 4 sistemas eléctricos (individualmente) poseen un ```__repr__``` que muestra el sistema desde las Elevadoras hasta las Casas de 'Tercer Nivel'.
21. En el tearDown del testing solo se colocó un mensaje indicando el término de cada test, ya que el setUp ya se encargaba de reiniciar la red eléctrica después de cada modificación.
22. Al simular o realizar modificaciones a la red solo se muestran mensajes indicando si es que se produjeron o no errores, y en caso de que hayan ocurrido se especifica el error encontrado.


## Referencias de código externo :book:
1. Contenidos semanas 6, 7 y 8 del curso.
