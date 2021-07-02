from pathlib import Path
import json
from PyQt5 import sip
from PyQt5.QtWidgets import QMainWindow, QMessageBox, qApp
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QKeyEvent, QIcon
from view.main_windows.main_window_ui import Ui_MainWindow
from view.pages.menu_ui import MenuUI
from view.pages.user_management_table_ui import UserManagementTable
from view.pages.user_profile_ui import UserProfile
from view.pages.equipment_card_ui import EquipmentCard
from view.pages.price_settings_page_ui import PriceSettingsPage
from view.pages.calendar_page_ui import CalendarPage
from view.pages.inventory_page_ui import InventoryPageUi
from view.pages.inventory_ui import InventoryUi
from view.pages.calendar_ui import CalendarUi
from view.pages.calculator_page_ui import CalculatorPageUi
from controller.login_window.login_page import LoginPage
from controller.login_window.reset_pass_page import ResetPassPage
from controller.login_window.registration_user_page import RegistrationPage
from controller.login_window.registration_company_page import RegistrationCompanyPage
from controller.login_window.acc_created_page import AccCreatedPage
from controller.content_window.main_menu import MainMenu
from controller.content_window.user_management import UserManagement
from controller.modal_window.modal_window import ModalWindow
from controller.content_window.profile_page import ProfilePage
from controller.content_window.equipment_page import EquipmentPage
from controller.content_window.configuration_page import ConfigurationPage
from controller.content_window.inventory_page import InventoryPage
from controller.content_window.calculator.calculator_main_page import CalculatorPage
from model.user.user import User
from model.user.user_privilege import UserPrivilege
from model.authorization import Authorization, AuthorizationError
from model.user.user_role import UserRole
from model.calendar import Calendar
from model.mover_amount import MoverAmount
from model.move_size import MoveSize
from model.floor_collection import FloorCollection


class MainWindow(QMainWindow):
    EXIT_CODE_REBOOT = -12345678

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(":/image/logo.svg"))
        self.setWindowTitle(" Moving Calculator")
        self.menu_ui = MenuUI(self)
        self.user_management_table_ui = UserManagementTable(self)
        self.user_profile_ui = UserProfile(self)
        self.equipment_card = EquipmentCard(self)
        self.price_settings_ui = PriceSettingsPage(self)
        self.calendar_page_ui = CalendarPage(self)
        self.inventory_page_ui = InventoryPageUi(self)
        self.inventory_ui = InventoryUi(self)
        self.calendar_ui = CalendarUi(self)
        self.calculator_page_ui = CalculatorPageUi(self)
        self.change_page_data = True
        self.user = User()
        self.user_role = UserRole()
        self.calendar = Calendar()
        self.move_size = MoveSize()
        self.floor_collection = FloorCollection()
        self.mover_amount = MoverAmount()
        self.modal_window = ModalWindow(self)
        self.login_page = LoginPage(self)
        self.reset_pass_page = ResetPassPage(self)
        self.reg_page = RegistrationPage(self)
        self.reg_comp_page = RegistrationCompanyPage(self)
        self.acc_created_page = AccCreatedPage(self)
        self.main_menu = MainMenu(self)
        self.user_management = UserManagement(self)
        self.profile = ProfilePage(self)
        self.equipment_page = EquipmentPage(self)
        self.configuration_page = ConfigurationPage(self)
        self.inventory_page = InventoryPage(self)
        self.calculator_page = CalculatorPage(self)
        self.check_authorization()
        self.get_mover_amount()
        self.get_move_size()
        self.get_floor()
        self.ui.window_pages.installEventFilter(self)
        self.read_inv_images()

    def get_floor(self):
        self.save_data(self.floor_collection)

    def set_calendar(self, calendar):
        self.save_data(self.calendar)
        self.calendar_ui.set_calendar_dates(calendar)

    def get_move_size(self):
        self.save_data(self.move_size)

    def get_mover_amount(self):
        self.save_data(self.mover_amount)

    def check_authorization(self):
        try:
            Authorization().check_authorization()
            self.get_user()
        except AuthorizationError:
            self.ui.window_pages.setCurrentWidget(self.ui.login_window)
            self.ui.login_pages.setCurrentWidget(self.ui.login_page)

    def log_out(self):
        Authorization.delete_token()
        qApp.exit(self.EXIT_CODE_REBOOT)

    def registration_error(self, text):
        self.acc_created_page.show_error(text)

    def get_data(self, end_point):
        api_end_point = end_point()
        response_code, response_data = api_end_point.get()
        if response_code > 399:
            self.modal_window.show_notification_page(description=response_data, is_error=True)
        else:
            return response_data

    def save_data(self, end_point):
        response_code, response_data = end_point.get()
        if response_code > 399:
            self.modal_window.show_notification_page(description=response_data, is_error=True)
        else:
            return response_code, response_data

    def get_user(self):
        response_code, response_data = self.save_data(self.user)
        if response_code > 399:
            print(response_data)
            raise Exception
        else:
            try:
                self.company_is_active(response_data)
                self.get_privilege()
            except AuthorizationError:
                self.modal_window.show_notification_page(description="account is not active", is_error=True)

    @staticmethod
    def company_is_active(user):
        if not user["company"]["is_active"]:
            raise AuthorizationError

    def get_privilege(self):
        user_privilege = UserPrivilege()
        response_code, response_data = user_privilege.get()
        if response_code > 399:
            print(response_data)
        else:
            self.main_menu.set_menu(response_data)
            self.ui.window_pages.setCurrentWidget(self.ui.content_window)
            self.ui.content_pages.setCurrentWidget(self.ui.calculator_page)
            self.save_data(self.user_role)

    def delete_layout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    sip.delete(widget)
                    # widget.deleteLater()
                else:
                    self.delete_layout(item.layout())
            sip.delete(layout)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Close Application', 'Are you sure you want to close the application?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.write_inv_images()
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        current_window = self.ui.window_pages.currentWidget().objectName()
        current_page = self.ui.login_pages.currentWidget().objectName()
        if event.key() == Qt.Key_Return and current_page == "login_page" and current_window == "login_window":
            self.login_page.login()
        elif event.key() == Qt.Key_Return and current_page == "registration_page" and current_window == "login_window":
            self.reg_page.registration()

    def eventFilter(self, obj, event) -> bool:
        if obj is self.ui.window_pages:
            if event.type() == QEvent.Show:
                self.change_page_data = True
                return True
            if event.type() == QEvent.Hide:
                self.change_page_data = False
                return True
        return False

    def read_inv_images(self):
        json_path = Path(__file__).parent.parent.joinpath("inv_images/images.json")
        with open(json_path, "r") as json_images:
            self.inventory_ui.image_dict = json.load(json_images)

    def write_inv_images(self):
        json_path = Path(__file__).parent.parent.joinpath("inv_images/images.json")
        with open(json_path, "w") as json_images:
            json.dump(self.inventory_ui.image_dict, json_images)
