from PySide6.QtWidgets import QApplication
from mainwindow import MainWindow

app = QApplication([])

window = MainWindow(app)
window.show()

app.exec()

