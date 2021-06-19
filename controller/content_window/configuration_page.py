from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QIcon
from model.calendar import Calendar
from model.price import Price


class ConfigurationPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.set_page = True
        self.price_page = True
        self.calendar = None
        self.main_window.ui.config_date_butt.clicked.connect(
            lambda: self.change_inside_page(True, self.main_window.ui.date_page)
        )
        self.main_window.ui.config_price_butt.clicked.connect(
            lambda: self.change_inside_page(False, self.main_window.ui.price_page)
        )
        self.buttons = []
        self.main_window.ui.config_date_update_butt.clicked.connect(self.update_date)
        self.main_window.ui.config_price_update_butt.clicked.connect(self.update_prices)
        self.main_window.ui.config_edit_price_butt.clicked.connect(self.enable_input_fields)
        self.main_window.ui.config_page.installEventFilter(self)
        self.main_window.ui.price_page.installEventFilter(self)

    def enable_input_fields(self):
        for field in self.main_window.ui.config_clear_frame.findChildren(QLineEdit):
            field.setEnabled(True)

    def update_prices(self):
        input_fields = self.main_window.ui.config_clear_frame.findChildren(QLineEdit)
        if input_fields[0].isEnabled():
            data = []
            for field in input_fields:
                price_tag_id = self.get_price_tag_id()
                data.append(self.get_price_data(field, price_tag_id))
            price = Price(*data)
            response_code, response_data = price.put()
            if response_code > 399:
                self.main_window.modal_window.show_notification_page(description=response_data, is_error=True)
            else:
                self.main_window.price_settings_ui.set_movers_prices(price_tag_id)
                self.main_window.modal_window.show_notification_page(
                    title="Mover prices were updated",
                    description="Mover prices were updated successfully",
                    is_error=False
                )

    def update_date(self):
        data = self.get_date_data()
        calendar = Calendar(**data)
        response_code, response_data = calendar.put()
        if response_code > 399:
            self.main_window.modal_window.show_notification_page(description=response_data, is_error=True)
        else:
            self.main_window.set_calendar(self.calendar)
            self.main_window.modal_window.show_notification_page(title="Calendar was updated",
                                                                 description="Calendar was updated successfully",
                                                                 is_error=False)

    @staticmethod
    def get_price_data(field, price_tag_id):
        return {
            "price": field.text(),
            "mover_amount_id": field.__getattribute__("mover_amount_id"),
            "price_tag_id": price_tag_id
        }

    def get_date_data(self):
        return {
            "start_date": self.main_window.ui.config_start_date_edit.date().toPyDate().isoformat(),
            "end_date": self.main_window.ui.config_end_date_edit.date().toPyDate().isoformat(),
            "price_tag_id": self.get_price_tag_id()
        }

    def get_price_tag_id(self):
        for button in self.buttons:
            if button.isChecked():
                return button.__getattribute__("id")

    def set_movers_price(self):
        self.main_window.price_settings_ui.set_movers_prices()

    def change_inside_page(self, is_date_setting, page):
        if is_date_setting:
            self.main_window.set_calendar(self.calendar)
        self.main_window.calendar_page_ui.change_page_selector_style(is_date_setting)
        self.main_window.ui.config_pages.setCurrentWidget(page)

    def set_event_filter(self):
        self.buttons = self.main_window.ui.config_price_type_butt_frame.findChildren(QPushButton)
        for button in self.buttons:
            button.installEventFilter(self)
            button.clicked.connect(self.change_button_background_mover_table(button))

    def set_price_tags_and_calendar(self):
        self.main_window.calendar_page_ui.set_price_tag(self.main_window.ui.config_price_type_butt_frame)
        self.calendar = self.main_window.calendar_page_ui.build_calendars()
        self.set_event_filter()

    def change_button_background_mover_table(self, checked_button):
        def wrap():
            for button in self.buttons:
                if checked_button != button:
                    button.setChecked(False)
                    button.setIcon(QIcon(":/image/check_icon_default.svg"))
                elif checked_button == button:
                    checked_button.setChecked(True)
            if self.price_page:
                self.main_window.price_settings_ui.set_movers_prices(checked_button.__getattribute__("id"))

        return wrap

    def eventFilter(self, obj, event) -> bool:
        if obj is self.main_window.ui.config_page:
            if event.type() == QEvent.Show:
                if self.set_page:
                    self.set_price_tags_and_calendar()
                    self.set_page = False
                self.change_inside_page(True, self.main_window.ui.date_page)
                return True
        if obj is self.main_window.ui.price_page:
            if event.type() == QEvent.Show:
                self.main_window.price_settings_ui.set_movers_prices(self.get_price_tag_id())
                self.price_page = True
                return True
            if event.type() == QEvent.Hide:
                self.price_page = False
        if obj in self.buttons:
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/check_icon_hover.svg"))
                return True
            if event.type() == QEvent.HoverLeave and not obj.isChecked():
                obj.setIcon(QIcon(":/image/check_icon_default.svg"))
                return True
        return False
