import sqlite3
import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from release.main_ui import Ui_MainWindow
from release.addEditCoffeeForm import Ui_MainForm

ID = None

class CoffeeSir(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.select_data()
        self.addButton.clicked.connect(self.addNewCoffee)
        self.editButton.clicked.connect(self.editCoffee)

    def select_data(self):
        query = 'SELECT * FROM Coffees'
        res = self.connection.cursor().execute(query).fetchall()
        self.tableWidget.setColumnCount(7)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(['ID', 'Название сорта', ' Степень обжарки', 'Молотый/в зернах',
                                                    'Описание вкуса', 'Цена', 'Объем упаковки'])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.connection.close()

    def addNewCoffee(self):
        self.new_form = CreateForm()
        self.new_form.show()
        self.close()

    def editCoffee(self):
        self.new_form = EditForm(self.tableWidget.currentRow() + 1)
        self.new_form.show()
        self.close()


class CreateForm(QMainWindow, Ui_MainForm):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.setText('Добавить')
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.pushButton.clicked.connect(self.save)

    def save(self):
        res = self.connection.cursor().execute(f'''
        INSERT INTO Coffees (name_of_sort, degree_of_roasting, coffee_grind_type, 
        description_of_taste, price, packaging_volume) 
        VALUES ("{self.lineEdit_2.text()}", "{self.lineEdit_3.text()}", "{self.lineEdit_4.text()}", 
        "{self.lineEdit_5.text()}", "{self.lineEdit_6.text()}", "{self.lineEdit_7.text()}");
        ''')
        self.connection.commit()
        self.main_form = CoffeeSir()
        self.main_form.show()
        self.close()


class EditForm(QMainWindow, Ui_MainForm):
    def __init__(self, *args):
        super().__init__()
        self.setupUi(self)
        self.connection = sqlite3.connect("data/coffee.sqlite")
        self.pushButton.clicked.connect(self.save)
        self.id = list(args)[0]
        query = f'SELECT * FROM Coffees WHERE id={self.id}'
        res = self.connection.cursor().execute(query).fetchall()
        self.lineEdit_2.setText(str(res[0][0]))
        self.lineEdit_3.setText(str(res[0][1]))
        self.lineEdit_4.setText(str(res[0][2]))
        self.lineEdit_5.setText(str(res[0][3]))
        self.lineEdit_6.setText(str(res[0][4]))
        self.lineEdit_7.setText(str(res[0][5]))

    def save(self):
        res = self.connection.cursor().execute(f'''
        UPDATE Coffees SET name_of_sort="{self.lineEdit_2.text()}", degree_of_roasting="{self.lineEdit_3.text()}", 
        coffee_grind_type="{self.lineEdit_4.text()}", description_of_taste="{self.lineEdit_5.text()}", 
        price="{self.lineEdit_6.text()}", packaging_volume="{self.lineEdit_7.text()}" WHERE id={self.id};
        ''')
        self.connection.commit()
        self.main_form = CoffeeSir()
        self.main_form.show()
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = CoffeeSir()
    ex.show()
    sys.exit(app.exec())
