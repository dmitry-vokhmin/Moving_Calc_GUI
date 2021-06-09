import re
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent
from model.inventory_category.inventory_category import InventoryCategory
from model.inventory.inventory import Inventory
from model.room_collection.room_collection import RoomCollection
from model.inventory_collections.inventory_collection import InventoryCollection
from model.inventory_inventory_collection.inventory_inventory_collection import InventoryInventoryCollection


class InventoryPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.set_left_menu = True
        self.all_menu_buttons = None
        self.preset_menu_buttons = None
        self.main_window.ui.inventory_all_menu_butt.clicked.connect(
            lambda: self.change_inside_page(True, self.main_window.ui.inventory_room_page)
        )
        self.main_window.ui.inventory_preset_choose_butt.clicked.connect(
            lambda: self.change_inside_page(False, self.main_window.ui.inventory_preset_page)
        )
        self.main_window.ui.inventory_page.installEventFilter(self)
        self.main_window.ui.inventory_search_input.installEventFilter(self)
        self.main_window.ui.inventory_save_butt.clicked.connect(self.update_preset)
        self.main_window.ui.inventory_add_butt.clicked.connect(self.main_window.modal_window.show_inventory_item_page)
        self.main_window.ui.inventory_search_input.textChanged.connect(self.search)
        self.main_window.ui.inventory_search_clear.clicked.connect(
            lambda: self.main_window.ui.inventory_search_input.clear()
        )
        self.main_window.ui.inventory_reset_btn.clicked.connect(self.reset)
        self.main_window.ui.inventory_reset_btn.installEventFilter(self)

    def reset(self):
        for button in self.main_window.ui.inventory_preset_menu_frame.findChildren(QPushButton):
            if button.isChecked():
                inventory_collection_id = button.__getattribute__("inventory_collection_id")
        inventory_collection = InventoryCollection(inventory_collection_id=inventory_collection_id)
        response_code, response_data = inventory_collection.delete()
        if response_code > 399:
            self.main_window.modal_window.show_notification_page(response_data, is_error=True)
        else:
            self.main_window.modal_window.show_notification_page(response_data, is_error=False)

    def change_inside_page(self, is_all_inventory, page):
        self.main_window.inventory_ui.change_page_selector_style(is_all_inventory)
        self.main_window.ui.inventory_size_menu.setCurrentWidget(page)

    def update_preset(self):
        data = self.get_update_data()
        inventory_collection_api = InventoryInventoryCollection(*data)
        response_code, response_data = inventory_collection_api.put()
        if response_code > 399:
            self.main_window.modal_window.show_notification_page(response_data, is_error=True)
        else:
            self.main_window.modal_window.show_notification_page(response_data, is_error=False)

    def get_update_data(self):
        data = []
        for frame in self.main_window.ui.inventory_content_clear_frame.findChildren(QFrame, "card_main_frame"):
            data_frame = {
                "inventory_id": frame.__getattribute__("inventory_id"),
                "inventory_collection_id": frame.__getattribute__("inventory_collection_id"),
                "count": frame.findChild(QComboBox).currentText()
            }
            data.append(data_frame)
        return data

    def get_response(self, end_point, room_id=None):
        if room_id:
            api_end_point = end_point(**room_id)
        else:
            api_end_point = end_point()
        response_code, response_data = api_end_point.get()
        if response_code > 399:
            print(response_data)
        else:
            return response_data

    def get_category_inventory(self, room_id, room_collection_id, button):
        def wrap():
            categories = self.get_response(InventoryCategory, {"room_id": room_id})
            self.main_window.inventory_ui.set_category_menu(categories, self.categorize_inventory, self)
            self.get_inventory({"room_collection_id": room_collection_id}, button, False)()

        return wrap

    def get_inventory(self, button_attribute, button, is_preset):
        def wrap():
            self.select_menu_point(button, is_preset)
            if is_preset:
                inventory = self.get_response(InventoryInventoryCollection, button_attribute)
            else:
                inventory = self.get_response(Inventory, button_attribute)
            self.main_window.inventory_ui.set_room_inventory_card(inventory,
                                                                  self.del_item,
                                                                  self.add_item,
                                                                  is_preset,
                                                                  self)
        return wrap

    def select_menu_point(self, button, is_preset):
        if is_preset:
            menu_buttons = self.preset_menu_buttons
        else:
            menu_buttons = self.all_menu_buttons
        for menu_button in menu_buttons:
            if menu_button == button:
                menu_button.setChecked(True)
            else:
                menu_button.setChecked(False)

    def add_item(self, inventory_id):
        def wrap():
            self.main_window.modal_window.show_inventory_item_preset_page(inventory_id)

        return wrap

    def del_item(self, inventory_id, inventory_collection_id: int = None):
        def wrap():
            if inventory_collection_id:
                inventory_collection_api = InventoryInventoryCollection(
                    inventory_id=inventory_id,
                    inventory_collection_id=inventory_collection_id
                )
                inventory_collection_api.delete()
            else:
                room_collection = RoomCollection(inventory_id)
                room_collection.delete()

        return wrap

    def search(self, text):
        text = text.lower()
        if text:
            self.main_window.ui.inventory_search_clear.setVisible(True)
        else:
            self.main_window.ui.inventory_search_clear.setVisible(False)
        cards = self.main_window.ui.inventory_content_clear_frame.findChildren(QFrame, "card_main_frame")
        for card in cards:
            item_text = card.__getattribute__("item_name")
            if re.search(fr"\b{text}", item_text.lower()):
                card.setVisible(True)
            else:
                card.setVisible(False)

    def categorize_inventory(self, button, category_id=None):
        def wrap():
            self.main_window.inventory_ui.categorize_inventory(category_id)
            self.select_category_menu_point(button)
        return wrap

    def select_category_menu_point(self, button):
        for menu_button in self.main_window.ui.inventory_categor_butt_frame.findChildren(QPushButton):
            if menu_button == button:
                menu_button.setChecked(True)
            else:
                menu_button.setChecked(False)
                menu_button.setIcon(QIcon(":/image/check_icon_default.svg"))

    def eventFilter(self, obj, event) -> bool:
        if obj is self.main_window.ui.inventory_page:
            if event.type() == QEvent.Show:
                if self.set_left_menu:
                    room_collection = self.get_response(RoomCollection)
                    self.main_window.inventory_ui.set_left_menu(self.main_window.ui.inventory_room_menu_frame,
                                                                self.main_window.ui.inventory_room_menu_layout,
                                                                self.get_category_inventory,
                                                                room_collection,
                                                                is_preset_menu=False)
                    self.all_menu_buttons = self.main_window.ui.inventory_room_menu_frame.findChildren(QPushButton)
                    inventory_collection = self.get_response(InventoryCollection)
                    self.main_window.inventory_ui.set_left_menu(self.main_window.ui.inventory_preset_menu_frame,
                                                                self.main_window.ui.inventory_preset_menu_layout,
                                                                self.get_inventory,
                                                                inventory_collection,
                                                                is_preset_menu=True)
                    self.preset_menu_buttons = self.main_window.ui.inventory_preset_menu_frame.findChildren(QPushButton)
                    self.set_left_menu = False
                self.change_inside_page(True, self.main_window.ui.inventory_room_page)
                return True
        if obj in self.main_window.ui.inventory_categor_butt_frame.findChildren(QPushButton):
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/check_icon_hover.svg"))
                return True
            if event.type() == QEvent.HoverLeave and not obj.isChecked():
                obj.setIcon(QIcon(":/image/check_icon_default.svg"))
                return True
        if obj in self.main_window.ui.inventory_content_clear_frame.findChildren(QPushButton, "add"):
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/plus_blue_icon.svg"))
                return True
            if event.type() == QEvent.HoverLeave:
                obj.setIcon(QIcon(":/image/plus_gray_icon.svg"))
                return True
        if obj in self.main_window.ui.inventory_content_clear_frame.findChildren(QPushButton, "delete"):
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/inventory_delete_hover.svg"))
                return True
            if event.type() == QEvent.HoverLeave:
                obj.setIcon(QIcon(":/image/inventory_delete_default.svg"))
                return True
        if obj is self.main_window.ui.inventory_search_input:
            if event.type() == QEvent.FocusIn:
                self.main_window.ui.inventory_search_frame.setStyleSheet(
                    "#inventory_search_frame{border: 0.5px solid #0915CC;background: #F2F3F6;border-radius: 5px;}")
                self.main_window.ui.inventory_search_label.setStyleSheet(
                    "image: url(:/image/search_icon_hover.svg);background: #F2F3F6;")
            if event.type() == QEvent.FocusOut:
                self.main_window.ui.inventory_search_frame.setStyleSheet(
                    "background: #F2F3F6;border-radius: 5px;")
                self.main_window.ui.inventory_search_label.setStyleSheet(
                    "image: url(:/image/search_icon_default.svg);background: #F2F3F6;")
        if obj is self.main_window.ui.inventory_reset_btn:
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/inventory_reset_hover.svg"))
                return True
            if event.type() == QEvent.HoverLeave:
                obj.setIcon(QIcon(":/image/inventory_reset_default.svg"))
                return True
        return False
