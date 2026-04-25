from duty_call import DutyCallWindow
from PySide6.QtWidgets import QApplication
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DutyCallWindow()
    app.exec()