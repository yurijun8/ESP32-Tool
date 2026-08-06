'''
This is responsible for the user interface of the application. It handles user interactions, displays information, and manages the layout of the application window.
'''

import sys
import os
import json
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from .assets_utils import resource_path
from .pin_data import LEFT_PINS, RIGHT_PINS, get_peripherals_for_pin
from .code_generator import generate_c_code
from .syntax_highlighter import CCodeHighlighter

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("ESP32 Tool")
        MainWindow.resize(1200, 900)
        MainWindow.setStyleSheet("""
        QMainWindow {
            background-color: #2E3440;
            color: #D8DEE9;
        }
        """)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        self.top_menu = QtWidgets.QFrame(self.centralwidget)
        self.top_menu.setMaximumSize(QtCore.QSize(16777215, 50))
        self.top_menu.setStyleSheet("""
        QFrame {
            background-color: #4C566A;
            border-bottom: 1px solid #3B4252;
        }
        """)
        self.horizontalLayout_top = QtWidgets.QHBoxLayout(self.top_menu)
        self.horizontalLayout_top.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_top.setSpacing(10)

        self.lineEdit = QtWidgets.QLineEdit(self.top_menu)
        self.lineEdit.setMinimumSize(QtCore.QSize(200, 30))
        self.lineEdit.setStyleSheet("""
        QLineEdit {
            background-color: #3B4252;
            border: 1px solid #434C5E;
            border-radius: 5px;
            padding: 5px;
            color: #D8DEE9;
        }
        """)
        self.lineEdit.setPlaceholderText("Project Name:")
        self.horizontalLayout_top.addWidget(self.lineEdit)

        self.save_button = QtWidgets.QPushButton("Save Preset")
        self.save_button.setStyleSheet("background-color: #5E81AC; color: #ECEFF4; border-radius: 5px; padding: 5px;")
        self.save_button.clicked.connect(self.save_preset)
        self.horizontalLayout_top.addWidget(self.save_button)

        self.load_button = QtWidgets.QPushButton("Load Preset")
        self.load_button.setStyleSheet("background-color: #5E81AC; color: #ECEFF4; border-radius: 5px; padding: 5px;")
        self.load_button.clicked.connect(self.load_preset)
        self.horizontalLayout_top.addWidget(self.load_button)

        self.GenerateCode = QtWidgets.QPushButton(self.top_menu)
        self.GenerateCode.setMinimumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        self.GenerateCode.setFont(font)
        self.GenerateCode.setStyleSheet("""
        QPushButton {
            background-color: #81A1C1;
            border: none;
            border-radius: 5px;
            color: #ECEFF4;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: #5E81AC;
        }
        """)
        self.GenerateCode.setText("Generate Code")
        self.horizontalLayout_top.addWidget(self.GenerateCode)

        self.verticalLayout.addWidget(self.top_menu)

        self.content = QtWidgets.QFrame(self.centralwidget)
        self.content.setStyleSheet("background-color: #2E3440;")
        self.horizontalLayout_content = QtWidgets.QHBoxLayout(self.content)
        self.horizontalLayout_content.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_content.setSpacing(0)

        self.left_frame = QtWidgets.QFrame(self.content)
        self.left_frame.setStyleSheet("background-color: #3B4252; border-radius: 10px;")
        self.left_layout = QtWidgets.QVBoxLayout(self.left_frame)
        self.left_layout.setContentsMargins(10, 5, 10, 10)
        self.left_layout.setSpacing(2)
        self.left_layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        self.center_frame = QtWidgets.QFrame(self.content)
        self.center_frame.setStyleSheet("background-color: transparent;")
        self.center_layout = QtWidgets.QVBoxLayout(self.center_frame)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setAlignment(QtCore.Qt.AlignCenter)

        image_path = resource_path('esp32-wroom-32.png')
        self.esp32Image = QtWidgets.QLabel(self.center_frame)
        pixmap = QtGui.QPixmap(image_path)
        desired_height = 450
        if not pixmap.isNull():
            aspect_ratio = pixmap.width() / pixmap.height()
            new_width = int(desired_height * aspect_ratio)
            pixmap = pixmap.scaled(new_width, desired_height, QtCore.Qt.KeepAspectRatio)
        self.esp32Image.setPixmap(pixmap)
        self.esp32Image.setAlignment(QtCore.Qt.AlignCenter)
        self.center_layout.addWidget(self.esp32Image)

        self.right_frame = QtWidgets.QFrame(self.content)
        self.right_frame.setStyleSheet("background-color: #3B4252; border-radius: 10px;")
        self.right_layout = QtWidgets.QVBoxLayout(self.right_frame)
        self.right_layout.setContentsMargins(10, 5, 10, 10)
        self.right_layout.setSpacing(2)
        self.right_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        self.horizontalLayout_content.addWidget(self.left_frame)
        self.horizontalLayout_content.addWidget(self.center_frame)
        self.horizontalLayout_content.addWidget(self.right_frame)
        self.horizontalLayout_content.setStretch(0, 1)
        self.horizontalLayout_content.setStretch(1, 0)
        self.horizontalLayout_content.setStretch(2, 1)

        self.verticalLayout.addWidget(self.content)
        MainWindow.setCentralWidget(self.centralwidget)

        self.add_comboboxes()
        self.add_checkboxes()

        self.GenerateCode.clicked.connect(self.generate_code_action)
        QtCore.QTimer.singleShot(0, self.adjust_layouts)
        self.code_window = None

    def adjust_layouts(self):
        image_pos = self.esp32Image.mapTo(self.content, QtCore.QPoint(0, 0))
        image_top_y = image_pos.y()
        combobox_height = 21
        offset = combobox_height * 3
        self.left_layout.setContentsMargins(10, image_top_y + offset, 10, 10)
        self.right_layout.setContentsMargins(10, image_top_y + offset, 10, 10)

    def add_comboboxes(self):
        combobox_height = 21
        for pin_name in LEFT_PINS:
            combo = QtWidgets.QComboBox()
            combo.setMinimumWidth(150)
            combo.setMaximumHeight(combobox_height)
            combo.setStyleSheet(f"""
            QComboBox {{
                background-color: #4C566A; border: 1px solid #434C5E; border-radius: 2px;
                padding: 1px; color: #D8DEE9; min-height: {combobox_height}px; max-height: {combobox_height}px;
            }}
            """)
            combo.addItems(get_peripherals_for_pin(pin_name))
            combo.setObjectName(f"combo_{pin_name}")
            combo.setCurrentText(f"Insert_{pin_name}")
            setattr(self, f"combo_{pin_name}", combo)

            label = QtWidgets.QLabel(pin_name)
            label.setStyleSheet("color: #D8DEE9;")
            label.setAlignment(QtCore.Qt.AlignRight)

            h_layout = QtWidgets.QHBoxLayout()
            h_layout.setSpacing(5)
            h_layout.setContentsMargins(0, 0, 0, 0)
            h_layout.addWidget(label)
            h_layout.addWidget(combo)
            self.left_layout.addLayout(h_layout)

        right_pins_reversed = list(reversed(RIGHT_PINS))
        for pin_name in right_pins_reversed:
            combo = QtWidgets.QComboBox()
            combo.setMinimumWidth(150)
            combo.setMaximumHeight(combobox_height)
            combo.setStyleSheet(f"""
            QComboBox {{
                background-color: #4C566A; border: 1px solid #434C5E; border-radius: 2px;
                padding: 1px; color: #D8DEE9; min-height: {combobox_height}px; max-height: {combobox_height}px;
            }}
            """)
            combo.addItems(get_peripherals_for_pin(pin_name))
            combo.setObjectName(f"combo_{pin_name}")
            combo.setCurrentText(f"Insert_{pin_name}")
            setattr(self, f"combo_{pin_name}", combo)

            label = QtWidgets.QLabel(pin_name)
            label.setStyleSheet("color: #D8DEE9;")
            label.setAlignment(QtCore.Qt.AlignRight)

            h_layout = QtWidgets.QHBoxLayout()
            h_layout.setSpacing(5)
            h_layout.setContentsMargins(0, 0, 0, 0)
            h_layout.addWidget(label)
            h_layout.addWidget(combo)
            self.right_layout.addLayout(h_layout)

    def add_checkboxes(self):
        self.checkboxes_frame = QtWidgets.QFrame(self.center_frame)
        self.checkboxes_frame.setStyleSheet("QFrame { background-color: transparent; }")
        v_layout = QtWidgets.QVBoxLayout(self.checkboxes_frame)
        v_layout.setContentsMargins(0, 10, 0, 0)
        v_layout.setSpacing(5)
        v_layout.setAlignment(QtCore.Qt.AlignCenter)

        font = QtGui.QFont()
        font.setBold(True)

        self.checkBox_wifi = QtWidgets.QCheckBox("Wi-Fi")
        self.checkBox_wifi.setFont(font)
        self.checkBox_wifi.setStyleSheet("QCheckBox { color: #D8DEE9; } QCheckBox::indicator { width: 20px; height: 20px; }")
        v_layout.addWidget(self.checkBox_wifi)

        self.checkBox_bluetooth = QtWidgets.QCheckBox("Bluetooth")
        self.checkBox_bluetooth.setFont(font)
        self.checkBox_bluetooth.setStyleSheet("QCheckBox { color: #D8DEE9; } QCheckBox::indicator { width: 20px; height: 20px; }")
        v_layout.addWidget(self.checkBox_bluetooth)

        self.checkBox_ble = QtWidgets.QCheckBox("BLE")
        self.checkBox_ble.setFont(font)
        self.checkBox_ble.setStyleSheet("QCheckBox { color: #D8DEE9; } QCheckBox::indicator { width: 20px; height: 20px; }")
        v_layout.addWidget(self.checkBox_ble)

        self.center_layout.addWidget(self.checkboxes_frame)

    def generate_code_action(self):
        project_name = self.lineEdit.text().strip()
        if not project_name:
            QMessageBox.warning(None, "Aviso", "Por favor, insira um nome para o projeto.")
            return

        pin_data = {}
        used_pins = set()

        for pin in LEFT_PINS + RIGHT_PINS:
            combo_attr = f"combo_{pin}"
            if hasattr(self, combo_attr):
                combo = getattr(self, combo_attr)
                val = combo.currentText()
                pin_data[pin] = val
                if val != f"Insert_{pin}":
                    if pin in used_pins:
                        QMessageBox.warning(None, "Conflito de Pinos", f"O pino {pin} está configurado para múltiplos periféricos.")
                        return
                    used_pins.add(pin)

        code = generate_c_code(
            project_name=project_name,
            pin_data=pin_data,
            wifi_checked=self.checkBox_wifi.isChecked(),
            bt_checked=self.checkBox_bluetooth.isChecked(),
            ble_checked=self.checkBox_ble.isChecked()
        )

        self.show_code_window(code, project_name)

    def show_code_window(self, code, project_name):
        self.code_window = QtWidgets.QWidget()
        self.code_window.setWindowTitle(f"Código Gerado - {project_name}")
        self.code_window.resize(800, 600)
        self.code_window.setStyleSheet("QWidget { background-color: #2E3440; color: #D8DEE9; }")

        layout = QtWidgets.QVBoxLayout(self.code_window)
        
        self.code_edit = QtWidgets.QTextEdit(self.code_window)
        self.code_edit.setReadOnly(True)
        self.code_edit.setStyleSheet("""
        QTextEdit {
            background-color: #3B4252; color: #ECEFF4; font-family: Consolas, monospace;
            font-size: 12pt; border: 1px solid #4C566A; border-radius: 5px; padding: 10px;
        }
        """)
        self.code_edit.setText(code)
        
        self.highlighter = CCodeHighlighter(self.code_edit.document())
        layout.addWidget(self.code_edit)

        buttons_layout = QtWidgets.QHBoxLayout()
        copy_button = QtWidgets.QPushButton("Copy Code")
        copy_button.setStyleSheet("background-color: #81A1C1; color: #ECEFF4; border-radius: 5px; padding: 5px;")
        copy_button.clicked.connect(self.copy_code)
        buttons_layout.addWidget(copy_button)

        export_button = QtWidgets.QPushButton("Export as .c File")
        export_button.setStyleSheet("background-color: #A3BE8C; color: #ECEFF4; border-radius: 5px; padding: 5px;")
        export_button.clicked.connect(lambda: self.export_code(project_name, self.code_edit.toPlainText()))
        buttons_layout.addWidget(export_button)

        layout.addLayout(buttons_layout)
        self.code_window.show()

    def copy_code(self):
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.code_edit.toPlainText())
        QMessageBox.information(None, "Sucesso", "Código copiado para a área de transferência.")

    def export_code(self, project_name, code):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(None, "Salvar Arquivo C", f"{project_name}.c", "C Files (*.c);;All Files (*)", options=options)
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(code)
            QMessageBox.information(None, "Sucesso", f"Código salvo em {file_path}")

    def save_preset(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(None, "Salvar Preset", "esp32_preset.json", "JSON Files (*.json);;All Files (*)", options=options)
        if file_path:
            preset_data = {
                "project_name": self.lineEdit.text(),
                "wifi": self.checkBox_wifi.isChecked(),
                "bluetooth": self.checkBox_bluetooth.isChecked(),
                "ble": self.checkBox_ble.isChecked(),
                "pins": {}
            }
            for pin in LEFT_PINS + RIGHT_PINS:
                combo = getattr(self, f"combo_{pin}", None)
                if combo:
                    preset_data["pins"][pin] = combo.currentText()
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(preset_data, f, indent=4)
            QMessageBox.information(None, "Sucesso", "Preset salvo com sucesso.")

    def load_preset(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(None, "Carregar Preset", "", "JSON Files (*.json);;All Files (*)", options=options)
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                self.lineEdit.setText(data.get("project_name", ""))
                self.checkBox_wifi.setChecked(data.get("wifi", False))
                self.checkBox_bluetooth.setChecked(data.get("bluetooth", False))
                self.checkBox_ble.setChecked(data.get("ble", False))
                pins = data.get("pins", {})
                for pin, val in pins.items():
                    combo = getattr(self, f"combo_{pin}", None)
                    if combo:
                        idx = combo.findText(val)
                        if idx >= 0:
                            combo.setCurrentIndex(idx)
                QMessageBox.information(None, "Sucesso", "Preset carregado com sucesso.")
            except Exception as e:
                QMessageBox.critical(None, "Erro", f"Falha ao carregar preset: {e}")