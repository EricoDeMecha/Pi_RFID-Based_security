from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

Builder.load_file('bios.kv')
Builder.load_file('status.kv')

class Bios(GridLayout):
    reg = ObjectProperty(None)
    serial_no = ObjectProperty(None)
    phone_no = ObjectProperty(None)
    cardData = ObjectProperty(None)
    keyData = ObjectProperty(None)

class Status(BoxLayout):
    cardBtn = ObjectProperty(None)
    keyBtn = ObjectProperty(None)
class Writer(BoxLayout):
    data_list = []
    def __init__(self,**kwargs):
        super(Writer,self).__init__(**kwargs)

    def collectData(self):
        self.data_list.extend([self.ids.bios.reg.text, self.ids.bios.serial_no.text, self.ids.bios.phone_no.text])
        print(self.data_list)
        print(self.ids.bios.cardData.text)
        print(self.ids.bios.keyData.text)
        #set button text
        self.ids.status.cardBtn.text = 'CardWritten'
        self.ids.status.keyBtn.text = 'KeyWritten'

class writeApp(App):
    def build(self):
        return Writer()

if __name__ == "__main__":
    writeApp().run()
