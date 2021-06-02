from PyQt5.QtWidgets import QPushButton, QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCursor


class MenuUI:
    def __init__(self, main_window):
        self.main_window = main_window

    def set_menu(self, data, page_mapper):
        menu = {}
        self.main_window.delete_layout(self.main_window.ui.menu_frame.layout())
        menu_layout = QHBoxLayout(self.main_window.ui.menu_frame)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(60)
        menu_layout.setObjectName("menu_layout")
        for privilege in data:
            menu_point = privilege["privilege"]
            menu[menu_point] = {}
            frame = QFrame(self.main_window.ui.menu_frame)
            frame.setFrameShape(QFrame.NoFrame)
            frame.setObjectName(f"frame_{menu_point}")
            layout = QVBoxLayout(frame)
            layout.setContentsMargins(0, 0, 0, 3)
            layout.setSpacing(0)
            layout.setObjectName(f"layout_{menu_point}")
            menu[menu_point]["layout"] = layout
            button = QPushButton(menu_point.replace("_", " ").title(), frame)
            button.setCursor(QCursor(Qt.PointingHandCursor))
            button.setCheckable(True)
            button.setObjectName(f"button_{menu_point}")
            menu[menu_point]["button"] = button
            layout.addWidget(button, 0, Qt.AlignVCenter)
            label = QLabel(frame)
            label.setMinimumSize(QSize(0, 3))
            label.setMaximumSize(QSize(16777215, 3))
            label.setText("")
            label.setVisible(False)
            label.setObjectName(f"label_{menu_point}")
            menu[menu_point]["label"] = label
            layout.addWidget(label)
            button.clicked.connect(page_mapper[menu_point])
            menu_layout.addWidget(frame)
        self.main_window.ui.profile_butt.setText(f" {self.main_window.user.fullname}")
        self.start_menu_point(menu)
        return menu

    @staticmethod
    def start_menu_point(menu):
        menu["calculator"]["button"].setProperty("selected", True)
        menu["calculator"]["label"].setVisible(True)
        menu["calculator"]["layout"].setContentsMargins(0, 0, 0, 0)

    @staticmethod
    def change_menu_button_style(ui_elem, is_active):
        label = ui_elem["label"]
        button = ui_elem["button"]
        layout = ui_elem["layout"]
        label.setVisible(is_active)
        layout.setContentsMargins(0, 0, 0, 0 if is_active else 3)
        button.setProperty("selected", is_active)
        button.setStyle(button.style())

    def change_profile_butt(self, is_selected):
        button = self.main_window.ui.profile_butt
        button.setProperty("selected", is_selected)
        button.setStyle(button.style())
        if is_selected:
            button.setIcon(QIcon(":/image/account_active@2x.svg"))
        else:
            button.setIcon(QIcon(":/image/account@2x.svg"))
