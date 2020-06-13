from kivy.app import App
from kivy.uix.anchorlayout import AnchorLayout

class Writer(AnchorLayout):
    pass

class writeApp(App):
    def build(self):
        return Writer()

if __name__ == "__main__":
    writeApp().run()
