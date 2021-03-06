from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.anchorlayout import  AnchorLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
#sub-class imports

from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout

import random
import sqlite3
import threading
from sqlitedict import SqliteDict

Window.clearcolor = (0.4,0.3,0.76,1)

Builder.load_file("bios.kv")
Builder.load_file("scanner1.kv")
Builder.load_file("scanner2.kv")
Builder.load_file("status.kv")
# The sub-classes
class Bios(GridLayout):
    reg = ObjectProperty(None)
    serial_no = ObjectProperty(None)
    phone_no = ObjectProperty(None)
    card = ObjectProperty(None)

class Scanner1(BoxLayout):
    scan1 = ObjectProperty(None)

class Scanner2(BoxLayout):
    scan2 = ObjectProperty(None)

class Status(BoxLayout):
    stat = ObjectProperty(None)


class Display(AnchorLayout):
    keys = ['key0','key1','key2','key3','key4','key5','key6','key7','key8','key9','key10','key11','key12','key13'
        ,'key14','key15','key16','key17','key18','key19','key20','key21','key22','key23','key24','key25','key26'
        ,'key27','key28','key29']
    cards = ['card0', 'card1', 'card2', 'card3', 'card4', 'card5', 'card6', 'card7', 'card8', 'card9', 'card10',
             'card11', 'card12', 'card13'
        , 'card14', 'card15', 'card16', 'card17', 'card18', 'card19', 'card20', 'card21', 'card22', 'card23', 'card24',
             'card25', 'card26'
        , 'card27', 'card28', 'card29']
    db_path = "../data/testData.db"

    # SqlDict
    dict_sqlite = 'data.sqlite'

    def __init__(self, **kwargs):
        super(Display,self).__init__(**kwargs)
        self.register_event_type('on_card')
        self.register_event_type('on_key')
        Clock.schedule_interval(self.keyEvent, 1)
        Clock.schedule_interval(self.cardEvent, 3)

    def on_key(self):
        lock = threading.Lock()
        threading.Thread(target=self.handle_key, args=(lock,)).start()
    def on_card(self):
        lock = threading.Lock()
        threading.Thread(target=self.handle_card, args=(lock,)).start()
    def keyEvent(self,dt):
        self.on_key()
    def cardEvent(self,dt):
        self.on_card()


    def get_keys(self):
        random.shuffle(self.keys)
        return random.choice(self.keys)

    def handle_key(self,lock):
        key_val  = self.get_keys()# get the key
        key_data = self.pullFromDb(key_val,3)# get the key-related data from the database
        # use  the card as the key
        lock.acquire()
        self.sqliteFileIO(key_data[-1], key_data)
        lock.release()

    def get_card(self):
        random.shuffle(self.cards)
        return random.choice(self.cards)

    def handle_card(self,lock):
        card_val = self.get_card()
        self.ids._status.stat.text = ''
        lock.acquire()
        self.sqliteFileIO(card_val)
        lock.release()

    def pullFromDb(self, item, row_pos):
        row_data = []
        conn = sqlite3.connect(self.db_path)
        with conn:
            cur = conn.cursor()
            cur.execute('select * from t_data')
            while True:
                row = cur.fetchone()
                if row == None:
                    break
                elif row[row_pos] == item:
                    row_data = row
        conn.close()
        return list(row_data)

    def sqliteFileIO(self, aKey, Val=None):
        # distinguish between reading  and writing
        if Val is None:
            #is reading
            key_dict = SqliteDict(self.dict_sqlite, autocommit=True)
            global card_data
            try:
                card_data = key_dict[aKey]
                self.ids._bios.reg.text = '{}'.format(f'{card_data[0]}')
                self.ids._bios.serial_no.text = '{}'.format(f'{card_data[1]}')
                self.ids._bios.phone_no.text = '{}'.format(f'{card_data[2]}')
                self.ids._bios.card.text = '{}'.format(f'{card_data[-1]}')
                self.ids._status.stat.text = "[INFO] Verification complete"
                # remove the key value pair
                del key_dict[str(aKey)]
                #reset the status
            except KeyError:
                self.ids._scanner2.scan2.text = f"[{aKey}] Card unrecognized(Scan Key)"
            key_dict.close()

        else:
            #is writing
            key_dict = SqliteDict(self.dict_sqlite, autocommit=True)
            try:
                key_dict[aKey] = Val
            except KeyError:
                self.ids._scanner1.scan1.text = f"[{aKey}] Key already scanned"

            key_dict.close()

class DisplayApp(App):
    def build(self):
        return Display()


if __name__ == "__main__":
    DisplayApp().run()