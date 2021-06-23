from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QStyledItemDelegate


class UserProfile:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.ui.role_combobox.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        self.main_window.ui.role_combobox.setItemDelegate(QStyledItemDelegate())

    def set_profile(self, staff_profile=None):
        self.main_window.ui.role_combobox.clear()
        if staff_profile:
            name, role, email = self.set_staff_profile(staff_profile)
        else:
            name, role, email = self.set_main_user_profile()
        self.main_window.ui.profile_change_pass_butt.setVisible(True)
        self.main_window.ui.profile_change_email_butt.setVisible(True)
        self.main_window.ui.profile_new_pass_frame.setVisible(False)
        self.main_window.ui.profile_new_email_frame.setVisible(False)
        self.main_window.ui.profile_comp_name_input.setText(self.main_window.user.company["name"].capitalize())
        self.main_window.ui.profile_comp_address_1_input.setText(
            self.main_window.user.company["address"]["street"].title()
        )
        self.main_window.ui.profile_comp_address_2_input.setText(
            self.main_window.user.company["address"]["apartment"].title()
        )
        self.main_window.ui.profile_comp_city_input.setText(
            self.main_window.user.company["address"]["zip_code"]["city"].title()
        )
        self.main_window.ui.profile_comp_state_input.setText(
            self.main_window.user.company["address"]["zip_code"]["state"].title()
        )
        self.main_window.ui.profile_comp_zip_code_input.setText(
            self.main_window.user.company["address"]["zip_code"]["zip_code"]
        )
        self.main_window.ui.profile_pass_input.setText("")
        self.main_window.ui.profile_new_pass_input.setText("")
        self.main_window.ui.profile_new_pass2_input.setText("")
        self.main_window.ui.profile_user_name.setText(name)
        self.main_window.ui.profile_role_label.setText(role)
        self.main_window.ui.profile_name_input.setText(name)
        self.main_window.ui.profile_email_field.setText(email)
        self.main_window.ui.profile_new_email_input.setText("")

    def set_staff_profile(self, staff_profile):
        name = staff_profile["fullname"]
        role = staff_profile["user_role"]["role"].capitalize()
        email = staff_profile["email"]
        self.main_window.ui.profile_comp_name_input.setEnabled(False)
        self.main_window.ui.profile_comp_address_1_input.setEnabled(False)
        self.main_window.ui.profile_comp_address_2_input.setEnabled(False)
        self.main_window.ui.profile_comp_city_input.setEnabled(False)
        self.main_window.ui.profile_comp_state_input.setEnabled(False)
        self.main_window.ui.profile_comp_zip_code_input.setEnabled(False)
        self.main_window.ui.profile_small_header.setText(name)
        self.main_window.ui.profile_log_out_butt.setVisible(False)
        self.main_window.ui.profile_delete_butt.setVisible(True)
        self.main_window.ui.profile_user_manage_butt.setVisible(True)
        self.main_window.ui.role_combobox.setEnabled(True)
        self.main_window.ui.role_combobox.addItem(staff_profile["user_role"]["role"].capitalize(),
                                                  staff_profile["user_role_id"])
        for allowed_role in self.main_window.user_role.children_roles:
            self.main_window.ui.role_combobox.addItem(allowed_role["role"].capitalize(), allowed_role["id"])
        return name, role, email

    def set_main_user_profile(self):
        name = self.main_window.user.fullname
        role = self.main_window.user.user_role["role"].capitalize()
        role_id = self.main_window.user.user_role["id"]
        email = self.main_window.user.email.capitalize()
        self.main_window.ui.profile_small_header.setText("My profile")
        self.main_window.ui.profile_log_out_butt.setVisible(True)
        self.main_window.ui.profile_delete_butt.setVisible(False)
        self.main_window.ui.profile_user_manage_butt.setVisible(False)
        self.main_window.ui.role_combobox.addItem(role, role_id)
        self.main_window.ui.role_combobox.setEnabled(False)
        if self.main_window.user.user_role["role"] == "owner":
            self.main_window.ui.profile_comp_name_input.setEnabled(True)
            self.main_window.ui.profile_comp_address_1_input.setEnabled(True)
            self.main_window.ui.profile_comp_address_2_input.setEnabled(True)
            self.main_window.ui.profile_comp_city_input.setEnabled(True)
            self.main_window.ui.profile_comp_state_input.setEnabled(True)
            self.main_window.ui.profile_comp_zip_code_input.setEnabled(True)
        return name, role, email
