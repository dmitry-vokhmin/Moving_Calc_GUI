from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QWidget
from model.user.registration import Registration
from controller.validator import validation


class RegistrationPage(QWidget):
    def __init__(self, main_window):
        QWidget.__init__(self, main_window)
        self.main_window = main_window
        self.validation = validation.Validation()
        self.fields = {
            "name": {
                "fields": (self.main_window.ui.reg_name_input, self.main_window.ui.reg_error_name),
                "validator": validation.EmptyStrValidation
            },
            "email": {
                "fields": (self.main_window.ui.reg_email_input, self.main_window.ui.reg_error_email),
                "validator": validation.EmailValidation
            },
            "password": {
                "fields": (self.main_window.ui.reg_pass_input, self.main_window.ui.reg_error_pass),
                "validator": validation.PasswordValidation
            },
            "password2": {
                "fields": (self.main_window.ui.reg_pass2_input,
                           self.main_window.ui.reg_error_pass2,
                           self.main_window.ui.reg_pass_input),
                "validator": validation.Password2Validation
            },
        }
        self.main_window.ui.reg_sign_but.clicked.connect(
            lambda: self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.login_page)
        )
        self.main_window.ui.reg_create_acc_butt.clicked.connect(self.registration)
        self.main_window.ui.registration_page.installEventFilter(self)
        self.set_field_validation()

    def set_field_validation(self):
        for field in self.fields.values():
            field["fields"][0].setValidator(field["validator"](*field["fields"]))

    def registration(self):
        if self.validation.check_validation(self.fields):
            user_data = self.get_user_data()
            registration = Registration(**user_data)
            response_code, response_data = registration.post()
            if response_code > 399:
                self.main_window.registration_error(
                    f"Looks like an account with the email {user_data['email']} already exists."
                )
                self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.acc_created_error_page)
            else:
                self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.acc_created_page)

    def get_user_data(self):
        return {
            "fullname": self.fields["name"]["fields"][0].text().title().strip(),
            "email": self.fields["email"]["fields"][0].text().lower(),
            "password": self.fields["password"]["fields"][0].text(),
            "company_id": self.main_window.reg_comp_page.company_id
        }

    def eventFilter(self, obj, event) -> bool:
        if obj is self.main_window.ui.registration_page:
            if event.type() == QEvent.Show and self.main_window.change_page_data:
                self.validation.reset_error_fields(self.fields)
                return True
        return False
