from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidgetItem
from PyQt5 import uic
from sys import exit, argv
import sqlite3


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUi()
        self.data = []

    def initUi(self):
        uic.loadUi('main.ui', self)
        self.load_button.clicked.connect(self.load_data)
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(('Название сорта', 'Степень прожарки',
                                              'Тип', 'Описание вкуса', 'Цена',
                                              'Объём (вес в граммах)'))
        self.table.resizeColumnsToContents()

    def load_data(self):
        try:
            filename = QFileDialog.getOpenFileName(
                self, 'Файл с базой данный', filter='Sqlite (*.sqlite , *.sqlite3)')[0]
            if not filename:
                raise ValueError()
            con = sqlite3.connect(filename)
            cur = con.cursor()
            data = cur.execute('SELECT coffe.name, degrees.name, ' +
                               'types.name, coffe.description, coffe.price, ' +
                               'coffe.volume FROM coffe INNER JOIN degrees ON ' +
                               'coffe.degree_id = degrees.id INNER JOIN types ' +
                               'ON coffe.type_id = types.id').fetchall()
            self.data = data
            self.update_table()
        except ValueError:
            QMessageBox.warning(
                self, 'Ошибка', 'Файл не выбран, данные не загружены')

    def update_table(self):
        self.table.setRowCount(len(self.data))
        for i, row in enumerate(self.data):
            for j, item in enumerate(row):
                text = str(item)
                if len(text) > 25:
                    text = text[:25] + '...'
                widget = QTableWidgetItem(text)
                self.table.setItem(i, j, widget)
        self.table.resizeColumnsToContents()


if __name__ == '__main__':
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec())
