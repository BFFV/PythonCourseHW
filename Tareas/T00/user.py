import events as e
import datetime as d


# Representa a los usuarios conectados
class User:
    def __init__(self, user):
        self.user = user

# Menú principal del usuario
    def main_menu(self):
        while True:
            print("Bienvenido(a) de nuevo, " + self.user + "!\n" +
                  "¿Qué acción desea realizar?\n" + "\n" +
                  "1) Enviar un Correo\n" + "2) Revisar Bandeja de Entrada\n" +
                  "3) Revisar Calendario\n" + "4) Desconectarse\n")
            option = input()
            if option in ("1", "2", "3", "4"):
                return option
            else:
                print("Por favor ingrese el número de la acción deseada\n")

# Bandeja de entrada del usuario
    def inbox(self, stack):
        while True:
            lstack = list(stack)
            mails = lstack[::-1]
            valid = list(range(len(lstack) + 1))
            for number in range(len(valid)):
                valid[number] = str(valid[number])
            print("Bandeja de Entrada de " + self.user + "\n")
            if len(lstack) != 0:
                length = 0
                for mail in lstack:
                    if len(mail.mtype) > length:
                        length = len(mail.mtype.replace(";", ", ")) + 5
                index = 0
                for i in range(len(lstack)):
                    mail = lstack.pop()
                    if mail.title[-1:] == ".":
                        topic = mail.title[:-1]
                    else:
                        topic = mail.title
                    space = length - len(str(index + 1) + ") " +
                                         mail.mtype.replace(";", ", "))
                    print(str(index + 1) + ") " + mail.mtype.replace(";", ", ")
                          + space * ' ' + "| " + topic)
                    index += 1
            else:
                print("No hay correos recibidos!\n")
            print()
            option = input(
                "Ingrese el número del correo para revisarlo, o ingrese "
                "'0' para volver al menú: ")
            print()
            if option in valid:
                if option != "0":
                    print()
                    return mails[int(option) - 1]
                else:
                    return False
            print("Por favor ingrese un número válido\n")

# Proceso de envío de mails
    @staticmethod
    def write():
        option = input("Ingrese los destinatarios del correo de la forma "
                       "usuario@proveedor.dominio \n(el formato debe ser "
                       "destinatario1,destinatario2...): ")
        print()
        destiny = option + ","
        destination = destiny.split(",")
        destination.pop()
        for user in destination:
            if validation(user) is False:
                print("Uno o más destinatarios no son válidos!!!\n")
                return False
        destination = ";".join(destination)
        option = input("Ingrese el asunto del correo \n"
                       "(debe tener entre 1 y 50 caracteres y no puede "
                       "llevar comillas simples ' '): ")
        print()
        if "'" in option:
            print("El asunto no debe llevar comillas simples!!!\n")
            return False
        topic = "'" + option.replace('"', "\"") + "'"
        if (len(topic) < 3) or (len(topic) > 52):
            print("El asunto no tiene entre 1 y 50 caracteres!!!\n")
            return False
        option = input("Escriba su mensaje (máximo 256 caracteres y no puede "
                       "llevar comillas simples ' '): ")
        print()
        if "'" in option:
            print("El texto no debe llevar comillas simples!!!\n")
            return False
        body = "'" + option.replace('"', "\"") + "'"
        if len(body) > 258:
            print("El texto es demasiado largo!!!\n")
            return False
        classes = ["Importante", "Publicidad", "Destacado", "Newsletter"]
        print("Clasificaciones:\n" + "1) " + classes[0] + "\n" + "2) " +
              classes[1] + "\n" + "3) " + classes[2] + "\n" + "4) "
              + classes[3] + "\n")
        option = input("Ingrese los números de las clasificaciones que desee "
                       "marcar \nutilizando el formato 1,2,3...(si no ingresa "
                       "nada el correo quedará sin clasificación): ")
        print()
        mtypes = option
        if mtypes is "":
            mtype = "sin clasificación"
        else:
            mtypes = (mtypes + ",").split(",")
            mtypes.pop()
            for types in mtypes:
                if types not in ("1", "2", "3", "4"):
                    print("Formato de clasificación no válido!!!\n")
                    return False
            classifications = []
            for types in set(mtypes):
                classifications.append(classes[int(types) - 1])
            mtype = ";".join(classifications)
        while True:
            option = input("Ingrese '1' para enviar el correo, o bien '0' si "
                           "desea cancelar la operación: ")
            print()
            if option is "1":
                print("El correo se ha enviado con éxito!!\n")
                return [destination, topic, body, mtype]
            elif option is "0":
                return False
            print("Por favor ingrese '1' o '0'\n")

