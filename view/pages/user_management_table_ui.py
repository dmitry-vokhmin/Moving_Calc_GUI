from PyQt5.QtWidgets import QVBoxLayout, QFrame, QHBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QCursor


class UserManagementTable:
    def __init__(self, main_window):
        self.main_window = main_window

    def set_table(self, edit_funk, delete_funk):
        self.main_window.delete_layout(self.main_window.ui.user_manage_clear_frame.layout())
        user_manage_clear_layout = QVBoxLayout(self.main_window.ui.user_manage_clear_frame)
        user_manage_clear_layout.setContentsMargins(0, 0, 0, 0)
        user_manage_clear_layout.setSpacing(0)
        user_manage_clear_layout.setObjectName("user_manage_clear_layout")
        background_gray = True
        for user in self.main_window.company_users.users:
            frame = QFrame(self.main_window.ui.user_manage_clear_frame)
            if background_gray:
                frame.setStyleSheet("QFrame {\n"
                                    "    background: #F2F3F6;\n"
                                    "    border-radius: 4px;\n"
                                    "}")
            background_gray = not background_gray
            frame.setFrameShape(QFrame.NoFrame)
            frame.setMinimumSize(QSize(0, 54))
            horizontal_layout = QHBoxLayout(frame)
            horizontal_layout.setContentsMargins(0, 0, 0, 0)
            horizontal_layout.setSpacing(0)
            frame_2 = QFrame(frame)
            frame_2.setFrameShape(QFrame.NoFrame)
            horizontal_layout_2 = QHBoxLayout(frame_2)
            horizontal_layout_2.setContentsMargins(17, 0, 0, 0)
            horizontal_layout_2.setSpacing(7)
            icon = QLabel(frame_2)
            icon.setMinimumSize(QSize(20, 20))
            icon.setMaximumSize(QSize(20, 20))
            icon.setStyleSheet(" image: url(:/image/account_user_manage.svg);")
            icon.setText("")
            icon.setAlignment(Qt.AlignLeading | Qt.AlignLeft | Qt.AlignVCenter)
            horizontal_layout_2.addWidget(icon)
            fullname = QLabel(frame_2)
            fullname.setStyleSheet("color: #070808;")
            fullname.setText(user["fullname"])
            horizontal_layout_2.addWidget(fullname)
            horizontal_layout.addWidget(frame_2, 0, Qt.AlignLeft)
            email = QLabel(frame)
            email.setStyleSheet("color: #4E50FF;")
            email.setText(user["email"].capitalize())
            horizontal_layout.addWidget(email)
            role = QLabel(frame)
            role.setText(user["user_role"]["role"].title())
            horizontal_layout.addWidget(role)
            frame_3 = QFrame(frame)
            frame_3.setFrameShape(QFrame.NoFrame)
            horizontal_layout_3 = QHBoxLayout(frame_3)
            horizontal_layout_3.setContentsMargins(0, 0, 50, 0)
            horizontal_layout_3.setSpacing(10)
            edit_button = QPushButton(frame_3)
            edit_button.setMinimumSize(QSize(24, 24))
            edit_button.setMaximumSize(QSize(24, 24))
            edit_button.setCursor(QCursor(Qt.PointingHandCursor))
            edit_button.setStyleSheet("QPushButton {\n"
                                      " image: url(:/image/edit_icon_default.svg);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover {\n"
                                      " image: url(:/image/edit_icon_hover.svg);\n"
                                      "}\n"
                                      "")
            edit_button.setText("")
            edit_button.setIconSize(QSize(24, 24))
            edit_button.clicked.connect(edit_funk(user))
            horizontal_layout_3.addWidget(edit_button)
            delete_button = QPushButton(frame_3)
            delete_button.setMinimumSize(QSize(24, 24))
            delete_button.setMaximumSize(QSize(24, 24))
            delete_button.setCursor(QCursor(Qt.PointingHandCursor))
            delete_button.setStyleSheet("QPushButton {\n"
                                        " image: url(:/image/delete_acc_icon_default.svg);\n"
                                        "}\n"
                                        "\n"
                                        "QPushButton:hover {\n"
                                        " image: url(:/image/delete_acc_icon_hover.svg);\n"
                                        "}")
            delete_button.setText("")
            delete_button.setIconSize(QSize(24, 24))
            delete_button.clicked.connect(delete_funk(user))
            horizontal_layout_3.addWidget(delete_button)
            horizontal_layout.addWidget(frame_3, 0, Qt.AlignRight)
            horizontal_layout.setStretch(0, 4)
            horizontal_layout.setStretch(1, 2)
            horizontal_layout.setStretch(2, 1)
            horizontal_layout.setStretch(3, 1)
            user_manage_clear_layout.addWidget(frame)
            self.disable_button(user, edit_button, delete_button)

    def disable_button(self, user, edit_button, delete_button):
        user_role = user["user_role"]["role"]
        profile_role_privilege = self.main_window.user_role.children_roles
        if user["id"] == self.main_window.user.id:
            delete_button.setEnabled(False)
            delete_button.setStyleSheet("QPushButton {\n"
                                        " image: url(:/image/delete_acc_icon_locked.svg);\n"
                                        "}")
        elif user_role not in [allowed_role["role"] for allowed_role in profile_role_privilege]:
            delete_button.setEnabled(False)
            delete_button.setStyleSheet("QPushButton {\n"
                                        " image: url(:/image/delete_acc_icon_locked.svg);\n"
                                        "}")
            edit_button.setEnabled(False)
            delete_button.setStyleSheet("QPushButton {\n"
                                        " image: url(:/image/edit_icon_locked.svg);\n"
                                        "}")
