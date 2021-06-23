from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtWidgets import QHBoxLayout, QPushButton
from model.price_tag import PriceTag


class CalendarPage:
    def __init__(self, main_window):
        self.main_window = main_window
        self.price_tag = PriceTag()

    def set_price_tag(self, frame):
        self.main_window.save_data(self.price_tag)
        self.main_window.delete_layout(frame.layout())
        config_price_type_button_layout = QHBoxLayout(frame)
        config_price_type_button_layout.setContentsMargins(20, 10, 0, 30)
        config_price_type_button_layout.setSpacing(5)
        for idx, price_tag in enumerate(self.price_tag.price_tags):
            config_butt = QPushButton(frame)
            config_butt.setCursor(QCursor(Qt.PointingHandCursor))
            config_butt.setCheckable(True)
            if idx == 0:
                config_butt.setChecked(True)
                config_butt.setStyleSheet("qproperty-icon: url(:/image/check_icon_hover.svg);")
            config_butt.setText(price_tag["name"].title())
            setattr(config_butt, "id", price_tag["id"])
            config_price_type_button_layout.addWidget(config_butt)

    def build_calendars(self):
        calendar = self.main_window.calendar_ui.build_calendar("#F9FAFB", "#070808", "16px", QColor(Qt.black), False)
        self.main_window.ui.config_calendar_layout2.addWidget(calendar)
        start_calendar = self.main_window.calendar_ui.build_calendar("#0915CC", "#FFFFFF", "14px", QColor(Qt.blue), True)
        end_calendar = self.main_window.calendar_ui.build_calendar("#0915CC", "#FFFFFF", "14px", QColor(Qt.blue), True)
        self.main_window.ui.config_start_date_edit.setCalendarWidget(start_calendar)
        self.main_window.ui.config_start_date_edit.setDate(QDate.currentDate())
        self.main_window.ui.config_end_date_edit.setCalendarWidget(end_calendar)
        self.main_window.ui.config_end_date_edit.setDate(QDate.currentDate())
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
