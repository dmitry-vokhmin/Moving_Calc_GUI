from PyQt5.QtGui import QColor, QCursor
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QComboBox, QStyledItemDelegate, QHBoxLayout, QPushButton, QLineEdit, QLabel


class CalculatorPageUi:
    def __init__(self, main_window):
        self.main_window = main_window
        self.set_combo_boxes()

    def set_combo_boxes(self):
        for combobox in self.main_window.ui.calc_general_info_frame.findChildren(QComboBox):
            combobox.view().window().setWindowFlags(
                Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
            )
            combobox.setItemDelegate(QStyledItemDelegate())

    def reset_pages(self):
        for input_field in self.main_window.ui.calc_zip_code_frame.findChildren(QLineEdit):
            input_field.setText("")
        for input_field in self.main_window.ui.calc_result_cus_info_frame.findChildren(QLineEdit):
            input_field.setText("")
        for combobox in self.main_window.ui.calc_general_info_frame.findChildren(QComboBox):
            combobox.setCurrentIndex(0)
        self.main_window.ui.calc_start_date_edit.setDate(QDate.currentDate())
        for label in self.main_window.ui.calc_menu_step_frame.findChildren(QLabel):
            label.setProperty("next", False)
            label.setStyle(label.style())
            label.setProperty("selected", False)
            label.setStyle(label.style())

    def set_calc_result(self, data):
        self.main_window.ui.calc_result_crew_size_info.setText(f"{data['crew_size']} movers")
        self.main_window.ui.calc_result_truck_size_info.setText(f"{data['truck_size']} ft truck")
        self.main_window.ui.calc_result_travel_time_info.setText(f"{data['travel_time']} minutes")
        self.main_window.ui.calc_result_hr_info.setText(f"{data['hourly_rate']}/hr")
        self.main_window.ui.calc_result_est_info.setText(
            f"{int(data['estimated_job_time'][0] // 1)} Hrs {int((data['estimated_job_time'][0] % 1) * 60)} Min - "
            f"{int(data['estimated_job_time'][1] // 1)} Hrs {int((data['estimated_job_time'][1] % 1) * 60)} Min"
        )
        self.main_window.ui.calc_result_quote_info.setText(
            f"${data['estimated_quote'][0]} - ${data['estimated_quote'][1]}"
        )

    def set_move_details_calc_result_page(self, data):
        self.main_window.ui.calc_result_details_date_info.setText(data["move_date"].strftime("%B %d, %Y"))
        self.main_window.ui.calc_result_details_zip_from_info.setText(data["zip_code_from"])
        self.main_window.ui.calc_result_details_zip_to_info.setText(data["zip_code_to"])
        self.main_window.ui.calc_result_details_size_info.setText(
            "; ".join([move_size[0] for move_size in data["move_size"]])
        )
        self.main_window.ui.calc_result_details_ent_from_info.setText(data["floor_collection_from"][0])
        self.main_window.ui.calc_result_details_ent_to_info.setText(data["floor_collection_to"][0])

    def build_calendars(self):
        calendar = self.main_window.calendar_ui.build_calendar("#F9FAFB", "#070808", "16px", QColor(Qt.black), False)
        self.main_window.ui.calc_calendar_layout2.addWidget(calendar)
        pop_up_calendar = self.main_window.calendar_ui.build_calendar("#0915CC", "#FFFFFF", "14px", QColor(Qt.blue),
                                                                      True)
        self.main_window.ui.calc_start_date_edit.setCalendarWidget(pop_up_calendar)
        self.main_window.ui.calc_start_date_edit.setDate(QDate.currentDate())
        return calendar

    def set_top_menu(self, sign_1, line, sing_2, is_current_page):
        sign_1.setProperty("next", is_current_page)
        sign_1.setStyle(sign_1.style())
        line.setProperty("selected", is_current_page)
        line.setStyle(line.style())
        sing_2.setProperty("selected", is_current_page)
        sing_2.setStyle(sing_2.style())

    def back_btn_visible(self, is_visible):
        self.main_window.ui.calc_back_btn.setVisible(is_visible)

    def set_move_details_page(self, funk):
        self.main_window.ui.calc_sevice_type.setEnabled(False)
        self.main_window.delete_layout(self.main_window.ui.calc_extra_room_btn_frame.layout())
        layout = QHBoxLayout(self.main_window.ui.calc_extra_room_btn_frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        for move_size in self.main_window.move_size.move_sizes:
            if move_size["is_extra"]:
                self.set_extra_rooms(move_size, self.main_window.ui.calc_extra_room_btn_frame, layout, funk)
            else:
                self.main_window.ui.calc_1_move_size_box.addItem(move_size["name"].title().replace("_", " "),
                                                                 move_size["id"])
        for floor in self.main_window.floor_collection.floor_collections:
            self.main_window.ui.calc_1_entrance_from_box.addItem(floor["name"].title().replace("_", " "), floor["id"])
            self.main_window.ui.calc_1_entrance_to_box.addItem(floor["name"].title().replace("_", " "), floor["id"])

    def set_extra_rooms(self, extra_room, frame, layout, funk):
        btn = QPushButton(frame)
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.setCheckable(True)
        btn.setText(extra_room["name"].title().replace("_", " "))
        btn.__setattr__("id", extra_room["id"])
        btn.clicked.connect(funk)
        layout.addWidget(btn)

    def change_inside_page(self, is_all_inventory, button):
        self.main_window.ui.calc_all_menu_butt.setProperty("selected", is_all_inventory)
        self.main_window.ui.calc_all_menu_butt.setStyle(self.main_window.ui.calc_all_menu_butt.style())
        self.main_window.ui.calc_preset_choose_butt.setProperty("selected", not is_all_inventory)
        self.main_window.ui.calc_preset_choose_butt.setStyle(
            self.main_window.ui.calc_preset_choose_butt.style()
        )
        self.main_window.ui.calc_preset_choose_line.setVisible(not is_all_inventory)
        self.main_window.ui.calc_all_menu_line.setVisible(is_all_inventory)
        self.main_window.ui.calc_inv_categor_frame.setVisible(is_all_inventory)
        button.click()
