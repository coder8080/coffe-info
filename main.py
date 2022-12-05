from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QPushButton
from PyQt5 import uic
from sys import exit, argv
import sqlite3


class addEditWindow(QMainWindow):
    def __init__(self, type: str, con, cur, id=None, on_close=None):
        if type not in ['add', 'edit']:
            raise ValueError(
                f"Доступные типы: 'add', 'edit'. Полученный тип: '{type}'")
        super().__init__()
        self.type = type
        self.con = con
        self.cur = cur
        self.id = id
        self.available_degrees = []
        self.available_types = []
        self.on_close = on_close
        self.initUi()

    def update_combo_boxes(self):
        self.available_degrees = self.cur.execute(
            'SELECT id, name FROM degrees').fetchall()
        self.degree_box.clear()
        self.degree_box.addItems([el[1] for el in self.available_degrees])

        self.available_types = self.cur.execute(
            'SELECT id, name FROM types').fetchall()
        self.type_box.clear()
        self.type_box.addItems([el[1] for el in self.available_types])

    def initUi(self):
        uic.loadUi('addEditCoffeeForm.ui', self)
        self.save_button.clicked.connect(self.submit)
        self.update_combo_boxes()
        if self.type == 'edit':
            self.setWindowTitle('Редактирование')
            data = self.cur.execute(
                f'SELECT coffe.name, degrees.name, types.name, coffe.description,' +
                f' coffe.price, coffe.volume FROM coffe INNER JOIN degrees ON ' +
                f'coffe.degree_id = degrees.id INNER JOIN types ON coffe.type_id =' +
                f' types.id WHERE coffe.id = {self.id}').fetchall()[0]
            name, degree_name, type_name, description, price, volume = data
            self.name_edit.setText(name)
            self.degree_box.setCurrentText(degree_name)
            self.type_box.setCurrentText(type_name)
            self.description_edit.setText(description)
            self.price_box.setValue(price)
            self.volume_box.setValue(volume)
        elif self.type == 'add':
            self.setWindowTitle('Создание')

    def submit(self):
        name = self.name_edit.text()
        degree_name = self.degree_box.currentText()
        type_name = self.type_box.currentText()
        description = self.description_edit.text()
        price = self.price_box.value()
        volume = self.volume_box.value()

        if not name or not degree_name or not type_name or not description or price == 0 or volume == 0:
            QMessageBox.critical(
                self, 'Ошибка', 'Все поля обызательны для заполнения. Объём и цена не могут быть равны 0')
            return

        degree_id = None
        type_id = None

        for id, test_degree_name in self.available_degrees:
            if degree_name == test_degree_name:
                degree_id = id

        for id, test_type_name in self.available_types:
            if type_name == test_type_name:
                type_id = id

        query = None
        if self.type == 'add':
            query = f'INSERT INTO coffe (name, degree_id, type_id, description,' + \
                f' price, volume) VALUES ("{name}", {degree_id}, {type_id}, ' + \
                f'"{description}", {price}, {volume});'
        elif self.type == 'edit':
            query = f'UPDATE coffe SET name = "{name}", degree_id = {degree_id}, ' + \
                f'type_id = {type_id}, description = "{description}", price = {price},' + \
                    f' volume = {volume} WHERE id = {self.id};'
        self.cur.execute(query)
        self.con.commit()
        if self.on_close:
            self.on_close()
        self.close()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.data = []
        self.con = sqlite3.connect('coffe.sqlite')
        self.cur = self.con.cursor()
        self.initUi()

    def initUi(self):
        uic.loadUi('main.ui', self)
        self.add_button.clicked.connect(self.open_add_window)
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(('ID', 'Название сорта', 'Степень прожарки',
                                              'Тип', 'Описание вкуса', 'Цена',
                                              'Объём (вес в граммах)', 'Редактировать'))
        self.load_data()

    def load_data(self):
        self.data = self.cur.execute('SELECT coffe.id, coffe.name, degrees.name, ' +
                                     'types.name, coffe.description, coffe.price, ' +
                                     'coffe.volume FROM coffe INNER JOIN degrees ON ' +
                                     'coffe.degree_id = degrees.id INNER JOIN types ' +
                                     'ON coffe.type_id = types.id').fetchall()
        self.update_table()

    def onclick_fabric(self, id):
        def result():
            self.item_window = addEditWindow(
                'edit', self.con, self.cur, id, self.load_data)
            self.item_window.show()
        return result

    def update_table(self):
        self.table.setRowCount(len(self.data))
        for i, row in enumerate(self.data):
            for j, item in enumerate(row):
                text = str(item)
                if len(text) > 25:
                    text = text[:25] + '...'
                widget = QTableWidgetItem(text)
                self.table.setItem(i, j, widget)
            button = QPushButton('Редактировать', self)
            button.clicked.connect(self.onclick_fabric(row[0]))
            self.table.setCellWidget(i, 7, button)
        self.table.resizeColumnsToContents()

    def open_add_window(self):
        self.item_window = addEditWindow('add', self.con, self.cur,
                                         on_close=self.load_data)
        self.item_window.show()


if __name__ == '__main__':
    app = QApplication(argv)
    main_window = MainWindow()
    main_window.show()
    exit(app.exec())
