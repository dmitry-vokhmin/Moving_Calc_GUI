from view.custom_widgets.flow_layout import FlowLayout
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QPushButton, QSizePolicy, QSpacerItem


class EquipmentCard:
    def __init__(self, main_window):
        self.main_window = main_window

    def set_truck_cards(self, truck_data, update_funk, add_new_funk):
        self.main_window.delete_layout(self.main_window.ui.equip_truck_main_frame.layout())
        flow_layout = FlowLayout(self.main_window.ui.equip_truck_main_frame)
        flow_layout.setContentsMargins(0, 0, 0, 0)
        for truck in truck_data:
            card_frame = QFrame(self.main_window.ui.equip_truck_main_frame)
            card_frame.setMinimumSize(QSize(324, 108))
            card_frame.setMaximumSize(QSize(324, 108))
            card_frame.setStyleSheet(".QFrame {\n"
                                     "    border: 0.5px solid rgba(181, 184, 199, 0.5);\n"
                                     "    border-radius: 10px;\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton {\n"
                                     "    background: transparent;\n"
                                     "    image: url(:/image/equip_edit_default.svg);\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover {\n"
                                     " image: url(:/image/equip_edit_hover.svg);\n"
                                     "}\n"
                                     "")
            card_frame.setFrameShape(QFrame.NoFrame)
            card_frame.setFrameShadow(QFrame.Raised)
            main_layout = QHBoxLayout(card_frame)
            main_layout.setContentsMargins(15, 15, 15, 15)
            main_layout.setSpacing(15)
            truck_icon = QLabel(card_frame)
            truck_icon.setMinimumSize(QSize(60, 60))
            truck_icon.setMaximumSize(QSize(60, 60))
            truck_icon.setStyleSheet("image: url(:/image/equip_truck.svg);")
            truck_icon.setText("")
            main_layout.addWidget(truck_icon, 0, Qt.AlignLeft | Qt.AlignTop)
            truck_description_frame = QFrame(card_frame)
            truck_description_frame.setStyleSheet("border: none;")
            truck_description_frame.setFrameShape(QFrame.NoFrame)
            truck_description_frame.setFrameShadow(QFrame.Raised)
            truck_description_layout = QVBoxLayout(truck_description_frame)
            truck_description_layout.setContentsMargins(0, 0, 0, 0)
            truck_description_layout.setSpacing(0)
            truck_name = QLabel(truck_description_frame)
            truck_name.setStyleSheet("color: #070808;\n"
                                     "font-size: 16px;\n"
                                     "margin-bottom: 4px;")
            truck_name.setAlignment(Qt.AlignJustify | Qt.AlignVCenter)
            truck_name.setText(truck["name"].capitalize())
            truck_description_layout.addWidget(truck_name)
            truck_length = QLabel(truck_description_frame)
            truck_length.setMinimumSize(QSize(80, 22))
            truck_length.setStyleSheet("background: #F2F3F6;\n"
                                       "border-radius: 4px;\n"
                                       "font-size: 14px;\n"
                                       "color: #757C9F;")
            truck_length.setAlignment(Qt.AlignCenter)
            truck_length.setText(truck["truck_type"]["name"].capitalize())
            truck_description_layout.addWidget(truck_length, 0, Qt.AlignLeft)
            sq_feet_frame = QFrame(truck_description_frame)
            sq_feet_frame.setFrameShape(QFrame.NoFrame)
            sq_feet_frame.setFrameShadow(QFrame.Raised)
            sq_feet_layout = QHBoxLayout(sq_feet_frame)
            sq_feet_layout.setContentsMargins(0, 10, 0, 0)
            sq_feet_layout.setSpacing(4)
            sq_feet_icon = QLabel(sq_feet_frame)
            sq_feet_icon.setMinimumSize(QSize(12, 12))
            sq_feet_icon.setStyleSheet("image: url(:/image/sq_feet_icon.svg);")
            sq_feet_icon.setText("")
            sq_feet_layout.addWidget(sq_feet_icon)
            sq_feet = QLabel(sq_feet_frame)
            sq_feet.setStyleSheet("color: #757C9F;\n"
                                  "font-size: 14px;")
            sq_feet.setText(f"Sq. Feet: {truck['truck_type']['dimension']} ft<sup>2</sup>")
            sq_feet_layout.addWidget(sq_feet)
            truck_description_layout.addWidget(sq_feet_frame)
            main_layout.addWidget(truck_description_frame, 0, Qt.AlignTop)
            edit_truck_butt = QPushButton(card_frame)
            edit_truck_butt.setMinimumSize(QSize(24, 24))
            edit_truck_butt.setMaximumSize(QSize(24, 24))
            edit_truck_butt.clicked.connect(update_funk(truck))
            edit_truck_butt.setText("")
            main_layout.addWidget(edit_truck_butt, 0, Qt.AlignRight | Qt.AlignTop)
            flow_layout.addWidget(card_frame)
        add_truck_butt = QPushButton(self.main_window.ui.equip_truck_main_frame)
        add_truck_butt.setMinimumSize(QSize(324, 108))
        add_truck_butt.setStyleSheet("QPushButton {\n"
                                     "    background: transparent;\n"
                                     "    image: url(:/image/new_asset_default.svg);\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover {\n"
                                     "    image: url(:/image/new_asset_hover.svg);\n"
                                     "}")
        add_truck_butt.setText("")
        add_truck_butt.clicked.connect(add_new_funk)
        flow_layout.addWidget(add_truck_butt)

    def set_truck_type_cards(self, truck_type_data, update_funk, add_new_funk):
        self.main_window.delete_layout(self.main_window.ui.equip_truck_type_main_frame.layout())
        flow_layout = FlowLayout(self.main_window.ui.equip_truck_type_main_frame)
        flow_layout.setContentsMargins(0, 0, 0, 0)
        for truck_type in truck_type_data:
            equip_truck_type_main_frame = QFrame(self.main_window.ui.equip_truck_type_main_frame)
            equip_truck_type_main_frame.setMinimumSize(QSize(324, 128))
            equip_truck_type_main_frame.setMaximumSize(QSize(324, 128))
            equip_truck_type_main_frame.setStyleSheet(".QFrame {\n"
                                                      "    border: 0.5px solid rgba(181, 184, 199, 0.5);\n"
                                                      "    border-radius: 10px;\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton {\n"
                                                      "    background: transparent;\n"
                                                      "    image: url(:/image/equip_edit_default.svg);\n"
                                                      "}\n"
                                                      "\n"
                                                      "QPushButton:hover {\n"
                                                      " image: url(:/image/equip_edit_hover.svg);\n"
                                                      "}\n"
                                                      "")
            equip_truck_type_main_frame.setFrameShape(QFrame.NoFrame)
            equip_truck_type_main_frame.setFrameShadow(QFrame.Raised)
            equip_truck_type_main_layout = QVBoxLayout(equip_truck_type_main_frame)
            equip_truck_type_main_layout.setContentsMargins(15, 15, 15, 15)
            equip_truck_type_main_layout.setSpacing(0)
            inside_vert_frame = QFrame(equip_truck_type_main_frame)
            inside_vert_frame.setStyleSheet("border: none;")
            inside_vert_frame.setFrameShape(QFrame.NoFrame)
            inside_vert_frame.setFrameShadow(QFrame.Raised)
            inside_vert_layout = QHBoxLayout(inside_vert_frame)
            inside_vert_layout.setContentsMargins(0, 0, 0, 0)
            inside_vert_layout.setSpacing(15)
            truck_icon = QLabel(inside_vert_frame)
            truck_icon.setMinimumSize(QSize(60, 60))
            truck_icon.setMaximumSize(QSize(60, 60))
            truck_icon.setStyleSheet("image: url(:/image/equip_truck.svg);")
            truck_icon.setText("")
            inside_vert_layout.addWidget(truck_icon)
            inside_top_frame = QFrame(inside_vert_frame)
            inside_top_frame.setStyleSheet("border: none;")
            inside_top_frame.setFrameShape(QFrame.NoFrame)
            inside_top_frame.setFrameShadow(QFrame.Raised)
            inside_top_layout = QVBoxLayout(inside_top_frame)
            inside_top_layout.setContentsMargins(0, 0, 0, 0)
            inside_top_layout.setSpacing(4)
            truck_type_label = QLabel(inside_top_frame)
            truck_type_label.setStyleSheet("color: #070808;\n"
                                           "font-size: 16px;\n"
                                           "margin-bottom: 4px;")
            truck_type_label.setAlignment(Qt.AlignJustify | Qt.AlignVCenter)
            truck_type_label.setText(truck_type["name"].capitalize())
            inside_top_layout.addWidget(truck_type_label)
            sq_feet_frame = QFrame(inside_top_frame)
            sq_feet_frame.setMinimumSize(QSize(0, 22))
            sq_feet_frame.setStyleSheet("background: #F2F3F6;\n"
                                        "border-radius: 4px;")
            sq_feet_frame.setFrameShape(QFrame.NoFrame)
            sq_feet_frame.setFrameShadow(QFrame.Raised)
            sq_feet_layout = QHBoxLayout(sq_feet_frame)
            sq_feet_layout.setContentsMargins(8, 0, 6, 0)
            sq_feet_layout.setSpacing(4)
            sq_feet_icon = QLabel(sq_feet_frame)
            sq_feet_icon.setMinimumSize(QSize(13, 13))
            sq_feet_icon.setStyleSheet("image: url(:/image/sq_feet_icon.svg);")
            sq_feet_icon.setText("")
            sq_feet_layout.addWidget(sq_feet_icon)
            sq_feet = QLabel(sq_feet_frame)
            sq_feet.setStyleSheet("color: #757C9F;\n"
                                  "font-size: 14px;")
            sq_feet.setText(f'{truck_type["dimension"]} ft<sup>2</sup>')
            sq_feet_layout.addWidget(sq_feet)
            inside_top_layout.addWidget(sq_feet_frame, 0, Qt.AlignLeft | Qt.AlignTop)
            spacer = QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Fixed)
            inside_top_layout.addItem(spacer)
            inside_vert_layout.addWidget(inside_top_frame)
            edit_truck_butt = QPushButton(inside_vert_frame)
            edit_truck_butt.setMinimumSize(QSize(22, 22))
            edit_truck_butt.setMaximumSize(QSize(22, 22))
            edit_truck_butt.clicked.connect(update_funk(truck_type))
            edit_truck_butt.setText("")
            inside_vert_layout.addWidget(edit_truck_butt, 0, Qt.AlignTop | Qt.AlignRight)
            equip_truck_type_main_layout.addWidget(inside_vert_frame)
            inside_bottom_frame = QFrame(equip_truck_type_main_frame)
            inside_bottom_frame.setFrameShape(QFrame.NoFrame)
            inside_bottom_frame.setFrameShadow(QFrame.Raised)
            inside_bottom_frame.setStyleSheet("QFrame {\n"
                                              "    border: none;\n"
                                              "}\n"
                                              "\n"
                                              "QLabel {\n"
                                              "color: #757C9F;\n"
                                              "font-size: 14px;\n"
                                              "}\n")
            inside_bottom_layout = QVBoxLayout(inside_bottom_frame)
            inside_bottom_layout.setContentsMargins(77, 0, 0, 0)
            inside_bottom_layout.setSpacing(0)
            width_height_frame = QFrame(inside_bottom_frame)
            width_height_frame.setFrameShape(QFrame.NoFrame)
            width_height_frame.setFrameShadow(QFrame.Raised)
            width_heigth_layout = QHBoxLayout(width_height_frame)
            width_heigth_layout.setContentsMargins(0, 0, 0, 0)
            width_heigth_layout.setSpacing(4)
            width_icon = QLabel(width_height_frame)
            width_icon.setMinimumSize(QSize(12, 12))
            width_icon.setStyleSheet("image: url(:/image/width_icon.svg);")
            width_icon.setText("")
            width_heigth_layout.addWidget(width_icon)
            width = QLabel(width_height_frame)
            width.setStyleSheet("margin-right: 12px;")
            width.setAlignment(Qt.AlignJustify | Qt.AlignVCenter)
            width.setText(f"Width: {truck_type['width'] or ''}")
            width_heigth_layout.addWidget(width)
            height_icon = QLabel(width_height_frame)
            height_icon.setMinimumSize(QSize(12, 12))
            height_icon.setStyleSheet("image: url(:/image/length_icon.svg);")
            height_icon.setText("")
            width_heigth_layout.addWidget(height_icon)
            height = QLabel(width_height_frame)
            height.setText(f"Height: {truck_type['height'] or ''}")
            width_heigth_layout.addWidget(height)
            inside_bottom_layout.addWidget(width_height_frame, 0, Qt.AlignLeft)
            length_frame = QFrame(inside_bottom_frame)
            length_frame.setFrameShape(QFrame.NoFrame)
            length_frame.setFrameShadow(QFrame.Raised)
            length_layout = QHBoxLayout(length_frame)
            length_layout.setContentsMargins(0, 0, 0, 0)
            length_layout.setSpacing(4)
            length_icon = QLabel(length_frame)
            length_icon.setMinimumSize(QSize(12, 12))
            length_icon.setStyleSheet("image: url(:/image/length_icon.svg);")
            length_icon.setText("")
            length_layout.addWidget(length_icon)
            length = QLabel(length_frame)
            length.setText(f"Length: {truck_type['length'] or ''}")
            length_layout.addWidget(length)
            inside_bottom_layout.addWidget(length_frame, 0, Qt.AlignLeft)
            equip_truck_type_main_layout.addWidget(inside_bottom_frame)
            flow_layout.addWidget(equip_truck_type_main_frame)
        add_truck_butt = QPushButton(self.main_window.ui.equip_truck_type_main_frame)
        add_truck_butt.setMinimumSize(QSize(324, 128))
        add_truck_butt.setStyleSheet("QPushButton {\n"
                                     "    background: transparent;\n"
                                     "    image: url(:/image/new_asset_type_default.svg);\n"
                                     "}\n"
                                     "\n"
                                     "QPushButton:hover {\n"
                                     "    image: url(:/image/new_asset_type_hover.svg);\n"
                                     "}")
        add_truck_butt.setText("")
        add_truck_butt.clicked.connect(add_new_funk)
        flow_layout.addWidget(add_truck_butt)
