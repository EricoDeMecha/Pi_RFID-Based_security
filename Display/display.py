from kivy.app import App
from kivy.uix.anchorlayout import  AnchorLayout
from kivy.lang import Builder
from kivy.core.window import Window

Window.clearcolor = (0.4,0.3,0.76,1)

Builder.load_file("bios.kv")
Builder.load_file("scanner1.kv")
Builder.load_file("scanner2.kv")
Builder.load_file("status.kv")

class Display(AnchorLayout):
    pass

class DisplayApp(App):
    def build(self):
        return Display()


if __name__ == "__main__":
    DisplayApp().run()