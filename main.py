from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QPushButton
from sys import exit, argv
import sqlite3


from PyQt5 import QtCore, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1167, 551)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.table = QtWidgets.QTableWidget(self.centralwidget)
        self.table.setGeometry(QtCore.QRect(10, 10, 1151, 481))
        self.table.setObjectName("table")
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.add_button = QtWidgets.QPushButton(self.centralwidget)
        self.add_button.setGeometry(QtCore.QRect(10, 500, 241, 42))
        self.add_button.setObjectName("add_button")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Капучино"))
        self.add_button.setText(_translate("MainWindow", "Добавить запись"))


class Ui_addEditWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(392, 370)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.formLayoutWidget.setGeometry(QtCore.QRect(10, 10, 383, 291))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.name_edit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.name_edit.setObjectName("name_edit")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.name_edit)
        self.name_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.name_label.setObjectName("name_label")
        self.formLayout.setWidget(
            0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.name_label)
        self.degree_box = QtWidgets.QComboBox(self.formLayoutWidget)
        self.degree_box.setObjectName("degree_box")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.degree_box)
        self.degree_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.degree_label.setObjectName("degree_label")
        self.formLayout.setWidget(
            1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.degree_label)
        self.type_box = QtWidgets.QComboBox(self.formLayoutWidget)
        self.type_box.setObjectName("type_box")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.type_box)
        self.type_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.type_label.setObjectName("type_label")
        self.formLayout.setWidget(
            2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.type_label)
        self.description_edit = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.description_edit.setObjectName("description_edit")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.ItemRole.LabelRole, self.description_edit)
        self.description_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.description_label.setObjectName("description_label")
        self.formLayout.setWidget(
            3, QtWidgets.QFormLayout.ItemRole.FieldRole, self.description_label)
        self.price_box = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.price_box.setMaximum(100000)
        self.price_box.setObjectName("price_box")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.ItemRole.LabelRole, self.price_box)
        self.price_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.price_label.setObjectName("price_label")
        self.formLayout.setWidget(
            4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.price_label)
        self.volume_box = QtWidgets.QSpinBox(self.formLayoutWidget)
        self.volume_box.setMaximum(100000)
        self.volume_box.setObjectName("volume_box")
        self.formLayout.setWidget(
            5, QtWidgets.QFormLayout.ItemRole.LabelRole, self.volume_box)
        self.volume_label = QtWidgets.QLabel(self.formLayoutWidget)
        self.volume_label.setObjectName("volume_label")
        self.formLayout.setWidget(
            5, QtWidgets.QFormLayout.ItemRole.FieldRole, self.volume_label)
        self.save_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_button.setGeometry(QtCore.QRect(260, 320, 124, 42))
        self.save_button.setObjectName("save_button")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "not set"))
        self.name_label.setText(_translate("MainWindow", "Название сорта"))
        self.degree_label.setText(_translate("MainWindow", "Степень прожарки"))
        self.type_label.setText(_translate("MainWindow", "Тип"))
        self.description_label.setText(
            _translate("MainWindow", "Описание вкуса"))
        self.price_label.setText(_translate("MainWindow", "Цена упаковки"))
        self.volume_label.setText(_translate("MainWindow", "Объём упаковки"))
        self.save_button.setText(_translate("MainWindow", "Сохранить"))


class addEditWindow(QMainWindow, Ui_addEditWindow):
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
        self.setupUi(self)
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


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.data = []
        self.con = sqlite3.connect('coffe.sqlite')
        self.cur = self.con.cursor()
        self.initUi()

    def initUi(self):
        self.setupUi(self)
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
