import entities as e
import structures as s


# Modificar la red
def new_connection(network, simulation=False):
    system = None
    change = False
    try:
        entities = s.Container(e.Generation, e.Intensification,
                               e.Transmission, e.Distribution, e.House)
        text = 'Seleccione el tipo de entidad de origen:\n1) Generadora\n' \
               '2) Elevadora\n3) Transmisión\n4) Distribución\n5) Consumo'
        origin = validate_input(text, entities)
        text = 'Ingrese el Id de la entidad de origen:'
        origin_id = validate_input(text, 'int')
        entities.pop_left()
        text = 'Seleccione el tipo de entidad de destino:\n1) Elevadora\n' \
               '2) Transmisión\n3) Distribución\n4) Consumo'
        destiny = validate_input(text, entities)
        text = 'Ingrese el Id de la entidad de destino:'
        destiny_id = validate_input(text, 'int')
        origin_node = None
        destiny_node = None
        for sys in network:
            if not (origin_node and destiny_node):
                origin_node = sys.nodes.get_node(origin, origin_id)
                destiny_node = sys.nodes.get_node(destiny, destiny_id)
                if origin_node and destiny_node:
                    system = sys
                else:
                    origin_node = None
                    destiny_node = None
        if not system:
            raise e.ForbiddenAction('Agregar Arista',
                                    'entre entidades inexistentes o de '
                                    'distintos sistemas!')
        for connection in origin_node.connections:
            if connection[0] == destiny_node:
                raise e.ForbiddenAction('Agregar Arista', 'entre entidades '
                                                          'ya conectadas!')
        incompatibility = f'desde {origin_node.value.__class__.__name__} ' \
                          f'hacia {destiny_node.value.__class__.__name__}!'
        if isinstance(origin_node.value, e.Generation):
            if not isinstance(destiny_node.value, e.Intensification):
                raise e.ForbiddenAction('Agregar Arista', incompatibility)
        elif isinstance(origin_node.value, e.Intensification):
            if not isinstance(destiny_node.value, e.Transmission):
                raise e.ForbiddenAction('Agregar Arista', incompatibility)
            if len(destiny_node.origins):
                raise e.ForbiddenAction(
                    'Agregar Arista', 'hacia una Subestación de Transmisión '
                                      'que ya está conectada a otra '
                                      'Subestación Elevadora!')
        elif isinstance(origin_node.value, e.Transmission):
            if not isinstance(destiny_node.value, e.Distribution):
                raise e.ForbiddenAction('Agregar Arista', incompatibility)
            if len(destiny_node.origins):
                raise e.ForbiddenAction(
                    'Agregar Arista', 'hacia una Subestación de Distribución '
                                      'que ya está conectada a otra '
                                      'Subestación de Transmisión!')
        elif isinstance(origin_node.value, e.Distribution):
            if not isinstance(destiny_node.value, e.House):
                raise e.ForbiddenAction('Agregar Arista', incompatibility)
            if destiny_node.value.commune != origin_node.value.commune:
                raise e.ForbiddenAction(
                    'Agregar Arista', 'entre una Subestación de Distribución '
                                      'y una Casa de comunas distintas!')
            for root in destiny_node.origins:
                if isinstance(root.value, e.House):
                    raise e.ForbiddenAction(
                        'Agregar Arista',
                        'entre una Subestación de Distribución y una Casa '
                        'que está colgada!')
        else:
            if not isinstance(destiny_node.value, e.House):
                raise e.ForbiddenAction('Agregar Arista', incompatibility)
            if destiny_node.value.commune != origin_node.value.commune:
                raise e.ForbiddenAction(
                    'Agregar Arista', 'entre Casas que tienen '
                                      'comunas distintas!')
            for root in destiny_node.origins:
                if isinstance(root.value, e.Distribution):
                    raise e.ForbiddenAction(
                        'Agregar Arista',
                        'entre una Casa y otra Casa que ya está conectada '
                        'directamente a una Subestación de Distribución!')
        text = 'Ingrese la distancia entre ambas entidades:'
        distance = validate_input(text, 'float')
        start = s.Container(origin, origin_id)
        end = s.Container(destiny, destiny_id)
        change = True
        system.add_connection(start, end, distance)
    except e.ForbiddenAction as err:
        print(err)
        if change:
            start = system.backup[0]
            end = system.backup[1]
            start.remove(end)
            system.system_demand()
            system.system_energy()
    except e.ElectricalOverload as err:
        print(err)
        if change:
            start = system.backup[0]
            end = system.backup[1]
            start.remove(end)
            system.system_demand()
            system.system_energy()
    else:
        if simulation:
            start = system.backup[0]
            end = system.backup[1]
            start.remove(end)
            system.system_demand()
            system.system_energy()
            print('El cambio no produjo problemas en la red!\n')
        else:
            print('Los cambios se han realizado correctamente!\n')


