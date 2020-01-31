import collections as c
import operator as op
import datetime as dt
import math as m
import itertools as it

# Variable global que indica el tamaño de la base de datos (aquí se cambia)
db_size = 'medium'


# Interpreta los str de operadores comparativos
def operators(value):
    op_dic = {x[0]: x[1] for x in zip(['<', '>', '==', '!=', '<=', '>='],
                                      [op.lt, op.gt, op.eq, op.ne, op.le,
                                       op.ge])}
    return op_dic[value]


# Transforma un str de fecha a un objeto datetime
def to_datetime(date):
    date_day = [int(x) for x in date.split(' ')[0].split('-')]
    date_time = [int(x) for x in date.split(' ')[1].split(':')]
    return dt.datetime(*date_day, *date_time)


# Calcula la distancia utilizando la fórmula de Haversine
def distance(lat1, long1, lat2, long2):
    r = 3440
    lat1, long1, lat2, long2 = map(m.radians, [float(x) for x in
                                               [lat1, long1, lat2, long2]])
    d_1 = m.sin((lat2 - lat1)/2)**2 + \
        m.cos(lat1)*m.cos(lat2)*m.sin((long2 - long1)/2)**2
    d_2 = 2*r*m.asin(m.sqrt(d_1))
    return d_2


# Realiza operaciones entre conjuntos
def set_operation(set1, set2, operation):
    if operation == 'AND':
        return set1 & set2
    elif operation == 'OR':
        return set1 | set2
    elif operation == 'XOR':
        return (set1 | set2) - (set1 & set2)
    elif operation == 'DIFF':
        return set1 - (set1 & set2)


# Consultas que retornan Generadores

def load_database(db_type):
    name = db_type[:-1]
    info_db = db_type
    if db_type == "Travels":
        name = 'Trip'
        info_db = 'flights-passengers2'
    with open('data/' + db_size + '/' + info_db + '.csv',
              encoding='utf-8-sig') as file:
        if db_type == 'Passengers':
            n_tuple = c.namedtuple(name, file.readline().strip().
                                   replace('class', 'f_class').split(","))
        else:
            n_tuple = c.namedtuple(name, file.readline().strip().split(","))
        for line in file:
            yield n_tuple(*line.strip().split(","))


def filter_flights(flights, airports, attr, symbol, value):
    operator = operators(symbol)
    if attr == 'date':
        return filter(
            lambda x: operator(to_datetime(x.date), to_datetime(value)),
            flights)
    else:
        airports_dic = {x.icao: (x.lat, x.long) for x in airports}
        f_flights = filter(lambda x: (x.airport_to in airports_dic) and (
                    x.airport_from in airports_dic), flights)
        return filter(lambda x: operator(distance(*airports_dic[
            x.airport_from], *airports_dic[x.airport_to]), float(value)),
                      f_flights)


def filter_passengers(passengers, flights, travels, icao, start, end):
    icao1, icao2 = it.tee(filter(lambda x: x.airport_to == icao, flights), 2)
    start_flights = filter_flights(icao1, [], 'date', '>=', start)
    finish_flights = filter_flights(icao2, [], 'date', '<=', end)
    flights_set = {x.id for x in (set(start_flights) & set(finish_flights))}
    travels_set = {x.passenger_id for x in travels if x.flight_id in
                   flights_set}
    return filter(lambda x: x.id in travels_set, passengers)


def filter_passengers_by_age(passengers, age, lower=True):
    if lower:
        symbol = '<'
    else:
        symbol = '>='
    operator = operators(symbol)
    return filter(lambda x: operator(int(x.age), int(age)), passengers)


def filter_airports_by_country(airports, iso):
    return filter(lambda x: x.iso_country == iso, airports)


