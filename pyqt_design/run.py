#!/usr/bin/python
from asyncore import loop
from main_ui import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication,QSizeGrip
from PyQt5.QtCore import Qt,QEasingCurve, QPropertyAnimation,QTimer
from PyQt5 import QtWidgets
import db
from configparser import ConfigParser
import os 
import socket

from threading import Thread 

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)
       
        
        #database
        self.database = db.database("config//")
        #configparser

        self.config = ConfigParser()
        if not(os.path.isfile("config//config.ini")):
            self.config["defaults"] = {"entrance": "5","UDP_IP " : "127.0.0.1", "UDP_PORT" : 5005,"buffer_size":1024}
            with open("config//config.ini","w") as file_object:
                self.config.write(file_object)

        self.config.read("config//config.ini")
        self.entrance_fee = self.config["defaults"]["entrance"]

        #socket

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.config["defaults"]["UDP_IP"], int(self.config["defaults"]["UDP_PORT"])))

        x = Thread(target=self.read_channel)
        x.start()

        #Menu 
        self.ui.menu_button.clicked.connect(lambda: self.menu_kaydir())
        self.ui.main_page_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.main_page))
        self.ui.users_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.users))
        self.ui.users_button.clicked.connect(lambda: self.show_users())
        self.ui.add_user_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.add_user))
        self.ui.update_user_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.update_user))
        self.ui.delete_user_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.delete_user))
        self.ui.add_balance_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.add_balance))
        self.ui.settings_button.clicked.connect(lambda: self.settings())
        #Buttons

        self.ui.add_user_frame_add_button.clicked.connect(lambda: self.add_user())
        
        self.ui.delete_user_frame_delete_button.clicked.connect(lambda: self.delete_user())
        self.ui.delete_frame_get_user_entry_button.clicked.connect(lambda: self.get_delete_user())
        self.ui.users_frame_search_button.clicked.connect(lambda: self.show_users())
        self.ui.update_frame_get_user_entry_button.clicked.connect(lambda: self.update_user())
        self.ui.update_user_frame_update_button.clicked.connect(lambda: self.update_database_user())

        self.ui.add_balance_frame_get_user_entry_button.clicked.connect(lambda: self.add_balance())
        self.ui.add_balance_user_frame_delete_button.clicked.connect(lambda: self.add_database_balance())
        self.ui.settings_frame_button.clicked.connect(lambda: self.change_settings())





        
        self.defaults()

    
    def defaults(self):
        self.card_uuid = ""
        self.ui.users_frame_tableWidget.horizontalHeader().setDefaultSectionSize(130)

    
    def read_channel(self):
        while True:
           self.card_uuid, addr = self.sock.recvfrom(int(self.config["defaults"]["buffer_size"]))
           print(self.card_uuid)



    def show_users(self):
        search_text = self.ui.users_frame_search_entry.text()
        if search_text == "":
            users = self.database.get_user("all")
        else:
            users = self.database.get_all_similar_users(search_text)
        while (self.ui.users_frame_tableWidget.rowCount() > 0): 
            self.ui.users_frame_tableWidget.removeRow(0)
        for i in users:
            self.addTableRow(self.ui.users_frame_tableWidget, i)

    def addTableRow(self, table, row_data):
        row = table.rowCount()
        table.setRowCount(row+1)
        col = 0
        for item in row_data:
            cell = QtWidgets.QTableWidgetItem(str(item))
            cell.setTextAlignment(Qt.AlignHCenter)
            table.setItem(row, col, cell)
            
            col += 1

    def add_user(self):
        user = [self.ui.add_user_frame_entry_name.text(),self.ui.add_user_frame_entry_surname.text(),self.ui.add_user_frame_entry_telephone.text(),self.ui.add_user_frame_entry_card_number.text(),self.ui.add_user_frame_entry_balance.text()]
        if "" in user:
            self.ui.add_user_frame_warning_label.setText("You entered incomplete information !!!")
            self.ui.add_user_frame_warning_label.setStyleSheet("color: red;")
        else:
            result = self.database.add_user(user)
            if result:
                self.ui.add_user_frame_warning_label.setText("User Added. !!!")
                self.ui.add_user_frame_warning_label.setStyleSheet("color: green;")
            else:
                self.ui.add_user_frame_warning_label.setText("User already added. !!!")
                self.ui.add_user_frame_warning_label.setStyleSheet("color: red;")
    def get_delete_user(self):
        data = self.database.get_user(self.ui.delete_frame_get_user_entry.text())
        if len(data) > 0:
            if len(data[0]) == 5:
                self.ui.delete_user_frame_name.setText(data[0][0])
                self.ui.delete_user_frame_surname.setText(data[0][1])
                self.ui.delete_user_frame_phone_number.setText(data[0][2])
                self.ui.delete_user_frame_card_number.setText(data[0][3])
                self.ui.delete_user_frame_balance.setText(data[0][4]+"  TL")
            else:
                self.ui.delete_frame_warning_label.setText("Error !!!")
                self.ui.delete_frame_warning_label.setStyleSheet("color: red;")
        else:
            self.ui.delete_frame_warning_label.setText("User not found !!!")
            self.ui.delete_frame_warning_label.setStyleSheet("color: red;")
    def delete_user(self):
        user_telefon = self.ui.delete_frame_get_user_entry.text()
        if user_telefon == "":
            self.ui.delete_frame_warning_label.setText("You entered incomplete information !!!")
            self.ui.delete_frame_warning_label.setStyleSheet("color: red;")
        else:
            result = self.database.delete_user(user_telefon)
            if result:
                self.ui.delete_frame_warning_label.setText("User Deleted. !!!")
                self.ui.delete_frame_warning_label.setStyleSheet("color: green;")
            else:
                self.ui.delete_frame_warning_label.setText("Can't delete non user !!!")
                self.ui.delete_frame_warning_label.setStyleSheet("color: red;")
    def update_user(self):
        user_telefon = self.ui.update_frame_get_user_entry.text()
        if user_telefon == "":
            self.ui.update_frame_warning_label.setText("Phone number to call was not entered !!!")
            self.ui.update_frame_warning_label.setStyleSheet("color: red;")
        else:
            data = self.database.get_user(user_telefon)
            if len(data) != 0:
                self.ui.update_user_frame_name.setPlaceholderText(data[0][0])
                self.ui.update_user_frame_surname.setPlaceholderText(data[0][1])
                self.ui.update_user_frame_phone_number.setText(data[0][2])
                self.ui.update_user_frame_card_number.setPlaceholderText(data[0][3])
                self.ui.update_user_frame_balance.setText(data[0][4]+"  TL")
            else:
                self.ui.update_frame_warning_label.setText("User not found !!!")
                self.ui.update_frame_warning_label.setStyleSheet("color: red;")
    def update_database_user(self):
        user_telefon = self.ui.update_frame_get_user_entry.text()
        if user_telefon == "":
            self.ui.update_frame_warning_label.setText("Phone number to call was not entered !!!")
            self.ui.update_frame_warning_label.setStyleSheet("color: red;")
        else:
            data = self.database.get_user(user_telefon)
            if len(data) != 0:
                res = self.database.update_user([data[0][0],data[0][1],data[0][2],data[0][3],data[0][4]])
                self.ui.update_frame_warning_label.setText("User information updated  !!!")
                self.ui.update_frame_warning_label.setStyleSheet("color: green;")
            else:
                self.ui.update_frame_warning_label.setText("User not found !!!")
                self.ui.update_frame_warning_label.setStyleSheet("color: red;")

    def  add_database_balance(self):
        user_telefon = self.ui.add_balance_frame_get_user_entry.text()
        if user_telefon == "":
            self.ui.add_balance_frame_warning_label.setText("Phone number to call was not entered !!!")
            self.ui.add_balance_frame_warning_label.setStyleSheet("color: red;")
        else:
            data = self.database.get_user(user_telefon)
            if len(data) != 0:
                if self.ui.add_balance_frame_how_much.text() == "" or not self.ui.add_balance_frame_how_much.text().isnumeric():
                    self.ui.add_balance_frame_warning_label.setText("Balance entered incorrectly !!!")
                    self.ui.add_balance_frame_warning_label.setStyleSheet("color: red;")
                else:
                    balance = str(float(data[0][4]) + float(self.ui.add_balance_frame_how_much.text()))
                    res = self.database.update_balance(data[0][2],balance)
                    self.ui.add_balance_frame_balance.setText(balance +"  TL")
                    self.ui.add_balance_frame_warning_label.setText("User information updated  !!!")
                    self.ui.add_balance_frame_warning_label.setStyleSheet("color: green;")
            else:
                self.ui.add_balance_frame_warning_label.setText("User not found !!!")
                self.ui.add_balance_frame_warning_label.setStyleSheet("color: red;")   
    def add_balance(self):
        user_telefon = self.ui.add_balance_frame_get_user_entry.text()
        if user_telefon == "":
            self.ui.add_balance_frame_warning_label.setText("Phone number to call was not entered !!!")
            self.ui.add_balance_frame_warning_label.setStyleSheet("color: red;")
        else:
            data = self.database.get_user(user_telefon)
            if len(data) != 0:
                self.ui.add_balance_frame_name.setText(data[0][0])
                self.ui.add_balance_frame_surname.setText(data[0][1])
                self.ui.add_balance_frame_phone_number.setText(data[0][2])
                self.ui.add_balance_frame_card_number.setText(data[0][3])
                self.ui.add_balance_frame_balance.setText(data[0][4] +"  TL")
            else:
                self.ui.add_balance_frame_warning_label.setText("User not found !!!")
                self.ui.add_balance_frame_warning_label.setStyleSheet("color: red;")
    def settings(self):
        self.ui.settings_frame_entry_entrance_fee.setPlaceholderText(self.config["defaults"]["entrance"] )
        self.ui.settings_frame_entry_udp_ip.setPlaceholderText(self.config["defaults"]["UDP_IP"] )
        self.ui.settings_frame_entry_buffer_size.setPlaceholderText(self.config["defaults"]["buffer_size"] )
        self.ui.settings_frame_entry_udp_port.setPlaceholderText(self.config["defaults"]["UDP_PORT"] )
        self.ui.settings_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.settings))
    def change_settings(self):
        if self.ui.settings_frame_entry_entrance_fee.text().isnumeric():
            self.entrance_fee = self.ui.settings_frame_entry_entrance_fee.text()
            self.config["defaults"]["entrance"] = self.entrance_fee
            print(1)
        if self.ui.settings_frame_entry_buffer_size.text() != "":
            self.config["defaults"]["buffer_size"] = self.ui.settings_frame_entry_buffer_size.text()
            print(2)
        if self.ui.settings_frame_entry_udp_ip.text() != "":
            self.config["defaults"]["UDP_IP"] = self.ui.settings_frame_entry_udp_ip.text()
            print(3)
        if self.ui.settings_frame_entry_udp_port.text() != "":
            self.config["defaults"]["UDP_PORT"] = self.ui.settings_frame_entry_udp_port.text()
            print(4)
            



        self.ui.settings_frame_entry_entrance_fee.setPlaceholderText(self.config["defaults"]["entrance"] +"  TL")
        self.ui.settings_frame_entry_udp_ip.setPlaceholderText(self.config["defaults"]["UDP_IP"] )
        self.ui.settings_frame_entry_buffer_size.setPlaceholderText(self.config["defaults"]["buffer_size"] )
        self.ui.settings_frame_entry_udp_port.setPlaceholderText(self.config["defaults"]["UDP_PORT"] )
    
        with open('config//config.ini', 'w') as configfile:
            self.config.write(configfile)

    def menu_kaydir(self):
        width = self.ui.left_menu.width()
        if width == 50:
            new_width = 150 
        else:
            new_width = 50
        self.animation = QPropertyAnimation(self.ui.left_menu,b"minimumWidth")
        self.animation.setDuration(250)
        self.animation.setStartValue(width)
        self.animation.setEndValue(new_width)
        self.animation.setEasingCurve(QEasingCurve.InOutQuart)
        self.animation.start()
    def listen_port(self):
        print("XX")
        data, addr = self.sock.recvfrom(1024) # buffer size is 1024 bytes
        #print("received message: %s" % data)
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())