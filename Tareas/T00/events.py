import datetime as d
import textwrap as txt
import user as u


# Representa a los eventos
class Event:
    def __init__(self, owner, name, start, finish, body, guests, tags, e_id):
        start_dt = date_validation(start)
        finish_dt = date_validation(finish)
        self.id = e_id
        self.owner = owner
        self.name = name.replace("'", "")
        self.start = start_dt
        self.finish = finish_dt
        self.body = body.replace("'", "")
        self.guests = guests.split(";")
        self.tags = tags.split(";")

# Muestra toda la información de un evento
    def show_event(self):
        name = self.name
        if name[-1:] == ".":
            name = name[:-1]
        body = "\n".join(txt.wrap(self.body, 90))
        owner = self.owner
        s_guests = set(self.guests)
        l_guests = sorted(list(s_guests))
        guests = "\n".join(txt.wrap(", ".join(l_guests), 90))
        s_tags = set(self.tags)
        l_tags = sorted(list(s_tags))
        tags = "\n".join(txt.wrap(", ".join(l_tags), 90))
        start = str(self.start).split(" ")[0] + \
            " a las " + str(self.start).split(" ")[1]
        finish = str(self.finish).split(" ")[0] + " a las " \
            + str(self.finish).split(" ")[1]
        print("Propietario: " + owner + "\n" + "Nombre: " + name)
        print("Fecha de Inicio: " + str(start) + "\n" + "Fecha de Término: "
              + str(finish) + "\n")
        print("Invitados: " + guests + 2*"\n" + "Etiquetas: " + tags + "\n")
        print("Descripción:\n" + body + "\n")
        input("Presione 'Enter' o ingrese algún carácter para volver: ")
        print()

# Permite editar los eventos
    def edit(self, events):
        name_input = input("Ingrese el nuevo nombre del evento (entre 6 y 50 "
                           "caracteres y no puede llevar comillas simples ' ')"
                           "\n(si no ingresa nada se mantendrá el actual => " +
                           self.name + "): ")
        print()
        if name_input == "":
            name = self.name
        elif (len(name_input) > 50) or ("'" in name_input) or \
                (len(name_input) < 6):
            print("El nombre ingresado no es válido!!!\n")
            return False
        else:
            name = "'" + name_input.replace('"', "\"") + "'"
        start_input = input("Ingrese la nueva fecha de inicio del evento en "
                            "el formato YYYY-MM-DD HH:MM:SS (Año-Mes-Día "
                            "Hora:Minuto:Segundo)\n(si no ingresa nada se "
                            "mantendrá la actual => " + str(self.start) + "): ")
        print()
        if start_input == "":
            start = self.start
        else:
            start = date_validation(start_input)
            if start is False:
                print("La fecha ingresada no es válida!!!\n")
                return False
        finish_input = input("Ingrese la nueva fecha de término del evento "
                             "en el formato YYYY-MM-DD HH:MM:SS (Año-Mes-Día "
                             "Hora:Minuto:Segundo)\n(si no ingresa nada se "
                             "fijará 1 hora después del inicio por default)"
                             "(fecha de término actual => " + str(self.finish)
                             + "): ")
        print()
        if finish_input == "":
            delta = d.timedelta(hours=1)
            finish = self.start + delta
        else:
            finish = date_validation(finish_input)
            if finish is False:
                print("La fecha ingresada no es válida!!!\n")
                return False
            elif start > finish:
                print("La fecha de término no puede ser anterior a la de "
                      "inicio!!!\n")
                return False
        for event in events:
            if (event.name == name) and (event.start == start) and \
                    (event.finish == finish) and (event.id != self.id):
                print("Ya existe otro evento con el mismo nombre y fechas!!!\n")
                return False
        body_input = input("Ingrese la nueva descripción del evento "
                           "(no puede llevar comillas simples ' ')(si no "
                           "ingresa nada se guardará como 'sin descripción')"
                           "\n(descripción actual => " +
                           "\n".join(txt.wrap(self.body, 90)) + "): \n")
        print()
        if body_input == "":
            body = "sin descripción"
        elif "'" in body_input:
            print("La descripción no debe llevar comillas!!!\n")
            return False
        else:
            body = "'" + body_input.replace('"', "\"") + "'"
        tag_input = input("Ingrese las nuevas etiquetas del evento en el "
                          "formato tag1,tag2...(no deben llevar ';')\n(si no "
                          "ingresa nada se guardará como 'sin etiquetas')"
                          "(etiquetas actuales => " +
                          "\n".join(txt.wrap(",".join(self.tags), 90)) + "):\n")
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
        self.name = name
        self.start = start
        self.finish = finish
        self.body = body
        self.tags = tags
        print("Se ha editado el evento con éxito!!!\n")
        return True

# Permite eliminar los eventos
    @staticmethod
    def delete():
        while True:
            print("¿Desea eliminar de forma permanente este evento?")
            print("1) Sí" + "\n" + "2) No\n")
            option = input()
            if option in ("1", "2"):
                if option == "1":
                    print("Se ha eliminado el evento exitosamente!\n")
                    return True
                else:
                    print("Se ha cancelado la eliminación!\n")
                    return False
            else:
                print("Por favor ingrese un número válido\n")