def filter_airports_by_distance(airports, icao, dist, lower=False):
    airports1, airports2 = it.tee(airports, 2)
    if lower:
        symbol = '<'
    else:
        symbol = '>'
    operator = operators(symbol)
    airports_dic = {x.icao: (x.lat, x.long) for x in airports1}
    if icao in airports_dic:
        return filter(lambda x: operator(distance(*airports_dic[icao], x.lat,
                                                  x.long), float(dist)) and (
                                            x.icao != icao), airports2)
    return ()


# Consultas que NO retornan Generadores

def favourite_airport(passengers, flights, travels):
    flights_dic = {x.id: x.airport_to for x in flights}
    passengers_dic = {x.id: [] for x in passengers}
    f_travels = filter(lambda x: (x.passenger_id in passengers_dic) and (
            x.flight_id in flights_dic), travels)
    [passengers_dic[x.passenger_id].append(flights_dic[x.flight_id]) for x in
     f_travels]
    return {x: c.Counter(passengers_dic[x]).most_common(1)[0][0]
            for x in passengers_dic if passengers_dic[x] != []}


def passenger_miles(passengers, airports, flights, travels):
    airports_dic = {x.icao: (x.lat, x.long) for x in airports}
    flights_dic = {x.id: (x.airport_from, x.airport_to) for x in flights}
    passengers_dic = {x.id: [] for x in passengers}
    f_travels = filter(lambda x: (x.passenger_id in passengers_dic) and (
            x.flight_id in flights_dic), travels)
    [passengers_dic[x.passenger_id].append(distance(
        *airports_dic[flights_dic[x.flight_id][0]],
        *airports_dic[flights_dic[x.flight_id][1]])) for x in
     f_travels]
    return {x: round(sum(passengers_dic[x]), 3) for x in passengers_dic
            if passengers_dic[x] != []}


def popular_airports(flights, airports, travels, topn, avg=False):
    flights_dic = {x.id: x.airport_to for x in flights}
    airports_set = {x.icao for x in airports}
    f_travels = filter(lambda x: (x.flight_id in flights_dic) and
                                 (flights_dic.get(x.flight_id, 'None') in
                                  airports_set), travels)
    airport_arrivals = c.Counter(flights_dic[x.flight_id] for x in f_travels)
    if avg:
        airport_flights = c.Counter(flights_dic[x] for x in flights_dic)
        avg_arrivals = c.Counter({x: airport_arrivals[x]/airport_flights[x]
                                  for x in airport_arrivals})
        return [x[0] for x in avg_arrivals.most_common(int(topn))]
    else:
        return [x[0] for x in airport_arrivals.most_common(int(topn))]


def airport_passengers(passengers, flights, travels, icao1, icao2, operation):
    passenger_dict = {x.id: (x.id, x.name) for x in passengers}
    flights_dic = {x.id: (x.airport_from, x.airport_to) for x in flights}
    f_travels1, f_travels2 = it.tee(filter(
        lambda x: (x.flight_id in flights_dic) and (
                    x.passenger_id in passenger_dict), travels), 2)
    s_icao1 = {passenger_dict[x.passenger_id] for x in f_travels1 if
               icao1 in flights_dic[x.flight_id]}
    s_icao2 = {passenger_dict[x.passenger_id] for x in f_travels2 if
               icao2 in flights_dic[x.flight_id]}
    return set_operation(s_icao1, s_icao2, operation)


def furthest_distance(passengers, airports, flights, travels, icao, n=3):
    airports_dic = {x.icao: (x.lat, x.long) for x in airports}
    passengers_dic = {x.id: x.name for x in passengers}
    if icao in airports_dic:
        flights_dic = {x.id: distance(*airports_dic[icao],
                                      *airports_dic[x.airport_to]) for x
                       in flights if x.airport_from == icao}
        f_travels = filter(lambda x: (x.flight_id in flights_dic) and (
                x.passenger_id in passengers_dic), travels)
        p_distance = c.Counter({(x.passenger_id,
                                 passengers_dic[x.passenger_id]):
                                flights_dic[x.flight_id] for x in
                                f_travels})
        return [x[0] for x in p_distance.most_common(int(n))]
    return []
