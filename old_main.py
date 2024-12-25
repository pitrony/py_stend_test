#from PySide6.QtCore import *
#from PySide6.QtGui import *
#from PySide6.QtWidgets import *
import sys
#import PySide6 import QtWidgets
#import for_rasb_stend

from PyQt5 import QtWidgets
from PyQt5.uic.Compiler.qtproxies import QtCore

import for_rasb_stend
import form_conf
import form_conf_speed

#class MainWindow(QtWidgets.QMainWindow, Ui_AuthWindow):
    #def __init__(self):
#Нужносоздатьклассдляформы:PythonВыделитькод
#class MyForm(QtWidgets.QDialog):
 #   def __init__(self, parent=None):
  #      super(MyForm, self).__init__(parent)
   #     self.form = Ui_Dialog()
    #    self.form.setupUi(self)


#Затемвфункциикнопкизаписатьследующиестроки:PythonВыделитькод

#def btnClick(self):
 #   dial = MyForm(self)
  #  dial.exec_()



   # super().__init__()
    #self.setupUi(self)
#self.input_nick.setPlaceholderText('input_nick')
#self.input_ip.setPlaceholderText('input_ip')
#self.input_port.setPlaceholderText('port')
 #   self.btn_connect.clicked.connect(self.add_label)
  #  self.configWindow = configWindow()
class MainApp(QtWidgets.QMainWindow, for_rasb_stend.Ui_MainWindow):
    def __init__(self):
        # Это здесь нужно для доступа к переменным, методам
        # и т.д. в файле design.py
        super().__init__()
        self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        self.pushButton_conf.clicked.connect(self.show_conf)  # Выполнить функцию browse_folder
        # при нажатии кнопки self.pushButton_conf.clicked.connect(MainApp.show_conf)

    def show_conf(self):
        self.switch_window.emit(self)
        #Confapp = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
        #MainApp.isHidden(self)
        #self.setupUi(self)
        #window = ConfApp  # Создаём объект класса ConfleApp
        #window.show()  # Показываем окно
        #confapp.focusWindowChanged()
class switch_windows:
    def __init__(self):
        pass
    def show_conf(self):
        self.conf=ConfApp()
        self.conf.switch_window.connect(self.show_main())
        self.conf.show()
    def show_main(self):
        self.window = MainApp()
        self.window.switch_window.connect(self.show_conf())
        self.conf.close()
        self.window.show()


class ConfApp(QtWidgets.QApplication, form_conf_speed.Ui_Form_conf_speed):
    switch_window=QtCore.pyqtSignal()

        def __init__(self):
            # Это здесь нужно для доступа к переменным, методам
            # и т.д. в файле design.py
            #QtWidgets.QWidget.__init__(self)

            super().__init__()
            self.setupUi(self)  # Это нужно для инициализации нашего дизайна
        def conf(self):
            self.switch_window.emit()
              # Выполнить функцию browse_folder
            # при нажатии кнопки
def main():
    app = QtWidgets.QApplication(sys.argv)  # Новый экземпляр QApplication
    switch=switch_windows()
    switch.show_main()
    #switch.show_conf()
    sys.exit(app.exec_())
    #window = MainApp()  # Создаём объект класса MainApp
    #window.show()  # Показываем окно

    #app.exec_()  # и запускаем приложение


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()



#app = QtWidgets.QApplication(sys.argv)
#
#AuthWindow = QtWidgets.QMainWindow()
#ui = Ui_AuthWindow()
#ui.setupUi(AuthWindow)
#AuthWindow.show()
#w = MainWindow()
#w.show()
#sys.exit(app.exec_())