def delete_connection(network, simulation=False):
    change = False
    system = None
    try:
        entities = s.Container(e.Generation, e.Intensification,
                               e.Transmission, e.Distribution, e.House)
        text = 'Seleccione el tipo de entidad de origen:\n1) Generadora\n' \
               '2) Elevadora\n3) Transmisión\n4) Distribución\n5) Consumo'
        origin = validate_input(text, entities)
        text = 'Ingrese el Id de la entidad de origen:'
        origin_id = validate_input(text, 'int')
        entities.pop_left()
        text = 'Seleccione el tipo de entidad de destino:\n1) Elevadora\n' \
               '2) Transmisión\n3) Distribución\n4) Consumo'
        destiny = validate_input(text, entities)
        text = 'Ingrese el Id de la entidad de destino:'
        destiny_id = validate_input(text, 'int')
        origin_node = None
        for sys in network:
            if not origin_node:
                origin_node = sys.nodes.get_node(origin, origin_id)
                if origin_node:
                    system = sys
        if not origin_node:
            raise e.ForbiddenAction('Remover Arista',
                                    'para un nodo origen inexistente!')
        exists = False
        for connection in origin_node.connections:
            if isinstance(connection[0].value, destiny) \
                    and (connection[0].value.id == destiny_id):
                exists = True
        if not exists:
            raise e.ForbiddenAction('Remover Arista',
                                    'en una arista inexistente!')
        start = s.Container(origin, origin_id)
        end = s.Container(destiny, destiny_id)
        change = True
        system.remove_connection(start, end)
    except e.ForbiddenAction as err:
        print(err)
    except e.ElectricalOverload as err:
        print(err)
        if change:
            start = system.backup[0]
            end = system.backup[1]
            distance = system.backup[2]
            start.connect(end, distance)
            system.system_demand()
            system.system_energy()
    else:
        if simulation:
            start = system.backup[0]
            end = system.backup[1]
            distance = system.backup[2]
            start.connect(end, distance)
            system.system_demand()
            system.system_energy()
            print('El cambio no produjo problemas en la red!\n')
        else:
            print('Los cambios se han realizado correctamente!\n')


