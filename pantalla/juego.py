from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.properties import NumericProperty

from logica.jugador import Jugador

class JuegoVisual(Screen):
    puntuacion = NumericProperty(0)
    
    def on_enter (self):
        self._event = Clock.schedule_interval (self.update, 1.0/60.0)
        
    def on_leave (self):
        if hasattr(self, "_event"):
            self._event.cancel()
            
    def update (self, dt):
        jugador = self.ids.player
        jugador.actualizar()
        
        #Por ahora le sumo un punto por segundo
        #Cuando tengamos los obstaculos, le sumamos el punto
        self.puntuacion += dt 
        
        altura = self.height
        #Si está tocando el suelo
        if jugador.y < 0:
            self.game_over()
        #Intento limitar que no se salta de la pantalla
        if jugador.top > altura:
            jugador.y = altura - jugador.height
            jugador.velocidad_y = 0
            
        if "puntaje_label" in self.ids:
            self.ids.puntaje_label.text = str(int(self.puntuacion))
    
    def on_touch_down(self, touch):
        try:
            self.ids.player.saltar()
        except Exception:
            pass
        return super().on_touch_down(touch)
    
    def resetear(self):
        jugador = self.ids.player
        jugador.pos = (self.width * 0.2, self.height * 0.5)
        jugador.velocidad_y = 0
        self.puntuacion = 0
        
        if "puntaje_label" in self.ids:
            self.ids.puntaje_label.text = str(int(self.puntuacion))
            
    def game_over (self):
        self.resetear()