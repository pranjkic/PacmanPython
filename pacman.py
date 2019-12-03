# ovo ce nam biti main
from PyQt5.QtWidgets import *

import sys
from PyQt5.QtWidgets import QWidget, QDesktopWidget, QApplication
from PyQt5.QtGui import QIcon


class MainWindow(QMainWindow, QWidget):

    def __init__(self):
        super().__init__()

        self.init()

    def init(self):
        self.resize(600, 650)
        self.center()
        self.setWindowTitle("PAC-MAN")
        self.seticon()
        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def seticon(self):
        self.setWindowIcon(QIcon('pm.png'))

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