def new_node(network, simulation=False):
    change = False
    system = None
    try:
        entities = s.Container(e.Generation, e.Intensification,
                               e.Transmission, e.Distribution, e.House)
        text = 'Seleccione el tipo de nodo a agregar:\n1) Generadora\n' \
               '2) Elevadora\n3) Transmisión\n4) Distribución\n5) Consumo'
        node_entity = validate_input(text, entities)
        _type = ''
        power = 0
        if node_entity == e.Generation:
            energy = s.Container('Termoelectrica', 'Solar', 'Biomasa')
            text = 'Seleccione el tipo de planta:\n1) Termoeléctrica\n' \
                   '2) Solar\n3) Biomasa'
            _type = validate_input(text, energy)
            text = 'Ingrese la potencia de la planta (MW):'
            power = validate_input(text, 'power')
        text = 'Ingrese el Id del nuevo nodo:'
        _id = validate_input(text, 'int')
        systems = s.Container('SING', 'SIC', 'AYSEN', 'MAGALLANES')
        text = 'Seleccione el sistema del nuevo nodo:\n1) SING\n2) SIC\n3) ' \
               'AYSEN\n4) MAGALLANES'
        _system = validate_input(text, systems)
        text = 'Ingrese la provincia del nuevo nodo:'
        province = validate_input(text, 'string')
        text = 'Ingrese la comuna del nuevo nodo:'
        commune = validate_input(text, 'string')
        name = None
        if node_entity != e.House:
            text = 'Ingrese el nombre del nuevo nodo:'
            name = validate_input(text, 'string')
        if node_entity != e.Generation:
            if node_entity == e.House:
                text = 'Ingrese el consumo propio del nuevo nodo (kW):'
                consumption = validate_input(text, 'float')
            else:
                text = 'Ingrese el consumo propio del nuevo nodo (MW):'
                consumption = validate_input(text, 'float')
            entity = node_entity(_id, _system, province, commune, name,
                                 consumption)
        else:
            entity = node_entity(_type, power, _id, _system, province,
                                 commune, name)
        for sys in network:
            if sys.nodes.get_node(node_entity, entity.id):
                raise e.ForbiddenAction(
                    'Agregar Nodo', 'para un nodo ya existente (Id y Tipo)!')
            elif sys.name == _system:
                system = sys
        change = True
        node = s.SystemNode(entity)
        system.add_node(node)
    except e.ForbiddenAction as err:
        print(err)
    except e.ElectricalOverload as err:
        print(err)
        if change:
            system.nodes.delete(system.backup)
            if isinstance(system.backup.value, e.Intensification):
                system.base.remove(system.backup)
            system.system_demand()
            system.system_energy()
    else:
        if simulation:
            system.nodes.delete(system.backup)
            if isinstance(system.backup.value, e.Intensification):
                system.base.remove(system.backup)
            system.system_demand()
            system.system_energy()
            print('El cambio no produjo problemas en la red!\n')
        else:
            print('Los cambios se han realizado correctamente!\n')


def delete_node(network, simulation=False):
    change = False
    system = None
    try:
        entities = s.Container(e.Generation, e.Intensification,
                               e.Transmission, e.Distribution, e.House)
        text = 'Seleccione el tipo de nodo a remover:\n1) Generadora\n' \
               '2) Elevadora\n3) Transmisión\n4) Distribución\n5) Consumo'
        entity = validate_input(text, entities)
        text = 'Ingrese el Id del nodo a remover:'
        _id = validate_input(text, 'int')
        origin_node = None
        for sys in network:
            if not origin_node:
                origin_node = sys.nodes.get_node(entity, _id)
                if origin_node:
                    system = sys
        if not system:
            raise e.ForbiddenAction('Remover Nodo', 'para un nodo inexistente!')
        node = s.Container(entity, _id)
        change = True
        system.remove_node(node)
    except e.ForbiddenAction as err:
        print(err)
    except e.ElectricalOverload as err:
        print(err)
        if change:
            recover_nodes = system.backup[0]
            recover_connections = system.backup[1]
            for node in recover_nodes:
                system.nodes.add(node)
            for connection in recover_connections:
                connection[0].connect(connection[1], connection[2])
            system.system_demand()
            system.system_energy()
    else:
        if simulation:
            recover_nodes = system.backup[0]
            recover_connections = system.backup[1]
            for node in recover_nodes:
                system.nodes.add(node)
            for connection in recover_connections:
                connection[0].connect(connection[1], connection[2])
            system.system_demand()
            system.system_energy()
            print('El cambio no produjo problemas en la red!\n')
        else:
            print('Los cambios se han realizado correctamente!\n')


