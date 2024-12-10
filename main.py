import sqlite3
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import  QWidget, QApplication, QListWidgetItem, QMessageBox
from PyQt5.uic import loadUi
import sys




from qtconsole.qtconsoleapp import QtCore

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("kalend.ui", self)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        self.saveButton.clicked.connect(self.saveChanges)
        self.addButton.clicked.connect(self.addNewTask)
    
    def calendarDateChanged(self):
        print("The calendar date was changed.")
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        print("Date selected:", dateSelected)
        self.updateTaskList(dateSelected)

    def updateTaskList(self, date):
        self.tasksListWidget.clear()

        db = sqlite3.connect("basa123442.db")
        cursor = db.cursor()

        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date,)
        results = cursor.execute(query, row).fetchall()
        for result in results:
            item = QListWidgetItem(str(result[0]))
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            if result[1] == "YES":
                item.setCheckState(QtCore.Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(QtCore.Qt.Unchecked)
                self.tasksListWidget.addItem(item)

    def saveChanges(self):
        db = sqlite3.connect("basa123442.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()

        for i in range(self.tasksListWidget.count()):
            item = self.tasksListWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                querry = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND DATE = ?"
            else:
                querry = "UPDATE tasks SET completed = 'NO' WHERE tasks = ? AND DATE = ?"
            row = (task, date,)
            cursor.execute(querry,row)
        db.commit()

        messageBox = QMessageBox()
        messageBox.setText("Changes Saved")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

    def addNewTask(self):
        db = sqlite3.connect("basa123442.db")
        cursor = db.cursor()

        newTask = str(self.taskLineEdit.text())
        date = self.calendarWidget.selectedDate().toPyDate()

        querry = "INSERT INTO tasks(task, completed, date) VALUES (?,?,?)"
        row = (newTask, "NO", date,)

        cursor.execute(querry,row)
        db.commit()
        self.updateTaskList(date)
        self.taskLineEdit.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())    
