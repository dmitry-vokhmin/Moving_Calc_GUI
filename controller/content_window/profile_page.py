from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QIcon
from model.user.user import User
from controller.validator.validation import Validation
from controller.validator import validation


class ProfilePage(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        QWidget.__init__(self, main_window, *args, **kwargs)
        self.main_window = main_window
        self.staff_profile = None
        self.validator = Validation()
        self.fields = {
            "name": {
                "fields": (self.main_window.ui.profile_name_input, self.main_window.ui.profile_error_name),
                "validator": validation.EmptyStrValidation
            },
            "email": {
                "fields": (self.main_window.ui.profile_new_email_input, self.main_window.ui.profile_error_email),
                "validator": validation.EmailValidation
            },
            "old_password": {
                "fields": (self.main_window.ui.profile_pass_input, self.main_window.ui.profile_error_old_pass),
                "validator": validation.EmptyStrValidation
            },
            "password": {
                "fields": (self.main_window.ui.profile_new_pass_input, self.main_window.ui.profile_error_pass),
                "validator": validation.PasswordValidation
            },
            "password2": {
                "fields": (self.main_window.ui.profile_new_pass2_input,
                           self.main_window.ui.profile_error_pass2,
                           self.main_window.ui.profile_new_pass_input),
                "validator": validation.Password2Validation
            }
        }
        self.main_window.ui.profile_change_pass_butt.clicked.connect(lambda: self.change_password(True))
        self.main_window.ui.profile_pass_cancel_butt.clicked.connect(lambda: self.change_password(False))
        self.main_window.ui.profile_change_email_butt.clicked.connect(lambda: self.change_email(True))
        self.main_window.ui.profile_email_cancel_butt.clicked.connect(lambda: self.change_email(False))
        self.main_window.ui.profile_log_out_butt.clicked.connect(
            lambda: self.main_window.modal_window.show_confirm_dialog("Log Out", self.main_window.log_out)
        )
        self.main_window.ui.profile_delete_butt.clicked.connect(
            lambda: self.main_window.modal_window.show_confirm_dialog(f"Delete {self.staff_profile['fullname']}",
                                                                      self.delete_user)
        )
        self.main_window.ui.profile_user_manage_butt.clicked.connect(
            lambda: self.main_window.ui.content_pages.setCurrentWidget(self.main_window.ui.user_management_page)
        )
        self.main_window.ui.profile_save_butt.clicked.connect(
            lambda: self.main_window.modal_window.show_confirm_dialog("Save Changes", self.save_changes)
        )
        self.main_window.ui.profile_log_out_butt.installEventFilter(self)
        self.main_window.ui.profile_delete_butt.installEventFilter(self)
        self.main_window.ui.profile_page.installEventFilter(self)
        self.set_field_validation()

    def set_field_validation(self):
        for field in self.fields.values():
            field["fields"][0].setValidator(field["validator"](*field["fields"]))

    def assign_staff_profile(self, profile):
        if profile["id"] != self.main_window.user.id:
            self.staff_profile = profile

    def set_user_profile(self):
        if self.staff_profile:
            self.main_window.user_profile_ui.set_profile(self.staff_profile)
        else:
            self.main_window.user_profile_ui.set_profile()

    def validate_page(self):
        new_fields = {
            "name": {"fields": self.fields["name"]["fields"]}
        }
        if not self.main_window.ui.profile_new_pass_frame.isHidden():
            new_fields["old_password"] = {"fields": self.fields["old_password"]["fields"]}
            new_fields["password"] = {"fields": self.fields["password"]["fields"]}
            new_fields["password2"] = {"fields": self.fields["password2"]["fields"]}
        if not self.main_window.ui.profile_new_email_frame.isHidden():
            new_fields["email"] = {"fields": self.fields["email"]["fields"]}
        return self.validator.check_validation(new_fields)

    def get_data_from_page(self):
        if self.staff_profile:
            user_id = self.staff_profile["id"]
        else:
            user_id = self.main_window.user.id
        data = {
            "id": user_id,
            "fullname": self.fields["name"]["fields"][0].text(),
            "user_role_id": self.main_window.ui.role_combobox.currentData()
        }
        if not self.main_window.ui.profile_new_pass_frame.isHidden():
            data["old_password"] = self.fields["old_password"]["fields"][0].text()
            data["password"] = self.fields["password"]["fields"][0].text()
        if not self.main_window.ui.profile_new_email_frame.isHidden():
            data["email"] = self.fields["email"]["fields"][0].text().lower()
        return data

    def save_changes(self):
        if self.validate_page():
            data = self.get_data_from_page()
            user_update = User(**data)
            response_code, response_data = user_update.put()
            if response_code > 399:
                self.main_window.modal_window.show_notification_page(description=response_data, is_error=True)
            else:
                if self.staff_profile:
                    self.staff_profile = response_data
                else:
                    self.main_window.user.set_attr(response_data)
                self.set_user_profile()
                self.validator.reset_error_fields(self.fields)
                self.main_window.ui.profile_butt.setText(f" {self.main_window.user.fullname}")

    def change_password(self, is_change_password):
        self.main_window.ui.profile_new_pass_frame.setVisible(is_change_password)
        self.main_window.ui.profile_change_pass_butt.setVisible(not is_change_password)

    def change_email(self, is_change_email):
        self.main_window.ui.profile_new_email_frame.setVisible(is_change_email)
        self.main_window.ui.profile_change_email_butt.setVisible(not is_change_email)

    def delete_user(self):
        user_del = User(**self.staff_profile)
        response_code, response_data = user_del.delete()
        if response_code > 399:
            self.main_window.modal_window.show_notification_page(is_error=True)
        else:
            self.main_window.ui.content_pages.setCurrentWidget(self.main_window.ui.user_management_page)

    def eventFilter(self, obj, event) -> bool:
        if obj is self.main_window.ui.profile_log_out_butt:
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/exit_app_hover.svg"))
                return True
            if event.type() == QEvent.HoverLeave:
                obj.setIcon(QIcon(":/image/exit_app_default.svg"))
                return True
        elif obj is self.main_window.ui.profile_delete_butt:
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/delete_acc_icon_hover_red.svg"))
                return True
            if event.type() == QEvent.HoverLeave:
                obj.setIcon(QIcon(":/image/delete_acc_icon_default.svg"))
                return True
        elif obj is self.main_window.ui.profile_page:
            if event.type() == QEvent.Show:
                self.validator.reset_error_fields(self.fields)
                self.set_user_profile()
                return True
            if event.type() == QEvent.Hide:
                self.staff_profile = None
                return True
        return False
