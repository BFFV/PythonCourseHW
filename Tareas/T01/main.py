import user as u
if __name__ == '__main__':
    try:
        current = 'main_menu'
        data = ()
        name = ''
        while True:
            if current == 'main_menu':
                option = u.main_menu()
                current = u.input_interpreter(option, current)
            elif current == 'open_file':
                data, option = u.file_menu()
                current = u.input_interpreter(option, current)
            elif current == 'read_file':
                name = data
                data, option = u.read_file(name)
                current = u.input_interpreter(option, current)
                if current == 'read_file':
                    data = name
            elif current == 'show_query':
                u.show_selected(data)
                data = name
                current = 'read_file'
            elif current == 'enter_query':
                option = u.query_menu()
                current = u.input_interpreter(option, current)
            elif current == 'output':
                data, option = u.open_output()
                current = u.input_interpreter(option, current)
            elif current == 'delete_query':
                option = u.output_menu(data)
                current = u.input_interpreter(option, current)
    # no es necesario que hagan una parte para salir del menu
    except KeyboardInterrupt():
        exit()
