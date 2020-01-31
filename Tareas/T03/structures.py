import entities as e
from csv import reader
from textwrap import indent, wrap

# Variable para elegir el tamaño de la base de datos (por default es 'large')
db_size = 'large'


# Nodos de la lista ligada
class Node:
    def __init__(self, value=None):
        self.value = value
        self.next = None
        self.previous = None


# Clase de la lista ligada (contenedor)
class Container:
    def __init__(self, *args):
        self.first = None
        self.last = None
        for element in args:
            self.add(element)

    def add(self, value):
        new = Node(value)
        if not self.first:
            self.first = new
            self.last = self.first
        else:
            new.previous = self.last
            self.last.next = new
            self.last = self.last.next

    def delete(self, value):
        if self.first:
            if self.first.value == value:
                self.pop_left()
            elif self.last.value == value:
                self.pop()
            else:
                current = self.first
                while current:
                    if current.value == value:
                        current.previous.next = current.next
                        current.next.previous = current.previous
                    current = current.next

    def pop(self):
        if not self:
            return
        last = self.last
        self.last = self.last.previous
        if self.last:
            self.last.next = None
        else:
            self.first = None
        return last.value

    def pop_left(self):
        if not self:
            return
        first = self.first
        self.first = first.next
        if self.first:
            self.first.previous = None
        else:
            self.last = None
        return first.value

    def index(self, element):
        number = 0
        current = self.first
        while current:
            if current.value == element:
                return number
            current = current.next
            number += 1
        return

    def get_node(self, instance, _id):
        current = self.first
        while current:
            if current.value.value:
                if current.value.value.id == _id:
                    if isinstance(current.value.value, instance):
                        return current.value
            current = current.next
        return

    def __contains__(self, item):
        current = self.first
        while current:
            if current.value == item:
                return True
            current = current.next
        return False

    def __len__(self):
        number = 0
        current = self.first
        while current:
            number += 1
            current = current.next
        return number

    def __getitem__(self, key):
        if (key >= len(self)) or (key < 0):
            raise IndexError
        current = self.first
        n = 0
        while n < key:
            if current:
                current = current.next
            n += 1
        return current.value

    def __eq__(self, other):
        n = 0
        while n < len(self):
            if self[n] != other[n]:
                return False
            n += 1
        return True

    def __iter__(self):
        current = self.first
        while current:
            yield current.value
            current = current.next
        return

    def __repr__(self):
        string = "["
        current = self.first
        while current:
            if isinstance(current.value, e.Entity):
                element = current.value
                string = f"{string}{element.__class__.__name__}_{element.id}, "
            else:
                string = f"{string}{current.value}, "
            current = current.next
        if len(string) > 2:
            string = string[: -2]
        return f'{string}]'


# Desempaqueta un generador en una lista ligada
class SuperContainer:
    def __init__(self, *args):
        self.container = Container()
        for arg in args:
            self.container.add(Container(*arg))


# Nodos del grafo
class SystemNode:
    def __init__(self, value, system=None):
        self.value = value
        self.connections = Container()
        self.origins = Container()
        self.generation = Container()
        self.level = 0
        self.isolated = False
        self.system = system
        if not self.system:
            self.system = self.value.system

    def connect(self, node, distance=0):
        connection = Container()
        connection.add(node)
        connection.add(distance)
        self.connections.add(connection)
        if isinstance(self.value, e.Generation):
            central_connection = Container()
            central_connection.add(self)
            central_connection.add(distance)
            node.generation.add(central_connection)
        else:
            node.origins.add(self)
            if isinstance(self.value, e.House):
                node.level = 5
            else:
                node.level = self.level + 1

    def remove(self, node):
        for connection in self.connections:
            if connection[0] == node:
                self.connections.delete(connection)
        if isinstance(self.value, e.Generation):
            for connection in node.generation:
                if connection[0] == self:
                    node.generation.delete(connection)
        else:
            for origin in node.origins:
                if origin == self:
                    node.origins.delete(origin)

    def __repr__(self):
        if self.value:
            if isinstance(self.value, e.Intensification):
                centrals = Container()
                for gen in self.generation:
                    centrals.add(gen[0].value)
                return ('\n' + 26 * ' ').join(Container(
                    *wrap(indent(f'{self.value.__class__.__name__}_'
                                 f'{self.value.id} <- {centrals}',
                                 self.level * '    '), 120)))
            if self.level == 5:
                hanging = Container()
                for house in self.connections:
                    hanging.add(house[0].value)
                return indent(f'{self.value.__class__.__name__}_'
                              f'{self.value.id} <- {hanging}', self.level
                              * '    ')
            return indent(f'{self.value.__class__.__name__}_'
                          f'{self.value.id}', self.level * '    ')
        return self.system


