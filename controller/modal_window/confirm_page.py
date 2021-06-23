class ConfirmPage:
    def __init__(self, main_modal_window):
        self.main_modal_window = main_modal_window
        self.main_modal_window.ui.confirm_cancel_butt.clicked.connect(self.main_modal_window.reject)
        self.main_modal_window.ui.confirm_accept_butt.clicked.connect(self.main_modal_window.accept)

    def confirm_changes(self, funk):
        self.main_modal_window.ui.confirm_accept_butt.clicked.disconnect()
        self.main_modal_window.ui.confirm_accept_butt.clicked.connect(lambda: self.close_confirm_page(funk()))
        self.main_modal_window.open()

    def close_confirm_page(self, _):
        if self.main_modal_window.ui.pages.currentWidget().objectName() == "error_page" or \
                self.main_modal_window.ui.pages.currentWidget().objectName() == "success_page":
            pass
        else:
            self.main_modal_window.close()

    def change_text(self, desc_text, btn_text):
        self.main_modal_window.ui.confirm_text.setText(f"Are you sure you want to {desc_text}")
        self.main_modal_window.ui.confirm_accept_butt.setText(f"Yes, {btn_text}")
