from kivy.app import App
from kivy.uix.anchorlayout import  AnchorLayout
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock

import random
import sqlite3
import threading
from sqlitedict import SqliteDict

Window.clearcolor = (0.4,0.3,0.76,1)

Builder.load_file("bios.kv")
Builder.load_file("scanner1.kv")
Builder.load_file("scanner2.kv")
Builder.load_file("status.kv")

class Display(AnchorLayout):
    keys = ['key0','key1','key2','key3','key4','key5','key6','key7','key8','key9','key10','key11','key12','key13'
        ,'key14','key15','key16','key17','key18','key19','key20','key21','key22','key23','key24','key25','key26'
        ,'key27','key28','key29']
    cards = ['card0', 'card1', 'card2', 'card3', 'card4', 'card5', 'card6', 'card7', 'card8', 'card9', 'card10',
             'card11', 'card12', 'card13'
        , 'card14', 'card15', 'card16', 'card17', 'card18', 'card19', 'card20', 'card21', 'card22', 'card23', 'card24',
             'card25', 'card26'
        , 'card27', 'card28', 'card29']
    db_path = "../DataBase/testData.db"

    # SqlDict
    dict_sqlite = 'data.sqlite'

    def __init__(self, **kwargs):
        super(Display,self).__init__(**kwargs)
        Clock.schedule_interval(self.key_thread_handler(), 1)
        Clock.schedule_interval(self.card_thread_handler(), 3)

    def  key_thread_handler(self):
        lock = threading.Lock()
        keyThread = threading.Thread(target=self.handle_key, args=(lock,))
        keyThread.start()
    def card_thread_handler(self):
        lock = threading.Lock()
        cardThread = threading.Thread(target=self.handle_card, args=(lock,))
        cardThread.start()

    def get_keys(self):
        random.shuffle(self.keys)
        return random.choice(self.keys)

    def handle_key(self,lock):
        key_val  = self.get_keys()# get the key
        key_data = self.pullFromDb(key_val,4)# get the key-related data from the database
        # use  the card as the key
        lock.acquire()
        self.sqliteFileIO(key_data[-1], key_data)
        lock.release()

    def get_card(self):
        random.shuffle(self.cards)
        return random.choice(self.cards)

    def handle_card(self,lock):
        card_val = self.get_card()
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
                print(card_data)
                print("[INFO] Verification complete")
                # remove the key value pair
                del key_dict[str(aKey)]
            except KeyError:
                print(f"[{aKey}] Card is unrecognized or its key not scanned yet")
            key_dict.close()

        else:
            #is writing
            key_dict = SqliteDict(self.dict_sqlite, autocommit=True)
            try:
                key_dict[aKey] = Val
                print(key_dict[aKey])
            except KeyError:
                print(f"[{aKey}] Key already scanned")

            key_dict.close()

class DisplayApp(App):
    def build(self):
        return Display()


if __name__ == "__main__":
    DisplayApp().run()