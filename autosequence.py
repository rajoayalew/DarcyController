from PySide6.QtWidgets import QMainWindow, QApplication
from test import Ui_MainWindow, saveNewAutosequence

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)

app = QApplication()
window = saveNewAutosequence()
window.show()
app.exec()