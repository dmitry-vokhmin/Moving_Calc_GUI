from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QIcon
from model.truck.truck import Truck
from controller.validator import validation
from model.truck.truck_type import TruckType


class AssetPage(QDialog):
    def __init__(self, main_modal_window):
        QDialog.__init__(self, main_modal_window)
        self.main_modal_window = main_modal_window
        self.validator = validation.Validation()
        self.fields = {
            "name": {
                "fields": (self.main_modal_window.ui.asset_name_input,
                           self.main_modal_window.ui.error_asset_name)
            },
        }
        self.main_modal_window.ui.cancel_asset_butt.clicked.connect(self.main_modal_window.reject)
        self.main_modal_window.ui.asset_add_asset_type.clicked.connect(self.change_page_to_asset_type)
        self.main_modal_window.ui.asset_name_input.setValidator(
            validation.EmptyStrValidation(*self.fields["name"]["fields"])
        )
        self.main_modal_window.ui.asset_add_asset_type.installEventFilter(self)
        self.main_modal_window.ui.asset_page.installEventFilter(self)

    def change_page_to_asset_type(self):
        self.main_modal_window.asset_type_page.set_asset_page(asset_data=None)
        self.main_modal_window.ui.pages.setCurrentWidget(self.main_modal_window.ui.asset_type_page)

    def set_asset_page(self, asset_data):
        truck_type_data = self.main_modal_window.main_window.get_data(TruckType)
        if asset_data:
            self.main_modal_window.asset_page_ui.set_update_asset(truck_type_data,
                                                                  asset_data,
                                                                  self.update_asset,
                                                                  self.delete_asset)
        else:
            self.main_modal_window.asset_page_ui.set_add_asset(truck_type_data, self.add_new_asset)
        self.main_modal_window.open()

    def add_new_asset(self):
        if self.validator.check_validation(self.fields):
            data = self.get_data()
            truck_api = Truck(**data)
            response_code, response_data = truck_api.post()
            self.show_notification(response_code,
                                   response_data,
                                   title="Asset was added",
                                   description=f"Asset {data['name']} was added to the pipeline"
                                   )

    def update_asset(self, asset_data):
        if self.validator.check_validation(self.fields):
            data = {"id": asset_data["id"]}
            data.update(self.get_data())
            truck_api = Truck(**data)
            response_code, response_data = truck_api.put()
            self.show_notification(response_code,
                                   response_data,
                                   title="Asset was updated",
                                   description=f"Asset {asset_data['name']} was updated successfully"
                                   )

    def delete_asset(self, asset_data):
        truck_api = Truck(**asset_data)
        response_code, response_data = truck_api.delete()
        self.show_notification(response_code,
                               response_data,
                               title="Asset was deleted",
                               description=f"Asset {asset_data['name']} was deleted successfully"
                               )

    def get_data(self):
        return {
            "name": self.main_modal_window.ui.asset_name_input.text(),
            "truck_type_id": self.main_modal_window.ui.asset_type_combobox.currentData()
        }

    def show_notification(self, response_code, response_data, title, description):
        if response_code > 399:
            self.main_modal_window.show_notification_page(
                description=response_data,
                is_error=True,
                previous_page=lambda: self.main_modal_window.ui.pages.setCurrentWidget(
                    self.main_modal_window.ui.asset_page
                )
            )
        else:
            self.main_modal_window.main_window.ui.equip_truck_page.setVisible(False)
            self.main_modal_window.main_window.ui.equip_truck_page.setVisible(True)
            self.main_modal_window.show_notification_page(title=title,
                                                          description=description,
                                                          is_error=False)

    def eventFilter(self, obj, event: QEvent) -> bool:
        if obj is self.main_modal_window.ui.asset_page:
            if event.type() == QEvent.Show:
                self.validator.reset_error_fields(self.fields)
                return True
        if obj is self.main_modal_window.ui.asset_add_asset_type:
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/round_plus_icon_hover.svg"))
                return True
            if event.type() == QEvent.HoverLeave:
                obj.setIcon(QIcon(":/image/round_plus_icon_default.svg"))
                return True
        return False
