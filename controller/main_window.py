from PyQt5 import sip
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeyEvent
from view.main_windows.main_window_ui import Ui_MainWindow
from view.pages.menu_ui import MenuUI
from view.pages.user_management_table_ui import UserManagementTable
from view.pages.user_profile_ui import UserProfile
from view.pages.equipment_card_ui import EquipmentCard
from view.pages.price_settings_page_ui import PriceSettingsPage
from view.pages.calendar_page_ui import CalendarPage
from view.pages.inventory_page_ui import InventoryPageUi
from controller.login_window.login_page import LoginPage
from controller.login_window.registration_page import RegistrationPage
from controller.login_window.acc_created_page import AccCreatedPage
from controller.content_window.main_menu import MainMenu
from controller.content_window.user_management import UserManagement
from controller.modal_window.modal_window import ModalWindow
from controller.content_window.profile_page import ProfilePage
from controller.content_window.equipment_page import EquipmentPage
from controller.content_window.configuration_page import ConfigurationPage
from controller.content_window.inventory_page import InventoryPage
from model.user.user import User
from model.user_privilege.user_privilege import UserPrivilege
from model.user.authorization import Authorization, AuthorizationError
from model.user.user_company import UserCompany
from model.user_role.user_role import UserRole
from model.truck.truck import Truck
from model.truck.truck_type import TruckType
from model.calendar.calendar import Calendar
from model.mover_amount.mover_amount import MoverAmount
from model.price_tag.price_tag import PriceTag


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.menu_ui = MenuUI(self)
        self.user_management_table_ui = UserManagementTable(self)
        self.user_profile_ui = UserProfile(self)
        self.equipment_card = EquipmentCard(self)
        self.price_settings_ui = PriceSettingsPage(self)
        self.calendar_ui = CalendarPage(self)
        self.inventory_ui = InventoryPageUi(self)
        self.user = User()
        self.company_users = UserCompany()
        self.user_role = UserRole()
        self.truck = Truck()
        self.truck_type = TruckType()
        self.calendar = Calendar()
        self.mover_amount = MoverAmount()
        self.price_tag = PriceTag()
        self.modal_window = ModalWindow(self)
        self.login_page = LoginPage(self)
        self.reg_page = RegistrationPage(self)
        self.acc_created_page = AccCreatedPage(self)
        self.main_menu = MainMenu(self)
        self.user_management = UserManagement(self)
        self.profile = ProfilePage(self)
        self.equipment_page = EquipmentPage(self)
        self.configuration_page = ConfigurationPage(self)
        self.inventory_page = InventoryPage(self)
        self.check_authorization()
        self.get_price_tags()
        self.get_mover_amount()

    def get_price_tags(self):
        self.get_data(self.price_tag.get)
        self.calendar_ui.set_price_tag(self.ui.config_price_type_butt_frame)
        self.calendar_ui.set_calendars()
        self.configuration_page.set_event_filter()

    def get_mover_amount(self):
        self.get_data(self.mover_amount.get)

    def check_authorization(self):
        try:
            Authorization().check_authorization()
            self.get_user()
        except AuthorizationError:
            self.ui.window_pages.setCurrentWidget(self.ui.login_window)
            self.ui.login_pages.setCurrentWidget(self.ui.login_page)

    def log_out(self):
        Authorization.delete_token()
        self.ui.window_pages.setCurrentWidget(self.ui.login_window)
        self.ui.login_pages.setCurrentWidget(self.ui.login_page)

    def registration_error(self, data):
        self.acc_created_page.show_error(data)

    def get_data(self, api_end_point):
        response_code, response_data = api_end_point()
        if response_code > 399:
            print(response_data)
        else:
            return response_code, response_data

    def get_user(self):
        response_code, response_data = self.user.get()
        if response_code > 399:
            print(response_data)
        else:
            self.get_privilege()

    def get_privilege(self):
        response_code, response_data = UserPrivilege.get()
        if response_code > 399:
            print(response_data)
        else:
            self.main_menu.set_menu(response_data)
            self.ui.window_pages.setCurrentWidget(self.ui.content_window)
            self.ui.content_pages.setCurrentWidget(self.ui.calculator_page)
            self.get_data(self.user_role.get)

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

    def keyPressEvent(self, event: QKeyEvent) -> None:
        current_window = self.ui.window_pages.currentWidget().objectName()
        current_page = self.ui.login_pages.currentWidget().objectName()
        if event.key() == Qt.Key_Return and current_page == "login_page" and current_window == "login_window":
            self.login_page.login()
        elif event.key() == Qt.Key_Return and current_page == "registration_page" and current_window == "login_window":
            self.reg_page.registration()
