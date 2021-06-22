from PyQt5.QtWidgets import QWidget, QPushButton, QFrame
from PyQt5.QtCore import QEvent
from controller.content_window.inventory import Inventory
from model.inventory.inventory_inventory_collection import InventoryInventoryCollection
from model.inventory.room_collection import RoomCollection


class CalcInventoryCheckPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.set_all_inventory = True
        self.inventory = Inventory(main_window,
                                   self.main_window.ui.calc_inv_categor_butt_frame_2,
                                   self.main_window.ui.calc_inv_content_clear_frame)
        self.preset_inventory = {}
        self.main_window.ui.calc_invnetory_check_page.installEventFilter(self)
        self.main_window.ui.calc_all_menu_butt.clicked.connect(
            lambda: self.change_inside_page(True, self.main_window.ui.calc_room_page, self.inventory.first_butt_all_inv)
        )
        self.main_window.ui.calc_preset_choose_butt.clicked.connect(
            lambda: self.change_inside_page(False, self.main_window.ui.calc_preset_page,
                                            self.inventory.first_butt_preset)
        )

    def add_item(self, inventory):
        def wrap():
            self.main_window.modal_window.show_inventory_item_preset_page(inventory, self.preset_inventory)

        return wrap

    def count_change(self, count, move_size_id, inventory_id):
        for inventory in self.preset_inventory[move_size_id]["inventory"]:
            if inventory["inventory_id"] == inventory_id:
                inventory["count"] = int(count)
                break

    def update_preset_inventory_cards(self, move_size_id):
        self.main_window.inventory_ui.create_preset_inventory_cards(move_size_id,
                                                                    self.preset_inventory,
                                                                    self.del_item,
                                                                    self.count_change,
                                                                    self.inventory)
        self.inventory.del_item_btn = {
            btn for btn in self.main_window.ui.calc_inv_content_clear_frame.findChildren(QPushButton, "delete")
        }

    def del_item(self, move_size_id, inventory_id):
        def wrap():
            for inventory in self.preset_inventory[move_size_id]["inventory"]:
                if inventory["inventory_id"] == inventory_id:
                    self.preset_inventory[move_size_id]["inventory"].remove(inventory)
                    break
            self.update_preset_inventory_cards(move_size_id)

        return wrap

    def update_preset_inventory(self, data, move_size_id):
        for inventory in self.preset_inventory[move_size_id]["inventory"]:
            if inventory["inventory_id"] == data["inventory_id"]:
                inventory["count"] += int(data["count"])
                return
        self.preset_inventory[move_size_id]["inventory"].append(data)

    def get_preset_inventory(self, move_details):
        self.preset_inventory.clear()
        for move_size in move_details["move_size"]:
            self.preset_inventory[move_size[1]] = {"move_size_name": move_size[0],
                                                   "inventory": self.inventory.get_response(
                                                       InventoryInventoryCollection,
                                                       {"move_size_id": move_size[1]})}

    def change_preset_inventory(self, button, move_size_id):
        def wrap():
            self.inventory.select_menu_point(button, is_preset=True)
            self.update_preset_inventory_cards(move_size_id)
            for frame in self.main_window.ui.calc_inv_content_clear_frame.findChildren(QFrame, "card_main_frame"):
                frame_id = frame.__getattribute__("move_size_id")
                if move_size_id != frame_id:
                    frame.setVisible(False)
                else:
                    frame.setVisible(True)

        return wrap

    def change_inside_page(self, is_all_inventory, page, button):
        self.main_window.calculator_page_ui.change_inside_page(is_all_inventory, button)
        self.main_window.ui.calc_size_menu.setCurrentWidget(page)

    def set_inventory(self, move_details):
        if self.set_all_inventory:
            room_collection = self.inventory.get_response(RoomCollection)
            self.inventory.set_left_menu(self.main_window.ui.calc_room_menu_frame,
                                         self.inventory.get_category_inventory,
                                         room_collection,
                                         self.add_item,
                                         is_preset_menu=False)
            self.set_all_inventory = False
        self.get_preset_inventory(move_details)
        self.inventory.set_calc_preset_menu(self.main_window.ui.calc_preset_menu_frame,
                                            self.preset_inventory,
                                            self.change_preset_inventory)
        self.inventory.assign_buttons(self.main_window.ui.calc_room_menu_frame,
                                      self.main_window.ui.calc_preset_menu_frame)

    def eventFilter(self, obj, event) -> bool:
        if obj is self.main_window.ui.calc_invnetory_check_page:
            if event.type() == QEvent.Show and self.main_window.change_page_data:
                self.change_inside_page(False, self.main_window.ui.calc_preset_page, self.inventory.first_butt_preset)
                return True
        return False
