import sqlite3
import threading

from kivy.core.window import Window
from kivy.uix.gridlayout import GridLayout
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.uix.popup import Popup


class Bios(GridLayout):
    reg = ObjectProperty(None)
    serial_no = ObjectProperty(None)
    phone_no = ObjectProperty(None)
    cardData = ObjectProperty(None)
    keyData = ObjectProperty(None)

    def handleDB(self, lock, text=None,row_pos=None):
        lock.acquire()
        if(text == None or row_pos == None):
            pass
        else:
            conn = sqlite3.connect("../../data/testData.db")
            with conn:
                cur = conn.cursor()
                cur.execute('select * from t_data')
                while True:
                    row = cur.fetchone()
                    if row == None:
                        break
                    elif row[row_pos] == text:
                        self.clear_text(row_pos)
                        self.createPopUp(row_pos)
            conn.close()
        lock.release()

    def createPopUp(self,row_pos):
        row_data_list = ["Reg", "Serial", "Phone No.", "key_tag","card_tag"]
        popup = Popup(title="Warning", size_hint=(None, None), size=(Window.width/4, Window.height/6),
                      content=Label(markup=True, text=f"[color=ff0000][b]{row_data_list[row_pos]} already exist[/b][/color]"),
                      auto_dismiss=True)
        popup.open()

    def clear_text(self, row_pos):
        if (row_pos == 0):
            self.reg.text = ''
        elif (row_pos == 1):
            self.serial_no.text = ''
        elif (row_pos == 2):
            self.phone_no.text = ''
        elif (row_pos == 3):
            self.keyData.text = ''
        elif (row_pos == 4):
            self.cardData.text = ''

    def validate_reg(self, text):
        lock = threading.Lock()
        threading.Thread(target=self.handleDB, args=(lock,text,0)).start()

    def validate_serial(self, text):
        lock = threading.Lock()
        threading.Thread(target=self.handleDB, args=(lock,text,1)).start()

    def validate_phone(self, text):
        lock = threading.Lock()
        threading.Thread(target=self.handleDB, args=(lock,text,2)).start()

    def validate_key(self, text):
        lock = threading.Lock()
        threading.Thread(target=self.handleDB, args=(lock,text,3)).start()

    def validate_card(self, text):
        lock = threading.Lock()
        threading.Thread(target=self.handleDB, args=(lock,text,4)).start()