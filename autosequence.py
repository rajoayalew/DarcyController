from PySide6.QtWidgets import QMainWindow, QApplication
from test import Ui_MainWindow, saveNewAutosequence


def main():
    app = QApplication([])
    main_window = QMainWindow()

    ui = Ui_MainWindow()
    ui.setupUi(main_window)

    main_window.show()
    app.exec_()

"""
def main():
    app = QApplication([])
    main_window = saveNewAutosequence()
    main_window.show()
    app.exec()
"""

if __name__ == "__main__":
    main()
