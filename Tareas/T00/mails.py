import textwrap as txt
import random as r


# Representa a los mails
class Mail:
    def __init__(self, origin, destiny, title, body, mtype):
        self.origin = origin
        self.destiny = destiny.split(";")
        self.title = title.replace("'", "")
        self.body = body.replace("'", "")
        self.mtype = mtype

# Se utiliza para enviar el mail
    def send(self):
        encrypted_body = encrypt(self.body)
        newline = open("datos/db_emails.csv")
        lines = newline.readlines()
        if "\n" in lines[-1]:
            skip = ""
        else:
            skip = "\n"
        newline.close()
        mail_data = open("datos/db_emails.csv", 'a', encoding="utf-8")
        mail_data.write(skip + self.origin + "," + ";".join(self.destiny) + ","
                        + "\"" + "'" + self.title + "'" + "\"" + "," +
                        encrypted_body + "," + self.mtype)
        mail_data.close()

# Se utiliza para mostrar toda la información de un mail
    def show(self):
        decrypted = decrypt(self.body)
        title = self.title
        if title[-1:] == ".":
            title = title[:-1]
        body = "\n".join(txt.wrap(decrypted, 90))
        origin = self.origin
        s_destiny = set(self.destiny)
        l_destiny = sorted(list(s_destiny))
        destiny = "\n".join(txt.wrap(", ".join(l_destiny), 90))
        mtype = self.mtype.replace(";", ", ")
        print("Asunto: " + title + "\n" + "Clasificación: " + mtype)
        print("De: " + origin + "\n" + "Para: " + destiny + "\n")
        print("Mensaje:\n" + body + "\n")
        input("Presione 'Enter' o ingrese algún carácter para regresar a la "
              "bandeja: ")
        print()


# Se utiliza para obtener y ordenar los mails de la bandeja de entrada
def mail_stack(user):
    mail_data = open("datos/db_emails.csv", encoding="utf-8")
    stack = list()
    # La siguiente parte se encarga de extraer la información diferenciando
    # las ',' textuales y separadoras
    for email in mail_data:
        message = []
        comma = 0
        deny_comma = 0
        split = [0]
        mail = email.strip()
        for index in range(len(mail)):
            if mail[index] == ",":
                if deny_comma == 0:
                    comma += 1
                    split.append(index + 1)
            elif mail[index] == "'":
                if comma == 2:
                    if deny_comma == 0:
                        deny_comma = 1
                    else:
                        deny_comma = 0
        i = 0
        while (i + 1) < len(split):
            message.append(mail[split[i]:split[i+1] - 1])
            i += 1
        message.append(mail[split[len(split) - 1]:])
        destinations = message[1].split(";")
        if user in destinations:
            if message[2][0] == "\"":
                message[2] = message[2][1:-1]
            stack.append(Mail(message[0], message[1], message[2], message[3],
                              message[4]))
    mail_data.close()
    return stack


# Se utiliza para encriptar el mensaje
def encrypt(text):
    caesar = ""
    for char in text:
        caesar += chr(int(ord(char) + 10))
    bin_txt = ""
    for char in caesar:
        binary = bin(ord(char)).replace("b", "")
        while len(binary) != 8:
            if len(binary) < 8:
                binary = "0" + binary
            elif len(binary) > 8:
                binary = binary[1:]
        bin_txt += binary
    password = "2233"
    random_chain = ""
    for n in range(10):
        number = r.randint(0, 9)
        random_chain += str(number)
    initial_chain = ""
    while len(initial_chain) < 256:
        if (len(initial_chain) + 14) <= 256:
            initial_chain += (password + random_chain)
        else:
            initial_chain += password
    number_chain = list(str(n) for n in range(256))
    for index in range(len(number_chain)):
        swap = index + int(initial_chain[index])
        if swap >= len(number_chain):
            swap -= 256
        n1 = number_chain[index]
        n2 = number_chain[swap]
        number_chain[index] = n2
        number_chain[swap] = n1
    bin_ord = ""
    for n in number_chain:
        binary = bin(int(n)).replace("b", "")
        while len(binary) != 8:
            if len(binary) < 8:
                binary = "0" + binary
            elif len(binary) > 8:
                binary = binary[1:]
        bin_ord += binary
    encrypted_chain = ""
    for char in range(len(bin_txt)):
        if bin_txt[char] == bin_ord[char]:
            encrypted_chain += "0"
        else:
            encrypted_chain += "1"
    return random_chain + encrypted_chain


# Se utiliza para desencriptar el mensaje
def decrypt(text):
    random_chain = text[:10]
    encrypted_chain = text[10:]
    password = "2233"
    initial_chain = ""
    while len(initial_chain) < 256:
        if (len(initial_chain) + 14) <= 256:
            initial_chain += (password + random_chain)
        else:
            initial_chain += password
    number_chain = list(str(n) for n in range(256))
    for index in range(len(number_chain)):
        swap = index + int(initial_chain[index])
        if swap >= len(number_chain):
            swap -= 256
        n1 = number_chain[index]
        n2 = number_chain[swap]
        number_chain[index] = n2
        number_chain[swap] = n1
    bin_ord = ""
    for n in number_chain:
        binary = bin(int(n)).replace("b", "")
        while len(binary) != 8:
            if len(binary) < 8:
                binary = "0" + binary
            elif len(binary) > 8:
                binary = binary[1:]
        bin_ord += binary
    decrypted_chain = ""
    for char in range(len(encrypted_chain)):
        if encrypted_chain[char] == "0":
            decrypted_chain += bin_ord[char]
        else:
            if bin_ord[char] == "0":
                decrypted_chain += "1"
            else:
                decrypted_chain += "0"
    decrypted_message = ""
    i = 0
    while (i + 8) <= len(decrypted_chain):
        ascii_char = int(decrypted_chain[i:i+8], 2)
        original_char = chr(ascii_char - 10)
        decrypted_message += original_char
        i += 8
    return decrypted_message
