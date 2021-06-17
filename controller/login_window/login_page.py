from model.user.user import User
from model.authorization import Authorization, AuthorizationError
from config import TOKEN_FILE


class LoginPage:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.ui.log_error_frame.setVisible(False)
        self.main_window.ui.log_create_acc_but.clicked.connect(
            lambda: self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.registration_page)
        )
        self.main_window.ui.log_sign_butt.clicked.connect(self.login)

    def login(self):
        self.main_window.ui.log_error_frame.setVisible(False)
        user = User(
            email=self.main_window.ui.log_email_input.text().lower(),
            password=self.main_window.ui.log_pass_input.text()
        )
        try:
            response_data = Authorization.post(user)
            if self.main_window.ui.log_keep_signed_btn.isChecked():
                TOKEN_FILE.write_text(response_data["access_token"])
            self.main_window.ui.log_pass_input.setText("")
            self.main_window.get_user()
        except AuthorizationError:
            self.main_window.ui.log_error_frame.setVisible(True)
