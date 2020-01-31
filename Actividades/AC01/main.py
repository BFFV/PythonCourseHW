from collections import namedtuple, defaultdict, deque

"""
Aquí están las estructuras de datos para guardar la información respectiva.

NO MODIFICAR.
"""

# Como se vio en la ayudantía, hay varias formas de declarar una namedtuple :)
Entrenador = namedtuple('Entrenador', 'nombre apellido')
Pokemon = namedtuple('Pokemon', ['nombre', 'tipo', 'max_solicitudes'])
Solicitud = namedtuple('Solicitud', ['id_entrenador', 'id_pokemon'])

################################################################################
"""
En esta sección debe completar las funciones para cargar los archivos al sistema.

Puedes crear funcionas auxiliar si tú quieres, ¡pero estas funciones DEBEN
retornar lo pedido en el enunciado!
"""

def cargar_entrenadores(ruta_archivo):
    """
    Esta función debería leer el archivo archivo_entrenadores y cargarlo usando
    las estructuras entregadas.
    """
    trainer_data = open(ruta_archivo, encoding="utf-8")
    trainer_dict = dict()
    for trainer in trainer_data:
        id, name, last = trainer.strip().split(";")
        trainer_dict[id] = Entrenador(name, last)
    return trainer_dict




def cargar_pokemones(ruta_archivo):
    """
    Esta función debería leer el archivo archivo_pokemones y cargarlo usando las
    estructuras entregadas.
    """
    pokemon_data = open(ruta_archivo, encoding="utf-8")
    pokemon_dict = dict()
    for pokemon in pokemon_data:
        id, name, tipo, max_sol = pokemon.strip().split(";")
        pokemon_dict[id] = Pokemon(name, tipo, int(max_sol))
    return pokemon_dict


def cargar_solicitudes(ruta_archivo):
    """
    Esta función debería leer el archivo archivo_solicitudes y cargarlo usando
    las estructuras entregadas.
    """
    sol_data = open(ruta_archivo, encoding="utf-8")
    sol_dict = defaultdict(deque)
    for sol in sol_data:
        trainer_id, pokemon_id = sol.strip().split(";")
        sol_dict[pokemon_id].append(Solicitud(trainer_id, pokemon_id))
    return sol_dict


################################################################################

"""
Lógica del Sistema.
Debes completar esta función como se dice en el enunciado.
"""

def sistema(modo, entrenadores, pokemones, solicitudes):
    """
    Esta función se encarga de llevar a cabo la 'simulación', de acuerdo al modo
    entregado.
    """
    trainer_wins = defaultdict(list)
    if modo == "1":
        for p_id in pokemones.keys():
            pokemon = pokemones[p_id]
            max_sol = pokemon.max_solicitudes
            sol = solicitudes[p_id]
            win = ""
            for i in range(int(max_sol)):
                win = sol.popleft().id_entrenador
            if pokemon not in trainer_wins[win]:
                trainer_wins[win].append(pokemon)
        return trainer_wins
    else:
        for p_id in pokemones.keys():
            pokemon = pokemones[p_id]
            max_sol = pokemon.max_solicitudes
            sol = solicitudes[p_id]
            win = ""
            for i in range(int(max_sol)):
                win = sol.pop().id_entrenador
            if p_id not in trainer_wins[win]:
                trainer_wins[win].append(pokemon)
        return trainer_wins



################################################################################
"""
Funciones de consultas, deben rellenarlos como dice en el enunciado :D.
"""

def pokemones_por_entrenador(id_entrenador, resultado_simulacion):
    """
    Esta función debe retornar todos los pokemones que ganó el entrenador con el
    id entregado.

    Recuerda que esta función debe retornar una lista.
    """
    return resultado_simulacion[id_entrenador]

def mismos_pokemones(id_entrenador1, id_entrenador2, resultado_simulacion):
    """
    Esta función debe retornar todos los pokemones que ganó tanto el entrenador
    con el id_entrenador1 como el entrenador con el id_entrenador2.

    Recuerda que esta función debe retornar una lista.
    """
    trainer_a = set(resultado_simulacion[id_entrenador1])
    trainer_b = set(resultado_simulacion[id_entrenador2])
    repetidos = trainer_a & trainer_b
    return list(repetidos)

def diferentes_pokemones(id_entrenador1, id_entrenador2, resultado_simulacion):
    """
    Esta función debe retornar todos los pokemones que ganó el entrenador con
    id_entrenador1 y que no ganó el entrenador con id_entrenador2.

    Recuerda que esta función debe retornar una lista.
    """
    trainer_a = set(resultado_simulacion[id_entrenador1])
    trainer_b = set(resultado_simulacion[id_entrenador2])
    distintos = trainer_a - trainer_b
    return list(distintos)


if __name__ == '__main__':

    ############################################################################
    """
    Poblando el sistema.
    Ya se hacen los llamados a las funciones, puedes imprimirlos para ver si se
    cargaron bien.
    """

    entrenadores = cargar_entrenadores('entrenadores.txt')
    pokemones = cargar_pokemones('pokemones.txt')
    solicitudes = cargar_solicitudes('solicitudes.txt')

    # print(entrenadores)
    # print(pokemones)
    # print(solicitudes)

    ################################   MENU   ##################################
    """
    Menú.
    ¡No debes cambiar nada! Simplemente nota que es un menú que pide input del
    usuario, y en el caso en que este responda con "1" ó "2", entonces se hace
    el llamado a la función. En otro caso, el programa termina.
    """

    eleccion = input('Ingrese el modo de lectura de solicitudes:\n'
                 '1: Orden de llegada\n'
                 '2: Orden Inverso de llegada\n'
                 '>\t')

    if eleccion in {"1", "2"}:
        resultados_simulacion = sistema(eleccion, entrenadores,
                                        pokemones, solicitudes)
    else:
        exit()

    ##############################   Pruebas   #################################
    """
    Casos de uso.

    Aquí pueden probar si sus consultas funcionan correctamente.
    """
