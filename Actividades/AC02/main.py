from collections import namedtuple
import statistics as s

# NO MODIFICAR ESTA FUNCION
def foreach(function, iterable):
    for elem in iterable:
        function(elem)


# Named tuples para cada entidad
Ciudad = namedtuple("Ciudad", ["sigla_pais", "nombre"])
Pais = namedtuple("Pais", ["sigla", "nombre"])
Persona = namedtuple("Persona", [
    "nombre", "apellido", "edad", "sexo", "ciudad_residencia",
    "area_de_trabajo", "sueldo"
])

###########################


def leer_ciudades(ruta_archivo_ciudades):
    with open(ruta_archivo_ciudades, 'r', encoding='utf-8') as file:
        for city in file:
            cities = city.strip().split(",")
            yield Ciudad(*cities)


def leer_paises(ruta_archivo_paises):
    with open(ruta_archivo_paises, 'r', encoding='utf-8') as file:
        for country in file:
            c = country.strip().split(",")
            yield Pais(*c)


def leer_personas(ruta_archivo_personas):
    with open(ruta_archivo_personas, 'r', encoding='utf-8') as file:
        for person in file:
            p = person.strip().split(",")
            yield Persona(*p)


def sigla_de_pais(nombre_pais, paises):
    return [p.sigla for p in paises if p.nombre == nombre_pais][0]


def ciudades_por_pais(nombre_pais, paises, ciudades):
    sigla = sigla_de_pais(nombre_pais, paises)
    return filter(lambda x: x.sigla_pais == sigla, ciudades)


def personas_por_pais(nombre_pais, paises, ciudades, personas):
    cities = list(ciudades_por_pais(nombre_pais, paises, ciudades))
    city_names = [x.nombre for x in cities]
    return filter(lambda x: x.ciudad_residencia in city_names, personas)


def sueldo_promedio(personas):
    sueldos = [float(x.sueldo) for x in personas]
    return s.mean(sueldos)


def cant_personas_por_area_de_trabajo(personas):
    people = list(personas)
    areas = list({x.area_de_trabajo for x in people})
    return {x: len(list(filter(lambda y: y.area_de_trabajo == x, people))) for x in areas}



if __name__ == '__main__':
    RUTA_PAISES = "Paises.txt"
    RUTA_CIUDADES = "Ciudades.txt"
    RUTA_PERSONAS = "Personas.txt"

    # (1) Ciudades en Chile
    ciudades_chile = ciudades_por_pais('Chile', leer_paises(RUTA_PAISES),
                                       leer_ciudades(RUTA_CIUDADES))

    #foreach(lambda ciudad: print(ciudad.sigla_pais, ciudad.nombre), ciudades_chile)

    # (2) Personas en Chile
    personas_chile = personas_por_pais('Chile', leer_paises(RUTA_PAISES),
                                       leer_ciudades(RUTA_CIUDADES),
                                       leer_personas(RUTA_PERSONAS))

    #foreach(lambda p: print(p.nombre, p.ciudad_residencia), personas_chile)

    # (3) Sueldo promedio de personas del mundo
    sueldo_mundo = sueldo_promedio(leer_personas(RUTA_PERSONAS))
    #print('Sueldo promedio: ', sueldo_mundo)

    # (4) Cantidad de personas por profesion
    dicc = cant_personas_por_area_de_trabajo(leer_personas(RUTA_PERSONAS))

    #foreach(lambda elem: print(f"{elem[0]}: {elem[1]}"), dicc.items())
