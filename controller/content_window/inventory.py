from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent
from model.inventory.inventory_category import InventoryCategory
from model.inventory.inventory import Inventory as InventoryApi
from model.inventory.inventory_inventory_collection import InventoryInventoryCollection


class Inventory(QWidget):
    def __init__(self, main_window, category_frame, content_frame):
        super().__init__()
        self.main_window = main_window
        self.category_frame = category_frame
        self.content_frame = content_frame
        self.all_menu_buttons = None
        self.preset_menu_buttons = None
        self.first_butt_all_inv = None
        self.first_butt_preset = None
        self.category_btn = set()
        self.add_item_btn = set()
        self.del_item_btn = set()

    def set_left_menu(self, frame, layout, menu_funk, data, add_funk, is_preset_menu, del_funk=None):
        self.main_window.inventory_ui.set_left_menu(frame, layout, menu_funk, data, add_funk, del_funk, is_preset_menu)

    def set_calc_preset_menu(self, frame, preset_inventory, menu_funk):
        self.main_window.inventory_ui.set_preset_menu(frame, preset_inventory, menu_funk)

    def assign_buttons(self, all_inventory_frame, preset_inventory_frame):
        all_inventory_buttons = all_inventory_frame.findChildren(QPushButton)
        preset_inventory_buttons = preset_inventory_frame.findChildren(QPushButton)
        self.first_butt_all_inv = all_inventory_buttons[0]
        self.first_butt_preset = preset_inventory_buttons[0]
        self.all_menu_buttons = all_inventory_buttons
        self.preset_menu_buttons = preset_inventory_buttons

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

    def get_category_inventory(self, room_id, room_collection_id, button, del_funk, add_funk):
        def wrap():
            categories = self.get_response(InventoryCategory, {"room_id": room_id})
            self.main_window.inventory_ui.set_category_menu(categories, self.categorize_inventory, self.category_frame,
                                                            self)
            self.get_inventory({"room_collection_id": room_collection_id}, button, False, del_funk, add_funk)()
            self.category_btn = {btn for btn in self.category_frame.findChildren(QPushButton)}
        return wrap

    def get_inventory(self, button_attribute, button, is_preset, del_funk, add_funk):
        def wrap():
            self.select_menu_point(button, is_preset)
            if is_preset:
                inventory = self.get_response(InventoryInventoryCollection, button_attribute)
            else:
                inventory = self.get_response(InventoryApi, button_attribute)
            self.main_window.inventory_ui.set_room_inventory_card(inventory,
                                                                  del_funk,
                                                                  add_funk,
                                                                  is_preset,
                                                                  self.content_frame,
                                                                  self)
            self.del_item_btn = {btn for btn in self.content_frame.findChildren(QPushButton, "delete")}
            self.add_item_btn = {btn for btn in self.content_frame.findChildren(QPushButton, "add")}
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

    def categorize_inventory(self, button, category_id=None):
        def wrap():
            self.main_window.inventory_ui.categorize_inventory(self.content_frame, category_id)
            self.select_category_menu_point(button)

        return wrap

    def select_category_menu_point(self, button):
        for menu_button in self.category_frame.findChildren(QPushButton):
            if menu_button == button:
                menu_button.setChecked(True)
            else:
                menu_button.setChecked(False)
                menu_button.setIcon(QIcon(":/image/check_icon_default.svg"))

    def eventFilter(self, obj, event) -> bool:
        if obj in self.category_btn:
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/check_icon_hover.svg"))
                return True
            if event.type() == QEvent.HoverLeave and not obj.isChecked():
                obj.setIcon(QIcon(":/image/check_icon_default.svg"))
                return True
        if obj in self.add_item_btn:
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/plus_blue_icon.svg"))
                return True
            if event.type() == QEvent.HoverLeave:
                obj.setIcon(QIcon(":/image/plus_gray_icon.svg"))
                return True
        if obj in self.del_item_btn:
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/inventory_delete_hover.svg"))
                return True
            if event.type() == QEvent.HoverLeave:
                obj.setIcon(QIcon(":/image/inventory_delete_default.svg"))
                return True
        return False
