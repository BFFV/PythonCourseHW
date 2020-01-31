import iic2233_utils as utils
import utils as u
import textwrap as txt
import os.path as os
import functools as ft


# Carga las consultas desde un archivo de texto
def load_queries(name):
    with open(name + '.txt', encoding='utf-8-sig') as file:
        return [x.strip() for x in file]


# Muestra las consultas cargadas desde un archivo de texto
def show_queries(queries):
    utils.foreach(lambda x: print(str(x[0] + 1) + ')' + x[1]),
                  enumerate(queries))


# Entrega el formato para mostrar cada tipo de resultado
def result_format(data, name):
    type_string = f'Tipo de Output: {type(data)}'
    if isinstance(data, (list, set, dict)):
        string = 'Consulta: ' + '\n'.join(txt.wrap(name, 120)) + 2 * '\n' \
                 + 'Resultado: \n' + '\n'.join(txt.wrap(str(data), 120))
        return (), string, type_string
    else:
        string = 'Consulta: ' + '\n'.join(txt.wrap(name, 120)) \
                 + 2 * '\n' + 'Resultado: \n'
        return data, string, type_string


# Imprime el resultado en la consola
def print_result(data, name):
    result, string, type_string = result_format(data, name)
    print('\n' + string)
    utils.foreach(print, result)
    print()


# Procesa y muestra las consultas elegidas (alto nivel)
def show_results(queries):
    utils.foreach(lambda x: print_result(*x), u.evaluate_input(queries))


# Valida un input en el formato 'n1,n2,n3...'
def validate(options, selection):
    check = [True if x in (str(y) for y in range(1, len(options) + 1))
             else False for x in selection]
    if False in check:
        return True
    return [options[x - 1] for x in sorted(int(y) for y in selection)]


# Conecta los distintos menús dependiendo del input del usuario
def input_interpreter(option, current):
    if not option:
        print('Por favor ingrese un input válido!\n')
        return current
    return option


# Menú Principal
def main_menu():
    print('Bienvenido a CRUNCHER FLIGHTS!!!\n')
    print('Ingrese el número de la acción que desea realizar:\n')
    print('1) Abrir un archivo con consultas')
    print('2) Ingresar consultas')
    print('3) Leer el archivo output.txt\n')
    option = input()
    if option == '1':
        return 'open_file'
    elif option == '2':
        return 'enter_query'
    elif option == '3':
        return 'output'
    return False


# Menú para abrir archivo con consultas
def file_menu():
    print("Ingrese el nombre del archivo de texto a abrir (sin el .txt) o "
          "ingrese '0' para volver al menú:\n")
    option = input()
    if option == '0':
        return option, 'main_menu'
    elif os.exists(option + '.txt'):
        return option, 'read_file'
    return (), False


# Menú para elegir consultas a mostrar
def read_file(name):
    print(f'\nConsultas de {name}.txt:\n')
    queries = load_queries(name)
    show_queries(queries)
    print("\nIngrese los números de las consultas a revisar de la forma "
          "n1,n2,n3...\n(Si desea seleccionarlas todas ingrese '.')(Si desea "
          "volver ingrese '0'):")
    option = input()
    if option == '0':
        return option, 'open_file'
    elif option == '.':
        return queries, 'show_query'
    if validate(queries, {x for x in option.split(',')}) is True:
        return (), False
    return validate(queries, {x for x in option.split(',')}), 'show_query'


# Muestra una selección de consultas
def show_selected(selection):
    utils.foreach(show_results, selection)
    print('\nPresione Enter o ingrese algún carácter para volver a la lista '
          'de consultas:')
    input()


# Menú para ingresar consultas directamente
def query_menu():
    print("Ingrese sus consultas con el formato {'consulta': [args]} "
          "o presione Enter sin ingresar nada para volver al menú:\n(para "
          "más de una consulta ingrese una lista [consulta1, consulta2,..])")
    option = input()
    if option == '':
        return 'main_menu'
    utils.foreach(lambda x: new_queries(*x), u.evaluate_input(option))
    return 'enter_query'