# Grafo dirigido que modela los sistemas eléctricos
class System:
    def __init__(self, name):
        self.name = name
        self.action = ''
        self.nodes = Container()
        self.backup = None
        self.demand = 0
        self.generation = load_entity(self.name, 'centrales')
        self.intensification = load_entity(self.name, 'elevadoras')
        self.transmission = load_entity(self.name, 'transmision')
        self.distribution = load_entity(self.name, 'distribucion')
        self.houses = load_entity(self.name, 'casas')
        self.base = SystemNode(None, self.name)
        self.nodes.add(self.base)
        for entity in self.intensification:
            new_node = SystemNode(entity)
            self.base.connect(new_node)
            self.nodes.add(new_node)
        for entity in self.generation:
            self.nodes.add(SystemNode(entity))
        for entity in self.transmission:
            self.nodes.add(SystemNode(entity))
        for entity in self.distribution:
            self.nodes.add(SystemNode(entity))
        for entity in self.houses:
            self.nodes.add(SystemNode(entity))
        self.create_connections('centrales_elevadoras', e.Generation,
                                e.Intensification)
        self.create_connections('transmision_elevadoras', e.Intensification,
                                e.Transmission)
        self.create_connections('distribucion_transmision', e.Transmission,
                                e.Distribution)
        self.create_connections('casas_distribucion', e.Distribution, e.House)
        self.create_connections('casas_casas', e.House, e.House)
        self.system_demand()
        self.system_energy()

    def create_connections(self, path, origin, destiny):
        with open(f'bd/{db_size}/{path}.csv', encoding='utf-8') as file:
            header = Container()
            origin_index = 0
            destiny_index = 0
            distance_index = 0
            for line in SuperContainer(*reader(file)).container:
                data = line
                if not len(header):
                    header = data
                    distance_index = header.index('distancia')
                    if path == 'centrales_elevadoras':
                        origin_index = header.index('id_central')
                        destiny_index = header.index('id_elevadora')
                    elif path == 'transmision_elevadoras':
                        origin_index = header.index('id_elevadora')
                        destiny_index = header.index('id_transmision')
                    elif path == 'distribucion_transmision':
                        origin_index = header.index('id_transmision')
                        destiny_index = header.index('id_distribucion')
                    elif path == 'casas_distribucion':
                        origin_index = header.index('id_distribucion')
                        destiny_index = header.index('id_casa')
                    else:
                        origin_index = header.index('id_desde')
                        destiny_index = header.index('id_hasta')
                else:
                    origin_id = int(data[origin_index])
                    destiny_id = int(data[destiny_index])
                    distance = float(data[distance_index])
                    origin_node = self.nodes.get_node(origin, origin_id)
                    if origin_node:
                        destiny_node = self.nodes.get_node(destiny, destiny_id)
                        origin_node.connect(destiny_node, distance)

    def system_demand(self):
        visited = Container()
        stack = Container(self.nodes[0])
        while stack:
            node = stack.pop()
            if not node.value:
                visited.add(node)
                for connection in node.connections:
                    if connection[0].generation:
                        stack.add(connection[0])
            elif node not in visited:
                visited.add(node)
                stack.add(node)
                for connection in node.connections:
                    stack.add(connection[0])
            else:
                node.value.calculate_demand(node.connections)
        loss = 0
        network_demand = 0
        for node in self.nodes:
            if node.value:
                node.value.energy = 0
            node.isolated = node not in visited
        for connection in self.nodes[0].connections:
            node = connection[0]
            network_demand += node.value.demand
            node.value.energy = 0
            for central in node.generation:
                gen = central[0]
                distance = central[1]
                total_demand = 0
                for destiny in gen.connections:
                    d_node = destiny[0]
                    d_distance = destiny[1]
                    resistance = min(Container((d_distance * 0.0172) /
                                     gen.value.cable_surface, 0.999))
                    total_demand += d_node.value.demand / len(
                        d_node.generation) * (1 - resistance)
                resistance = min(Container(0.0172 * distance /
                                 gen.value.cable_surface, 0.999))
                current = node.value.demand / len(node.generation) * (
                            1 - resistance)
                try:
                    proportion = current / total_demand
                except ZeroDivisionError:
                    proportion = 0
                generate = min(Container(
                    gen.value.power, total_demand)) * proportion
                loss += generate * resistance
                node.value.energy += generate * (1 - resistance)
        self.demand = network_demand + loss

    def system_energy(self):
        visited = Container()
        stack = Container(self.nodes[0])
        while stack:
            node = stack.pop_left()
            if not node.value:
                visited.add(node)
                for connection in node.connections:
                    stack.add(connection[0])
            elif node not in visited:
                ready = True
                for origin in node.origins:
                    if (origin not in visited) and (not origin.isolated):
                        ready = False
                if ready:
                    if isinstance(node.value, e.House):
                        if node.value.energy > 30:
                            raise e.ElectricalOverload(self.action,
                                                       node.value.energy * 1000)
                    visited.add(node)
                    for connection in node.connections:
                        stack.add(connection[0])
                    node.value.deliver_flow(node.connections)

    def add_connection(self, origin, destiny, distance):
        self.action = 'Agregar Arista'
        start = self.nodes.get_node(origin[0], origin[1])
        end = self.nodes.get_node(destiny[0], destiny[1])
        self.backup = Container(start, end)
        start.connect(end, distance)
        stack = Container(end)
        while stack:
            current = stack.pop_left()
            for connection in current.connections:
                if connection[0] == start:
                    raise e.ForbiddenAction(
                        self.action, f'entre {start.value.__class__.__name__}'
                                     f'_{start.value.id} y '
                                     f'{end.value.__class__.__name__}_'
                                     f'{end.value.id} porque se formaría un '
                                     f'ciclo!')
                else:
                    stack.add(connection[0])
        self.system_demand()
        self.system_energy()

    def remove_connection(self, origin, destiny):
        self.action = 'Remover Arista'
        start = self.nodes.get_node(origin[0], origin[1])
        end = self.nodes.get_node(destiny[0], destiny[1])
        for connection in start.connections:
            if connection[0] == end:
                self.backup = Container(start, end, connection[1])
        start.remove(end)
        self.system_demand()
        self.system_energy()

    def add_node(self, node):
        self.action = 'Agregar Nodo'
        self.nodes.add(node)
        if isinstance(node.value, e.Intensification):
            self.base.connect(node)
        self.backup = node
        self.system_demand()
        self.system_energy()

    def remove_node(self, node):
        self.action = 'Remover Nodo'
        old_node = self.nodes.get_node(node[0], node[1])
        self.backup = Container(Container(), Container())
        self.nodes.delete(old_node)
        if isinstance(old_node.value, e.Intensification):
            for gen in old_node.generation:
                gen[0].remove(old_node)
                self.backup[1].add(Container(gen[0], old_node, gen[1]))
        for origin in old_node.origins:
            for connection in origin.connections:
                if connection[0] == old_node:
                    self.backup[1].add(Container(origin, old_node,
                                                 connection[1]))
            origin.remove(old_node)
        stack = Container(old_node)
        while stack:
            current = stack.pop_left()
            if isinstance(current.value, e.Intensification):
                if not current.generation:
                    for origin in current.origins:
                        for connection in origin.connections:
                            if connection[0] == current:
                                self.backup[1].add(Container(origin, current,
                                                             connection[1]))
                        origin.remove(current)
            if not current.origins:
                for connection in current.connections:
                    current.remove(connection[0])
                    self.backup[1].add(Container(current, connection[0],
                                                 connection[1]))
                    if isinstance(connection[0].value, e.Intensification):
                        if not connection[0].generation:
                            stack.add(connection[0])
                    elif not connection[0].origins:
                        stack.add(connection[0])
                self.backup[0].add(current)
                self.nodes.delete(current)
        self.system_demand()
        self.system_energy()

    # Sólo muestra hasta el tercer nivel de casas
    def __repr__(self):
        stack = Container(self.nodes[0])
        while stack:
            node = stack.pop()
            print(node)
            for connection in node.connections:
                if not node.level == 5:
                    stack.add(connection[0])
        return ''


