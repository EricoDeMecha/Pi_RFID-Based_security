import sqlite3

from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar

Builder.load_file('bios.kv')
Builder.load_file('status.kv')

class Writer(BoxLayout):
    def __init__(self,**kwargs):
        super(Writer,self).__init__(**kwargs)
    def collectData(self):
        data_list = []
        reg = self.ids.bios.reg.text
        serial_no = self.ids.bios.serial_no.text
        phone_no = self.ids.bios.phone_no.text
        cardData = self.ids.bios.cardData.text
        keyData = self.ids.bios.keyData.text
        data_list.extend([reg, serial_no, phone_no, cardData, keyData])
        if self.checkList(data_list):
            popup = Popup(title = "Warning" , size_hint=(None, None), size=(160,160),
                          content=Label(markup=True,text="[color=ff0000][b]Field(s) empty[/b][/color]"),
                          auto_dismiss=True)
            popup.open()
        else:
            self.save_data(data_list)

    def checkList(self, myList):
        global flag
        flag = False
        for item in myList:
            if not item:
                flag = True
        return flag

    def clearWindowData(self):
        self.ids.bios.reg.text = ''
        self.ids.bios.serial_no.text = ''
        self.ids.bios.phone_no.text = ''
        self.ids.bios.cardData.text = ''
        self.ids.bios.keyData.text = ''

    def save_data(self,data_list):
        global conn
        try:
            conn = sqlite3.connect('../../data/testData.db')
            cursor = conn.cursor()

            sqlite_insert_with_param = """INSERT INTO t_data
                                  (reg_no, serial_no,phone_no,uid_tag1,uid_tag2) 
                                  VALUES (?, ?, ?, ?, ?);"""

            data_tuple = tuple(data_list)
            cursor.execute(sqlite_insert_with_param, data_tuple)
            conn.commit()# data saved
            # content
            box = BoxLayout(orientation="vertical")
            box.add_widget(Label(markup=True,text="[color=00FF00][b]Data saved[/b][/color]"))
            box.add_widget(ProgressBar(max=100, value=40))
            popup = Popup(title = "Info" , size_hint=(None, None), size=(Window.width/4, Window.height/4),
                          content=box,
                          auto_dismiss=True)
            popup.open()
            # clear window
            self.clearWindowData()
            cursor.close()
        except sqlite3.Error as error:
            popup = Popup(title = "Error" , size_hint=(None, None), size=(Window.width/2,Window.height/3),
                          content=Label(markup=True,text=f"[color=ff0000][b]{error}[/b][/color]"),
                          auto_dismiss=True)
            popup.open()
        finally:
            if (conn):
                conn.close()
class writeApp(App):
    def build(self):
        return Writer()

if __name__ == "__main__":
    writeApp().run()
