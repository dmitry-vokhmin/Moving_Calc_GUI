# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'calendar.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class CalendarWidget(QtWidgets.QCalendarWidget):
    def __init__(self, parent=None):
        super(CalendarWidget, self).__init__(parent)
        date = QtCore.QDate().currentDate()
        self.dates = date

    @QtCore.pyqtSlot(QtCore.QDate)
    def on_clicked(self, date):
        self._selected_dates.add(date)

    def paintCell(self, painter, rect, date):
        super(CalendarWidget, self).paintCell(painter, rect, date)
        if date == self.dates:
            painter.save()
            painter.setBrush(QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.SolidPattern))
            painter.drawEllipse(rect.topLeft() + QtCore.QPoint(35, 40), 5, 5)
            painter.restore()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(452, 413)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet(".QFrame{\n"
"border: 0.5px solid rgba(181, 184, 199, 0.5);\n"
"background: #F9FAFB;\n"
"border-radius: 10px;\n"
"}\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.calendarWidget = CalendarWidget(self.frame)
        self.calendarWidget.setStyleSheet("/* navigation bar */\n"
"\n"
"QCalendarWidget QMenu{\n"
"    background-color: #F9FAFB;\n"
"}\n"
"#qt_calendar_calendarview {\n"
"    background-color: #F9FAFB;\n"
"    font: 16px;\n"
"}\n"
"#qt_calendar_monthbutton {\n"
"    background-color: #F9FAFB;\n"
"}\n"
"#qt_calendar_yearbutton {\n"
"    background-color: #F9FAFB;\n"
"}\n"
"#qt_calendar_yearedit {\n"
"    background-color: #F9FAFB;\n"
"}\n"
"#qt_calendar_navigationbar {\n"
"    background-color: #F9FAFB;\n"
"}\n"
"\n"
"QCalendarWidget QWidget#qt_calendar_navigationbar { background-color: #F9FAFB;}\n"
"QCalendarWidget QToolButton {\n"
"    color: black;\n"
"    font-size: 16px;\n"
"    icon-size: 24px, 24px;\n"
"}\n"
"\n"
"QCalendarWidget QToolButton:hover  {\n"
"    border: none\n"
"}\n"
"\n"
"QCalendarWidget QToolButton:pressed {\n"
"    border: none\n"
"}\n"
"\n"
"QCalendarWidget QToolButton#qt_calendar_prevmonth  {\n"
"    qproperty-icon: url(:/image/left_arrow_default.svg);\n"
"}\n"
"\n"
"QCalendarWidget QToolButton#qt_calendar_nextmonth {\n"
"    qproperty-icon: url(:/image/right_arrow_default.svg);\n"
"}\n"
"\n"
"QCalendarWidget QToolButton::menu-indicator#qt_calendar_monthbutton{\n"
"    background-color: transparent;\n"
"}\n"
"\n"
"/* header row */\n"
"QCalendarWidget QWidget { \n"
"    alternate-background-color: #F9FAFB;\n"
"}\n"
" \n"
"/* normal days */\n"
"QCalendarWidget QAbstractItemView:enabled \n"
"{\n"
"    outline: 0;\n"
"    color: #070808;\n"
"    selection-background-color: #0915CC;\n"
"    selection-color: #FFFFFF;\n"
"}\n"
" \n"
"/* days in other months */\n"
"QCalendarWidget QAbstractItemView:disabled { color: #757C9F;}")
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setSelectionMode(QtWidgets.QCalendarWidget.SingleSelection)
        self.calendarWidget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.ShortDayNames)
        self.calendarWidget.setVerticalHeaderFormat(QtWidgets.QCalendarWidget.NoVerticalHeader)
        self.calendarWidget.setNavigationBarVisible(True)
        self.calendarWidget.setDateEditEnabled(False)
        self.calendarWidget.setStyleSheet("/* navigation bar */\n"
                                          "\n"
                                          "#qt_calendar_calendarview {\n"
                                          "    background-color: #F9FAFB;\n"
                                          "    font: 16px;\n"
                                          "}\n"
                                          "\n"
                                          "#qt_calendar_yearedit {\n"
                                          "    background-color: #F9FAFB;\n"
                                          "}\n"
                                          "\n"
                                          "QCalendarWidget QToolButton::menu-indicator#qt_calendar_monthbutton{\n"
                                          "    background-color: transparent;\n"
                                          "}\n"
                                          "\n"
                                          "QCalendarWidget QWidget#qt_calendar_navigationbar { background-color: #F9FAFB;}\n"
                                          "QCalendarWidget QToolButton {\n"
                                          "    background-color: #F9FAFB;\n"
                                          "    color: black;\n"
                                          "    font-size: 16px;\n"
                                          "    icon-size: 24px, 24px;\n"
                                          "}\n"
                                          "\n"
                                          "QCalendarWidget QToolButton:hover  {\n"
                                          "    border: none\n"
                                          "}\n"
                                          "\n"
                                          "QCalendarWidget QToolButton:pressed {\n"
                                          "    border: none\n"
                                          "}\n"
                                          "\n"
                                          "QCalendarWidget QToolButton#qt_calendar_prevmonth  {\n"
                                          "    qproperty-icon: url(:/image/left_arrow_default.svg);\n"
                                          "}\n"
                                          "\n"
                                          "QCalendarWidget QToolButton#qt_calendar_nextmonth {\n"
                                          "    qproperty-icon: url(:/image/right_arrow_default.svg);\n"
                                          "}\n"
                                          "\n"
                                          "\n"
                                          "\n"
                                          "/* header row */\n"
                                          "QCalendarWidget QWidget { \n"
                                          "    alternate-background-color: #F9FAFB;\n"
                                          "}\n"
                                          "\n"
                                          "QCalendarWidget QMenu {\n"
                                          "    font-size: 16px;\n"
                                          "    background: #F9FAFB;\n"
                                          "    padding-left: 15px;\n"
                                          "    border: 0.5px solid rgba(181, 184, 199, 0.5);\n"
                                          "    border-radius: 8px;\n"
                                          "    color: #070808;\n"
                                          "    selection-background-color: #F2F3F6;\n"
                                          "    selection-color: #0915CC;\n"
                                          "}\n"
                                          " \n"
                                          "/* normal days */\n"
                                          "QCalendarWidget QAbstractItemView:enabled \n"
                                          "{\n"
                                          "    outline: 0;\n"
                                          "    color: #070808;\n"
                                          "    selection-background-color: #0915CC;\n"
                                          "    selection-color: #FFFFFF;\n"
                                          "}\n"
                                          " \n"
                                          "/* days in other months */\n"
                                          "QCalendarWidget QAbstractItemView:disabled { color: #757C9F;}")
        self.calendarWidget.setObjectName("calendarWidget")
        self.verticalLayout.addWidget(self.calendarWidget)
        self.verticalLayout_2.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 452, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
import resources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())