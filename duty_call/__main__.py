from datetime import datetime
import sys
import threading

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PySide6.QtCore import QTimer, QThread

from duty_call.tts import tts
from duty_call.types import DutyStudents

from .config import load_config

from .ui_MainWindow import Ui_MainWindow

class DutyCallWindow(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.datetime_update_timer = QTimer(self)
        self.datetime_update_timer.timeout.connect(self.update_datetime)
        self.datetime_update_timer.setInterval(1000)
        self.datetime_update_timer.start()

        try:
            self.config = load_config()
        except Exception as e:
            QMessageBox.critical(self, "加载配置失败", str(e))
            self.close()
        self.duty_students = self.get_duty_students()
        self.setup_duty_students()

        # 设置提醒定时器
        self.setup_reminder()
        # self.remind()


    def setup_reminder(self) -> None:
        """设置提醒定时器，使用singleShot设置一次性定时器"""
        dt = datetime.now()
        for time in self.config.reminder.times:
            t = datetime.now().replace(hour=time[0], minute=time[1])
            if t > dt:
                QTimer.singleShot(round((t - dt).total_seconds() * 1000), self.remind)
                print(f"Set reminder at {t.isoformat()}")


    def remind(self) -> None:
        self.showMaximized()
        separator = " " * self.config.reminder.tts_pause_spaces
        names_text = separator.join(self.get_duty_student_list())
        threading.Thread(target=tts, args=(self.config.reminder.text.format(names_text), )).start()
        QTimer.singleShot(self.config.reminder.alive_time * 1000, self.close)

    def get_duty_student_list(self) -> list[str]:
        students = []
        for group in self.duty_students.values():
            for student in group:
                students.append(student)
        return students


    def setup_duty_students(self) -> None:
        text ='<table style="text-align: center; width:100%; background:#fff; border-collapse:separate; border-spacing:0; border-radius:18px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.03); font-size:30px">'
        for work, students in self.duty_students.items():
            text += f'<tr><td style="padding:14px 18px; border-bottom:1px solid #eef2f6">{work}</td>'
            for student in students:
                text += f'<td style="padding:14px 18px; border-bottom:1px solid #eef2f6">{student}</td>'
            text += "</tr>"
        text += "</table>"
        self.students.setText(text)
        

    
    def get_duty_students(self) -> DutyStudents:
        dt = datetime.now()
        weekday = dt.weekday()
        if not (schedule := self.config.schedule.get(str(weekday))):
            raise Exception("今天没有值日生")
        students = {}
        for work, student in schedule:
            work_name = self.config.workAlias.get(work, work)
            if work_name not in students:
                students[work_name] = []
            students[work_name].append(student)
        return students

        


    def update_datetime(self):
        dt = datetime.now()
        self.dt.setText(dt.strftime("%Y-%m-%d %H:%M:%S %A"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DutyCallWindow()
    app.exec()