# Permite agregar invitados a los eventos
    def invite(self):
        option = input("Ingrese los correos de los usuarios que desee agregar "
                       "a la lista de invitados del evento de la forma \n"
                       "usuario@proveedor.dominio (el formato debe ser "
                       "invitado1,invitado2...): ")
        print()
        people = option + ","
        guests = people.split(",")
        guests.pop()
        for guest in guests:
            if u.validation(guest) is False:
                print("Uno o más correos de invitados no son válidos!!!\n")
                return False
        print("Se han añadido los invitados con éxito!!!\n")
        self.guests.extend(guests)
        if self.guests[0] == 'sin invitados':
            self.guests.pop(0)
        return True

# Realiza los cambios en la base de datos
    def change(self, mode, events):
        if mode == "edit":
            status = self.edit(events)
            if status is True:
                events[self.id] = Event(self.owner, self.name, str(self.start),
                                        str(self.finish), self.body,
                                        ";".join(self.guests),
                                        ";".join(self.tags), self.id)
                event_data = open("datos/db_events.csv", 'w', encoding="utf-8")
                for event in events:
                    if event.owner == "owner":
                        event_data.write("owner" + "," + "name" + "," + "start"
                                         + "," + "finish" + "," + "description"
                                         + "," + "invited" + "," + "tags" +
                                         "\n")
                    else:
                        event_data.write(event.owner + "," + "\"" + "'" +
                                         event.name + "'" + "\"" + "," +
                                         str(event.start) + "," +
                                         str(event.finish) + "," + "\"" + "'"
                                         + event.body + "'" + "\"" + "," +
                                         ";".join(event.guests) + "," +
                                         ";".join(event.tags) + "\n")
                event_data.close()
            else:
                print("Se ha cancelado la edición del evento!\n")
        elif mode == "delete":
            status = self.delete()
            if status is True:
                events.pop(self.id)
                event_data = open("datos/db_events.csv", 'w', encoding="utf-8")
                for event in events:
                    if event.owner == "owner":
                        event_data.write("owner" + "," + "name" + "," + "start"
                                         + "," + "finish" + "," + "description"
                                         + "," + "invited" + "," + "tags" +
                                         "\n")
                    else:
                        event_data.write(event.owner + "," + "\"" + "'" +
                                         event.name + "'" + "\"" + "," +
                                         str(event.start) + "," +
                                         str(event.finish) + "," + "\"" + "'"
                                         + event.body + "'" + "\"" + "," +
                                         ";".join(event.guests) + "," +
                                         ";".join(event.tags) + "\n")
                event_data.close()
        else:
            status = self.invite()
            if status is True:
                events[self.id] = Event(self.owner, self.name, str(self.start),
                                        str(self.finish), self.body,
                                        ";".join(self.guests),
                                        ";".join(self.tags), self.id)
                event_data = open("datos/db_events.csv", 'w', encoding="utf-8")
                for event in events:
                    if event.owner == "owner":
                        event_data.write("owner" + "," + "name" + "," + "start"
                                         + "," + "finish" + "," + "description"
                                         + "," + "invited" + "," + "tags" +
                                         "\n")
                    else:
                        event_data.write(event.owner + "," + "\"" + "'" +
                                         event.name + "'" + "\"" + "," +
                                         str(event.start) + "," +
                                         str(event.finish) + "," + "\"" + "'"
                                         + event.body + "'" + "\"" + "," +
                                         ";".join(event.guests) + "," +
                                         ";".join(event.tags) + "\n")
                event_data.close()
            else:
                print("Se ha cancelado la agregación de invitados!\n")


# Se utiliza para obtener los eventos del calendario
def event_list(user):
    event_data = open("datos/db_events.csv", encoding="utf-8")
    events = list()
    user_events = list()
    event_id = 0
    # La siguiente parte se encarga de extraer la información diferenciando
    # las ',' textuales y separadoras
    for event in event_data:
        event_string = []
        comma = 0
        deny_comma = 0
        split = [0]
        info = event.strip()
        for index in range(len(info)):
            if info[index] == ",":
                if deny_comma == 0:
                    comma += 1
                    split.append(index + 1)
            elif info[index] == "'":
                if comma in (1, 4):
                    if deny_comma == 0:
                        deny_comma = 1
                    else:
                        deny_comma = 0
        x = 0
        while (x + 1) < len(split):
            event_string.append(info[split[x]:split[x + 1] - 1])
            x += 1
        event_string.append(info[split[len(split) - 1]:])
        origin = event_string[0]
        guests = event_string[5].split(";")
        if event_string[1][0] == "\"":
            event_string[1] = event_string[1][1:-1]
        if event_string[4][0] == "\"":
            event_string[4] = event_string[4][1:-1]
        if (user == origin) or (user in guests):
            user_events.append(Event(event_string[0], event_string[1],
                                     event_string[2], event_string[3],
                                     event_string[4], event_string[5],
                                     event_string[6], event_id))
        events.append(Event(event_string[0], event_string[1],
                            event_string[2], event_string[3],
                            event_string[4], event_string[5],
                            event_string[6], event_id))
        event_id += 1
    event_data.close()
    return user_events, events


