from PyQt5.QtWidgets import QWidget, QPushButton
from PyQt5.QtCore import QEvent
from PyQt5.QtGui import QIcon
from controller.validator import validation
from controller.content_window.calculator.calc_inventory_check_page import CalcInventoryCheckPage
from controller.content_window.calculator.calc_personal_info_page import CalcPersonalInfoPage
from model.calculator import Calculator


class CalculatorPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.inventory_check_page = CalcInventoryCheckPage(main_window)
        self.personal_info_page = CalcPersonalInfoPage(main_window, self)
        self.set_page = True
        self.set_preset_inventory = True
        self.current_page = 0
        self.calc_result = None
        self.extra_room_btn = set()
        self.calendar = None
        self.validation = validation.Validation()
        self.inner_pages = [
            self.main_window.ui.calc_move_detail_page,
            self.main_window.ui.calc_invnetory_check_page,
            self.main_window.ui.calc_calculation_result_page,
            self.main_window.ui.calc_result_customer_info_page,
        ]
        self.extra_rooms = {"1 bedroom apartment", "room", "studio", "2 bedroom apartment"}
        self.move_details = None
        self.move_details_fields = {
            "zip_from": {
                "fields": (self.main_window.ui.calc_zip_from_input, self.main_window.ui.error_calc_zip_from),
                "validator": validation.ZipValidation
            },
            "zip_to": {
                "fields": (self.main_window.ui.calc_zip_to_input, self.main_window.ui.error_calc_zip_to),
                "validator": validation.ZipValidation
            },
        }
        self.main_window.ui.calculator_page.installEventFilter(self)
        self.main_window.ui.calc_reset_btn.installEventFilter(self)
        self.main_window.ui.calc_1_move_size_box.currentTextChanged.connect(self.show_extra_rooms)
        self.main_window.ui.calc_next_btn.clicked.connect(lambda: self.change_inner_page(self.current_page + 1))
        self.main_window.ui.calc_back_btn.clicked.connect(lambda: self.change_inner_page(self.current_page - 1))
        self.main_window.ui.calc_reset_btn.clicked.connect(
            lambda: self.main_window.modal_window.show_confirm_dialog(
                self.reset_pages,
                desc_text="reset? "
                          "The changes you made have not been submitted yet. All data will be lost when you reset.",
                btn_text="reset")
        )
        self.main_window.ui.calc_result_cus_info_submit_btn.clicked.connect(
            lambda: self.personal_info_page.submit_form(self.move_details,
                                                        self.inventory_check_page.preset_inventory,
                                                        self.calc_result)
        )
        self.set_field_validation()

    def set_event_filter(self):
        for button in self.main_window.ui.calc_extra_room_btn_frame.findChildren(QPushButton):
            self.extra_room_btn.add(button)
            button.installEventFilter(self)

    def set_field_validation(self):
        for field in self.move_details_fields.values():
            field["fields"][0].setValidator(field["validator"](*field["fields"]))

    def reset_pages(self):
        self.main_window.calculator_page_ui.reset_pages()
        self.change_next_btn(lambda: self.change_inner_page(self.current_page + 1), "Continue ")
        self.validation.reset_error_fields(self.move_details_fields)
        self.change_inner_page(0)

    def show_extra_rooms(self, text):
        if text.lower() in self.extra_rooms:
            self.main_window.ui.calc_extra_room_frame.setVisible(True)
        else:
            self.main_window.ui.calc_extra_room_frame.setVisible(False)
            for btn in self.main_window.ui.calc_extra_room_btn_frame.findChildren(QPushButton):
                btn.setChecked(False)
        if not self.set_preset_inventory:
            self.set_preset_inventory = True

    def extra_room_inventory(self):
        if not self.set_preset_inventory:
            self.set_preset_inventory = True

    def save_move_details(self):
        self.move_details = {
            "move_date": self.main_window.ui.calc_start_date_edit.date().toPyDate(),
            "zip_code_from": self.main_window.ui.calc_zip_from_input.text(),
            "zip_code_to": self.main_window.ui.calc_zip_to_input.text(),
            "move_size": self.get_move_size(),
            "floor_collection_from": self.get_floor_collection(self.main_window.ui.calc_1_entrance_from_box),
            "floor_collection_to": self.get_floor_collection(self.main_window.ui.calc_1_entrance_to_box)
        }

    @staticmethod
    def get_floor_collection(field):
        return field.currentText(), field.currentData()

    def get_move_size(self):
        data = [(self.main_window.ui.calc_1_move_size_box.currentText(),
                 self.main_window.ui.calc_1_move_size_box.currentData())]
        for btn in self.main_window.ui.calc_extra_room_btn_frame.findChildren(QPushButton):
            if btn.isChecked():
                data.append((btn.text(), btn.__getattribute__("id")))
        return data

    def get_calculation_result(self):
        new_preset_inventory = {str(key): value for key, value in self.inventory_check_page.preset_inventory.items()}
        new_preset_inventory.update(self.move_details)
        new_preset_inventory["move_date"] = self.move_details["move_date"].isoformat()
        calculator_api = Calculator(**new_preset_inventory)
        response_code, response_data = calculator_api.post()
        if response_code > 399:
            self.main_window.modal_window.show_notification_page(description=response_data, is_error=True)
        else:
            return response_data

    def set_calculation_result(self):
        self.calc_result = self.get_calculation_result()
        if self.calc_result:
            self.main_window.calculator_page_ui.set_calc_result(self.calc_result)
            self.main_window.calculator_page_ui.set_move_details_calc_result_page(self.move_details)

    def change_inner_page(self, current_page):
        self.current_page = current_page
        if current_page == 0:
            self.set_move_details_menu(self.inner_pages[current_page])
        elif current_page == 1:
            if self.validation.check_validation(self.move_details_fields):
                self.save_move_details()
                self.set_inventory_check_menu(self.inner_pages[current_page])
            else:
                self.current_page -= 1
        elif current_page == 2:
            self.set_calculation_result()
            self.set_calc_result_menu(self.inner_pages[current_page])
        elif current_page == 3:
            self.set_customer_info_menu(self.inner_pages[current_page])

    def set_customer_info_menu(self, page):
        self.main_window.calculator_page_ui.set_top_menu(
            self.main_window.ui.calc_3_sign,
            self.main_window.ui.calc_3_line,
            self.main_window.ui.calc_4_sign,
            is_current_page=True
        )
        self.change_next_btn(lambda: self.personal_info_page.submit_form(
            self.move_details,
            self.inventory_check_page.preset_inventory,
            self.calc_result
        ), "Submit Info ")
        self.main_window.ui.calc_result_pages.setCurrentWidget(page)

    def set_calc_result_menu(self, page):
        self.main_window.calculator_page_ui.set_top_menu(
            self.main_window.ui.calc_2_sign,
            self.main_window.ui.calc_2_line,
            self.main_window.ui.calc_3_sign,
            is_current_page=True
        )
        self.main_window.calculator_page_ui.set_top_menu(
            self.main_window.ui.calc_3_sign,
            self.main_window.ui.calc_3_line,
            self.main_window.ui.calc_4_sign,
            is_current_page=False
        )
        self.change_next_btn(lambda: self.change_inner_page(self.current_page + 1), "Continue ")
        self.main_window.ui.calc_menu_pages.setCurrentWidget(page)
        self.main_window.ui.calc_result_pages.setCurrentWidget(self.main_window.ui.calc_result_details_page)

    def set_inventory_check_menu(self, page):
        self.main_window.calculator_page_ui.set_top_menu(
            self.main_window.ui.calc_1_sign,
            self.main_window.ui.calc_1_line,
            self.main_window.ui.calc_2_sign,
            is_current_page=True
        )
        self.main_window.calculator_page_ui.set_top_menu(
            self.main_window.ui.calc_2_sign,
            self.main_window.ui.calc_2_line,
            self.main_window.ui.calc_3_sign,
            is_current_page=False
        )
        self.change_preset_inventory()
        self.main_window.calculator_page_ui.back_btn_visible(True)
        self.main_window.ui.calc_menu_pages.setCurrentWidget(page)

    def set_move_details_menu(self, page):
        self.main_window.calculator_page_ui.set_top_menu(
            self.main_window.ui.calc_1_sign,
            self.main_window.ui.calc_1_line,
            self.main_window.ui.calc_2_sign,
            is_current_page=False
        )
        self.main_window.calculator_page_ui.back_btn_visible(False)
        self.main_window.ui.calc_menu_pages.setCurrentWidget(page)

    def change_preset_inventory(self):
        if self.set_preset_inventory:
            self.inventory_check_page.set_inventory(self.move_details)
            self.set_preset_inventory = False

    def change_next_btn(self, funk, text):
        self.main_window.ui.calc_next_btn.setText(text)
        self.main_window.ui.calc_next_btn.clicked.disconnect()
        self.main_window.ui.calc_next_btn.clicked.connect(funk)

    def build_calendar(self):
        self.calendar = self.main_window.calculator_page_ui.build_calendars()

    def eventFilter(self, obj, event) -> bool:
        if obj is self.main_window.ui.calculator_page:
            if event.type() == QEvent.Show and self.main_window.change_page_data:
                if self.set_page:
                    self.main_window.calculator_page_ui.set_move_details_page(self.extra_room_inventory)
                    self.build_calendar()
                    self.set_event_filter()
                    self.set_page = False
                self.validation.reset_error_fields(self.move_details_fields)
                self.reset_pages()
                self.main_window.set_calendar(self.calendar)
                return True
            if event.type() == QEvent.Hide:
                self.inventory_check_page.set_all_inventory = True
                return True
        if obj is self.main_window.ui.calc_reset_btn:
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/inventory_reset_hover.svg"))
                return True
            if event.type() == QEvent.HoverLeave:
                obj.setIcon(QIcon(":/image/inventory_reset_default.svg"))
                return True
        if obj in self.extra_room_btn:
            if event.type() == QEvent.HoverEnter:
                obj.setIcon(QIcon(":/image/check_icon_hover.svg"))
                return True
            if event.type() == QEvent.HoverLeave and not obj.isChecked():
                obj.setIcon(QIcon(":/image/check_icon_default.svg"))
                return True
        return False
