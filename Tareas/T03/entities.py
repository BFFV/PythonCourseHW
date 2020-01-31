# Modelación de entidades de la red
class Entity:
    def __init__(self, _id, system, province, commune, name=None,
                 consumption=0):
        self.id = int(_id)
        self.name = name
        self.system = system
        self.province = province
        self.commune = commune
        self.consumption = consumption
        self.demand = 0
        self._energy = 0
        self.cable_surface = 0

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, value):
        if self.demand > value:
            new_value = value
        else:
            new_value = self.demand
        if new_value < 0:
            new_value = 0
        self._energy = new_value

    def calculate_demand(self, connections):
        connection_demand = 0
        for connection in connections:
            node = connection[0]
            distance = connection[1]
            resistance = (distance * 0.0172) / self.cable_surface
            if resistance > 0.999:
                resistance = 0.999
            demand = node.value.demand / len(node.origins)
            connection_demand += demand / (1 - resistance)
        self.demand = connection_demand + self.consumption

    def deliver_flow(self, connections):
        if (self.energy - self.consumption) < 0:
            flow = 0
        else:
            flow = self.energy - self.consumption
        total_demand = 0
        for connection in connections:
            node = connection[0]
            distance = connection[1]
            resistance = (distance * 0.0172) / self.cable_surface
            if resistance > 0.999:
                resistance = 0.999
            demand = node.value.demand / len(node.origins)
            total_demand += demand / (1 - resistance)
        for connection in connections:
            node = connection[0]
            distance = connection[1]
            resistance = (distance * 0.0172) / self.cable_surface
            if resistance > 0.999:
                resistance = 0.999
            demand = node.value.demand / (len(node.origins) * (1 - resistance))
            try:
                proportion = demand / total_demand
            except ZeroDivisionError:
                proportion = 0
            deliver = flow * proportion
            node.value.energy += deliver * (1 - resistance)


class Generation(Entity):
    def __init__(self, _type, power, *args):
        super().__init__(*args)
        self.type = _type
        self.power = float(power)
        self.cable_surface = 253


class Intensification(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self.consumption = float(self.consumption)
        self.cable_surface = 202.7


class Transmission(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self.consumption = float(self.consumption)
        self.cable_surface = 152


class Distribution(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self.consumption = float(self.consumption)
        self.cable_surface = 85


class House(Entity):
    def __init__(self, *args):
        super().__init__(*args)
        self.consumption = float(self.consumption) / 1000
        self.cable_surface = 85


# Modelación de Excepciones Customizadas
class ElectricalOverload(Exception):
    def __init__(self, action, power):
        super().__init__(f"ElectricalOverload: La acción {action} "
                         f"sobrecarga la red a {power} kW/ 30000 kW!\n")


class ForbiddenAction(Exception):
    def __init__(self, action, cause):
        super().__init__(f"ForbiddenAction: Acción {action} "
                         f"no está permitida {cause}\n")


class InvalidQuery(Exception):
    def __init__(self, cause):
        super().__init__(f"InvalidQuery: {cause}\n")
