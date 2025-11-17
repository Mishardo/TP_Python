from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.properties import NumericProperty

from logica.jugador import Jugador
from logica.obstaculos import ParObstaculos

class JuegoVisual(Screen):
    puntuacion = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.pares_obstaculos = []
        
    def on_enter(self):
        # Esperar a que el widget esté completamente inicializado
        Clock.schedule_once(self.iniciar_juego, 0.1)
        
    def iniciar_juego(self, dt):
        """Inicializa el juego después de que la pantalla esté lista"""
        self.resetear()
        self._event = Clock.schedule_interval(self.update, 1.0/60.0)
        
    def on_leave(self):
        if hasattr(self, "_event"):
            self._event.cancel()
    
    def calcular_hueco(self):
        """Calcula el tamaño del hueco según la puntuación"""
        hueco_inicial = 300  # Hueco grande al inicio
        hueco_minimo = 150   # Hueco mínimo (no se hace más pequeño que esto)
        reduccion_por_punto = 5  # Reduce 5 píxeles por cada punto
        
        hueco = hueco_inicial - (self.puntuacion * reduccion_por_punto)
        return max(hueco, hueco_minimo)  # No menor al mínimo
    
    def calcular_distancia_obstaculos(self):
        """Calcula la distancia entre obstáculos según la puntuación"""
        distancia_inicial = 500  # Muy separados al inicio
        distancia_minima = 300   # Distancia mínima entre obstáculos
        reduccion_por_punto = 8  # Se acercan 8 píxeles por cada punto
        
        distancia = distancia_inicial - (self.puntuacion * reduccion_por_punto)
        return max(distancia, distancia_minima)  # No menor a la mínima
    
    def crear_obstaculos(self):
        # Evitar crear obstáculos antes de que exista tamaño real
        if self.width == 0 or self.height == 0:
            Clock.schedule_once(lambda dt: self.crear_obstaculos(), 0.05)
            return

        # Limpiar anteriores
        for par in self.pares_obstaculos:
            if par.superior.parent:
                self.remove_widget(par.superior)
            if par.inferior.parent:
                self.remove_widget(par.inferior)

        self.pares_obstaculos.clear()

        distancia = self.calcular_distancia_obstaculos()

        # Crear 3 pares
        for i in range(3):
            hueco = self.calcular_hueco()
            par = ParObstaculos(self.width, self.height, hueco_inicial=hueco)

            x_pos = self.width + i * distancia
            par.superior.x = x_pos
            par.inferior.x = x_pos

            self.add_widget(par.inferior)
            self.add_widget(par.superior)

            self.pares_obstaculos.append(par)
            
    def update(self, dt):
        if not hasattr(self.ids, 'player'):
            return
            
        jugador = self.ids.player
        jugador.actualizar()
        
        altura = self.height
        
        # Verificar límites de pantalla
        if jugador.y < 0:
            self.game_over()
            return
            
        if jugador.top > altura:
            jugador.y = altura - jugador.height
            jugador.velocidad_y = 0
        
        # Actualizar obstáculos
        for par in self.pares_obstaculos:
            par.actualizar()
            
            # Si el obstáculo salió de la pantalla, reposicionarlo
            if par.superior.right < 0:
                max_x = max(p.get_x() for p in self.pares_obstaculos)
                distancia = self.calcular_distancia_obstaculos()
                nueva_x = max_x + distancia
                par.reiniciar(nueva_x=nueva_x, altura_pantalla=self.height)
            
            # Sumar punto cuando el jugador pasa el obstáculo
            if not par.pasado and par.get_x() + 60 < jugador.x:
                par.pasado = True
                self.puntuacion += 1
        
        # Actualizar etiqueta de puntuación
        if "puntaje_label" in self.ids:
            self.ids.puntaje_label.text = str(int(self.puntuacion))
        
        # Verificar colisiones
        self.verificar_colision()
        
    def on_touch_down(self, touch):
        try:
            if hasattr(self.ids, 'player'):
                self.ids.player.saltar()
        except Exception as e:
            print(f"Error en salto: {e}")
        return super().on_touch_down(touch)

    def hay_colision(self, a, b):
        """Detecta si hay colisión entre dos widgets"""
        if (a.x < b.right and a.right > b.x and 
            a.y < b.top and a.top > b.y):
            return True
        return False
      
    def verificar_colision(self):
        """Verifica colisiones con todos los obstáculos"""
        if not hasattr(self.ids, 'player'):
            return
            
        jugador = self.ids.player
        
        for par in self.pares_obstaculos:
            if self.hay_colision(jugador, par.superior):
                self.game_over()
                return
            if self.hay_colision(jugador, par.inferior):
                self.game_over()
                return
                
    def resetear(self):
        """Reinicia el juego"""
        if not hasattr(self.ids, 'player'):
            return
            
        jugador = self.ids.player
        jugador.pos = (self.width * 0.2, self.height * 0.5)
        jugador.velocidad_y = 0
        self.puntuacion = 0
        
        # Crear nuevos obstáculos
        self.crear_obstaculos()
        
        if "puntaje_label" in self.ids:
            self.ids.puntaje_label.text = str(int(self.puntuacion))
            
    def game_over(self):
        """Maneja el fin del juego"""
        print("Game Over!")  # Debug
        self.resetear()