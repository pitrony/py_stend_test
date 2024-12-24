from PyQt5 import QtWidgets
from for_rasb_stend import Ui_MainWindow
from form_conf_speed import Ui_Form_conf_speed
import sys

class MainApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()
        self.main_window = Ui_MainWindow()
        self.main_window.setupUi(self)
        
        self.config_window = QtWidgets.QWidget()
        self.config_ui = Ui_Form_conf_speed()
        self.config_ui.setupUi(self.config_window)

        self.main_window.pushButton_conf.clicked.connect(self.show_config)
        self.config_ui.pushButton_cancel.clicked.connect(self.show_main)
        self.config_ui.pushButtonOk.clicked.connect(self.save_settings)

    def show_config(self):
        self.hide()
        self.config_window.show()

    def show_main(self):
        self.config_window.hide()
        self.show()
    
    def save_settings(self):
        settings = {
            'leveling': self.config_ui.radioButton_rh_l.isChecked(),
            'floor_approach': self.config_ui.radioButton_rf_f.isChecked(),
            'max_speed': self.config_ui.radioButton_rf_h.isChecked(),
        }
        with open('config_settings.txt', 'w') as file:
            file.write(str(settings))
        self.show_main()

    def update_main_window(self, data1, data2):
        # Decode data1 for speed and PTC
        speed = data1 & 0b111
        ptc = (data1 >> 3) & 0b1
        frn = (data1 >> 4) & 0b1
        ru1 = (data1 >> 5) & 0b1
        ru2 = (data1 >> 6) & 0b1
        rgk = (data1 >> 7) & 0b1
        
        # Update main window checkboxes
        self.main_window.radioButton_ptc.setChecked(bool(ptc))
        self.main_window.radioButton_frn.setChecked(bool(frn))
        self.main_window.radioButton_817.setChecked(bool(ru1))
        self.main_window.radioButton_818.setChecked(bool(ru2))
        self.main_window.radioButton_rgk.setChecked(bool(rgk))
        
        # Handle speed logic
        if speed == 1:
            self.config_ui.radioButton_rh_l.setChecked(True)
            self.config_ui.radioButton_rf_f.setChecked(False)
            self.config_ui.radioButton_ry_ret.setChecked(False)
        elif speed == 2:
            self.config_ui.radioButton_rh_l.setChecked(False)
            self.config_ui.radioButton_rf_f.setChecked(True)
            self.config_ui.radioButton_ry_ret.setChecked(False)
        elif speed == 3:
            self.config_ui.radioButton_rh_l.setChecked(True)
            self.config_ui.radioButton_rf_f.setChecked(True)
            self.config_ui.radioButton_ry_ret.setChecked(False)
        elif speed == 4:
            self.config_ui.radioButton_rh_l.setChecked(False)
            self.config_ui.radioButton_rf_f.setChecked(False)
            self.config_ui.radioButton_ry_ret.setChecked(True)
        
        # Decode data2 for movement and door state
        up = data2 & 0b1
        down = (data2 >> 1) & 0b1
        insp = (data2 >> 2) & 0b1
        ml1 = (data2 >> 3) & 0b1
        ml2 = (data2 >> 4) & 0b1
        door = (data2 >> 5) & 0b1
        top = (data2 >> 6) & 0b1
        bot = (data2 >> 7) & 0b1
        
        # Update main window status
        self.main_window.radioButton_opcl.setChecked(bool(door))
        self.main_window.radioButton_ml1.setChecked(bool(ml1))
        self.main_window.radioButton_ml2.setChecked(bool(ml2))
        self.main_window.radioButton_ins.setChecked(bool(insp))
        
        if not top:
            self.main_window.radioButton_817.setChecked(True)
        if not bot:
            self.main_window.radioButton_818.setChecked(True)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())
