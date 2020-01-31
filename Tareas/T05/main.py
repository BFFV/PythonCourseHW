import functionalities as f

use = True
while use:
    options = [1, 0]
    text = 'Bienvenido a DCConnect!!!\nSeleccione la acción a ' \
           'realizar:\n\n1) Iniciar Sesión\n2) Salir'
    option = f.validate_input(text, options)
    if option:
        search = False
        user = f.validate_username()
        if user:
            password = f.validate_password()
            if password:
                search = True
        while search:
            options = [1, 2, 0]
            text = 'Seleccione el formato de búsqueda:\n\n1) ' \
                   'Categorías\n2) Descripción\n3) Volver'
            option = f.validate_input(text, options)
            if option == 1:
                f.search_venues('category')
            elif option == 2:
                f.search_venues('keyword')
            else:
                search = False
    else:
        use = False
