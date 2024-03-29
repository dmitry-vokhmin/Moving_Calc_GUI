from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QEvent
from model.truck.truck_type import TruckType
from model.truck.truck import Truck


class EquipmentPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.main_window.ui.equip_asset_butt.clicked.connect(
            lambda: self.change_inside_page(True, self.main_window.ui.equip_truck_page)
        )
        self.main_window.ui.equip_asset_type_butt.clicked.connect(
            lambda: self.change_inside_page(False, self.main_window.ui.equip_truck_type_page)
        )
        self.main_window.ui.equip_new_asset_butt.clicked.connect(self.main_window.modal_window.show_asset_page)
        self.main_window.ui.equip_new_asset_type_butt.clicked.connect(self.main_window.modal_window.show_asset_type_page)
        self.main_window.ui.equipment_page.installEventFilter(self)
        self.main_window.ui.equip_truck_page.installEventFilter(self)
        self.main_window.ui.equip_truck_type_page.installEventFilter(self)

    def set_truck_cards(self, truck_data):
        self.main_window.equipment_card.set_truck_cards(
            truck_data,
            self.update_asset,
            self.main_window.modal_window.show_asset_page
        )

    def set_truck_type_cards(self, truck_type_data):
        self.main_window.equipment_card.set_truck_type_cards(
            truck_type_data,
            self.update_asset_type,
            self.main_window.modal_window.show_asset_type_page
        )

    def change_inside_page(self, is_truck_line, page):
        self.main_window.ui.equip_asset_type_line.setVisible(not is_truck_line)
        self.main_window.ui.equip_asset_line.setVisible(is_truck_line)
        self.main_window.ui.equip_truck_pages.setCurrentWidget(page)

    def update_asset(self, asset_data):
        def wrap():
            self.main_window.modal_window.show_asset_page(asset_data)
        return wrap

    def update_asset_type(self, asset_data):
        def wrap():
            self.main_window.modal_window.show_asset_type_page(asset_data)
        return wrap

    def truck_table_update(self):
        truck_data = self.main_window.get_data(Truck)
        self.set_truck_cards(truck_data)
        self.main_window.ui.equip_asset_butt.setText(f"All Assets ({len(truck_data)})")

    def truck_type_table_update(self):
        truck_type_data = self.main_window.get_data(TruckType)
        self.set_truck_type_cards(truck_type_data)
        self.main_window.ui.equip_asset_type_butt.setText(f"Asset Type ({len(truck_type_data)})")

    def eventFilter(self, obj, event) -> bool:
        if obj is self.main_window.ui.equipment_page:
            if event.type() == QEvent.Show and self.main_window.change_page_data:
                self.change_inside_page(True, self.main_window.ui.equip_truck_page)
                self.truck_type_table_update()
                return True
        if obj is self.main_window.ui.equip_truck_page:
            if event.type() == QEvent.Show and self.main_window.change_page_data:
                self.truck_table_update()
                return True
        elif obj is self.main_window.ui.equip_truck_type_page:
            if event.type() == QEvent.Show and self.main_window.change_page_data:
                self.truck_type_table_update()
                return True
        return False