# Proceso de creación de eventos
    def create(self, events):
        name_input = input("Ingrese el nombre del evento (entre 6 y 50 "
                           "caracteres y no puede llevar comillas simples ' '"
                           "): ")
        print()
        if (len(name_input) > 50) or ("'" in name_input) or \
                (len(name_input) < 6):
            print("El nombre ingresado no es válido!!!\n")
            return False
        else:
            name = name_input.replace('"', "\"")
        start_input = input("Ingrese la fecha de inicio del evento en el "
                            "formato YYYY-MM-DD HH:MM:SS (Año-Mes-Día "
                            "Hora:Minuto:Segundo): ")
        print()
        start = e.date_validation(start_input)
        if start is False:
            print("La fecha ingresada no es válida!!!\n")
            return False
        finish_input = input("Ingrese la fecha de término del evento en "
                             "el formato YYYY-MM-DD HH:MM:SS (Año-Mes-Día "
                             "Hora:Minuto:Segundo)\n(si no ingresa nada se "
                             "fijará 1 hora después del inicio por default): ")
        print()
        if finish_input == "":
            delta = d.timedelta(hours=1)
            finish = start + delta
        else:
            finish = e.date_validation(finish_input)
            if finish is False:
                print("La fecha ingresada no es válida!!!\n")
                return False
            elif start > finish:
                print("La fecha de término no puede ser anterior a la de "
                      "inicio!!!\n")
                return False
        for event in events:
            if (event.name == name) and (event.start == start) and \
                    (event.finish == finish):
                print("Ya existe otro evento con el mismo nombre y fechas!!!\n")
                return False
        body_input = input("Ingrese la descripción del evento "
                           "(no puede llevar comillas simples ' ')\n(si no "
                           "ingresa nada se guardará como 'sin descripción'): ")
        print()
        if body_input == "":
            body = "sin descripción"
        elif "'" in body_input:
            print("La descripción no debe llevar comillas simples!!!\n")
            return False
        else:
            body = body_input.replace('"', "\"")
        guest_input = input("Ingrese los correos de los usuarios que desee "
                            "invitar al evento de la forma "
                            "usuario@proveedor.dominio \n"
                            "(el formato debe ser invitado1,invitado2...)(si no"
                            " ingresa nada se guardará como 'sin invitados'): ")
        print()
        if guest_input == "":
            guests = ['sin invitados']
        else:
            people = guest_input + ","
            guests = people.split(",")
            guests.pop()
            if guests != ['sin invitados']:
                for guest in guests:
                    if validation(guest) is False:
                        print("Uno o más correos de invitados no son válidos"
                              "!!!\n")
                        return False
        tag_input = input("Ingrese las etiquetas del evento en el "
                          "formato tag1,tag2...(no deben llevar ';')\n(si no "
                          "ingresa nada se guardará como 'sin etiquetas'): ")
        print()
        if tag_input == "":
            tags = ['sin etiquetas']
        elif ";" in tag_input:
            print("Las etiquetas no pueden llevar ';'!!!\n")
            return False
        else:
            tag_aux = tag_input + ","
            labels = tag_aux.split(",")
            labels.pop()
            for l_index in range(len(labels)):
                if labels[l_index] is "":
                    labels.pop(l_index)
            tags = labels
        newline = open("datos/db_events.csv")
        lines = newline.readlines()
        if "\n" in lines[-1]:
            skip = ""
        else:
            skip = "\n"
        newline.close()
        event_data = open("datos/db_events.csv", 'a', encoding="utf-8")
        event_data.write(skip + self.user + "," + "\"" + "'" +
                         name + "'" + "\"" + "," + str(start)
                         + "," + str(finish) + "," + "\"" + "'" +
                         body + "'" + "\"" + "," +
                         ";".join(guests) + "," +
                         ";".join(tags))
        event_data.close()
        print("Se ha creado el evento con éxito!!!\n")

