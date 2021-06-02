
class ConfirmPage:
    def __init__(self, main_modal_window):
        self.main_modal_window = main_modal_window
        self.main_modal_window.ui.confirm_cancel_butt.clicked.connect(self.main_modal_window.reject)

    def confirm_changes(self, funk):
        self.main_modal_window.ui.confirm_accept_butt.clicked.connect(lambda: self.close_confirm_page(funk()))
        self.main_modal_window.open()

    def close_confirm_page(self, _):
        self.main_modal_window.close()