# Consultas
def energy_by_commune(network):
    try:
        system = None
        text = 'Ingrese el nombre de la comuna:'
        commune = validate_input(text, 'string')
        for sys in network:
            if not system:
                for node in sys.nodes:
                    if node.value:
                        if node.value.commune == commune:
                            system = sys
        if not system:
            raise e.InvalidQuery(f"La comuna '{commune}' no existe!")
    except e.InvalidQuery as err:
        print(err)
    else:
        energy = 0
        for node in system.nodes:
            if isinstance(node.value, e.Distribution) or isinstance(node.value,
                                                                    e.House):
                if node.value.commune == commune:
                    if node.value.demand == node.value.consumption:
                        energy += node.value.energy
                    else:
                        energy += min(s.Container(node.value.energy,
                                                  node.value.consumption))
        system_energy = 0
        net_energy = 0
        for sys in network:
            if sys == system:
                for node in sys.nodes:
                    if isinstance(node.value, e.Intensification):
                        system_energy += node.value.energy
                        net_energy += node.value.energy
            else:
                for node in sys.nodes:
                    if isinstance(node.value, e.Intensification):
                        net_energy += node.value.energy
        try:
            sys_proportion = energy / system_energy
        except ZeroDivisionError:
            sys_proportion = 0
        try:
            net_proportion = energy / net_energy
        except ZeroDivisionError:
            net_proportion = 0
        print(f'Consumo Total de la Comuna {commune}: {energy * 1000} kW')
        print(f'Porcentaje con Respecto a su Sistema: {sys_proportion * 100} %')
        print(f'Porcentaje con Respecto a la Red: {net_proportion * 100} %')


def largest_consumer(network):
    try:
        system = None
        text = 'Ingrese la sigla del sistema eléctrico:'
        name = validate_input(text, 'string')
        for sys in network:
            if sys.name == name:
                system = sys
        if not system:
            raise e.InvalidQuery(f"El sistema '{name}' no existe!")
        current_max = float('-inf')
        largest = None
        for node in system.nodes:
            if isinstance(node.value, e.House):
                if node.value.demand == node.value.consumption:
                    consumption = node.value.energy
                else:
                    consumption = min(s.Container(node.value.energy,
                                                  node.value.consumption))
                if consumption > current_max:
                    current_max = consumption
                    largest = node.value
        if not largest:
            raise e.InvalidQuery(f"El sistema '{name}' no tiene casas!")
    except e.InvalidQuery as err:
        print(err)
    else:
        print(f'Cliente con Mayor Consumo en el Sistema {largest.system} -> '
              f'Id: {largest.id}, Provincia: {largest.province}, '
              f'Comuna: {largest.commune}')


def lowest_consumer(network):
    try:
        system = None
        text = 'Ingrese la sigla del sistema eléctrico:'
        name = validate_input(text, 'string')
        for sys in network:
            if sys.name == name:
                system = sys
        if not system:
            raise e.InvalidQuery(f'El sistema {name} no existe!')
        current_min = float('inf')
        lowest = None
        for node in system.nodes:
            if isinstance(node.value, e.House):
                if node.value.demand == node.value.consumption:
                    consumption = node.value.energy
                else:
                    consumption = min(s.Container(node.value.energy,
                                                  node.value.consumption))
                if consumption < current_min:
                    current_min = consumption
                    lowest = node.value
        if not lowest:
            raise e.InvalidQuery(f'El sistema {name} no tiene casas!')
    except e.InvalidQuery as err:
        print(err)
    else:
        print(f'Cliente con Menor Consumo en el Sistema {lowest.system} -> '
              f'Id: {lowest.id}, Provincia: {lowest.province}, '
              f'Comuna: {lowest.commune}')


