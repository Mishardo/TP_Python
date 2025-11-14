#Importe de bibliotecas kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager

#Importe de archivos
from pantalla.menu import MenuPantalla
from pantalla.juego import JuegoVisual

class FlappyApp(App):
    def build(self):
        return Builder.load_file("flappykivy.kv")

if __name__ == "__main__":
    FlappyApp().run()
