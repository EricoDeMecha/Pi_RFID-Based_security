class DBHandler:
    dbPath = "../../DataBase/testData.db"
    def __init__(self):
        pass
    def handle_data(self,lock, text):
        if not text:
            pass
        else:
            lock.acquire()
            # handle data
            print(text)
            lock.release()