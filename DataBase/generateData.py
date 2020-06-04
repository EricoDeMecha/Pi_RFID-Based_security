import random
import sqlite3
import sys
import os

class GenerateData():
    # uid_tag1
    const_key = "key"
    keys = []
    # uid_tag2
    const_card = "card"
    cards = []
    # reg
    pre_reg = "ENM221-00"
    post_reg = "/2017"
    regs = []
    # secret codes
    const_scode = "secret_"
    scodes = []
    # phone_no
    num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    pre_nos = "07"
    phone_nos = []
    # serial
    serial_nos = []
    # query data list
    query_datalist = []
    # db stuff
    db_name = "testData.db"
    def __init__(self):
        self.checkDbExistence()
        self.generate_reg()
        self.generate_phoneNos()
        self.generate_scode()
        self.generate_key()
        self.generate_card()
        self.generate_serial()

    def generate_key(self):
        for i in range(30):
            key_str = self.const_key + str(i)
            self.keys.append(key_str)

    def generate_card(self):
        for i in range(30):
            card_str = self.const_card + str(i)
            self.cards.append(card_str)

    def generate_reg(self):
        for i in range(30, 60):
            reg_str = self.pre_reg + str(i) + self.post_reg
            self.regs.append(reg_str)

    def generate_scode(self):
        for i in range(30):
            scode_str = self.const_scode + self.const_key + self.const_card + str(i)
            self.scodes.append(scode_str)

    def generate_phoneNos(self):
        global num
        for i in range(30):
            num = self.pre_nos
            for i in range(8):
                random.shuffle(self.num_list)
                temp_num = random.choice(self.num_list)
                num = str(num) + str(temp_num)
            self.phone_nos.append(num)

    def generate_serial(self):
        for i in range(30):
            serial_str = self.const_key + '-' + self.const_card + '-' + str(i)
            self.serial_nos.append(serial_str)

    def generate_data(self):
        for i in range(30):
            query_tuple  = (self.regs[i],self.serial_nos[i],self.phone_nos[i],self.scodes[i],self.keys[i],self.cards[i])
            self.query_datalist.append(query_tuple)

    def insertDB(self,my_data):
        global con
        try:
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()
            cur.executemany('INSERT INTO t_data VALUES (?,?,?,?,?,?)', my_data)
            con.commit()
        except sqlite3.Error as e:
            if con:
                con.rollback()
            print("Error {}:".format(e.args[0]))
            sys.exit(1)
        finally:
            if con:
                con.close()

    def checkDbExistence(self):
        if os.path.exists(self.db_name):
            # remove existing
            print("[INFO] Database file already exist")
            print("[INFO] removing...")
            os.remove(self.db_name)
            print("[INFO] recreating...")
            self.createDb()
        else:
            print("[INFO] Creating DB...")
            self.createDb()

    def createDb(self):
        # create a new one
        stream = os.popen(f'sqlite3 {self.db_name}')
        print(f'[INFO] {stream}')
        global con
        try:
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()
            cur.execute('CREATE TABLE t_data( reg_no TEXT PRIMARY KEY,serial_no TEXT, phone_no TEXT NOT NULL,secret_code TEXT NOT NULL,uid_tag1 TEXT NOT NULL , uid_tag2 TEXT NOT NULL)')
            con.commit()
        except sqlite3.Error as e:
            if con:
                con.rollback()
            print("Error {}:".format(e.args[0]))
            sys.exit(1)
        finally:
            if con:
                con.close()

if __name__ == "__main__":
    gen = GenerateData()
    gen.generate_data()
    print("[INFO] inserting data...")
    gen.insertDB(gen.query_datalist)
    print("[INFO] done")
