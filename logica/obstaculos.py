from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, BooleanProperty
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock
import random

class Obstaculo(Widget):
    velocidad_x = NumericProperty(-3)  # Velocidad de movimiento hacia la izquierda
    es_obstaculo = BooleanProperty(True)  # Para identificarlo en las colisiones
    pasado = BooleanProperty(False)  # Para saber si el jugador ya lo pasó
    
    def __init__(self, es_superior=False, **kwargs):
        super().__init__(**kwargs)
        self.es_superior = es_superior
        self.rectangulo = None
        
        # IMPORTANTE: Desactivar size_hint para usar tamaños absolutos
        self.size_hint = (None, None)
        
        # Bind ANTES de crear el canvas
        self.bind(pos=self.actualizar_rectangulo, size=self.actualizar_rectangulo)
        
        # Forzar actualización después de la inicialización
        Clock.schedule_once(self.crear_canvas, 0)
    
    def crear_canvas(self, dt):
        """Crea el canvas visual del obstáculo"""
        with self.canvas:
            Color(0, 1, 0, 1)  # Color verde para los obstáculos
            self.rectangulo = Rectangle(size=self.size, pos=self.pos)
    
    def actualizar_rectangulo(self, *args):
        if self.rectangulo:
            self.rectangulo.pos = self.pos
            self.rectangulo.size = self.size
    
    def mover(self):
        """Mueve el obstáculo hacia la izquierda"""
        self.x += self.velocidad_x


class ParObstaculos:
    """Maneja un par de obstáculos (superior e inferior) con un hueco en el medio"""
    
    def __init__(self, ancho_pantalla, altura_pantalla, ancho_obstaculo=60, hueco_inicial=300):
        self.ancho_pantalla = ancho_pantalla
        self.altura_pantalla = altura_pantalla
        self.ancho_obstaculo = ancho_obstaculo
        self.hueco = hueco_inicial  # Espacio entre obstáculos superior e inferior
        self.pasado = False
        
        # Crear los dos obstáculos
        self.superior = Obstaculo(es_superior=True)
        self.inferior = Obstaculo(es_superior=False)
        
        self.reiniciar()
    
    def reiniciar(self, nueva_x=None, altura_pantalla=None):
        if altura_pantalla is not None:
            self.altura_pantalla = altura_pantalla

        altura_hueco = random.randint(150, int(self.altura_pantalla - 150))

        if nueva_x is None:
            nueva_x = self.ancho_pantalla

        self.inferior.size = (self.ancho_obstaculo, altura_hueco - self.hueco // 2)
        self.inferior.pos = (nueva_x, 0)

        altura_superior = self.altura_pantalla - (altura_hueco + self.hueco // 2)
        self.superior.size = (self.ancho_obstaculo, altura_superior)
        self.superior.pos = (nueva_x, altura_hueco + self.hueco // 2)

        self.pasado = False

    
    def actualizar(self):
        """Actualiza la posición de ambos obstáculos"""
        self.superior.mover()
        self.inferior.mover()
        
        # Si el obstáculo salió de la pantalla, reiniciarlo
        if self.superior.right < 0:
            self.reiniciar()
            return True  # Indica que se reinició
        return False
    
    def esta_fuera_de_pantalla(self):
        """Verifica si el par de obstáculos salió completamente de la pantalla"""
        return self.superior.right < 0
    
    def get_x(self):
        """Obtiene la posición X del par de obstáculos"""
        return self.superior.x