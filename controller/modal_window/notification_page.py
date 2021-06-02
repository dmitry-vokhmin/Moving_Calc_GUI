
class NotificationPage:
    def __init__(self, main_modal_window):
        self.main_modal_window = main_modal_window
        self.main_modal_window.ui.error_cancel_butt.clicked.connect(self.main_modal_window.reject)
        self.main_modal_window.ui.success_butt.clicked.connect(self.main_modal_window.accept)

    def show_error_page(self, error):
        print(error)
        self.main_modal_window.ui.pages.setCurrentWidget(self.main_modal_window.ui.error_page)
        self.main_modal_window.open()

    def show_success_page(self, data):
        print(data)
        self.main_modal_window.ui.pages.setCurrentWidget(self.main_modal_window.ui.success_page)
        self.main_modal_window.open()

    def error_button(self, previous_page=None):
        if previous_page:
            self.main_modal_window.ui.error_butt.clicked.connect(previous_page)
        self.main_modal_window.ui.error_butt.clicked.connect(self.main_modal_window.reject)
