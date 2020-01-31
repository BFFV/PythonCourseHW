import user as u
import mails as m
use = True
while use is True:
    name = u.login()
    if name is not False:
        user = u.User(name)
        menu = True
        while menu is True:
            option = user.main_menu()
            if option == "1":
                send = True
                while send is True:
                    send_info = user.write()
                    if send_info is not False:
                        email = m.Mail(user.user, send_info[0], send_info[1],
                                       send_info[2], send_info[3])
                        email.send()
                        send = False
                    else:
                        send = False
            elif option == "2":
                box = True
                while box is True:
                    stack = m.mail_stack(user.user)
                    read = user.inbox(tuple(stack))
                    if read is not False:
                        read.show()
                    else:
                        box = False
            elif option == "3":
                schedule = True
                while schedule is True:
                    events = user.calendar()
                    if events is False:
                        schedule = False
            else:
                menu = False
    else:
        use = False