# Calendario
    def calendar(self):
        print("Calendario de " + self.user + "\n" +
              "¿Qué acción desea realizar?\n" + "\n" +
              "1) Crear un nuevo evento\n" + "2) Consultar y editar eventos\n" +
              "3) Volver al menú\n")
        option = input()
        if option in ("1", "2", "3"):
            if option == "1":
                u_events, full_events = e.event_list(self.user)
                self.create(full_events)
            elif option == "2":
                name = input("Ingrese un nombre o parte de uno para filtrar en "
                             "el calendario (Máx. 50 caracteres y no puede "
                             "llevar comillas simples ' ')\n(si no ingresa "
                             "nada no se considerará este parámetro): ")
                print()
                if (len(name) > 50) or ('"' in name) or ("'" in name):
                    print("El nombre ingresado no es válido!!!\n")
                    return True
                start = input("Ingrese una fecha de inicio mínima para filtrar "
                              "en el calendario en el formato YYYY-MM-DD "
                              "HH:MM:SS\n(Año-Mes-Día Hora:Minuto:Segundo)(si "
                              "no ingresa nada no se considerará este "
                              "parámetro): ")
                print()
                if start == "":
                    s_date = start
                else:
                    s_date = e.date_validation(start)
                if s_date is False:
                    print("La fecha ingresada no es válida!!!\n")
                    return True
                finish = input("Ingrese una fecha de término máxima para "
                               "filtrar en el calendario en el formato "
                               "YYYY-MM-DD HH:MM:SS\n(Año-Mes-Día "
                               "Hora:Minuto:Segundo)(si no ingresa nada no se "
                               "considerará este parámetro): ")
                print()
                if finish == "":
                    f_date = finish
                else:
                    f_date = e.date_validation(finish)
                if f_date is False:
                    print("La fecha ingresada no es válida!!!\n")
                    return True
                tags = input("Ingrese una o más etiquetas para filtrar en el "
                             "calendario en el formato tag1,tag2...(no deben "
                             "llevar ';')\n(si no ingresa nada no se "
                             "considerará este parámetro): ")
                print()
                if ";" in tags:
                    print("Las etiquetas no pueden llevar ';'!!!\n")
                    return True
                tag_aux = tags + ","
                labels = tag_aux.split(",")
                labels.pop()
                for l_index in range(len(labels)):
                    if labels[l_index] is "":
                        labels.pop(l_index)
                filter_info = [name, s_date, f_date, labels]
                filtering = True
                while filtering is True:
                    user_events, events = e.event_list(self.user)
                    filter_list = e.filter_events(user_events, filter_info)
                    valid = list(range(len(filter_list) + 1))
                    for number in range(len(valid)):
                        valid[number] = str(valid[number])
                    e.show_calendar(filter_list, filter_info)
                    option = input("Ingrese el número del evento para revisarlo"
                                   "/editarlo, o ingrese '0' para volver: ")
                    print()
                    if option in valid:
                        if option != "0":
                            print()
                            choice = filter_list[int(option) - 1]
                            editing = True
                            while editing is True:
                                if choice.owner == self.user:
                                    print("Evento: " + choice.name.strip(".") +
                                          "     Fecha de Inicio: " +
                                          str(choice.start).split(" ")[0] +
                                          " a las "
                                          + str(choice.start).split(" ")[1])
                                    print()
                                    print("¿Qué acción desea realizar?\n" + "\n"
                                          + "1) Ver información de evento\n" +
                                          "2) Editar evento\n" +
                                          "3) Eliminar evento\n" +
                                          "4) Agregar invitados\n" +
                                          "5) Volver\n")
                                    option = input()
                                    if option in ("1", "2", "3", "4", "5"):
                                        if option == "1":
                                            choice.show_event()
                                        elif option == "2":
                                            choice.change("edit", events)
                                            editing = False
                                        elif option == "3":
                                            choice.change("delete", events)
                                            editing = False
                                        elif option == "4":
                                            choice.change("invite", events)
                                            editing = False
                                        else:
                                            editing = False
                                    else:
                                        print("Por favor ingrese el número de "
                                              "la acción deseada\n")
                                else:
                                    print("Evento: " + choice.name.strip(".") +
                                          "     Fecha de Inicio: " +
                                          str(choice.start).split(" ")[0] +
                                          " a las "
                                          + str(choice.start).split(" ")[1])
                                    print()
                                    print("¿Qué acción desea realizar?\n" + "\n"
                                          + "1) Ver información de evento\n" +
                                          "2) Volver\n")
                                    option = input()
                                    if option in ("1", "2"):
                                        if option == "1":
                                            choice.show_event()
                                        else:
                                            editing = False
                                    else:
                                        print("Por favor ingrese el número de "
                                              "la acción deseada\n")
                        else:
                            filtering = False
                    else:
                        print("Por favor ingrese un número válido\n")
            else:
                return False
        else:
            print("Por favor ingrese el número de la acción deseada\n")
        return True


