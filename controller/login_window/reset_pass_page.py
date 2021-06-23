from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEvent
from controller.validator import validation
from model.user.user_reset_pass import UserResetPass


class ResetPassPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.email = None
        self.one_time_pass = None
        self.validation = validation.Validation()
        self.email_fields = {
            "email": {
                "fields": (self.main_window.ui.reset_pass_email_input, self.main_window.ui.reset_pass_emai_error),
                "validator": validation.EmailValidation
            }
        }
        self.pass_fields = {
            "password": {
                "fields": (self.main_window.ui.reset_pass_new_pass_input_1,
                           self.main_window.ui.reset_pass_new_pass_error_1),
                "validator": validation.PasswordValidation
            },
            "password2": {
                "fields": (self.main_window.ui.reset_pass_new_pass_input_2,
                           self.main_window.ui.reset_pass_new_pass_error_2,
                           self.main_window.ui.reset_pass_new_pass_input_1),
                "validator": validation.Password2Validation
            }
        }
        self.main_window.ui.reset_pass_email_back_btn.clicked.connect(
            lambda: self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.login_page)
        )
        self.main_window.ui.reset_pass_email_send_btn.clicked.connect(self.send_email)
        self.main_window.ui.reset_pass_pass_next_btn.clicked.connect(self.check_one_time_pass)
        self.main_window.ui.reset_pass_new_pass_save_btn.clicked.connect(self.change_password)
        self.main_window.ui.reset_pass_email_page.installEventFilter(self)
        self.main_window.ui.reset_pass_pass_page.installEventFilter(self)
        self.main_window.ui.reset_pass_new_pass_page.installEventFilter(self)
        self.set_field_validation()

    def set_field_validation(self):
        for field in self.email_fields.values():
            field["fields"][0].setValidator(field["validator"](*field["fields"]))
        for field in self.pass_fields.values():
            field["fields"][0].setValidator(field["validator"](*field["fields"]))

    def send_email(self):
        if self.validation.check_validation(self.email_fields):
            self.email = self.main_window.ui.reset_pass_email_input.text().lower()
            reset_pass_api = UserResetPass(self.email)
            response_code, response_data = reset_pass_api.get()
            if response_code > 399:
                self.main_window.modal_window.show_notification_page(description=response_data, is_error=True)
            else:
                self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.reset_pass_pass_page)

    def check_one_time_pass(self):
        self.one_time_pass = self.main_window.ui.reset_pass_pass_input.text()
        reset_pass_api = UserResetPass(self.email, self.one_time_pass)
        response_code, response_data = reset_pass_api.get()
        if response_code > 399:
            self.main_window.ui.reset_pass_error_frame.setVisible(True)
        else:
            self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.reset_pass_new_pass_page)

    def change_password(self):
        if self.validation.check_validation(self.pass_fields):
            data = self.get_password_data()
            reset_pass_api = UserResetPass(**data)
            response_code, response_data = reset_pass_api.put()
            if response_code > 399:
                self.main_window.modal_window.show_notification_page(description=response_data, is_error=True)
            else:
                self.main_window.modal_window.show_notification_page(title="Password updated",
                                                                     description="Password was updated successfully",
                                                                     is_error=False)
                self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.login_page)

    def get_password_data(self):
        return {
            "email": self.email,
            "one_time_password": self.one_time_pass,
            "password": self.main_window.ui.reset_pass_new_pass_input_1.text()
        }

    def eventFilter(self, obj, event) -> bool:
        if obj is self.main_window.ui.reset_pass_email_page:
            if event.type() == QEvent.Show and self.main_window.change_page_data:
                self.validation.reset_error_fields(self.email_fields)
                self.main_window.ui.reset_pass_email_input.setText("")
                return True
        if obj is self.main_window.ui.reset_pass_pass_page:
            if event.type() == QEvent.Show and self.main_window.change_page_data:
                self.main_window.ui.reset_pass_error_frame.setVisible(False)
                return True
        if obj is self.main_window.ui.reset_pass_new_pass_page:
            if event.type() == QEvent.Show and self.main_window.change_page_data:
                self.validation.reset_error_fields(self.pass_fields)
                self.main_window.ui.reset_pass_new_pass_input_1.setText("")
                self.main_window.ui.reset_pass_new_pass_input_2.setText("")
                return True
        return False
