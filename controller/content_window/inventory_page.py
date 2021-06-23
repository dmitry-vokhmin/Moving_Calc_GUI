import re
from PyQt5.QtWidgets import QWidget, QFrame, QPushButton, QComboBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QEvent
from model.inventory.room_collection import RoomCollection
from model.inventory.inventory_collection import InventoryCollection
from model.inventory.inventory_inventory_collection import InventoryInventoryCollection
from controller.content_window.inventory import Inventory


class InventoryPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.set_left_menu = True
        self.inventory = Inventory(main_window,
                                   self.main_window.ui.inventory_categor_butt_frame,
                                   self.main_window.ui.inventory_content_clear_frame)
        self.main_window.ui.inventory_all_menu_butt.clicked.connect(
            lambda: self.change_inside_page(True,
                                            self.main_window.ui.inventory_room_page,
                                            self.inventory.first_butt_all_inv)
        )
        self.main_window.ui.inventory_preset_choose_butt.clicked.connect(
            lambda: self.change_inside_page(False,
                                            self.main_window.ui.inventory_preset_page,
                                            self.inventory.first_butt_preset)
        )
        self.main_window.ui.inventory_page.installEventFilter(self)
        self.main_window.ui.inventory_search_input.installEventFilter(self)
        self.main_window.ui.inventory_save_butt.clicked.connect(
            lambda: self.main_window.modal_window.show_confirm_dialog(self.update_preset,
                                                                      desc_text="save changes?",
                                                                      btn_text="save")
        )
        self.main_window.ui.inventory_add_butt.clicked.connect(self.main_window.modal_window.show_inventory_item_page)
        self.main_window.ui.inventory_search_input.textChanged.connect(self.search)
        self.main_window.ui.inventory_search_clear.clicked.connect(
            lambda: self.main_window.ui.inventory_search_input.setText("")
        )
        self.main_window.ui.inventory_reset_btn.clicked.connect(self.notification_reset_btn)
        self.main_window.ui.inventory_reset_btn.installEventFilter(self)

    def notification_reset_btn(self):
        for button in self.main_window.ui.inventory_preset_menu_frame.findChildren(QPushButton):
            if button.isChecked():
                inventory_collection_id = getattr(button, "inventory_collection_id")
                btn_text = button.text()
        self.main_window.modal_window.show_confirm_dialog(funk=self.reset(inventory_collection_id, btn_text),
                                                          desc_text=f"reset {btn_text} to its default settings?",
                                                          btn_text="reset")

    def reset(self, inventory_collection_id, btn_text):
        def wrap():
            inventory_collection = InventoryCollection(inventory_collection_id=inventory_collection_id)
            response_code, response_data = inventory_collection.delete()
            if response_code > 399:
                self.main_window.modal_window.show_notification_page(description=response_data, is_error=True)
            else:
                self.main_window.modal_window.show_notification_page(
                    title=f"{btn_text} restored",
                    description=f"{btn_text} was successfully restored",
                    is_error=False)
                self.reset_inventory(self.main_window.ui.inventory_preset_menu_frame)
        return wrap

    def change_inside_page(self, is_all_inventory, page, button):
        self.main_window.inventory_page_ui.change_page_selector_style(is_all_inventory, button)
        self.main_window.ui.inventory_size_menu.setCurrentWidget(page)

    def update_preset(self):
        data = self.get_update_data()
        inventory_collection_api = InventoryInventoryCollection(*data)
        response_code, response_data = inventory_collection_api.put()
        if response_code > 399:
            self.main_window.modal_window.show_notification_page(description=response_data, is_error=True)
        else:
            self.main_window.modal_window.show_notification_page(title="All changes saved",
                                                                 description="All changes were saved",
                                                                 is_error=False)

    def get_update_data(self):
        data = []
        for frame in self.main_window.ui.inventory_content_clear_frame.findChildren(QFrame, "card_main_frame"):
            data_frame = {
                "inventory_id": getattr(frame, "inventory_id"),
                "inventory_collection_id": getattr(frame, "inventory_collection_id"),
                "count": frame.findChild(QComboBox).currentText()
            }
            data.append(data_frame)
        return data

    def add_item(self, inventory):
        def wrap():
            self.main_window.modal_window.show_inventory_item_preset_page(inventory)

        return wrap

    def del_item(self, inventory_id, inventory_collection_id: int = None):
        def wrap():
            if inventory_collection_id:
                inventory_collection_api = InventoryInventoryCollection(
                    inventory_id=inventory_id,
                    inventory_collection_id=inventory_collection_id
                )
                inventory_collection_api.delete()
                self.reset_inventory(self.main_window.ui.inventory_preset_menu_frame)
            else:
                room_collection = RoomCollection(inventory_id)
                room_collection.delete()
                self.reset_inventory(self.main_window.ui.inventory_room_menu_frame)

        return wrap

    @staticmethod
    def reset_inventory(frame):
        for btn in frame.findChildren(QPushButton):
            if btn.isChecked():
                btn.click()

    def search(self, text):
        text = text.lower()
        if text:
            self.main_window.ui.inventory_search_clear.setVisible(True)
            self.main_window.ui.inventory_search_frame.setProperty("selected", True)
            self.main_window.ui.inventory_search_frame.setStyle(self.main_window.ui.inventory_search_frame.style())
            self.main_window.ui.inventory_search_label.setStyleSheet("image: url(:/image/search_icon_hover.svg)")
        else:
            self.main_window.ui.inventory_search_clear.setVisible(False)
            self.main_window.ui.inventory_search_frame.setProperty("selected", False)
            self.main_window.ui.inventory_search_frame.setStyle(self.main_window.ui.inventory_search_frame.style())
            self.main_window.ui.inventory_search_label.setStyleSheet("image: url(:/image/search_icon_default.svg);")
        cards = self.main_window.ui.inventory_content_clear_frame.findChildren(QFrame, "card_main_frame")
        for card in cards:
            item_text = getattr(card, "item_name")
            if re.search(fr"\b{text}", item_text.lower()):
                card.setVisible(True)
            else:
                card.setVisible(False)

    def eventFilter(self, obj, event) -> bool:
        if obj is self.main_window.ui.inventory_page:
            if event.type() == QEvent.Show and self.main_window.change_page_data:
                if self.set_left_menu:
                    room_collection = self.inventory.get_response(RoomCollection)
                    self.inventory.set_left_menu(self.main_window.ui.inventory_room_menu_frame,
                                                 self.inventory.get_category_inventory,
                                                 room_collection,
                                                 add_funk=self.add_item,
                                                 is_preset_menu=False,
                                                 del_funk=self.del_item)
                    inventory_collection = self.inventory.get_response(InventoryCollection)
                    self.inventory.set_left_menu(self.main_window.ui.inventory_preset_menu_frame,
                                                 self.inventory.get_inventory,
                                                 inventory_collection,
                                                 add_funk=self.add_item,
                                                 is_preset_menu=True,
                                                 del_funk=self.del_item)
                    self.inventory.assign_buttons(self.main_window.ui.inventory_room_menu_frame,
                                                  self.main_window.ui.inventory_preset_menu_frame)
                    self.set_left_menu = False
                self.change_inside_page(True, self.main_window.ui.inventory_room_page,
                                        self.inventory.first_butt_all_inv)
                return True
            if event.type() == QEvent.Hide:
                self.set_left_menu = True
                return True
        if obj is self.main_window.ui.inventory_search_input:
            if event.type() == QEvent.HoverEnter:
                self.main_window.ui.inventory_search_frame.setProperty("selected", True)
                self.main_window.ui.inventory_search_frame.setStyle(self.main_window.ui.inventory_search_frame.style())
                self.main_window.ui.inventory_search_label.setStyleSheet(
                    "image: url(:/image/search_icon_hover.svg)")
                return True
            if event.type() == QEvent.HoverLeave and not self.main_window.ui.inventory_search_input.text():
                self.main_window.ui.inventory_search_frame.setProperty("selected", False)
                self.main_window.ui.inventory_search_frame.setStyle(self.main_window.ui.inventory_search_frame.style())
                self.main_window.ui.inventory_search_label.setStyleSheet(
                    "image: url(:/image/search_icon_default.svg);")
                return True
        if obj is self.main_window.ui.inventory_reset_btn:
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/inventory_reset_hover.svg"))
                return True
            if event.type() == QEvent.HoverLeave:
                obj.setIcon(QIcon(":/image/inventory_reset_default.svg"))
                return True
        return False
