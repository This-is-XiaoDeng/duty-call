from datetime import datetime
import sys
import threading

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QMainWindow, QApplication, QMessageBox, QSizePolicy
from PySide6.QtCore import QTimer, QThread

from duty_call.table import build_students_table
from duty_call.tts import tts
from duty_call.types import DutyStudents

from .config import load_config

from .ui_MainWindow import Ui_MainWindow

class DutyCallWindow(QMainWindow, Ui_MainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        # 不让表格的 sizeHint 反过来把窗口最小尺寸撑到屏幕之外
        self.students.setMinimumSize(0, 0)
        self.students.setSizePolicy(
            QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred
        )
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
        if not self.config.reminder.times:
            self.remind()
        for time in self.config.reminder.times:
            t = datetime.now().replace(hour=time[0], minute=time[1])
            if t > dt:
                QTimer.singleShot(round((t - dt).total_seconds() * 1000), self.remind)
                print(f"Set reminder at {t.isoformat()}")


    def remind(self) -> None:
        self.showMaximized()
        names = self.get_duty_student_list()
        text = self.config.reminder.text.format(self.config.reminder.name_separator.join(names))
        threading.Thread(target=tts, args=(text, self.config.reminder.volume)).start()
        QTimer.singleShot(self.config.reminder.alive_time * 1000, self.hide)

    def get_duty_student_list(self) -> list[str]:
        students = []
        for group in self.duty_students.values():
            for student in group:
                students.append(student)
        return students


    def setup_duty_students(self) -> None:
        screen = self.screen() or QApplication.primaryScreen()
        geometry = screen.availableGeometry()
        margins = self.verticalLayout_2.contentsMargins()

        # 标题、时间以及三个最小高度 40px 的间隔器都会占用高度，
        # 再为布局边距和间距预留 80px，避免表格把窗口撑出屏幕。
        reserved_height = (
            self.label.sizeHint().height()
            + self.dt.sizeHint().height()
            + 3 * 40
            + margins.top()
            + margins.bottom()
            + 80
        )
        self.students.setText(
            build_students_table(
                self.duty_students,
                max_width=max(
                    1,
                    geometry.width() - margins.left() - margins.right() - 16,
                ),
                max_height=max(1, geometry.height() - reserved_height),
            )
        )

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