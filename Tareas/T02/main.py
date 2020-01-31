import simulation as s

print('Bienvenido al simulador de DCCasino!!!\n')
days = input('Ingrese la cantidad de días de la simulación: ')
while (len([x for x in days if x not in '0123456789'])) or (days == ''):
    print('Por favor ingrese un número entero válido!\n')
    days = input('Ingrese la cantidad de días de la simulación: ')
max_time = int(days) * 86400
print('Seleccione la velocidad de la simulación:\n')
print('1) Baja (Simulación de 1 día)\n2) Media (Simulación de 2 días)'
      '\n3) Alta (Simulación de 3 o más días)')
speed = input()
while speed not in ('1', '2', '3'):
    print('Por favor seleccione un número válido!\n')
    print('Seleccione la velocidad de la simulación:\n')
    print('1) Baja (Simulación de 1 día)\n2) Media (Simulación de 2 días)'
          '\n3) Alta (Simulación de 3 o más días)')
    speed = input()
if speed == '1':
    delay = 5
elif speed == '2':
    delay = 1
else:
    delay = 0.1
sim = s.Simulation(max_time, delay)
sim.run()
