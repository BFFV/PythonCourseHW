import requests
import re
import math as m
from credentials import SQUARE_CLIENT, SQUARE_SECRET, STACK_KEY
from datetime import datetime
from collections import deque


# Inicio de Sesión
def validate_username():
    login = True
    pattern = '^\w{3,8}@(?=\w*\.\w*$)[\w(\.)?]{4,12}$'
    while login:
        print("Ingrese el correo electrónico (para volver ingrese '0'):\n")
        user = input()
        if user == '0':
            return False
        elif bool(re.fullmatch(pattern, user)):
            login = False
        else:
            print('\nEl correo ingresado es inválido!!!\n')
    return True


def validate_password():
    login = True
    pattern = '^(?=\w*[A-Z])\w{8,12}$'
    while login:
        print("Ingrese la contraseña (para volver ingrese '0'):\n")
        password = input()
        if password == '0':
            return False
        elif bool(re.fullmatch(pattern, password)):
            login = False
        else:
            print('\nLa contraseña ingresada es inválida!!!\n')
    return True


# Cálculo de Distancia
def distance(lat1, long1, lat2, long2):
    r = 6371
    lat1, long1, lat2, long2 = map(m.radians, [float(x) for x in
                                               [lat1, long1, lat2, long2]])
    d_1 = m.sin((lat2 - lat1)/2)**2 + \
        m.cos(lat1)*m.cos(lat2)*m.sin((long2 - long1)/2)**2
    d_2 = 2*r*m.asin(m.sqrt(d_1))
    return d_2


# Flujo del Programa
def foursquare_categories():
    square_url = 'https://api.foursquare.com/v2/venues/categories'
    square_client = SQUARE_CLIENT
    square_secret = SQUARE_SECRET
    request_parameters = dict(client_id=square_client,
                              client_secret=square_secret, v='20180323')
    response = requests.get(square_url, request_parameters).json()
    category_dict = dict()
    stack = deque(response['response']['categories'])
    while stack:
        category = stack.popleft()
        for subcategory in category['categories']:
            stack.append(subcategory)
        category_dict[category['name']] = category['id']
        category_dict[category['pluralName']] = category['id']
        category_dict[category['shortName']] = category['id']
    return category_dict


def foursquare_request(keyword, category):
    square_url = 'https://api.foursquare.com/v2/venues/search'
    square_client = SQUARE_CLIENT
    square_secret = SQUARE_SECRET
    if not category:
        request_parameters = dict(client_id=square_client,
                                  client_secret=square_secret, intent='browse',
                                  v='20180323', ll='-33.459229, -70.645348',
                                  radius=26000, limit=50, query=keyword)
    else:
        category_dict = foursquare_categories()
        categories = category.split(',')
        valid = True
        category_list = list()
        for cat in categories:
            if cat not in category_dict:
                valid = False
            else:
                category_list.append(category_dict[cat])
        if valid:
            request_parameters = dict(client_id=square_client,
                                      client_secret=square_secret,
                                      intent='browse',
                                      v='20180323', ll='-33.459229, -70.645348',
                                      radius=26000, limit=50,
                                      categoryId=','.join(category_list))
        else:
            return []
    response = requests.get(square_url, request_parameters).json()
    return response['response']['venues']


def venues_list(venues):
    venue_list = list()
    for venue in venues:
        venue_dict = {'name': venue['name'], 'lat': venue['location']['lat'],
                      'lng': venue['location']['lng']}
        if 'address' in venue['location']:
            venue_dict['address'] = \
                ', '.join(venue['location']['formattedAddress'])
        else:
            venue_dict['address'] = 'No disponible!'
        if venue['categories']:
            venue_dict['categories'] = [x['name'] for x in venue['categories']]
        else:
            venue_dict['categories'] = []
        venue_list.append(venue_dict)
    return venue_list


def ip_stack_request():
    access_key = STACK_KEY
    stack_url = f'http://api.ipstack.com/check?access_key={access_key}'
    response = requests.get(stack_url).json()
    return [response['latitude'], response['longitude']]


def stop_request(lat, long):
    stops_url = 'https://api.scltrans.it/v1/stops'
    request_parameters = dict(limit='3', center_lon=long, center_lat=lat)
    response = requests.get(stops_url, request_parameters).json()
    return [x['stop_id'] for x in response['results']]


def route_request(stops):
    routes_set = set()
    routes_dict = dict()
    for stop in stops:
        route_url = f'https://api.scltrans.it/v3/stops/{stop}/stop_routes'
        response = requests.get(route_url).json()
        new_routes = set([x['route']['route_id']
                          for x in response['results']])
        routes_dict[stop] = new_routes
        routes_set = routes_set | new_routes
    return [routes_set, routes_dict]


def near_stop_request(lat, long, routes):
    stops_url = 'https://api.scltrans.it/v1/stops'
    request_parameters = dict(center_lon=long,
                              center_lat=lat)
    response = requests.get(stops_url, request_parameters).json()
    start_stop = None
    valid_routes = None
    for stop in response['results']:
        if not start_stop:
            intersection = route_request([stop['stop_id']])[0] & routes
            if intersection:
                start_stop = stop
                valid_routes = intersection
    if (not start_stop) or \
            (distance(lat, long, start_stop['stop_lat'],
                      start_stop['stop_lon']) > 10):
        return None
    return {'stop': start_stop['stop_id'], 'routes': valid_routes,
            'lat': start_stop['stop_lat'], 'long': start_stop['stop_lon'],
            'name': start_stop['stop_name']}


