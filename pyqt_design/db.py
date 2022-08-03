import sqlite3
import os 

class database:
    def __init__(self,path_):
        self.path = path_
        self.set_folder()
        self.create_database()
        
    def set_folder(self):
        if not(os.path.exists(self.path)):
            os.mkdir(self.path)
    def create_database(self):
        
        baglan = sqlite3.connect( self.path +"//dataes.db")
        veri = baglan.cursor()
        veri.execute("""CREATE TABLE IF NOT EXISTS data (
            'adi'	TEXT,
            'soyadi'	TEXT,
            'telefon'  TEXT UNIQUE,
            'kart_num'     TEXT,
            'bakiye' TEXT,
            PRIMARY KEY(telefon));""")
        baglan.commit()
        baglan.close()
        
        return True
    def add_user(self,user_info):#user_info is array
        baglan = sqlite3.connect( self.path +"//dataes.db")
        veri = baglan.cursor()
        result = veri.execute("select exists(select * from data where telefon = "+  user_info[2] + ")").fetchone()[0]
        if result == 0:
            veri.execute("INSERT INTO data (adi, soyadi, telefon, kart_num, bakiye) VALUES (?,?,?,?,?)",(user_info[0],user_info[1],user_info[2],user_info[3],user_info[4]))
        else:
            return False
        baglan.commit()
        baglan.close()
        return True
    def delete_user(self,telefon):
        baglan = sqlite3.connect( self.path +"//dataes.db")
        veri = baglan.cursor()
        result = veri.execute("select exists(select * from data where telefon = "+  telefon + ")").fetchone()[0]
        if result == 0:
            return False
        else:
            veri.execute("Delete from data where telefon='" + telefon + "'")
        baglan.commit()
        baglan.close()
        return True
    def update_user(self,user_info):#user_info is array
        baglan = sqlite3.connect( self.path +"//dataes.db")
        veri = baglan.cursor()
        print("select exists(select * from data where telefon = "+  user_info[2] + ")")  
        result = veri.execute("select exists(select * from data where telefon = "+  user_info[2] + ")").fetchone()[0]
        if result == 0:
            return False
        else:
            veri.execute("UPDATE data SET adi = '" + user_info[0] + "' WHERE telefon = '" + str(user_info[2])+"'" )
            veri.execute("UPDATE data SET soyadi = '" + user_info[1] + "' WHERE telefon = '" + str(user_info[2])+"'" )
            veri.execute("UPDATE data SET kart_num = '" + user_info[3] + "' WHERE telefon = '" + str(user_info[2])+"'" )
            veri.execute("UPDATE data SET bakiye = '" + user_info[4] + "' WHERE telefon = '" + str(user_info[2])+"'" )
        baglan.commit()
        baglan.close()
        return True
            





