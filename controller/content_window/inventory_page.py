from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEvent


class InventoryPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.set_left_menu = True
        self.main_window.ui.inventory_all_menu_butt.clicked.connect(
            lambda: self.change_inside_page(True, self.main_window.ui.inventory_room_page)
        )
        self.main_window.ui.inventory_preset_choose_butt.clicked.connect(
            lambda: self.change_inside_page(False, self.main_window.ui.inventory_preset_page)
        )
        self.main_window.ui.inventory_page.installEventFilter(self)
        self.main_window.ui.inventory_save_butt.clicked.connect(self.update_preset)
        self.main_window.ui.inventory_add_butt.clicked.connect(self.main_window.modal_window.show_inventory_item_page)

    def change_inside_page(self, is_all_inventory, page):
        self.main_window.inventory_ui.change_page_selector_style(is_all_inventory)
        self.main_window.ui.inventory_size_menu.setCurrentWidget(page)

    def update_preset(self):
        pass

    def eventFilter(self, obj, event) -> bool:
        if obj is self.main_window.ui.inventory_page:
            if event.type() == QEvent.Show:
                self.change_inside_page(True, self.main_window.ui.inventory_room_page,)
                if self.set_left_menu:
                    self.main_window.inventory_ui.set_left_menu(self.main_window.ui.inventory_room_menu_frame,
                                                                self.main_window.ui.inventory_room_menu_layout)
                    self.main_window.inventory_ui.set_left_menu(self.main_window.ui.inventory_preset_menu_frame,
                                                                self.main_window.ui.inventory_preset_menu_layout)
                    self.set_left_menu = False
                return True
        return False
