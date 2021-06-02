from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCursor
from PyQt5.QtWidgets import QStyledItemDelegate, QPushButton


class InventoryPageUi:
    def __init__(self, main_window):
        self.main_window = main_window
        # self.main_window.ui.asset_type_combobox.view().window().setWindowFlags(
        #     Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        # )
        # self.main_window.ui.asset_type_combobox.setItemDelegate(QStyledItemDelegate())

    def change_page_selector_style(self, is_all_inventory):
        self.main_window.ui.inventory_all_menu_butt.setProperty("selected", is_all_inventory)
        self.main_window.ui.inventory_all_menu_butt.setStyle(self.main_window.ui.inventory_all_menu_butt.style())
        self.main_window.ui.inventory_preset_choose_butt.setProperty("selected", not is_all_inventory)
        self.main_window.ui.inventory_preset_choose_butt.setStyle(
            self.main_window.ui.inventory_preset_choose_butt.style()
        )
        self.main_window.ui.inventory_preset_choose_line.setVisible(not is_all_inventory)
        self.main_window.ui.inventory_all_menu_line.setVisible(is_all_inventory)
        self.main_window.ui.inventory_add_butt.setVisible(is_all_inventory)
        self.main_window.ui.inventory_save_butt.setVisible(not is_all_inventory)

    def set_left_menu(self, frame, layout):
        for _ in range(10):
            room_menu_butt = QPushButton(frame)
            room_menu_butt.setMinimumSize(QSize(208, 54))
            room_menu_butt.setMaximumSize(QSize(208, 54))
            room_menu_butt.setCursor(QCursor(Qt.PointingHandCursor))
            room_menu_butt.setIconSize(QSize(20, 20))
            room_menu_butt.setCheckable(True)
            room_menu_butt.setText("  All Items")
            room_menu_butt.setIcon(QIcon(":/image/custom_item_icon.svg"))
            layout.addWidget(room_menu_butt)

