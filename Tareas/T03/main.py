import structures as s
import functionalities as f

print('Cargando...')
Sing = s.System('SING')
Sic = s.System('SIC')
Aysen = s.System('AYSEN')
Magallanes = s.System('MAGALLANES')
network = s.Container(Sing, Sic, Aysen, Magallanes)
use = True
while use:
    options = s.Container(1, 2, 3, 0)
    text = '\nBienvenido a ELECTROMATIC!!!\nSeleccione la acción a ' \
           'realizar:\n\n1) Realizar Modificaciones\n2) Simular ' \
           'Modificaciones\n3) Realizar Consultas\n4) Salir'
    option = f.validate_input(text, options)
    if option in s.Container(1, 2):
        edit = True
        while edit:
            if option == 1:
                simulation = False
            else:
                simulation = True
            actions = s.Container(1, 2, 3, 4, 0)
            text = '\nSeleccione el tipo de modificación:\n\n1) Agregar ' \
                   'Arista\n2) Remover Arista\n3) Agregar Nodo\n4) Remover ' \
                   'Nodo\n5) Volver'
            action = f.validate_input(text, actions)
            if action == 1:
                f.new_connection(network, simulation)
            elif action == 2:
                f.delete_connection(network, simulation)
            elif action == 3:
                f.new_node(network, simulation)
            elif action == 4:
                f.delete_node(network, simulation)
            else:
                edit = False
    elif option == 3:
        info = True
        while info:
            queries = s.Container(1, 2, 3, 4, 5, 0)
            text = '\nSeleccione la consulta a realizar:\n\n1) Energía Total ' \
                   'Consumida en una Comuna\n2) Cliente con Mayor Consumo\n' \
                   '3) Cliente con Menor Consumo\n4) Potencia Perdida en ' \
                   'Transmisión\n5) Consumo de una Subestación\n6) Volver'
            query = f.validate_input(text, queries)
            if query == 1:
                f.energy_by_commune(network)
            elif query == 2:
                f.largest_consumer(network)
            elif query == 3:
                f.lowest_consumer(network)
            elif query == 4:
                f.power_loss(network)
            elif query == 5:
                f.energy_by_substation(network)
            else:
                info = False
    else:
        use = False
