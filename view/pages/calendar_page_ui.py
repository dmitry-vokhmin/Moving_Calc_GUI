import datetime as dt
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QTextCharFormat, QColor, QCursor
from PyQt5.QtWidgets import QCalendarWidget, QWidget, QToolButton, QHBoxLayout, QPushButton
from view.custom_widgets.calendar import CalendarWidget
from model.price_tag.price_tag import PriceTag


class CalendarPage:
    def __init__(self, main_window):
        self.main_window = main_window
        self.calendar = CalendarWidget()
        self.price_tag = PriceTag()

    def set_calendar_dates(self):
        self.calendar.regular.clear()
        self.calendar.discount.clear()
        self.calendar.subpeak.clear()
        self.calendar.peak.clear()
        for date in self.main_window.calendar.dates:
            self.add_dates(date)

    def set_price_tag(self, frame):
        self.main_window.delete_layout(frame.layout())
        config_price_type_button_layout = QHBoxLayout(frame)
        config_price_type_button_layout.setContentsMargins(20, 10, 0, 30)
        config_price_type_button_layout.setSpacing(5)
        for idx, price_tag in enumerate(self.main_window.price_tag.price_tags):
            config_butt = QPushButton(frame)
            config_butt.setCursor(QCursor(Qt.PointingHandCursor))
            config_butt.setCheckable(True)
            if idx == 0:
                config_butt.setChecked(True)
                config_butt.setStyleSheet("qproperty-icon: url(:/image/check_icon_hover.svg);")
            config_butt.setText(price_tag["name"].title())
            config_butt.__setattr__("id", price_tag["id"])
            config_price_type_button_layout.addWidget(config_butt)

    def set_calendars(self):
        self.build_calendar("#F9FAFB", "#070808", "16px", QColor(Qt.black), False)
        start_calendar = self.build_calendar("#0915CC", "#FFFFFF", "14px", QColor(Qt.blue), True)
        end_calendar = self.build_calendar("#0915CC", "#FFFFFF", "14px", QColor(Qt.blue), True)
        self.main_window.ui.config_start_date_edit.setCalendarWidget(start_calendar)
        self.main_window.ui.config_start_date_edit.setDate(QDate.currentDate())
        self.main_window.ui.config_end_date_edit.setCalendarWidget(end_calendar)
        self.main_window.ui.config_end_date_edit.setDate(QDate.currentDate())

    def add_dates(self, date):
        start_date = dt.datetime.strptime(date["start_date"], "%Y-%m-%d")
        end_date = dt.datetime.strptime(date["end_date"], "%Y-%m-%d")
        delta = end_date - start_date
        if date["price_tag"]["name"] == "regular":
            self.calendar.regular.update(self.update_calendar(start_date, delta))
        elif date["price_tag"]["name"] == "discount":
            self.calendar.discount.update(self.update_calendar(start_date, delta))
        elif date["price_tag"]["name"] == "subpeak":
            self.calendar.subpeak.update(self.update_calendar(start_date, delta))
        elif date["price_tag"]["name"] == "peak":
            self.calendar.peak.update(self.update_calendar(start_date, delta))

    @staticmethod
    def update_calendar(start_date, delta):
        return {QDate.fromString((start_date + dt.timedelta(days=i)).strftime("%Y-%m-%d"), "yyyy-MM-dd")
                for i in range(delta.days + 1)}

    def build_calendar(self, background_color, color, font_size, foreground, is_pop_up):
        if is_pop_up:
            calendar = CalendarWidget()
            calendar.findChildren(QWidget)[0].setCursor(Qt.PointingHandCursor)
        else:
            calendar = self.calendar
            calendar.setSelectionMode(QCalendarWidget.NoSelection)
            self.main_window.ui.config_calendar_layout2.addWidget(calendar)
        calendar.setStyleSheet(self.set_stylesheet_calendar(background_color, color, font_size))
        calendar.setHorizontalHeaderFormat(QCalendarWidget.SingleLetterDayNames)
        calendar.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        calendar.setDateEditEnabled(False)
        for button in calendar.findChildren(QToolButton):
            button.setCursor(Qt.PointingHandCursor)
        day_format = QTextCharFormat()
        day_format.setForeground(foreground)
        calendar.setWeekdayTextFormat(Qt.Saturday, day_format)
        calendar.setWeekdayTextFormat(Qt.Sunday, day_format)
        return calendar

    def change_page_selector_style(self, is_date_setting):
        self.main_window.ui.config_date_butt.setProperty("selected", is_date_setting)
        self.main_window.ui.config_date_butt.setStyle(self.main_window.ui.config_date_butt.style())
        self.main_window.ui.config_price_butt.setProperty("selected", not is_date_setting)
        self.main_window.ui.config_price_butt.setStyle(self.main_window.ui.config_price_butt.style())
        self.main_window.ui.config_date_update_butt.setVisible(is_date_setting)
        self.main_window.ui.config_price_update_butt.setVisible(not is_date_setting)
        self.main_window.ui.config_price_line.setVisible(not is_date_setting)
        self.main_window.ui.config_date_line.setVisible(is_date_setting)
        self.main_window.ui.config_edit_price_butt.setVisible(not is_date_setting)
        if is_date_setting:
            self.main_window.ui.config_alert_text.setText("Select price type and manage its time period.")
        else:
            self.main_window.ui.config_alert_text.setText(
                "Manage prices for a certain number of movers for each price type."
            )

    @staticmethod
    def set_stylesheet_calendar(background_color, color, font_size):
        stylesheet = "/* navigation bar */ " \
                     "#qt_calendar_calendarview { " \
                     "background-color: #F9FAFB;" \
                     f"font: {font_size};" \
                     "}" \
                     "#qt_calendar_yearedit {" \
                     "background-color: #F9FAFB;}" \
                     "QCalendarWidget QToolButton::menu-indicator#qt_calendar_monthbutton{" \
                     "background-color: transparent;" \
                     "}" \
                     "QCalendarWidget QWidget#qt_calendar_navigationbar { background-color: #F9FAFB;}" \
                     "QCalendarWidget QToolButton {" \
                     "background-color: #F9FAFB;" \
                     "color: black;" \
                     f"font-size: {font_size};" \
                     "icon-size: 24px, 24px;" \
                     "}" \
                     "QCalendarWidget QToolButton:hover  {" \
                     "border: none" \
                     "}" \
                     "QCalendarWidget QToolButton:pressed {" \
                     "border: none" \
                     "}" \
                     "QCalendarWidget QToolButton#qt_calendar_prevmonth  {" \
                     "qproperty-icon: url(:/image/left_arrow_default.svg);" \
                     "}" \
                     "QCalendarWidget QToolButton#qt_calendar_nextmonth {" \
                     "qproperty-icon: url(:/image/right_arrow_default.svg);" \
                     "}" \
                     "/* header row */" \
                     "QCalendarWidget QWidget {" \
                     "alternate-background-color: #F9FAFB;" \
                     "}" \
                     "QCalendarWidget QMenu {" \
                     f"font-size: {font_size};" \
                     "background: #F9FAFB;" \
                     "padding-left: 15px;" \
                     "border: 0.5px solid rgba(181, 184, 199, 0.5);" \
                     "border-radius: 8px;" \
                     "color: #070808;" \
                     "selection-background-color: #F2F3F6;" \
                     "selection-color: #0915CC;" \
                     "}" \
                     "/* normal days */" \
                     "QCalendarWidget QAbstractItemView:enabled " \
                     "{" \
                     "outline: 0;" \
                     "color: #070808;" \
                     f"selection-background-color: {background_color};" \
                     f"selection-color: {color};" \
                     "}" \
                     "/* days in other months */" \
                     "QCalendarWidget QAbstractItemView:disabled { color: #757C9F;}"
        return stylesheet
