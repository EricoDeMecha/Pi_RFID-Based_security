from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty

class Bios(GridLayout):
    reg = ObjectProperty(None)
    serial_no = ObjectProperty(None)
    phone_no = ObjectProperty(None)
    cardData = ObjectProperty(None)
    keyData = ObjectProperty(None)

    def validate_reg(self, text):
        pass