def stop_info(lat1, long1, stop):
    stop_url = f'https://api.scltrans.it/v1/stops/{stop}'
    response = requests.get(stop_url).json()
    dist = distance(lat1, long1, response['stop_lat'], response['stop_lon'])
    name = response['stop_name']
    return [round(dist, 3), name]


def bus_request(stop, routes):
    success = False
    response = dict()
    while not success:
        try:
            bus_url = f'https://api.scltrans.it/v2/stops/{stop}/next_arrivals'
            response = requests.get(bus_url).json()
            if "title" in response:
                raise TimeoutError
            else:
                success = True
        except TimeoutError:
            print('Ha ocurrido un error, realizando nuevamente la consulta...')
    return [x for x in response['results'] if x['route_id'] in routes]


def validate_input(text, option, exception=False):
    while True:
        try:
            print(text)
            chosen = int(input())
            if exception:
                if chosen < 0:
                    raise IndexError
            else:
                if chosen <= 0:
                    raise IndexError
            return option[chosen - 1]
        except ValueError:
            print('Por favor ingresa un número válido!\n')
        except IndexError:
            print('Por favor ingresa un número válido!\n')


def search_venues(option):
    if option == 'category':
        choice = input('Ingrese la o las categorías deseadas separadas '
                       'por comas (cat1,cat2,cat3...) y respetando '
                       'mayúsculas:\n')
        result = foursquare_request(None, choice)
        if not result:
            print('\nUna o más categorías ingresadas son inválidas!!!\n')
            return
    else:
        choice = input('Ingrese la descripción deseada:\n')
        result = foursquare_request(choice, None)
        if not result:
            print('No se encontraron resultados!!!\n')
            return
    print()
    index = 1
    for venue in venues_list(result):
        print(f"{index}) {venue['name']} | Dirección: {venue['address']} | "
              f"Categorías: {venue['categories']}")
        index += 1
    options = list(range(1, len(result) + 1)) + [0]
    text = "\nIngrese el número del destino a visitar, o bien '0' " \
           "para volver:\n"
    option = validate_input(text, options, True)
    if not option:
        return
    route = calculate_route(result[option - 1])
    if not route:
        print('\nNo se encontró un paradero de origen válido!!!\n')
        return
    print(f"\nParadero de salida elegido: {route['stop']}\n")
    print(f"Distancia hasta el "
          f"destino {route['destiny']}: {route['distance']} km\n")
    print('Microbuses hacia el destino:\n')
    if not route['bus']:
        print('No hay microbuses en dirección al paradero!!!\n')
    else:
        for bus in route['bus']:
            print(f"{bus['route_id']} -> Tiempo de llegada "
                  f"aproximado: {bus['arrival_estimation']} (se encuentra "
                  f"a {bus['bus_distance']} m), Paradero de "
                  f"destino: {bus['finish']}\n       Distancia del "
                  f"viaje: {bus['trip_distance']} km, Tiempo estimado de "
                  f"viaje: {bus['estimate']} min.\n")
    input('\nIngrese algún carácter para volver:\n')
    return


def calculate_route(venue):
    print('Obteniendo rutas hacia el destino...')
    stops = stop_request(venue['location']['lat'], venue['location']['lng'])
    routes_info = route_request(stops)
    routes = routes_info[0]
    routes_dict = routes_info[1]
    print('Buscando paraderos cercanos de origen (esta operación puede tardar '
          'un tiempo)...')
    current_location = ip_stack_request()
    near_stop = near_stop_request(*current_location, routes)
    if not near_stop:
        return None
    print('Obteniendo información del viaje (esta operación puede tardar '
          'un tiempo)...')
    bus_info = bus_request(near_stop['stop'], near_stop['routes'])
    destiny_distance = round(distance(near_stop['lat'], near_stop['long'],
                                      venue['location']['lat'],
                                      venue['location']['lng']), 3)
    info_dict = {x: stop_info(near_stop['lat'], near_stop['long'], x)
                 for x in routes_dict}
    valid_buses = []
    for bus in bus_info:
        if bus['bus_plate_number']:
            bus['destiny'] = None
            for stop in routes_dict:
                if not bus['destiny']:
                    if bus['route_id'] in routes_dict[stop]:
                        bus['destiny'] = stop
            estimate = trip_time(bus['route_id'], near_stop['stop'],
                                 bus['destiny'], bus['direction_id'])
            if estimate:
                bus['estimate'] = estimate
                bus['trip_distance'], bus['finish'] = info_dict[bus['destiny']]
                valid_buses.append(bus)
    return {'bus': valid_buses, 'distance': destiny_distance,
            'destiny': venue['name'], 'stop': near_stop['name']}


def trip_time(route, origin, destiny, direction):
    if direction not in (0, 1):
        return None
    routes_url = f'https://api.scltrans.it/v2/routes/{route}/directions'
    response = requests.get(routes_url).json()
    start_time = None
    finish_time = None
    chosen_direction = None
    for direct in response['results']:
        if direct['direction_id'] == direction:
            chosen_direction = direct['stop_times']
    for stop in chosen_direction:
        if (stop['stop_id'] == origin) and not finish_time:
            start_time = stop['departure_time']
        elif (stop['stop_id'] == destiny) and start_time:
            finish_time = stop['arrival_time']
    if (not start_time) or (not finish_time):
        return None
    now = datetime.now()
    day_date = [now.year, now.month, now.day]
    start = [int(x) for x in start_time.split(':')]
    finish = [int(x) for x in finish_time.split(':')]
    return round(((datetime(*day_date, *finish) -
                   datetime(*day_date, *start)).seconds) / 60, 3)