# Muestra el calendario
def show_calendar(events, info):
    t_events = tuple(events)
    l_events = list(t_events)
    if info[0] == "":
        info_name = "CUALQUIERA"
    else:
        info_name = info[0]
    if info[1] == "":
        info_start = "CUALQUIERA"
    else:
        info_start = str(info[1])
    if info[2] == "":
        info_finish = "CUALQUIERA"
    else:
        info_finish = str(info[2])
    if len(info[3]) == 0:
        info_tags = "CUALQUIERA"
    else:
        info_tags = "\n".join(txt.wrap(", ".join(info[3]), 90))
    print("Filtro Actual:" + 2*"\n" + "Nombre (o parte de él): " + info_name)
    print("Fecha de Inicio: " + info_start)
    print("Fecha de Término: " + info_finish)
    print("Etiquetas: " + info_tags + "\n")
    print("Eventos encontrados: " + 2*"\n")
    if len(l_events) != 0:
        length = 0
        for event in l_events:
            if len(event.name) > length:
                length = len(event.name) + 8
        index = 0
        for x in range(len(l_events)):
            current = l_events.pop(0)
            if current.name[-1:] == ".":
                title = current.name[:-1]
            else:
                title = current.name
            space = length - len(str(index + 1) + ") " + title)
            print(str(index + 1) + ") " + title + space * ' ' + "| "
                  + "Inicia el " + str(current.start).split(" ")[0] + " a las "
                  + str(current.start).split(" ")[1])
            index += 1
    else:
        print("No se encontraron eventos con el filtro actual!\n")
    print()


# Valida los inputs de las fechas y los transforma a datetime
def date_validation(date):
    space_split = date.split(" ")
    if len(space_split) != 2:
        return False
    if (len(space_split[0]) != 10) or (len(space_split[1]) != 8):
        return False
    hyphen_split = space_split[0].split("-")
    if len(hyphen_split) != 3:
        return False
    if (len(hyphen_split[0]) != 4) or (len(hyphen_split[1]) != 2) or \
            (len(hyphen_split[2]) != 2):
        return False
    for number in hyphen_split[0]:
        if number not in (list("0123456789")):
            return False
    if hyphen_split[0] == "0000":
        return False
    for number in hyphen_split[1]:
        if number not in (list("0123456789")):
            return False
    if (int(hyphen_split[1]) <= 0) or (int(hyphen_split[1]) > 12):
        return False
    for number in hyphen_split[2]:
        if number not in list("0123456789"):
            return False
    if hyphen_split[1] in ("01", "03", "05", "07", "08", "10", "12"):
        if (int(hyphen_split[2]) <= 0) or (int(hyphen_split[2]) > 31):
            return False
    elif hyphen_split[1] in ("04", "06", "09", "11"):
        if (int(hyphen_split[2]) <= 0) or (int(hyphen_split[2]) > 30):
            return False
    elif hyphen_split[1] in "02":
        if (int(hyphen_split[2]) <= 0) or (int(hyphen_split[2]) > 28):
            return False
    else:
        return False
    colon_split = space_split[1].split(":")
    if len(colon_split) != 3:
        return False
    if (len(colon_split[0]) != 2) or (len(colon_split[1]) != 2) or \
            (len(colon_split[2]) != 2):
        return False
    for number in colon_split[0]:
        if number not in (list("0123456789")):
            return False
    if (int(colon_split[0]) < 0) or (int(colon_split[0]) > 23):
        return False
    for number in colon_split[1]:
        if number not in (list("0123456789")):
            return False
    if (int(colon_split[1]) < 0) or (int(colon_split[1]) > 59):
        return False
    for number in colon_split[2]:
        if number not in (list("0123456789")):
            return False
    if (int(colon_split[2]) < 0) or (int(colon_split[2]) > 59):
        return False
    year = int(hyphen_split[0])
    month = int(hyphen_split[1])
    day = int(hyphen_split[2])
    hour = int(colon_split[0])
    minute = int(colon_split[1])
    second = int(colon_split[2])
    return d.datetime(year, month, day, hour, minute, second)


# Se encarga de filtrar y ordenar por fecha los eventos en el calendario
def filter_events(events, filter_info):
    f_events = []
    for event in events:
        matched_event = 0
        if filter_info[0] in event.name:
            matched_event += 1
        if filter_info[1] == "":
            matched_event += 1
        elif filter_info[1] <= event.start:
            matched_event += 1
        if filter_info[2] == "":
            matched_event += 1
        elif filter_info[2] >= event.finish:
            matched_event += 1
        if len(filter_info[3]) == 0:
            matched_event += 1
        elif set(filter_info[3]).issubset(set(event.tags)):
            matched_event += 1
        if matched_event == 4:
            f_events.append(event)
    f_events.sort(key=lambda x: x.start)
    return f_events
