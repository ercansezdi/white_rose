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
        
        baglan = sqlite3.connect( self.path +"dataes.db")
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
        baglan = sqlite3.connect( self.path +"dataes.db")
        veri = baglan.cursor()
        result = veri.execute("select exists(select * from data where telefon = '"+  user_info[2] + "')").fetchone()[0]
        if result == 0:
            veri.execute("INSERT INTO data (adi, soyadi, telefon, kart_num, bakiye) VALUES (?,?,?,?,?)",(user_info[0],user_info[1],user_info[2],user_info[3],user_info[4]))
        else:
            return False
        baglan.commit()
        baglan.close()
        return True
    def delete_user(self,telefon):
        baglan = sqlite3.connect( self.path +"dataes.db")
        veri = baglan.cursor()
        result = veri.execute("select exists(select * from data where telefon = '"+  telefon + "')").fetchone()[0]
        if result == 0:
            return False
        else:
            veri.execute("Delete from data where telefon='" + telefon + "'")
        baglan.commit()
        baglan.close()
        return True
    def update_user(self,user_info):#user_info is array
        baglan = sqlite3.connect( self.path +"dataes.db")
        veri = baglan.cursor()
        result = veri.execute("select exists(select * from data where telefon = '"+  user_info[2] + "')").fetchone()[0]
        baglan.commit()
        baglan.close()
        if result == 0:
            return False
        else:
            baglan = sqlite3.connect( self.path +"dataes.db")
            veri = baglan.cursor()
            print(2)
            veri.execute("UPDATE data SET adi = '" + user_info[0] + "' WHERE telefon = '" + str(user_info[2])+"'" )
            veri.execute("UPDATE data SET soyadi = '" + user_info[1] + "' WHERE telefon = '" + str(user_info[2])+"'" )
            veri.execute("UPDATE data SET kart_num = '" + user_info[3] + "' WHERE telefon = '" + str(user_info[2])+"'" )
            veri.execute("UPDATE data SET bakiye = '" + user_info[4] + "' WHERE telefon = '" + str(user_info[2])+"'" )
            baglan.commit()
            baglan.close()
            print(3)
        return True
    def get_user(self,telefon):
        baglan = sqlite3.connect( self.path +"dataes.db")
        veri = baglan.cursor()
        if telefon == "all":
            data = veri.execute("SELECT * FROM data ").fetchall()
        else:
            data = veri.execute("SELECT * FROM data WHERE telefon = '{}'".format(telefon)).fetchall()
        baglan.commit()
        baglan.close()
        return data
    def get_user_with_card_num(self,card_num):
        baglan = sqlite3.connect( self.path +"dataes.db")
        veri = baglan.cursor()
        data = veri.execute("SELECT * FROM data WHERE kart_num = '{}'".format(card_num)).fetchall()
        baglan.commit()
        baglan.close()
        return data
    def get_all_similar_users(self,telefon):
        baglan = sqlite3.connect( self.path +"dataes.db")
        veri = baglan.cursor()
        veri.execute("select * from data")
        column = [name[0] for name in veri.description]
        data = []
        for column_name in column:
            result  = veri.execute("select * from data where {} like ? ".format(column_name),('%'+telefon+'%',)).fetchall()
            if len(result) != 0:
                data.append(result)
        baglan.commit()
        baglan.close()
        return data[0]
    def update_balance(self,telefon_number, new_balance):#user_info is array
        new_balance = str(new_balance)
        baglan = sqlite3.connect( self.path +"dataes.db")
        veri = baglan.cursor()
        veri.execute("UPDATE data SET bakiye = '" + new_balance + "' WHERE telefon = '" + str(telefon_number)+"'" )
        baglan.commit()
        baglan.close()
        return True