# Guarda las consultas en 'output.txt'
def save_query(data, name):
    with open('output.txt', 'a+', encoding='utf-8-sig') as file:
        file.seek(0)
        numbers = [x.strip() for x in file if x[0] == '-']
        if len(numbers) == 0:
            last = 0
            newline = ''
        else:
            newline = '\n'
            last = int(numbers.pop().split(' ')[2])
        file.write(f'{newline}---------- Consulta {str(last + 1)} ----------\n')
        result, string, type_string = result_format(data, name)
        file.write(string)
        utils.foreach(lambda x: file.write(str(x) + '\n'), result)
        file.write(2 * '\n' + type_string)


# Menú para mostrar resultados y dar la opción de guardar consultas
def new_queries(data, name):
    if isinstance(data, (list, set, dict)):
        print_result(data, name)
        l_data = ()
    else:
        l_data = [x for x in data]
        print_result((x for x in l_data), name)
    option = input("Ingrese '1' si desea guardar esta consulta en "
                   "'output.txt', en caso contrario ingrese otro carácter:\n")
    if option == '1':
        if isinstance(data, (list, set, dict)):
            save_query(data, name)
        else:
            save_query((x for x in l_data), name)
        print('La consulta ha sido guardada exitosamente!!!\n')


# Carga el archivo 'output.txt'
def load_output():
    with open('output.txt', encoding='utf-8-sig') as file:
        output_list = [x for x in file]
    return output_list


# Verifica si el archivo 'output.txt' existe o está vacío
def open_output():
    if not os.exists('output.txt'):
        print('El archivo output.txt no ha sido creado aún!!!\n')
        return (), 'main_menu'
    with open('output.txt', encoding='utf-8-sig') as file:
        content = [x for x in file]
        if len(content) == 0:
            print('El archivo output.txt se encuentra vacío!!!\n')
            return (), 'main_menu'
    return load_output(), 'delete_query'


# Elimina las consultas seleccionadas en el archivo 'output.txt'
def edit_output(out_list, del_input):
    indexes = [out_list.index(x) for x in out_list if x[0] == '-']
    if validate(indexes, {x for x in del_input.split(',')}) is True:
        return False
    del_list = validate(indexes, {x for x in del_input.split(',')})
    delete = [indexes[indexes.index(x): min(indexes.index(x) + 2,
                                            len(indexes))] for x in del_list]
    del_ranges = [list(range(*x)) if len(x) == 2
                  else list(range(x[0], len(out_list))) for x in delete]
    new_list = [out_list[x] for x in range(len(out_list)) if x not in
                ft.reduce(lambda x, y: x + y, del_ranges)]
    print('Se han eliminado las consultas con éxito!!!\n')
    rewrite_output(reset_index(new_list))
    return 'output'


# Reescribe los números de las consultas en el archivo 'output.txt' al editarlo
def reset_index(new_list):
    if len(new_list) == 0:
        return []
    indexes = (x for x in range(1, len([x for x in new_list
                                        if x[0] == '-']) + 1))
    return [f'---------- Consulta {next(indexes)} ----------\n'
            if new_list[x][0] == '-' else new_list[x] for x in
            range(len(new_list))]


# Menú para leer y editar el archivo 'output.txt'
def output_menu(out_list):
    print('Consultas y resultados de output.txt:\n')
    utils.foreach(lambda x: print(x.strip()), out_list)
    print("\nIngrese los números de las consultas que desea eliminar de la "
          "forma n1,n2,n3...\n(Si desea seleccionarlas todas ingrese '.')(Si "
          "desea volver al menú sin eliminar nada ingrese '0'):")
    option = input()
    if option == '0':
        return 'main_menu'
    if option == '.':
        rewrite_output([])
        print('Se han eliminado las consultas con éxito!!!\n')
        return 'main_menu'
    print('(Eliminando consultas...)(Esto podría tardar un tiempo)\n')
    return edit_output(out_list, option)


# Crea el nuevo archivo 'output.txt' con los cambios realizados
def rewrite_output(out_list):
    with open('output.txt', 'w', encoding='utf-8-sig') as file:
        utils.foreach(file.write, out_list)
