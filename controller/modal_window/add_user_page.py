from PyQt5.QtWidgets import QDialog, QRadioButton, QLineEdit
from PyQt5.QtCore import QEvent
from model.user.add_new_user import AddNewUser
from controller.validator import validation


class AddUserPage(QDialog):
    def __init__(self, main_modal_window):
        QDialog.__init__(self, main_modal_window)
        self.main_modal_window = main_modal_window
        self.validation = validation.Validation()
        self.radio_buttons = {}
        self.role_update = True
        self.fields = {
            "name": {
                "fields": (self.main_modal_window.ui.name_input, self.main_modal_window.ui.error_name),
                "validator": validation.EmptyStrValidation
            },
            "email": {
                "fields": (self.main_modal_window.ui.email_input, self.main_modal_window.ui.error_email),
                "validator": validation.EmailValidation
            },
            "password": {
                "fields": (self.main_modal_window.ui.pass_input, self.main_modal_window.ui.error_pass),
                "validator": validation.PasswordValidation
            },
            "password2": {
                "fields": (self.main_modal_window.ui.pass2_input,
                           self.main_modal_window.ui.error_pass2,
                           self.main_modal_window.ui.pass_input),
                "validator": validation.Password2Validation
            }
        }
        self.main_modal_window.ui.add_user_cancel_butt.clicked.connect(self.main_modal_window.reject)
        self.main_modal_window.ui.add_user_butt.clicked.connect(self.add_user)
        self.main_modal_window.ui.add_user_page.installEventFilter(self)
        self.set_field_validation()

    def set_field_validation(self):
        for field in self.fields.values():
            field["fields"][0].setValidator(field["validator"](*field["fields"]))

    def set_radio_buttons(self):
        for role in self.main_modal_window.main_window.user_role.children_roles:
            radio_button = QRadioButton(self.main_modal_window.ui.add_user_radio_butt_frame)
            if role["role"] == "sales":
                radio_button.setChecked(True)
            radio_button.setText(role["role"].capitalize())
            radio_button.__setattr__("role_id", role["id"])
            self.radio_buttons[role["role"]] = radio_button
            self.main_modal_window.ui.add_user_radio_butt_layout.addWidget(radio_button)

    def add_user(self):
        if self.validation.check_validation(self.fields):
            radio_button_id = self.get_selected_radio_button_id()
            data = self.get_data(radio_button_id)
            new_user = AddNewUser(**data)
            response_code, response_data = new_user.post()
            if response_code > 399:
                self.main_modal_window.show_notification_page(
                    is_error=True,
                    previous_page=lambda: self.main_modal_window.ui.pages.setCurrentWidget(
                        self.main_modal_window.ui.add_user_page)
                )
            else:
                self.main_modal_window.main_window.ui.user_management_page.setVisible(False)
                self.main_modal_window.main_window.ui.user_management_page.setVisible(True)
                self.main_modal_window.show_notification_page(
                    title="New user added",
                    description="New user account was added successfully, "
                                "a new user will receive an email with the login instructions shortly.",
                    is_error=False)
                self.clear_page()

    def clear_page(self):
        for input_field in self.main_modal_window.ui.main_frame.findChildren(QLineEdit):
            input_field.setText("")

    def get_data(self, radio_button_id):
        return {
            "fullname": self.fields["name"]["fields"][0].text().title().strip(),
            "email": self.fields["email"]["fields"][0].text().lower(),
            "password": self.fields["password"]["fields"][0].text(),
            "company_id": self.main_modal_window.main_window.user.company_id,
            "user_role_id": radio_button_id
        }

    def get_selected_radio_button_id(self):
        for button in self.radio_buttons.values():
            if button.isChecked():
                return button.__getattribute__("role_id")

    def eventFilter(self, obj, event: QEvent) -> bool:
        if obj is self.main_modal_window.ui.add_user_page:
            if event.type() == QEvent.Show:
                self.validation.reset_error_fields(self.fields)
                if self.role_update:
                    self.set_radio_buttons()
                    self.role_update = False
                return True
        return False
