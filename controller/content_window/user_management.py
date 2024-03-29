from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEvent
from model.user.user import User
from model.user.user_company import UserCompany


class UserManagement(QWidget):
    def __init__(self, main_window):
        QWidget.__init__(self, main_window)
        self.main_window = main_window
        self.main_window.ui.user_manage_add_butt.clicked.connect(self.main_window.modal_window.show_add_user_page)
        self.main_window.ui.user_management_page.installEventFilter(self)

    def set_user_table(self):
        user_company_data = self.get_data()
        self.main_window.user_management_table_ui.set_table(self.user_profile,
                                                            self.show_notification_window,
                                                            user_company_data)

    def get_data(self):
        user_company_api = UserCompany()
        response_code, response_data = user_company_api.get()
        if response_code > 399:
            self.main_window.modal_window.show_notification_page(description=response_data, is_error=True)
        else:
            return response_data

    def show_notification_window(self, user):
        def wrap():
            self.main_window.modal_window.show_confirm_dialog(self.delete_user(user),
                                                              f"delete {user['fullname']}?",
                                                              "delete")
        return wrap

    def delete_user(self, user):
        def wrap():
            user_del = User(**user)
            response_code, response_data = user_del.delete()
            if response_code > 399:
                self.main_window.modal_window.show_notification_page(is_error=True)
            else:
                self.set_user_table()
        return wrap

    def user_profile(self, user):
        def wrap():
            self.main_window.profile.assign_staff_profile(user)
            self.main_window.ui.content_pages.setCurrentWidget(self.main_window.ui.profile_page)
        return wrap

    def eventFilter(self, obj, event) -> bool:
        if obj is self.main_window.ui.user_management_page:
            if event.type() == QEvent.Show and self.main_window.change_page_data:
                self.set_user_table()
                return True
        return False
