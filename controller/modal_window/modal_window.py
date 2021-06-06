from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt, QEvent
from view.main_windows.modal_window_ui import Ui_dialog
from controller.modal_window.confirm_page import ConfirmPage
from controller.modal_window.notification_page import NotificationPage
from controller.modal_window.add_user_page import AddUserPage
from controller.modal_window.asset_page import AssetPage
from controller.modal_window.asset_type_page import AssetTypePage
from controller.modal_window.inventory_item_page import InventoryItemPage
from controller.modal_window.inventory_item_preset_page import InventoryItemPresetPage
from view.pages.asset_page_ui import AssetPageUi
from view.pages.asset_type_page_ui import AssetTypePageUi
from view.pages.inventory_add_item_ui import InventoryAddItemUi


class ModalWindow(QDialog):
    def __init__(self, main_window, *args, **kwargs):
        super().__init__(main_window, *args, **kwargs)
        self.main_window = main_window
        self.ui = Ui_dialog()
        self.ui.setupUi(self)
        self.asset_page_ui = AssetPageUi(self)
        self.asset_type_page_ui = AssetTypePageUi(self)
        self.inventory_add_item_ui = InventoryAddItemUi(self)
        self.notification_page = NotificationPage(self)
        self.confirm_page = ConfirmPage(self)
        self.add_user_page = AddUserPage(self)
        self.asset_page = AssetPage(self)
        self.asset_type_page = AssetTypePage(self)
        self.inventory_item_page = InventoryItemPage(self)
        self.inventory_item_preset_page = InventoryItemPresetPage(self)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.ui.pages.installEventFilter(self)

    def show_add_user_page(self):
        self.ui.pages.setCurrentWidget(self.ui.add_user_page)
        self.open()

    def show_notification_page(self, data, is_error, previous_page=None):
        if is_error:
            self.notification_page.show_error_page(data)
            self.notification_page.error_button(previous_page)
        else:
            self.notification_page.show_success_page(data)

    def show_confirm_dialog(self, funk):
        self.confirm_page.confirm_changes(funk)
        self.ui.pages.setCurrentWidget(self.ui.confirm_page)

    def show_asset_page(self, asset_data=None):
        self.ui.pages.setCurrentWidget(self.ui.asset_page)
        self.asset_page.set_asset_page(asset_data)

    def show_asset_type_page(self, asset_data=None):
        self.ui.pages.setCurrentWidget(self.ui.asset_type_page)
        self.asset_type_page.set_asset_page(asset_data)

    def show_inventory_item_page(self):
        self.ui.pages.setCurrentWidget(self.ui.invetory_item_page)
        self.show()

    def show_inventory_item_preset_page(self, inventory_id):
        self.ui.pages.setCurrentWidget(self.ui.inventory_preset_page)
        self.inventory_item_preset_page.inventory_id = inventory_id
        self.show()

    def eventFilter(self, obj, event: QEvent) -> bool:
        if obj is self.ui.pages:
            if event.type() == QEvent.Show:
                self.setGeometry(self.main_window.geometry())
                return True
        return False
