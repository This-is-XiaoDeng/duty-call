"""值日表 HTML 生成与自适应缩放。"""

from __future__ import annotations

from html import escape

from PySide6.QtGui import QTextDocument

from .types import DutyStudents

MAX_FONT_SIZE = 30
MIN_FONT_SIZE = 6

_TABLE_STYLE = (
    "text-align: center; width:100%; background:#fff; "
    "border-collapse:separate; border-spacing:0; border-radius:18px; "
    "overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.03);"
)


def _render_table(
    duty_students: DutyStudents,
    font_size: int,
    padding_vertical: int,
    padding_horizontal: int,
) -> str:
    cell_style = (
        f"padding:{padding_vertical}px {padding_horizontal}px; "
        "border-bottom:1px solid #eef2f6"
    )
    rows = []
    for work, students in duty_students.items():
        cells = [f'<td style="{cell_style}">{escape(work)}</td>']
        cells.extend(
            f'<td style="{cell_style}">{escape(student)}</td>' for student in students
        )
        rows.append("<tr>" + "".join(cells) + "</tr>")
    return (
        f'<table style="{_TABLE_STYLE} font-size:{font_size}px">'
        + "".join(rows)
        + "</table>"
    )


def build_students_table(
    duty_students: DutyStudents,
    max_width: int,
    max_height: int,
) -> str:
    """生成能放进给定区域的表格 HTML。

    字号从 30px 开始逐级缩小，内边距随字号等比例收缩；同时约束
    ``idealWidth``，避免列数很多时表格把窗口横向撑出屏幕。
    若最小字号仍放不下，则返回最小字号的结果，由布局自行裁剪。
    """

    table = ""
    for font_size in range(MAX_FONT_SIZE, MIN_FONT_SIZE - 1, -1):
        padding_vertical = max(4, round(font_size * 14 / MAX_FONT_SIZE))
        padding_horizontal = max(6, round(font_size * 18 / MAX_FONT_SIZE))
        table = _render_table(
            duty_students, font_size, padding_vertical, padding_horizontal
        )

        document = QTextDocument()
        document.setDocumentMargin(0)
        document.setHtml(table)
        if document.idealWidth() > max_width:
            continue
        document.setTextWidth(max_width)
        if document.size().height() <= max_height:
            break
    return table
