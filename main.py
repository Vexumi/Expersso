import sys
import sqlite3
from PyQt5.QtCore import Qt
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtWidgets import QLCDNumber, QLabel, QLineEdit, QCheckBox, QTableWidgetItem


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("main.ui", self)
        self.view()
        self.setWindowTitle('QCB')
        self.show()

    def view(self):
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()

        data = self.cur.execute('SELECT * FROM Coffee')
        data = [i for i in data]

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(('ID', 'Название', 'Степень обжарки',
                                                    'Молотый/в зернах', 'Описание вкуса', 'Цена',
                                                    'Объем упаковки'))
        self.tableWidget.setRowCount(0)
        for i, row in enumerate(data):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))
        self.tableWidget.resizeColumnsToContents()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
