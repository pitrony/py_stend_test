from PyQt5 import QtWidgets
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QListWidget, QListView, QApplication
from PyQt5.uic.Compiler.qtproxies import QtGui, QtCore
#from PyQt5 import QtCore.QStringListModel, QtCore.QPropertyAnimation
#from PySide6.QtCore import QPropertyAnimation
#from PyQt5 import QtCore.QPropertyAnimation
from PyQt5.QtCore import QPropertyAnimation, QPoint
from for_rasb_stend import Ui_MainWindow
from form_conf_speed import Ui_Form_conf_speed
import sys, ast, time
from functools import partial
from PyQt5.QtCore import QTimer, QPropertyAnimation
import smbus
import paho.mqtt.publish as publish
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap



bus = smbus.SMBus(1)
# bWrite=0x00
mask=0xFF
adr_3 = 0x22
adr_2 = 0x24
adr_1 = 0x20
i = 0
data1 = 255
data2 = 255
data3 = 255
alarms = str('')

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self)
        #self.mylist = self.main_window.listView_alarms
        #self.model=QtCore.QStringListModel(self)
        self.config_window = QtWidgets.QWidget()
        self.config_ui = Ui_Form_conf_speed()
        self.config_ui.setupUi(self.config_window)
        self.main_window.pushButton_conf.clicked.connect(self.show_config)
        self.main_window.actionconfig.triggered.connect(self.show_config)
        self.main_window.actionStart.triggered.connect(self.start_transmitting)
        self.main_window.actionStop.triggered.connect(self.stop_transmitting)
        self.main_window.actionexit.triggered.connect(self.main_window.pushButton_exit.clicked)
        self.config_ui.pushButton_cancel.clicked.connect(self.show_main)
        self.config_ui.pushButtonOk.clicked.connect(self.save_settings)
        self.main_window.label_updw.setScaledContents(True)
        self.main_window.label_opcl.setScaledContents(True)
        self.main_window.label_updw.setPixmap(QPixmap('move_stop.png'))
        self.main_window.label_move.setPixmap(QPixmap('lift_cab_64.png'))
        #self.main_window.radioButton_rgk.setEnabled(False)
        #self.main_window.radioButton_fri.setEnabled(False)
        self.init_timer()
        self.init_connections()
        self.init_list_view()

    def init_connections(self):
        self.main_window.pushButton_start.clicked.connect(self.start_transmitting)
        self.main_window.pushButton_stop.clicked.connect(self.stop_transmitting)
        self.main_window.radioButton_501.toggled.connect(self.move_lift_up)
        self.main_window.radioButton_500.toggled.connect(self.move_lift_down)

    def move_lift_up(self, checked):
        if checked:
            if(self.main_window.radioButton_500.isChecked() != True):# Lift should move up when radioButton_501 is checked
                self.animate_lift_up()

    def move_lift_down(self, checked):
        if checked:
            if(self.main_window.radioButton_501.isChecked() != True):
                self.animate_lift_down()

    def animate_lift_up(self):
        self.animation = QPropertyAnimation(self.main_window.label_move, b"pos")
        self.animation.setDuration(2000)  # 1 second duration
        self.animation.setStartValue(QPoint(100, 190))
        self.animation.setEndValue(QPoint(100, 10))
        self.animation.start()
        # Create animation for smooth movement
        #animation = QtCore.QPropertyAnimation(self.main_window.label_move, b"geometry")
        #animation.setDuration(1000)  # 1 second duration
        #current_geometry = self.main_window.label_move.geometry()
        # Target position - Adjust Y coordinate to move up
        #target_y = max(0, current_geometry.y() - 50)  # Move 50px up, adjust as needed
        # Set start and end geometry
        #animation.setStartValue(current_geometry)
        #animation.setEndValue(QtCore.QRect(current_geometry.x(), target_y, current_geometry.width(), current_geometry.height()))
        #animation.start()

    def animate_lift_down(self):
        #self.animation = QtCore.QPropertyAnimation(self.main_window.label_move, b"geometry")
        self.animation = QPropertyAnimation(self.main_window.label_move, b"pos")
        self.animation.setDuration(2000)  # 1 second duration
        #current_geometry = self.main_window.label_move.geometry()
        # Target position - Adjust Y coordinate to move down
        #max_y = self.main_window.frame_for_mov.geometry().height() - current_geometry.height()
        #target_y = min(max_y, current_geometry.y() + 50)  # Move 50px down, adjust as needed
        #print(target_y)
        # Set start and end geometry
        self.animation.setStartValue(QPoint(100, 190))
        self.animation.setEndValue(QPoint(100, 400))
        #self.animation.setEndValue(QtCore.QRect(current_geometry.x(), target_y, current_geometry.width(), current_geometry.height()))
        self.animation.start()

    def start_saving_alarms(self):
        self.save_alarms_to_file()
        self.timer.start(5000)  # Save every 5000 ms (5 seconds)

    def stop_saving_alarms(self):
        self.timer.stop()

    def save_alarms_to_file(self):
        # Get model from listView_alarms
        model = self.main_window.listView_alarms.model()
        if model:
            with open("alarms_log.txt", "w") as file:
                for row in range(model.rowCount()):
                    item = model.data(model.index(row, 0))
                    file.write(item + "\n")
    def start_transmitting(self):
        # Start timer to update main window periodically
        self.timer.start(5000)  # 500 ms interval
        self.main_window.pushButton_stop.setChecked(False)

    def stop_transmitting(self):
        # Stop timer to halt updates to the main window and alarms
        self.timer.stop()
        self.main_window.pushButton_start.setChecked(False)

    def init_list_view(self):
        #list alarms
        self.model = QStandardItemModel()
        self.main_window.listView_alarms.setModel(self.model)


    def init_timer(self): #timer
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.save_alarms_to_file)
        self.timer.timeout.connect(self.read_raspb)
        #self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(lambda: self.update_main_window(data1, data2, data3, alarms))
        #self.timer.timeout.connect(self.update_main_window(data1, data2, alarms))
        #self.timer.start(5000)  # 500 milliseconds = 0.5 seconds
    def list_adding(self, alarms):
        if (alarms != ''):
            item = QStandardItem(alarms)
            self.model.appendRow(item)

    def show_config(self):
        self.hide()
        self.load_settings()
        self.config_window.show()

    def show_main(self):
        self.config_window.hide()
        self.show()
        if(self.main_window.pushButton_start.isChecked()):
            self.read_raspb()
            self.update_main_window(data1, data2, data3, alarms)


    def save_settings(self):
        settings = {
            'leveling': (self.config_ui.radioButton_rh_l.isChecked(), self.config_ui.radioButton_rf_l.isChecked(), self.config_ui.radioButton_ry_l.isChecked(),),
            'floor_approach': (self.config_ui.radioButton_rh_f.isChecked(), self.config_ui.radioButton_rf_f.isChecked(), self.config_ui.radioButton_ry_f.isChecked(),),
            'return_back': (self.config_ui.radioButton_rh_ret.isChecked(), self.config_ui.radioButton_rf_ret.isChecked(), self.config_ui.radioButton_ry_ret.isChecked(),),
            'card_revision': (self.config_ui.radioButton_rh_c.isChecked(), self.config_ui.radioButton_rf_c.isChecked(),
                              self.config_ui.radioButton_ry_c.isChecked(),),
            'shaft_revision': (self.config_ui.radioButton_rh_sh.isChecked(), self.config_ui.radioButton_rf_sh.isChecked(),
                              self.config_ui.radioButton_ry_sh.isChecked(),),
            'normal': (self.config_ui.radioButton_rh_n.isChecked(), self.config_ui.radioButton_rf_n.isChecked(),
                       self.config_ui.radioButton_ry_n.isChecked(),),
            'high': (self.config_ui.radioButton_rh_h.isChecked(), self.config_ui.radioButton_rf_h.isChecked(),
                     self.config_ui.radioButton_ry_h.isChecked(),),
            'max_speed': (self.config_ui.radioButton_rh_m.isChecked(), self.config_ui.radioButton_rf_m.isChecked(), self.config_ui.radioButton_ry_m.isChecked(),),
            'reading_shaft': (self.config_ui.radioButton_rh_read.isChecked(), self.config_ui.radioButton_rf_read.isChecked(), self.config_ui.radioButton_ry_read.isChecked(),),
        }
        with open('config_settings.txt', 'w') as file:
            file.write(str(settings))
        self.show_main()

    def load_settings(self):
        try:
            with open('config_settings.txt', 'r') as file:
                data = file.read()
                settings = ast.literal_eval(data)  # Преобразуем строку обратно в словарь

            # Восстанавливаем состояние радиокнопок на основе сохраненных значений
            self.config_ui.radioButton_rh_l.setChecked(settings.get('leveling', ())[0])
            self.config_ui.radioButton_rf_l.setChecked(settings.get('leveling', ())[1])
            self.config_ui.radioButton_ry_l.setChecked(settings.get('leveling', ())[2])

            self.config_ui.radioButton_rh_f.setChecked(settings.get('floor_approach', ())[0])
            self.config_ui.radioButton_rf_f.setChecked(settings.get('floor_approach', ())[1])
            self.config_ui.radioButton_ry_f.setChecked(settings.get('floor_approach', ())[2])

            self.config_ui.radioButton_rh_ret.setChecked(settings.get('return_back', ())[0])
            self.config_ui.radioButton_rf_ret.setChecked(settings.get('return_back', ())[1])
            self.config_ui.radioButton_ry_ret.setChecked(settings.get('return_back', ())[2])

            self.config_ui.radioButton_rh_c.setChecked(settings.get('card_revision', (False, False, False))[0])
            self.config_ui.radioButton_rf_c.setChecked(settings.get('card_revision', (False, False, False))[1])
            self.config_ui.radioButton_ry_c.setChecked(settings.get('card_revision', (False, False, False))[2])

            self.config_ui.radioButton_rh_sh.setChecked(settings.get('shaft_revision', (False, False, False))[0])
            self.config_ui.radioButton_rf_sh.setChecked(settings.get('shaft_revision', (False, False, False))[1])
            self.config_ui.radioButton_ry_sh.setChecked(settings.get('shaft_revision', (False, False, False))[2])

            self.config_ui.radioButton_rh_n.setChecked(settings.get('normal', (False, False, False))[0])
            self.config_ui.radioButton_rf_n.setChecked(settings.get('normal', (False, False, False))[1])
            self.config_ui.radioButton_ry_n.setChecked(settings.get('normal', (False, False, False))[2])

            self.config_ui.radioButton_rh_h.setChecked(settings.get('high', (False, False, False))[0])
            self.config_ui.radioButton_rf_h.setChecked(settings.get('high', (False, False, False))[1])
            self.config_ui.radioButton_ry_h.setChecked(settings.get('high', (False, False, False))[2])

            self.config_ui.radioButton_rh_m.setChecked(settings.get('max_speed', (False, False, False))[0])
            self.config_ui.radioButton_rf_m.setChecked(settings.get('max_speed', (False, False, False))[1])
            self.config_ui.radioButton_ry_m.setChecked(settings.get('max_speed', (False, False, False))[2])

            self.config_ui.radioButton_rh_read.setChecked(settings.get('reading_shaft', (False, False, False))[0])
            self.config_ui.radioButton_rf_read.setChecked(settings.get('reading_shaft', (False, False, False))[1])
            self.config_ui.radioButton_ry_read.setChecked(settings.get('reading_shaft', (False, False, False))[2])

        except FileNotFoundError:
            print("Configuration file not found, using default settings.")
            # Если файл не найден, используем стандартные значения
            pass



    def update_main_window(self, data1, data2, data3, alarms):
        data1, data2, data3 = self.read_raspb()
        #print(data1, ' ', data2, ' ', data3, ' \n')
        # Decode data1 for speed and other
        speed = data1 & 0b111
        ru1= (data1 >> 3) & 0b1
        ru2 = (data1 >> 4) & 0b1
        krc= (data1 >> 5) & 0b1
        frn= (data1 >> 6) & 0b1
        ptc  = (data1 >> 7) & 0b1
        # Update main window checkboxes
        self.main_window.radioButton_ptc.setChecked(bool(ptc))
        self.main_window.radioButton_frn.setChecked(bool(frn))
        self.main_window.radioButton_ru1.setChecked(bool(ru1))
        self.main_window.radioButton_ru2.setChecked(bool(ru2))
        self.main_window.radioButton_krc.setChecked(bool(krc))
        #self.list_adding(alarms)
       # self.main_window.listView_alarms(alarms)
        # Handle speed logic reading config_settings.txt after than set speed label !
        if speed==7:
            self.main_window.label_speed.setText('Speed 7 rh=1 rf=1 ry=1')
        elif speed==6:
            self.main_window.label_speed.setText('Speed 6 rh=1 rf=1 ry=0')
        elif speed==5:
            self.main_window.label_speed.setText('Speed 5 rh=1 rf=0 ry=1')
        elif speed==4:
            self.main_window.label_speed.setText('Speed 4 rh=1 rf=0 ry=0')
        elif speed==3:
            self.main_window.label_speed.setText('Speed 3 rh=0 rf=1 ry=1')
        elif speed==2:
            self.main_window.label_speed.setText('Speed 2 rh=0 rf=1 ry=0')
        elif speed == 1:
            self.main_window.label_speed.setText('Speed 1 rh=0 rf=0 ry=1')
        elif speed == 0:
            self.main_window.label_speed.setText('Speed 0 rh=0 rf=0 ry=0')

        #elif speed == 2:
         #   self.config_ui.radioButton_rh_l.setChecked(False)
          #  self.config_ui.radioButton_rf_f.setChecked(True)
           # self.config_ui.radioButton_ry_ret.setChecked(False)

        # Decode data2 for movement and door state
        ins = data2 & 0b1
        up = (data2 >> 1) & 0b1
        down= (data2 >> 2) & 0b1
        ml1 = (data2 >> 3) & 0b1
        ml2 = (data2 >> 4) & 0b1
        door = (data2 >> 5) & 0b1
        top = (data2 >> 6) & 0b1
        bot = (data2 >> 7) & 0b1

        if(door == 1):
            self.main_window.label_opcl.setPixmap(QPixmap('close_door.png'))
            #self.main_window.label_opcl.setPixmap(QPixmap('1_d_cl_64.png'))
        else:
            self.main_window.label_opcl.setPixmap(QPixmap('open_door.png'))

        if (ru1 == 1 and ru2 !=1):
            self.main_window.label_updw.setPixmap(QPixmap('move_up.png'))

        if(ru2 == 1 and ru1 !=1):
            self.main_window.label_updw.setPixmap(QPixmap('move_dwn.png'))

        if ((ru2 == 1 and ru1 == 1) or (ru2 == 0 and ru1 == 0)):
            self.main_window.label_updw.setPixmap(QPixmap('move_stop.png'))


        self.main_window.radioButton_500.setChecked(bool(up))
        self.main_window.radioButton_501.setChecked(bool(down))
        self.main_window.radioButton_opcl.setChecked(bool(door))
        self.main_window.radioButton_ml1.setChecked(bool(ml1))
        self.main_window.radioButton_ml2.setChecked(bool(ml2))
        self.main_window.radioButton_ins.setChecked(bool(ins))
        self.main_window.radioButton_817.setChecked(bool(bot))
        self.main_window.radioButton_818.setChecked(bool(top))

        if(top==0 and bot==0):
           alarms=str("Error 1: 817 and 818 both off ")
           self.list_adding(alarms)
        if (down == 1 and up == 1):
            alarms = str("Error 2: UP and Down both on ")
            self.list_adding(alarms)
        if (ru1 == 1 and ru2 == 1):
            alarms = str("Error 3:  up direct and down direct both on ")
            self.list_adding(alarms)
        if (ml1 == 0 and ml2 == 0 and door == 1):
            alarms = str("Error 4:  try open not in floor ")
            self.list_adding(alarms)
        if ((ru1 == 1 or ru2 == 1) and krc == 0):
            alarms = str("Error 5:  contactor not on in move ")
            self.list_adding(alarms)
        if (ptc == 0):
            alarms = str('Error 6: Overheat motor')
            self.list_adding(alarms)
        rgk = data3 & 0b1
        fri = (data3 >> 1) & 0b1
        ppp = (data3 >> 2) & 0b1
        safe = (data3 >> 3) & 0b1
        d_sh = (data3 >> 4) & 0b1
        d_cab = (data3 >> 5) & 0b1
        light = (data3 >> 6) & 0b1
        rez1 = (data3 >> 7) & 0b1
        self.main_window.radioButton_rgk.setChecked(bool(rgk))
        self.main_window.radioButton_fri.setChecked(bool(fri))
        #self.main_window.radioButton_ppp.setChecked(bool(ppp))
        self.main_window.radioButton_120.setChecked(bool(safe))
        self.main_window.radioButton_130.setChecked(bool(d_sh))
        self.main_window.radioButton_140.setChecked(bool(d_cab))
        self.main_window.radioButton_light.setChecked(bool(light))
        self.main_window.radioButton_rez1.setChecked(bool(rez1))


    def read_raspb(self):
        bus.write_byte(adr_2, 0xFF)
        bus.write_byte(adr_1, 0xFF)
        bus.write_byte(adr_3, 0xFF)
        data1 = bus.read_byte(adr_1)
        data2 = bus.read_byte(adr_2)
        data3 = bus.read_byte(adr_3)
        #print(data1, ' ', data2, ' ', data3, ' \n')

        msgs = [{'topic': "/orange/data1", 'payload': data1}, ("/orange/data2", data2, 0, False),
                ("/orange/data3", data3, 0, False)]
        publish.multiple(msgs, hostname="mqtt.eclipseprojects.io")
        time.sleep(1)
        return data1, data2, data3

# printing result
#print("Extracted Rows : " + str(res))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())