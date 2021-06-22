class AccCreatedPage:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.ui.acc_created_butt.clicked.connect(
            lambda: self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.login_page)
        )
        self.main_window.ui.acc_create_error_butt.clicked.connect(
            lambda: self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.login_page)
        )
        self.main_window.ui.acc_create_error_bot_but.clicked.connect(
            lambda: self.main_window.ui.login_pages.setCurrentWidget(self.main_window.ui.reset_pass_email_page)
        )

    def show_error(self, text):
        self.main_window.ui.acc_create_error_text.setText(str(text))
