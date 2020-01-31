import math
class Circulo:
    def __init__(self, radio, x, y):
        self.radio = radio
        self.x = x
        self.y = y
    def obtener_area(self):
        print("Área:", str(math.pi*(self.radio)**2))
    def obtener_perimetro(self):
        print("Perímetro:", str(2*math.pi*self.radio))
    def __str__(self):
        return "Círculo de Radio " + str(self.radio)
class Rectangulo:
    def __init__(self, x, y, h, l):
        self.x = x
        self.y = y
        self.h = h
        self.l = l
    def obtener_area(self):
        print("Área:", str(self.h*self.l))
    def obtener_perimetro(self):
        print("Perímetro:", str(2*self.l + 2*self.h))
    def es_cuadrado(self):
        if self.l == self.h:
            print("Es Cuadrado")
        else:
            print("No es Cuadrado")
    def __str__(self):
        return "Rectángulo de "  + str(self.l) + "x" + str(self.h)
c = Circulo(4,1,1)
r = Rectangulo(0,0,1,2)
print(r)
r.obtener_area()
r.obtener_perimetro()
r.es_cuadrado()
print(c)
c.obtener_perimetro()
c.obtener_area()