"""from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton, QWidget, QHBoxLayout, QDockWidget

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QHBoxLayout(central_widget)
        button1 = QPushButton("Button 1")
        button2 = QPushButton("Button 2")
        button3 = QPushButton("Button 3")

        dock_widget = QDockWidget("Dock", self)
        print (dock_widget.allowedAreas())

        button4 = QPushButton("Button 4")
        dock_widget.setWidget(button4)

        layout.addWidget(button1)
        layout.addWidget(button2)
        layout.addWidget(button3)

app = QApplication([])

window = MyWindow()
window.setWindowTitle("Application #1")

window.show()
app.exec()"""

from communications import PortConnection
import time

NewConnect = PortConnection()

print (NewConnect.connectionStatus())

time.sleep(5)

NewConnect.updatePortList()
print (NewConnect.connectionStatus())


NewConnect.printPortList()

print(NewConnect.connectToPort())

while True:
    NewConnect.printLine()