def power_loss(network):
    try:
        text = 'Ingrese el Id de la casa:'
        _Id = validate_input(text, 'int')
        system = None
        for sys in network:
            if not system:
                for node in sys.nodes:
                    if node.value:
                        if (node.value.id == _Id) and isinstance(node.value,
                                                                 e.House):
                            system = sys
        if not system:
            raise e.InvalidQuery(f"No existe una casa con Id '{_Id}'!")
    except e.InvalidQuery as err:
        print(err)
    else:
        start = system.nodes.get_node(e.House, _Id)
        visited = s.Container(start)
        stack = s.Container(start)
        total_loss = 0
        while stack:
            current = stack.pop_left()
            if not isinstance(current.value, e.Intensification):
                for origin in current.origins:
                    for connection in origin.connections:
                        if connection[0] == current:
                            resistance = min(
                                s.Container((connection[1] * 0.0172) /
                                            origin.value.cable_surface, 0.999))
                            total_loss += current.value.energy * resistance / (
                                    1 - resistance)
                    if origin not in visited:
                        stack.add(origin)
                        visited.add(origin)
        print(f'Energía Total Perdida en la Transmisión hacia la Casa '
              f'(Id: {_Id}): {total_loss * 1000} kW')


def energy_by_substation(network):
    try:
        system = None
        stations = s.Container(e.Transmission, e.Distribution)
        text = 'Seleccione el tipo de subestación:\n1) Transmisión\n2) ' \
               'Distribución'
        station = validate_input(text, stations)
        text = 'Ingrese el Id de la subestación:'
        _Id = validate_input(text, 'int')
        if station == e.Transmission:
            station_type = 'Transmisión'
        else:
            station_type = 'Distribución'
        for sys in network:
            if not system:
                for node in sys.nodes:
                    if isinstance(node.value, station):
                        if node.value.id == _Id:
                            system = sys
        if not system:
            raise e.InvalidQuery(f"No existe una subestación de {station_type} "
                                 f"con Id '{_Id}'!")
    except e.InvalidQuery as err:
        print(err)
    else:
        for node in system.nodes:
            if isinstance(node.value, station):
                if node.value.id == _Id:
                    consumption = node.value.energy
        print(f'Consumo de la Subestación de {station_type} '
              f'(Id: {_Id}): {consumption} MW')


# Valida los input del usuario
def validate_input(text, option):
    while True:
        try:
            print(text)
            if isinstance(option, s.Container):
                return option[int(input()) - 1]
            elif option == 'int':
                number = int(input())
                if number >= 0:
                    return number
                else:
                    print('Debe ser un número entero mayor o igual a 0!\n')
            elif option == 'float':
                number = float(input())
                if number >= 0:
                    return number
                else:
                    print('Debe ser un número mayor o igual a 0!\n')
            elif option == 'power':
                number = int(input())
                if 20 <= number <= 200:
                    return number
                else:
                    print('Debe ser un número entero entre 20 y 200!\n')
            elif option == 'string':
                string_input = input()
                if string_input.replace(' ', ''):
                    return string_input
                else:
                    print('No puede ser un nombre vacío!\n')
        except ValueError:
            print('Por favor ingresa un número válido!\n')
        except IndexError:
            print('Por favor ingresa un número válido!\n')


# Versiones adaptadas de las funciones de más arriba para su uso en testing
def testing_energy_by_commune(network, commune):
        system = None
        for sys in network:
            if not system:
                for node in sys.nodes:
                    if node.value:
                        if node.value.commune == commune:
                            system = sys
        if not system:
            raise e.InvalidQuery(f"La comuna '{commune}' no existe!")
        energy = 0
        for node in system.nodes:
            if isinstance(node.value, e.Distribution) or isinstance(node.value,
                                                                    e.House):
                if node.value.commune == commune:
                    if node.value.demand == node.value.consumption:
                        energy += node.value.energy
                    else:
                        energy += min(s.Container(node.value.energy,
                                                  node.value.consumption))
        system_energy = 0
        net_energy = 0
        for sys in network:
            if sys == system:
                for node in sys.nodes:
                    if isinstance(node.value, e.Intensification):
                        system_energy += node.value.energy
                        net_energy += node.value.energy
            else:
                for node in sys.nodes:
                    if isinstance(node.value, e.Intensification):
                        net_energy += node.value.energy
        sys_proportion = energy / system_energy
        net_proportion = energy / net_energy
        output = s.Container(energy * 1000, sys_proportion * 100,
                             net_proportion * 100)
        return output


