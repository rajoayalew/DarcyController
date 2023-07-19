from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow
from communications import PortConnection

app = QApplication([])
comm = PortConnection()

window = MainWindow(app, comm)
window.show()

app.exec()

