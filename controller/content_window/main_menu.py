from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon


class MainMenu(QWidget):
    def __init__(self, main_window, *args, **kwargs):
        QWidget.__init__(self, main_window, *args, **kwargs)
        self.main_window = main_window
        self.privilege = {}
        self._page_mapper = {
            "user management": lambda: self.change_menu_page(
                lambda: self.main_window.ui.content_pages.setCurrentWidget(self.main_window.ui.user_management_page)
            ),
            "calculator": lambda: self.change_menu_page(
                lambda: self.main_window.ui.content_pages.setCurrentWidget(self.main_window.ui.calculator_page)
            ),
            "equipment": lambda: self.change_menu_page(
                lambda: self.main_window.ui.content_pages.setCurrentWidget(self.main_window.ui.equipment_page)
            ),
            "configurations": lambda: self.change_menu_page(
                lambda: self.main_window.ui.content_pages.setCurrentWidget(self.main_window.ui.config_page)
            ),
            "inventory": lambda: self.change_menu_page(
                lambda: self.main_window.ui.content_pages.setCurrentWidget(self.main_window.ui.inventory_page)
            ),
        }
        self.main_window.ui.profile_butt.clicked.connect(lambda: self.change_menu_page(
            lambda: self.main_window.ui.content_pages.setCurrentWidget(self.main_window.ui.profile_page)
        ))
        self.main_window.ui.profile_butt.installEventFilter(self)

    def set_menu(self, data):
        self.privilege = self.main_window.menu_ui.set_menu(data, self._page_mapper)

    def change_menu_page(self, show_page_funk):
        for ui_elem in self.privilege.values():
            if ui_elem["button"].isChecked():
                self.main_window.menu_ui.change_menu_button_style(ui_elem, True)
                ui_elem["button"].nextCheckState()
            else:
                self.main_window.menu_ui.change_menu_button_style(ui_elem, False)
        if self.main_window.ui.profile_butt.isChecked():
            self.main_window.menu_ui.change_profile_butt(is_selected=True)
            self.main_window.ui.profile_butt.nextCheckState()
            self.main_window.ui.profile_page.setVisible(False)
            self.main_window.ui.profile_page.setVisible(True)
        else:
            self.main_window.menu_ui.change_profile_butt(is_selected=False)
        show_page_funk()

    def eventFilter(self, obj, event) -> bool:
        if event.type() == QtCore.QEvent.HoverEnter:
            obj.setIcon(QIcon(":/image/account_active.svg"))
            return True
        if event.type() == QtCore.QEvent.HoverLeave and \
                (self.main_window.ui.content_pages.currentWidget().objectName() != "profile_page"
                 or self.main_window.profile.staff_profile):
            obj.setIcon(QIcon(":/image/account.svg"))
            return True
        return False