def testing_largest_consumer(network, name):
        system = None
        for sys in network:
            if sys.name == name:
                system = sys
        if not system:
            raise e.InvalidQuery(f"El sistema '{name}' no existe!")
        current_max = float('-inf')
        largest = None
        for node in system.nodes:
            if isinstance(node.value, e.House):
                if node.value.demand == node.value.consumption:
                    consumption = node.value.energy
                else:
                    consumption = min(s.Container(node.value.energy,
                                                  node.value.consumption))
                if consumption > current_max:
                    current_max = consumption
                    largest = node.value
        if not largest:
            raise e.InvalidQuery(f"El sistema '{name}' no tiene casas!")
        output = s.Container(largest.id, largest.province, largest.commune)
        return output


def testing_lowest_consumer(network, name):
        system = None
        for sys in network:
            if sys.name == name:
                system = sys
        if not system:
            raise e.InvalidQuery(f'El sistema {name} no existe!')
        current_min = float('inf')
        lowest = None
        for node in system.nodes:
            if isinstance(node.value, e.House):
                if node.value.demand == node.value.consumption:
                    consumption = node.value.energy
                else:
                    consumption = min(s.Container(node.value.energy,
                                                  node.value.consumption))
                if consumption < current_min:
                    current_min = consumption
                    lowest = node.value
        if not lowest:
            raise e.InvalidQuery(f'El sistema {name} no tiene casas!')
        output = s.Container(lowest.id, lowest.province, lowest.commune)
        return output


def testing_power_loss(network, identification):
    _Id = identification
    system = None
    for sys in network:
        if not system:
            for node in sys.nodes:
                if node.value:
                    if (node.value.id == _Id) and isinstance(node.value,
                                                             e.House):
                        system = sys
    if not system:
        raise e.InvalidQuery(f"No existe una casa con Id '{_Id}'!")
    start = system.nodes.get_node(e.House, _Id)
    visited = s.Container(start)
    stack = s.Container(start)
    total_loss = 0
    while stack:
        current = stack.pop_left()
        if not isinstance(current.value, e.Intensification):
            for origin in current.origins:
                for connection in origin.connections:
                    if connection[0] == current:
                        resistance = min(s.Container((connection[1] * 0.0172) /
                                         origin.value.cable_surface, 0.999))
                        total_loss += current.value.energy * resistance / (
                                1 - resistance)
                if origin not in visited:
                    stack.add(origin)
                    visited.add(origin)
    output = total_loss * 1000
    return output


def testing_energy_by_substation(network, station, identification):
        _Id = identification
        system = None
        if station == e.Transmission:
            station_type = 'Transmisión'
        else:
            station_type = 'Distribución'
        for sys in network:
            if not system:
                for node in sys.nodes:
                    if isinstance(node.value, station):
                        if node.value.id == _Id:
                            system = sys
        if not system:
            raise e.InvalidQuery(f"No existe una subestación de {station_type} "
                                 f"con Id '{_Id}'!")
        output = 0
        for node in system.nodes:
            if isinstance(node.value, station):
                if node.value.id == _Id:
                    consumption = node.value.energy
                    output = consumption
        return output


def testing_delete_node(network, entity, identification):
    system = None
    _id = identification
    origin_node = None
    for sys in network:
        if not origin_node:
            origin_node = sys.nodes.get_node(entity, _id)
            if origin_node:
                system = sys
    if not system:
        raise e.ForbiddenAction('Remover Nodo', 'para un nodo inexistente!')
    node = s.Container(entity, _id)
    system.remove_node(node)


