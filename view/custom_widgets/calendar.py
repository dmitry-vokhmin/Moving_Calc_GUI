from PyQt5.QtWidgets import QCalendarWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QBrush, QColor


class CalendarWidget(QCalendarWidget):
    def __init__(self, parent=None):
        super(CalendarWidget, self).__init__(parent)
        self.regular = set()
        self.discount = set()
        self.subpeak = set()
        self.peak = set()

    def paintCell(self, painter, rect, date):
        super(CalendarWidget, self).paintCell(painter, rect, date)
        painter.setPen(Qt.NoPen)
        if date in self.peak:
            painter.setBrush(QBrush(QColor(255, 60, 47), Qt.SolidPattern))
            painter.drawEllipse(rect.center() + QPoint(1, 14), 3, 3)
        elif date in self.subpeak:
            painter.setBrush(QBrush(QColor(255, 172, 47), Qt.SolidPattern))
            painter.drawEllipse(rect.center() + QPoint(1, 14), 3, 3)
        elif date in self.discount:
            painter.setBrush(QBrush(QColor(38, 169, 93), Qt.SolidPattern))
            painter.drawEllipse(rect.center() + QPoint(1, 14), 3, 3)
        elif date in self.regular:
            painter.setBrush(QBrush(QColor(78, 80, 255), Qt.SolidPattern))
            painter.drawEllipse(rect.center() + QPoint(1, 14), 3, 3)
