#Importe de bibliotecas kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window

#Importe de archivos
from pantalla.menu import MenuPantalla
from pantalla.juego import JuegoVisual

class FlappyApp(App):
    def build(self):
        # Configurar tamaño de ventana para simular celular (desarrollo)
        Window.size = (380, 700)
        
        # Cargar el archivo kv y retornarlo
        return Builder.load_file("flappykivy.kv")

if __name__ == "__main__":
    FlappyApp().run()

class FlappyApp(App):
    def build(self):
        return Builder.load_file("flappykivy.kv")

if __name__ == "__main__":
    FlappyApp().run()