# Carga las bases de datos
def load_entity(sys, entity):
    with open(f'bd/{db_size}/{entity}.csv', encoding='utf-8') as file:
        lines = Container()
        header = Container()
        system = 0
        _id = 0
        province = 0
        commune = 0
        _type = 0
        power = 0
        name = 0
        consumption = 0
        for line in SuperContainer(*reader(file)).container:
            data = line
            if not len(header):
                header = data
                _id = header.index('id')
                system = header.index('sistema_electrico')
                province = header.index('provincia')
                commune = header.index('comuna')
                if entity == 'centrales':
                    name = header.index('nombre')
                    _type = header.index('tipo')
                    power = header.index('potencia')
                elif entity == 'casas':
                    consumption = header.index('consumo_kw')
                else:
                    name = header.index('nombre')
                    consumption = header.index('consumo_mw')
            else:
                if (entity == 'centrales') and (data[system] == sys):
                    lines.add(e.Generation(data[_type], data[power], data[_id],
                                           data[system], data[province],
                                           data[commune], data[name]))
                elif (entity == 'casas') and (data[system] == sys):
                    lines.add(e.House(data[_id], data[system], data[province],
                                      data[commune], None, data[consumption]))
                elif data[system] == sys:
                    if entity == 'elevadoras':
                        lines.add(
                            e.Intensification(data[_id], data[system],
                                              data[province],
                                              data[commune], data[name],
                                              data[consumption]))
                    elif entity == 'transmision':
                        lines.add(
                            e.Transmission(data[_id], data[system],
                                           data[province],
                                           data[commune], data[name],
                                           data[consumption]))
                    else:
                        lines.add(
                            e.Distribution(data[_id], data[system],
                                           data[province],
                                           data[commune], data[name],
                                           data[consumption]))
    return lines
