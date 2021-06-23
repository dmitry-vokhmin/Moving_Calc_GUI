class NotificationPage:
    def __init__(self, main_modal_window):
        self.main_modal_window = main_modal_window
        self.main_modal_window.ui.error_cancel_butt.clicked.connect(self.main_modal_window.reject)
        self.main_modal_window.ui.error_butt.clicked.connect(self.main_modal_window.accept)
        self.main_modal_window.ui.success_butt.clicked.connect(self.main_modal_window.accept)

    def show_error_page(self, error_title, error_description):
        if error_description or error_title:
            self.main_modal_window.ui.error_text.setText(
                f"Your request cannot be completed. Reason: {error_description}."
            )
        else:
            self.main_modal_window.ui.error_text.setText("Your request cannot be completed, please try again.")
        self.main_modal_window.ui.pages.setCurrentWidget(self.main_modal_window.ui.error_page)
        self.main_modal_window.open()

    def show_success_page(self, title, description):
        if description and title:
            self.main_modal_window.ui.success_header.setText(title)
            self.main_modal_window.ui.success__text.setText(description)
        self.main_modal_window.ui.pages.setCurrentWidget(self.main_modal_window.ui.success_page)
        self.main_modal_window.open()

    def success_button(self, next_page, btn_text):
        self.main_modal_window.ui.success_butt.clicked.disconnect()
        if next_page:
            self.main_modal_window.ui.success_butt.clicked.connect(next_page)
            self.main_modal_window.ui.success_butt.setText(btn_text)
        else:
            self.main_modal_window.ui.success_butt.clicked.connect(self.main_modal_window.accept)
            self.main_modal_window.ui.success_butt.setText("Got it")

    def error_button(self, previous_page):
        self.main_modal_window.ui.error_butt.clicked.disconnect()
        if previous_page:
            self.main_modal_window.ui.error_butt.clicked.connect(previous_page)
        else:
            self.main_modal_window.ui.error_butt.clicked.connect(self.main_modal_window.accept)
