from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QLabel, QLineEdit, QHBoxLayout, QVBoxLayout,
                             QWidget, QPushButton, QTabWidget,
                             QCheckBox)
from PyQt6.QtGui import QAction, QFont

from pathlib import Path

import sys

from bacon_binary_hide import BaconEncryptor


class MainWindow(QMainWindow):

    base_encrypt_layout: QVBoxLayout
    base_decrypt_layout: QVBoxLayout

    input_encrypt_layout: QHBoxLayout
    input_decrypt_layout: QHBoxLayout

    container_encrypt_layout: QVBoxLayout
    message_encrypt_layout: QVBoxLayout

    container_decrypt_layout: QVBoxLayout
    message_decrypt_layout: QVBoxLayout

    label_header_container: QLabel
    label_container: QLabel
    input_container: QLineEdit

    decrypt_label_header_container: QLabel
    decrypt_label_container: QLabel
    decrypt_input_container: QLineEdit

    label_header_message: QLabel
    label_message: QLabel
    input_encrypt_message: QLineEdit

    decrypt_label_header_message: QLabel
    decrypt_label_message: QLabel
    decrypt_input_encrypt_message: QLineEdit

    label_result: QLabel

    decrypt_label_result: QLabel

    decrypt_button_get_result: QPushButton
    decrypt_button_clear: QPushButton


    button_get_result: QPushButton
    button_clear: QPushButton

    result_buttons_layout: QHBoxLayout

    decrypt_result_buttons_layout: QHBoxLayout

    checkbox_simple: QCheckBox

    checkbox_simple_mode: QCheckBox

    menu_bar = QMainWindow.menuBar

    open_file: QAction
    choose_mode: QAction

    def __init__(self):

        self.bc = BaconEncryptor()
        super().__init__()

        self.setWindowTitle("Bacon Cipher")

        self.init_status_bar()

        self.init_encrypt_input_UI()
        self.encrypt_container = QWidget()
        self.update_encrypt_layout()

        self.init_decrypt_input_UI()
        self.decrypt_container = QWidget()
        self.update_decrypt_layout()

        self.tab_menu = QTabWidget()
        self.tab_menu.setTabPosition(QTabWidget.TabPosition.North)
        self.tab_menu.setMovable(True)
        for title, widget in {"Encryption": self.encrypt_container, "Decryption": self.decrypt_container}.items():
            self.tab_menu.addTab(widget, title)
        self.setCentralWidget(self.tab_menu)

    def init_status_bar(self):
        self.statusBar()

        self.menu_bar = self.menuBar()

        self.open_file = QAction('Open', self)
        self.open_file.setShortcut('Ctrl+O')
        self.open_file.setStatusTip('Open cipher table file')
        self.open_file.triggered.connect(self.show_file_dialog)

        self.file_menu = self.menu_bar.addMenu('&File')
        self.file_menu.addAction(self.open_file)
        
        self.choose_mode1 = QAction("Set",self)
        self.choose_mode1.triggered.connect(self.show_mode_dialog1)

        self.choose_mode2 = QAction("Set",self)
        self.choose_mode2.triggered.connect(self.show_mode_dialog2)

        self.mode_menu = self.menu_bar.addMenu('&Mode')
        self.mode_menu1 = self.mode_menu.addMenu('&Mode 2 letters')
        self.mode_menu2 = self.mode_menu.addMenu('&Mode 3 letters')
        self.mode_menu1.addAction(self.choose_mode1)
        self.mode_menu2.addAction(self.choose_mode2)

    def show_mode_dialog1(self):
        self.bc=  BaconEncryptor(mode = 2)
        pass

    def show_mode_dialog2(self):
        self.bc = BaconEncryptor(mode = 3)
        pass

    def show_file_dialog(self):
        home_dir = str(Path.home())
        file_name = QFileDialog.getOpenFileName(self, 'Open file', home_dir, "Alphabet given in JSON-format (*.json)")

        if file_name[0]:
            self.bc.get_alph_from_json(file_name[0])

    def set_initial_encrypt_layout(self):
        self.label_result.setText(None)
        self.label_message.setText(None)
        self.label_container.setText(None)

        self.input_container.setText(None)
        self.input_encrypt_message.setText(None)

        self.update_encrypt_layout()

    def update_encrypt_layout(self):
        self.encrypt_container.setLayout(self.base_encrypt_layout)

    def init_encrypt_input_UI(self):
        # init container input elements
        self.label_header_container = QLabel()
        self.label_header_container.setText("Enter container:")
        self.label_container = QLabel(wordWrap=True)
        self.input_container = QLineEdit()
        self.input_container.textChanged.connect(self.label_container.setText)

        # collect container input elements into a vertical layout
        self.container_encrypt_layout = QVBoxLayout()
        self.container_encrypt_layout.addWidget(self.label_header_container)
        self.container_encrypt_layout.addWidget(self.input_container)
        self.container_encrypt_layout.addWidget(self.label_container)

        # init message input elements
        self.label_header_message = QLabel()
        self.label_header_message.setText("Enter message:")
        self.label_message = QLabel(wordWrap=True)
        self.input_encrypt_message = QLineEdit()
        self.input_encrypt_message.textChanged.connect(self.label_message.setText)

        # collect message input elements into a vertical layout
        self.message_encrypt_layout = QVBoxLayout()
        self.message_encrypt_layout.addWidget(self.label_header_message)
        self.message_encrypt_layout.addWidget(self.input_encrypt_message)
        self.message_encrypt_layout.addWidget(self.label_message)

        # collect container and message layouts together

        self.input_encrypt_layout = QHBoxLayout()
        self.input_encrypt_layout.addLayout(self.container_encrypt_layout)
        self.input_encrypt_layout.addLayout(self.message_encrypt_layout)

        # init button to get result
        self.button_get_result = QPushButton("Get text with hidden message")
        self.button_get_result.setCheckable(True)
        self.button_get_result.clicked.connect(self.button_get_result_was_clicked)

        # init checkbox to remove (or not) redundancy
        self.checkbox_simple = QCheckBox("Remove redundancy")
        self.checkbox_simple.setCheckable(True)
        self.checkbox_simple.toggled.connect(self.is_redundancy_removed)


        # collect buttons into one layout
        self.result_buttons_layout = QHBoxLayout()
        self.result_buttons_layout.addWidget(self.button_get_result)
        if self.bc.getmode()==2:
            self.result_buttons_layout.addWidget(self.checkbox_simple)

        # init button to clear all input and result text labels
        self.button_clear = QPushButton("Clear")
        self.button_clear.setCheckable(True)
        self.button_clear.clicked.connect(self.button_encrypt_clear_was_clicked)

        # init text label to present result (will appear after first result got)
        self.label_result = QLabel(wordWrap=True)

        # collect input fields and buttons into the initial layout of the app
        self.base_encrypt_layout = QVBoxLayout()
        self.base_encrypt_layout.addLayout(self.input_encrypt_layout)
        self.base_encrypt_layout.addLayout(self.result_buttons_layout)

    def is_redundancy_removed(self):
        if self.sender().isChecked():
            self.bc = BaconEncryptor(remove_redundancy=True)
        else:
            self.bc = BaconEncryptor(remove_redundancy=False)
     

    def set_initial_decrypt_layout(self):
        self.decrypt_label_result.setText(None)
        self.decrypt_label_message.setText(None)

        self.input_decrypt_message.setText(None)

        self.update_decrypt_layout()

    def update_decrypt_layout(self):
        self.decrypt_container.setLayout(self.base_decrypt_layout)

    def init_decrypt_input_UI(self):
        
        self.bold_button = QPushButton("bold the text", self)
        self.bold_button.clicked.connect(self.bold_text)

        # init message input elements
        self.decrypt_label_header_message = QLabel()
        self.decrypt_label_header_message.setText("Enter message:")
        self.decrypt_label_message = QLabel(wordWrap=True)
        self.input_decrypt_message = QLineEdit()
        self.input_decrypt_message.textChanged.connect(self.decrypt_label_message.setText)

        # collect message input elements into a vertical layout
        self.message_decrypt_layout = QVBoxLayout()
        self.message_decrypt_layout.addWidget(self.decrypt_label_header_message)
        self.message_decrypt_layout.addWidget(self.input_decrypt_message)
        self.message_decrypt_layout.addWidget(self.decrypt_label_message)
        self.message_decrypt_layout.addWidget(self.bold_button)

         # init button to get result
        self.decrypt_button_get_result = QPushButton("decrypt")
        self.decrypt_button_get_result.setCheckable(True)
        self.decrypt_button_get_result.clicked.connect(self.decrypt_button_get_result_was_clicked)

        # init button to clear all input and result text labels
        self.decrypt_button_clear = QPushButton("Clear")
        self.decrypt_button_clear.setCheckable(True)
        self.decrypt_button_clear.clicked.connect(self.button_decrypt_clear_was_clicked)

        # init text label to present result (will appear after first result got)
        self.decrypt_label_result = QLabel(wordWrap=True)

        # collect input fields and buttons into the initial layout of the app
        self.base_decrypt_layout = QVBoxLayout()
        self.base_decrypt_layout.addLayout(self.message_decrypt_layout)
        self.base_decrypt_layout.addWidget(self.decrypt_button_get_result)

    def button_get_result_was_clicked(self):
        self.bc.process(self.label_message.text(), self.label_container.text())
        res = str(self.bc)
        self.label_result.setText(res)
        self.base_encrypt_layout.addWidget(self.label_result)
        self.base_encrypt_layout.addWidget(self.button_clear)

        self.update_encrypt_layout()

    def decrypt_button_get_result_was_clicked(self):
        if self.bc.mode == 2:
            res = self.bc.reveal_message_simple(self.decrypt_label_message.text())
        else:
            res = self.bc.reveal_message_mode3(self.decrypt_label_message.text())
        self.decrypt_label_result.setText(res)
        self.base_decrypt_layout.addWidget(self.decrypt_label_result)
        self.base_decrypt_layout.addWidget(self.decrypt_button_clear)

        self.update_decrypt_layout()

    def button_encrypt_clear_was_clicked(self):
        self.set_initial_encrypt_layout()
    
    def button_decrypt_clear_was_clicked(self):
        self.set_initial_decrypt_layout()
    
    def bold_text(self):
        if (self.input_decrypt_message.selectedText()!=''):
            self.input_decrypt_message.insert(''.join(f"<b>{letter}</b>" for letter in self.input_decrypt_message.selectedText()))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
