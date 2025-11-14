from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Rectangle, Color
#Aca defino las propiedades del objeto
class Jugador(Widget):
    velocidad_y = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        with self.canvas:
            Color(1,0,0,1)
            self.rectangulo = Rectangle(size = self.size, pos=self.pos)           

        self.bind(pos = self.actualizar_rectangulo, size = self.actualizar_rectangulo)
    
    def actualizar_rectangulo (self, *args):
        self.rectangulo.pos = self.pos
        self.rectangulo.size = self.size
    
    
    def actualizar(self):
        self.velocidad_y -= 0.4
        self.y += self.velocidad_y

    def saltar(self):
        self.velocidad_y = 10
