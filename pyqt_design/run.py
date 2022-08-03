from main_ui import Ui_MainWindow
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication,QSizeGrip
from PyQt5.QtCore import QTimer,Qt,QEasingCurve, QPropertyAnimation
from PyQt5 import QtGui
import io

class MainWindow(QMainWindow):
    def __init__(self):
        super(QMainWindow,self).__init__()
        self.ui= Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.menu_button.clicked.connect(lambda: self.menu_kaydir())

        self.ui.main_page_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.main_page))
        self.ui.users_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.users))
        self.ui.add_user_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.add_user))
        self.ui.update_user_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.update_user))
        self.ui.delete_user_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.delete_user))
        self.ui.add_balance_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.add_balance))
        self.ui.settings_button.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.settings))




        


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
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())