# Diccionario de usuarios registrados en DCCorreos
def user_dict():
    user_data = open("datos/db_users.csv", encoding="utf-8")
    user_list = dict()
    for user in user_data:
        email = user.strip().split(",")[0]
        code = user.strip().split(",")[1]
        if email != "user":
            user_list[email] = code
    user_data.close()
    return user_list


# Registra una cuenta nueva en la base de datos de los usuarios
def register_user(usermail, password):
    newline = open("datos/db_users.csv")
    lines = newline.readlines()
    if "\n" in lines[-1]:
        skip = ""
    else:
        skip = "\n"
    newline.close()
    user_data = open("datos/db_users.csv", 'a', encoding="utf-8")
    user_data.write(skip + usermail + "," + password)
    user_data.close()


# Se encarga del menú de entrada al correo
def login():
    while True:
        print("Bienvenido(a) a DCCorreos!!!\n" + "¿Qué acción desea realizar?\n"
              + "\n" + "1) Iniciar sesión\n" + "2) Crear una cuenta nueva\n"
              + "3) Salir\n")
        option = input()
        if option in ("1", "2", "3"):
            if option == "1":
                user = input("Ingrese su nombre de usuario (email): ")
                password = input("Ingrese su contraseña: ")
                print()
                users = user_dict()
                if users.get(user, "none") == password:
                    return user
                print("El usuario o la contraseña son incorrectos!!!\n")
            if option == "2":
                user = input("Ingrese su correo electrónico\n(debe ser único, "
                             "sin ',' ni ';' y sin espacios con el formato "
                             "usuario@proveedor.dominio): ")
                print()
                validate = validation(user)
                if validate is True:
                    users = user_dict()
                    if user not in users:
                        password = input("Ingrese su contraseña "
                                         "(sin ',' ni ';' y "
                                         "mín. 6 carácteres): ")
                        print()
                        if ("," not in password) and \
                                (";" not in password):
                            if len(password) >= 6:
                                print("Su cuenta ha sido registrada "
                                      "con éxito!!!\n")
                                register_user(user, password)
                            else:
                                print("Contraseña demasiado corta!!!\n")
                        else:
                            print("Contraseña inválida!!!\n")
                    else:
                        print("El usuario ya existe!!!\n")
                else:
                    print("El correo no es válido!!!\n")
            if option == "3":
                return False
        else:
            print("Por favor ingrese el número de la acción deseada\n")


# Se encarga de validar el correo del usuario
def validation(user):
    if ("," not in user) and (";" not in user) and ("@" in user) \
            and (" " not in user):
        check = user.split("@")
        if (len(check) == 2) and (check[0] != ""):
            if ("." in check[1]) and (user[len(user) - 1] != ".") \
                    and (check[1][0] != "."):
                return True
    return False
