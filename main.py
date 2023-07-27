import sys
from PyQt5.QtWidgets import QWidget, QApplication, \
    QFileDialog, QMessageBox, QButtonGroup
from PyQt5 import QtCore, QtGui
from mform import Ui_Form
from mserial import MySerial
import serial.tools.list_ports

class MainWin(QWidget, Ui_Form):
    def __init__(self, app) -> None:
        super().__init__()
        self.ports_list = []
        self.ports_status = []
        self.app = app
        self.setupUi(self)
        self.widget_setting()
        # self.ser = MySerial()
        self.scan_port()
    
    def widget_setting(self):
        self.comboBoxlist = [9600, 115200]
        self.comboBox_2.addItems(["9600", "115200"])
        self.comboBox_2.setCurrentIndex(1)

    def scan_port(self):
        self.ports_list = list(serial.tools.list_ports.comports())
        self.ports_status = [False] * len(self.ports_list)
        for comport in self.ports_list:
            self.comboBox.addItem(comport)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWin(app) # 必须赋值，不然python会回收这个对象
    mw.show()
    sys.exit(app.exec_())