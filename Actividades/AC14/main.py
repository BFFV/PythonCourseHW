import json
import re
from time import sleep

import requests

from credenciales import API_KEY


API_URL = "https://api.nasa.gov/planetary/apod"
DIR_IMAGENES = 'imagenes'
PATH_RESULTADOS = 'resultados.txt'


def limpiar_fecha(linea):
    pattern = '</?\w+>'
    result = re.sub(pattern, '', linea)
    return result


def chequear_fecha(fecha):
    pattern = "\d{4}-\d{2}-\d{2}"
    return bool(re.fullmatch(pattern, fecha))


def obtener_fechas(path):
    clean = []
    with open(path) as file:
        for line in file:
            result = limpiar_fecha(line.strip())
            if chequear_fecha(result):
                clean.append(result)
    return clean


def obtener_info(fecha):
    response = requests.get(
        API_URL, params={'api_key': API_KEY, 'date': fecha}).json()
    response_dict = dict()
    response_dict['title'] = response['title']
    response_dict['date'] = response['date']
    response_dict['url'] = response['url']
    return response_dict


def escribir_respuesta(datos):
    with open('resultados.txt', 'a') as file:
        file.write(f'{datos["date"]} --> {datos["title"]}: {datos["url"]}\n')
    name = datos['url'].split('/')[-1]
    descargar_imagen(datos['url'], f'imagenes/{name}')


def descargar_imagen(url, path):
    respuesta = requests.get(url, stream=True)
    if respuesta.status_code == 200:
        with open(path, 'wb') as f:
            for chunk in respuesta:
                f.write(chunk)


if __name__ == "__main__":
    PATH_FECHAS = 'fechas_secretas.txt'
    for fecha in obtener_fechas(PATH_FECHAS):
        respuesta = obtener_info(fecha)
        escribir_respuesta(respuesta)
