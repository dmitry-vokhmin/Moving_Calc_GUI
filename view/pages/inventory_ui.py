from urllib.request import urlopen
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QCursor, QIntValidator, QPixmap
from PyQt5.QtWidgets import QPushButton, QFrame, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QStyledItemDelegate
from view.custom_widgets.flow_layout import FlowLayout


class InventoryUi:
    def __init__(self, main_window):
        self.main_window = main_window

    def set_left_menu(self, frame, layout, funk, data, add_funk, del_funk, is_preset_menu):
        for room in data:
            room_menu_butt = QPushButton(frame)
            room_menu_butt.setMinimumSize(QSize(208, 54))
            room_menu_butt.setMaximumSize(QSize(208, 54))
            room_menu_butt.setCursor(QCursor(Qt.PointingHandCursor))
            room_menu_butt.setIconSize(QSize(20, 20))
            room_menu_butt.setCheckable(True)
            layout.addWidget(room_menu_butt)
            if is_preset_menu:
                room_menu_butt.setText(room["move_size"]["name"].title().replace("_", " "))
                room_menu_butt.setIcon(QIcon(":/image/inventory_preset_image.svg"))
                room_menu_butt.__setattr__("inventory_collection_id", room["id"])
                room_menu_butt.clicked.connect(funk({"inventory_collection_id": room["id"]}, room_menu_butt,
                                                    del_funk, add_funk, True))
            else:
                room_menu_butt.setText(room["rooms"]["name"].title().replace("_", " "))
                data = urlopen(room["rooms"]["image"]).read()
                pixmap = QPixmap()
                pixmap.loadFromData(data)
                room_menu_butt.setIcon(QIcon(pixmap))
                room_menu_butt.clicked.connect(funk(room["room_id"], room["id"], room_menu_butt, del_funk, add_funk))
                self.main_window.ui.inventory_search_clear.setVisible(False)

    def set_category_menu(self, categories, funk, frame, instance):
        self.main_window.delete_layout(frame.layout())
        inventory_categor_butt_layout = FlowLayout(frame)
        inventory_categor_butt_layout.setContentsMargins(0, 0, 0, 0)
        inventory_categor_butt_layout.setSpacing(5)
        button_all = QPushButton(frame)
        button_all.setCursor(QCursor(Qt.PointingHandCursor))
        button_all.setCheckable(True)
        button_all.setChecked(True)
        button_all.setText("All")
        button_all.setStyleSheet("qproperty-icon: url(:/image/check_icon_hover.svg);")
        button_all.clicked.connect(funk(button_all))
        button_all.installEventFilter(instance)
        inventory_categor_butt_layout.addWidget(button_all)
        for category in categories:
            button = QPushButton(frame)
            button.setCursor(QCursor(Qt.PointingHandCursor))
            button.setCheckable(True)
            button.setText(category["name"].title())
            button.clicked.connect(funk(button, category["id"]))
            button.installEventFilter(instance)
            inventory_categor_butt_layout.addWidget(button)

    def set_preset_menu(self, frame, preset_inventory, menu_funk):
        self.main_window.delete_layout(frame.layout())
        calc_preset_menu_layout = QVBoxLayout(frame)
        calc_preset_menu_layout.setContentsMargins(0, 0, 0, 0)
        calc_preset_menu_layout.setSpacing(2)
        for key, value in preset_inventory.items():
            room_menu_butt = QPushButton(frame)
            room_menu_butt.setMinimumSize(QSize(208, 54))
            room_menu_butt.setMaximumSize(QSize(208, 54))
            room_menu_butt.setCursor(QCursor(Qt.PointingHandCursor))
            room_menu_butt.setIconSize(QSize(20, 20))
            room_menu_butt.setCheckable(True)
            calc_preset_menu_layout.addWidget(room_menu_butt)
            room_menu_butt.setText(value["move_size_name"])
            room_menu_butt.setIcon(QIcon(":/image/inventory_preset_image.svg"))
            room_menu_butt.clicked.connect(menu_funk(room_menu_butt, key))

    def set_room_inventory_card(
            self,
            inventories,
            del_funk,
            add_funk,
            is_preset_menu,
            frame,
            instance,
    ):
        for button in frame.findChildren(QPushButton):
            button.removeEventFilter(instance)
        self.main_window.delete_layout(frame.layout())
        inventory_content_clear_layout = FlowLayout(frame)
        inventory_content_clear_layout.setContentsMargins(0, 0, 0, 0)
        inventory_content_clear_layout.setSpacing(8)
        for inventory in inventories:
            if is_preset_menu:
                self.set_preset_card(inventory,
                                     inventory_content_clear_layout,
                                     frame,
                                     del_funk,
                                     instance=instance)
            elif inventory["company_id"]:
                self.set_custom_room_card(inventory,
                                          inventory_content_clear_layout,
                                          frame,
                                          del_funk,
                                          add_funk,
                                          instance)
            else:
                self.set_room_card(inventory,
                                   inventory_content_clear_layout,
                                   frame,
                                   add_funk,
                                   instance)

    def create_preset_inventory_cards(self, move_size_id, preset_inventory, del_funk, count_funk, instance):
        self.main_window.delete_layout(self.main_window.ui.calc_inv_content_clear_frame.layout())
        inventory_content_clear_layout = FlowLayout(self.main_window.ui.calc_inv_content_clear_frame)
        inventory_content_clear_layout.setContentsMargins(0, 0, 0, 0)
        inventory_content_clear_layout.setSpacing(8)
        for inventory in preset_inventory[move_size_id]["inventory"]:
            self.set_preset_card(inventory,
                                 inventory_content_clear_layout,
                                 self.main_window.ui.calc_inv_content_clear_frame,
                                 del_funk,
                                 move_size_id=move_size_id,
                                 count_funk=count_funk,
                                 instance=instance)

    def set_preset_card(self, inventory, layout, frame, del_funk, move_size_id=None, count_funk=None, instance=None):
        card_main_frame = QFrame(frame)
        card_main_frame.setMinimumSize(QSize(324, 119))
        card_main_frame.setMaximumSize(QSize(324, 119))
        card_main_frame.setStyleSheet("#card_main_frame {\n"
                                      "    border: 0.5px solid rgba(181, 184, 199, 0.5);\n"
                                      "    border-radius: 10px;\n"
                                      "}\n"
                                      "\n"
                                      "#card_main_frame:hover {\n"
                                      "    border: 0.5px solid #0915CC;\n"
                                      "}")
        card_main_frame.setFrameShape(QFrame.NoFrame)
        card_main_frame.setFrameShadow(QFrame.Raised)
        card_main_frame.setObjectName("card_main_frame")
        card_main_layout = QVBoxLayout(card_main_frame)
        card_main_layout.setContentsMargins(15, 15, 15, 15)
        card_main_layout.setSpacing(15)
        inner_frame = QFrame(card_main_frame)
        inner_frame.setFrameShape(QFrame.NoFrame)
        inner_frame.setFrameShadow(QFrame.Raised)
        inner_layout = QHBoxLayout(inner_frame)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(0)
        item_image = QLabel(inner_frame)
        item_image.setMinimumSize(QSize(56, 56))
        item_image.setMaximumSize(QSize(56, 56))
        item_image.setStyleSheet("image: url(:/image/Login_pic.png);")
        item_image.setText("")
        inner_layout.addWidget(item_image)
        delete_item_butt = QPushButton(inner_frame)
        delete_item_butt.setMinimumSize(QSize(103, 28))
        delete_item_butt.setCursor(QCursor(Qt.PointingHandCursor))
        delete_item_butt.setLayoutDirection(Qt.RightToLeft)
        delete_item_butt.setStyleSheet("QPushButton {\n"
                                       "    border: none;"
                                       "    background: transparent;\n"
                                       "    font-size: 14px;\n"
                                       "    color: #757C9F;\n"
                                       "    qproperty-icon: url(:/image/inventory_delete_default.svg);\n"
                                       "}\n"
                                       "\n"
                                       "QPushButton:hover {\n"
                                       "    color: #FF3C2F;\n"
                                       "}")
        delete_item_butt.setIconSize(QSize(24, 24))
        delete_item_butt.setText("Delete")
        delete_item_butt.setObjectName("delete")
        inner_layout.addWidget(delete_item_butt, 0, Qt.AlignLeft | Qt.AlignTop)
        combobox = QComboBox(inner_frame)
        combobox.setMinimumSize(QSize(60, 24))
        combobox.setMaximumSize(QSize(60, 24))
        combobox.setCursor(QCursor(Qt.PointingHandCursor))
        combobox.view().window().setWindowFlags(
            Qt.Popup | Qt.FramelessWindowHint | Qt.NoDropShadowWindowHint
        )
        combobox.setItemDelegate(QStyledItemDelegate())
        combobox.setEditable(True)
        combobox.addItem(str(inventory["count"]))
        combobox.setValidator(QIntValidator())
        for number in range(1, 10):
            combobox.addItem(str(number))
        inner_layout.addWidget(combobox, 0, Qt.AlignTop)
        card_main_layout.addWidget(inner_frame)
        item_description = QLabel(card_main_frame)
        item_description.setStyleSheet("color: #070808;\n"
                                       "font-size: 14px;")
        item_description.setText(inventory["inventories"]["name"].title())
        card_main_layout.addWidget(item_description)
        if move_size_id:
            card_main_frame.__setattr__("move_size_id", move_size_id)
            delete_item_butt.clicked.connect(del_funk(move_size_id, inventory["inventory_id"]))
            combobox.currentTextChanged.connect(lambda x: count_funk(x, move_size_id, inventory["inventory_id"]))
        else:
            card_main_frame.__setattr__("inventory_id", inventory["inventory_id"])
            card_main_frame.__setattr__("inventory_collection_id", inventory["inventory_collection_id"])
            delete_item_butt.clicked.connect(
                lambda: self.main_window.modal_window.show_confirm_dialog(
                    del_funk(inventory["inventory_id"],
                             inventory["inventory_collection_id"]))
            )
        delete_item_butt.installEventFilter(instance)
        layout.addWidget(card_main_frame)

    def set_room_card(self, inventory, layout, frame, add_funk, instance):
        card_main_frame = QFrame(frame)
        card_main_frame.setMinimumSize(QSize(324, 119))
        card_main_frame.setMaximumSize(QSize(324, 119))
        card_main_frame.setStyleSheet(".QFrame {\n"
                                      "    border: 0.5px solid rgba(181, 184, 199, 0.5);\n"
                                      "    border-radius: 10px;\n"
                                      "}\n"
                                      "\n"
                                      ".QFrame:hover {\n"
                                      "    border: 0.5px solid #0915CC;\n"
                                      "}")
        card_main_frame.setFrameShape(QFrame.NoFrame)
        card_main_frame.setFrameShadow(QFrame.Raised)
        card_main_frame.__setattr__("category_id", inventory["inventory_category_id"])
        card_main_frame.__setattr__("item_name", inventory["name"])
        card_main_frame.setObjectName("card_main_frame")
        card_main_layout = QVBoxLayout(card_main_frame)
        card_main_layout.setContentsMargins(15, 15, 15, 15)
        card_main_layout.setSpacing(15)
        inner_frame = QFrame(card_main_frame)
        inner_frame.setStyleSheet("border: none;")
        inner_frame.setFrameShape(QFrame.NoFrame)
        inner_frame.setFrameShadow(QFrame.Raised)
        inner_layout = QHBoxLayout(inner_frame)
        inner_layout.setContentsMargins(0, 0, 0, 0)
        inner_layout.setSpacing(0)
        item_image = QLabel(inner_frame)
        item_image.setMinimumSize(QSize(56, 56))
        item_image.setMaximumSize(QSize(56, 56))
        item_image.setStyleSheet("image: url(:/image/Login_pic.png);")
        item_image.setText("")
        inner_layout.addWidget(item_image)
        add_item_butt = QPushButton(inner_frame)
        add_item_butt.setMinimumSize(QSize(103, 28))
        add_item_butt.setCursor(QCursor(Qt.PointingHandCursor))
        add_item_butt.setLayoutDirection(Qt.RightToLeft)
        add_item_butt.setStyleSheet("QPushButton {\n"
                                    "    background: #F2F3F6;\n"
                                    "    border-radius: 5px;\n"
                                    "    color: #757C9F;\n"
                                    "    qproperty-icon: url(:/image/plus_gray_icon.svg);\n"
                                    "    font-size: 14px;\n"
                                    "}\n"
                                    "\n"
                                    "QPushButton:hover {\n"
                                    "    color: #0915CC;\n"
                                    "}\n"
                                    "")
        add_item_butt.setIconSize(QSize(24, 24))
        add_item_butt.setText("Add Item")
        add_item_butt.clicked.connect(add_funk(inventory))
        add_item_butt.installEventFilter(instance)
        add_item_butt.setObjectName("add")
        inner_layout.addWidget(add_item_butt, 0, Qt.AlignLeft | Qt.AlignTop)
        card_main_layout.addWidget(inner_frame)
        item_description = QLabel(card_main_frame)
        item_description.setStyleSheet("color: #070808;\n"
                                       "font-size: 14px;")
        item_description.setText(inventory["name"].title())
        card_main_layout.addWidget(item_description)
        layout.addWidget(card_main_frame)

    def set_custom_room_card(self, inventory, layout, frame, del_funk, add_funk, instance):
        main_frame = QFrame(frame)
        main_frame.setMinimumSize(QSize(324, 162))
        main_frame.setMaximumSize(QSize(324, 162))
        main_frame.setStyleSheet(".QFrame {\n"
                                 "    border: 0.5px solid rgba(181, 184, 199, 0.5);\n"
                                 "    border-radius: 10px;\n"
                                 "}\n"
                                 "\n"
                                 ".QFrame:hover {\n"
                                 "    border: 0.5px solid #0915CC;\n"
                                 "}")
        main_frame.setFrameShape(QFrame.NoFrame)
        main_frame.setFrameShadow(QFrame.Raised)
        main_frame.__setattr__("item_name", inventory["name"])
        main_frame.setObjectName("card_main_frame")
        main_layout = QVBoxLayout(main_frame)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(0)
        top_inner_frame = QFrame(main_frame)
        top_inner_frame.setStyleSheet("border: none;")
        top_inner_frame.setFrameShape(QFrame.NoFrame)
        top_inner_frame.setFrameShadow(QFrame.Raised)
        top_inner_layout = QHBoxLayout(top_inner_frame)
        top_inner_layout.setContentsMargins(0, 0, 0, 15)
        top_inner_layout.setSpacing(11)
        item_image = QLabel(top_inner_frame)
        item_image.setMinimumSize(QSize(56, 56))
        item_image.setMaximumSize(QSize(56, 56))
        item_image.setStyleSheet("image: url(:/image/custom_item_icon.svg);")
        item_image.setText("")
        top_inner_layout.addWidget(item_image)
        if del_funk:
            delete_butt = QPushButton(top_inner_frame)
            delete_butt.setCursor(QCursor(Qt.PointingHandCursor))
            delete_butt.setLayoutDirection(Qt.RightToLeft)
            delete_butt.setStyleSheet("QPushButton {\n"
                                      "    background: transparent;\n"
                                      "    font-size: 14px;\n"
                                      "    color: #757C9F;\n"
                                      "    qproperty-icon: url(:/image/inventory_delete_default.svg);\n"
                                      "}\n"
                                      "\n"
                                      "QPushButton:hover {\n"
                                      "    color: #FF3C2F;\n"
                                      "}")
            delete_butt.setIconSize(QSize(24, 24))
            delete_butt.setText("Delete ")
            delete_butt.clicked.connect(
                lambda: self.main_window.modal_window.show_confirm_dialog(del_funk(inventory["id"]))
            )
            delete_butt.installEventFilter(instance)
            delete_butt.setObjectName("delete")
            top_inner_layout.addWidget(delete_butt, 0, Qt.AlignLeft | Qt.AlignTop)
        add_butt = QPushButton(top_inner_frame)
        add_butt.setMinimumSize(QSize(103, 28))
        add_butt.setCursor(QCursor(Qt.PointingHandCursor))
        add_butt.setLayoutDirection(Qt.RightToLeft)
        add_butt.setStyleSheet("QPushButton {\n"
                               "    background: #F2F3F6;\n"
                               "    border-radius: 5px;\n"
                               "    color: #757C9F;\n"
                               "    qproperty-icon: url(:/image/plus_gray_icon.svg);\n"
                               "    font-size: 14px;\n"
                               "}\n"
                               "\n"
                               "QPushButton:hover {\n"
                               "    color: #0915CC;\n"
                               "}\n"
                               "")
        add_butt.setIconSize(QSize(24, 24))
        add_butt.setText("Add Item ")
        add_butt.clicked.connect(add_funk(inventory))
        add_butt.installEventFilter(instance)
        add_butt.setObjectName("add")
        top_inner_layout.addWidget(add_butt, 0, Qt.AlignLeft | Qt.AlignTop)
        main_layout.addWidget(top_inner_frame)
        item_name = QLabel(main_frame)
        item_name.setStyleSheet("color: #070808;\n"
                                "font-size: 14px;")
        item_name.setText(inventory["name"].title())
        main_layout.addWidget(item_name)
        bottom_inner_frame = QFrame(main_frame)
        bottom_inner_frame.setStyleSheet("QFrame {\n"
                                         "    border: none;\n"
                                         "}\n"
                                         "\n"
                                         "QLabel {\n"
                                         "    color: #757C9F;\n"
                                         "    font-size: 14px;\n"
                                         "}")
        bottom_inner_frame.setFrameShape(QFrame.NoFrame)
        bottom_inner_frame.setFrameShadow(QFrame.Raised)
        bottom_inner_layout = QVBoxLayout(bottom_inner_frame)
        bottom_inner_layout.setContentsMargins(0, 5, 0, 0)
        bottom_inner_layout.setSpacing(2)
        width_height_frame = QFrame(bottom_inner_frame)
        width_height_frame.setFrameShape(QFrame.NoFrame)
        width_height_frame.setFrameShadow(QFrame.Raised)
        width_heigth_layout = QHBoxLayout(width_height_frame)
        width_heigth_layout.setContentsMargins(0, 0, 0, 0)
        width_heigth_layout.setSpacing(4)
        width_heigth_layout.setObjectName("width_heigth_layout")
        width_image = QLabel(width_height_frame)
        width_image.setMinimumSize(QSize(12, 12))
        width_image.setStyleSheet("image: url(:/image/width_icon.svg);")
        width_image.setText("")
        width_image.setObjectName("width_image")
        width_heigth_layout.addWidget(width_image)
        width_text = QLabel(width_height_frame)
        width_text.setStyleSheet("margin-right: 12px;")
        width_text.setAlignment(Qt.AlignJustify | Qt.AlignVCenter)
        width_text.setText(f'Width: {inventory["width"]}')
        width_heigth_layout.addWidget(width_text)
        height_image = QLabel(width_height_frame)
        height_image.setMinimumSize(QSize(12, 12))
        height_image.setStyleSheet("image: url(:/image/length_icon.svg);")
        height_image.setText("")
        width_heigth_layout.addWidget(height_image)
        height_text = QLabel(width_height_frame)
        height_text.setStyleSheet("")
        height_text.setText(f'Height: {inventory["height"]}')
        width_heigth_layout.addWidget(height_text)
        bottom_inner_layout.addWidget(width_height_frame, 0, Qt.AlignLeft)
        length_frame = QFrame(bottom_inner_frame)
        length_frame.setFrameShape(QFrame.NoFrame)
        length_frame.setFrameShadow(QFrame.Raised)
        length_layout = QHBoxLayout(length_frame)
        length_layout.setContentsMargins(0, 0, 0, 0)
        length_layout.setSpacing(4)
        length_image = QLabel(length_frame)
        length_image.setMinimumSize(QSize(12, 12))
        length_image.setStyleSheet("image: url(:/image/length_icon.svg);")
        length_image.setText("")
        length_layout.addWidget(length_image)
        length_text = QLabel(length_frame)
        length_text.setStyleSheet("")
        length_text.setText(f'Length: {inventory["length"]}')
        length_layout.addWidget(length_text)
        bottom_inner_layout.addWidget(length_frame, 0, Qt.AlignLeft)
        main_layout.addWidget(bottom_inner_frame, 0, Qt.AlignLeft)
        layout.addWidget(main_frame)

    def categorize_inventory(self, frame, category_id):
        cards = frame.findChildren(QFrame, "card_main_frame")
        for card in cards:
            if category_id:
                if card.__getattribute__("category_id") != category_id:
                    card.setVisible(False)
                else:
                    card.setVisible(True)
            else:
                card.setVisible(True)
