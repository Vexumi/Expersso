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

        self.pushButton.clicked.connect(self.open_menu)
        self.pushButton_2.clicked.connect(self.view)
        self.setWindowTitle('Coffee, coffee, coffee!')
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
        self.con.close()

    def open_menu(self):
        self.menu = Menu()
        self.menu.show()


class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        uic.loadUi("addEditCoffeeForm.ui", self)
        self.show()

        self.pushButton.clicked.connect(self.add_item)
        self.pushButton_2.clicked.connect(self.del_item)

    def add_item(self):
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()

        if self.lineEdit.text() != '' and \
                self.lineEdit_2.text() != '' and \
                self.lineEdit_4.text() != '' and \
                self.lineEdit_5.text() != '' and \
                self.lineEdit_6.text() != '':
            zapros = 'INSERT INTO Coffee(Название_сорта, ' \
                     'Степень_обжарки, ' \
                     'Молотый_или_нет, ' \
                     'Описание_вкуса, ' \
                     'Цена, О' \
                     'бъем_упаковки) VALUES("{}", "{}", "{}", "{}", "{}", "{}")'.format(
                self.lineEdit.text(),
                self.lineEdit_2.text(),
                self.comboBox.currentText(),
                self.lineEdit_4.text(),
                self.lineEdit_5.text(),
                self.lineEdit_6.text())
            self.cur.execute(zapros)
            self.con.commit()
        else:
            QtWidgets.QMessageBox.information(self, 'Error', 'Заполните все поля!')
        self.con.close()
        self.exit()

    def del_item(self):
        self.con = sqlite3.connect('coffee.sqlite')
        self.cur = self.con.cursor()

        is_yes = QtWidgets.QMessageBox.question(
            self, 'Agree', 'Удалить {} элемент?'.format(
                self.spinBox.text()),
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No)

        if is_yes == QtWidgets.QMessageBox.Yes:
            zapros = 'DELETE FROM Coffee WHERE ID = {}'.format(self.spinBox.text())
            self.cur.execute(zapros)
            self.con.commit()
        self.con.close()
        self.exit()

    def exit(self):
        self.close()



def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
