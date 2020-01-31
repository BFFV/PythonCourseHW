import iic2233_utils as utils
import f_queries as f


# Interpreta una consulta literal
def evaluate_input(string):
    parsed = utils.parse(string)
    if isinstance(parsed, dict):
        queries = (x for x in [parsed])
    else:
        queries = (x for x in parsed)
    for q in queries:
        print('(Procesando consulta...)')
        yield (process_query(q), str(q))


# Procesa consultas anidadas
def process_query(query):
    name = [key for key in query][0]
    args = [process_query(x) if isinstance(x, dict) else x for x in query[name]]
    return query_dict(name)(*args)


# Asocia cada nombre de consulta a la función correspondiente
def query_dict(key):
    query_dic = {x[0]: x[1] for x in zip(
        ['load_database', 'filter_flights', 'filter_passengers',
         'filter_passengers_by_age', 'filter_airports_by_country',
         'filter_airports_by_distance', 'favourite_airport', 'passenger_miles',
         'popular_airports', 'airport_passengers', 'furthest_distance'],
        [f.load_database, f.filter_flights,
         f.filter_passengers, f.filter_passengers_by_age,
         f.filter_airports_by_country,
         f.filter_airports_by_distance, f.favourite_airport,
         f.passenger_miles, f.popular_airports,
         f.airport_passengers, f.furthest_distance])}
    return query_dic[key]
