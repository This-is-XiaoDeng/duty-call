import sys
import platform

from PySide6.QtWidgets import QApplication, QMessageBox

if platform.system() != "Windows":
    app = QApplication(sys.argv)
    QMessageBox.warning(
        None,
        "不支持的平台",
        "DutyCall 仅支持 Windows 系统运行，当前平台为 " + platform.system() + "。\n程序即将退出。"
    )
    sys.exit(1)

from duty_call import DutyCallWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DutyCallWindow()
    app.exec()