# Se encarga de agregar y conectar un nodo nuevo para obtener el
# ElectricalOverload del testing
def testing_overload(network, destiny, destiny_id, _system, province, commune,
                     consumption, origin, origin_id, distance,
                     name=None, _type='', power=0):
    system = None
    _id = destiny_id
    if destiny != e.Generation:
        entity = destiny(_id, _system, province, commune, name, consumption)
    else:
        entity = destiny(_type, power, _id, _system, province, commune, name)
    for sys in network:
        if sys.nodes.get_node(destiny, entity.id):
            raise e.ForbiddenAction(
                'Agregar Nodo', 'para un nodo ya existente (Id y Tipo)!')
        elif sys.name == _system:
            system = sys
    node = s.SystemNode(entity)
    system.add_node(node)
    system = None
    origin_node = None
    destiny_node = None
    for sys in network:
        if not (origin_node and destiny_node):
            origin_node = sys.nodes.get_node(origin, origin_id)
            destiny_node = sys.nodes.get_node(destiny, destiny_id)
            if origin_node and destiny_node:
                system = sys
            else:
                origin_node = None
                destiny_node = None
    if not system:
        raise e.ForbiddenAction('Agregar Arista',
                                'entre entidades inexistentes o de '
                                'distintos sistemas!')
    for connection in origin_node.connections:
        if connection[0] == destiny_node:
            raise e.ForbiddenAction('Agregar Arista', 'entre entidades '
                                                      'ya conectadas!')
    incompatibility = f'desde {origin_node.value.__class__.__name__} ' \
                      f'hacia {destiny_node.value.__class__.__name__}!'
    if isinstance(origin_node.value, e.Generation):
        if not isinstance(destiny_node.value, e.Intensification):
            raise e.ForbiddenAction('Agregar Arista', incompatibility)
    elif isinstance(origin_node.value, e.Intensification):
        if not isinstance(destiny_node.value, e.Transmission):
            raise e.ForbiddenAction('Agregar Arista', incompatibility)
        if len(destiny_node.origins):
            raise e.ForbiddenAction(
                'Agregar Arista', 'hacia una Subestación de Transmisión '
                                  'que ya está conectada a otra '
                                  'Subestación Elevadora!')
    elif isinstance(origin_node.value, e.Transmission):
        if not isinstance(destiny_node.value, e.Distribution):
            raise e.ForbiddenAction('Agregar Arista', incompatibility)
        if len(destiny_node.origins):
            raise e.ForbiddenAction(
                'Agregar Arista', 'hacia una Subestación de Distribución '
                                  'que ya está conectada a otra '
                                  'Subestación de Transmisión!')
    elif isinstance(origin_node.value, e.Distribution):
        if not isinstance(destiny_node.value, e.House):
            raise e.ForbiddenAction('Agregar Arista', incompatibility)
        if destiny_node.value.commune != origin_node.value.commune:
            raise e.ForbiddenAction(
                'Agregar Arista', 'entre una Subestación de Distribución '
                                  'y una Casa de comunas distintas!')
        for root in destiny_node.origins:
            if isinstance(root.value, e.House):
                raise e.ForbiddenAction(
                    'Agregar Arista',
                    'entre una Subestación de Distribución y una Casa '
                    'que está colgada!')
    else:
        if not isinstance(destiny_node.value, e.House):
            raise e.ForbiddenAction('Agregar Arista', incompatibility)
        if destiny_node.value.commune != origin_node.value.commune:
            raise e.ForbiddenAction(
                'Agregar Arista', 'entre Casas que tienen '
                                  'comunas distintas!')
        for root in destiny_node.origins:
            if isinstance(root.value, e.Distribution):
                raise e.ForbiddenAction(
                    'Agregar Arista',
                    'entre una Casa y otra Casa que ya está conectada '
                    'directamente a una Subestación de Distribución!')
    start = s.Container(origin, origin_id)
    end = s.Container(destiny, destiny_id)
    system.add_connection(start, end, distance)
