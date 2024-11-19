# -*- coding: utf-8 -*-

import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog

# Obter o caminho absoluto da imagem
image_path = os.path.join(os.path.dirname(__file__), 'esp32-wroom-32.png')

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowTitle("ESP32 Tool")  # Definir o nome da ferramenta
        MainWindow.resize(1200, 900)
        MainWindow.setStyleSheet("""
        QMainWindow {
            background-color: #2E3440;
            color: #D8DEE9;
        }
        """)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Layout vertical principal
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")

        # Top menu
        self.top_menu = QtWidgets.QFrame(self.centralwidget)
        self.top_menu.setMaximumSize(QtCore.QSize(16777215, 50))
        self.top_menu.setStyleSheet("""
        QFrame {
            background-color: #4C566A;
            border-bottom: 1px solid #3B4252;
        }
        """)
        self.top_menu.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.top_menu.setObjectName("top_menu")

        self.horizontalLayout_top = QtWidgets.QHBoxLayout(self.top_menu)
        self.horizontalLayout_top.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout_top.setSpacing(10)
        self.horizontalLayout_top.setObjectName("horizontalLayout_top")

        # Campo de entrada para o nome do projeto
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
        QLineEdit:focus {
            border: 1px solid #81A1C1;
        }
        """)
        self.lineEdit.setPlaceholderText("Project Name:")
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_top.addWidget(self.lineEdit)

        # Botão "Generate Code"
        self.GenerateCode = QtWidgets.QPushButton(self.top_menu)
        self.GenerateCode.setMinimumSize(QtCore.QSize(150, 30))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
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
        self.GenerateCode.setObjectName("GenerateCode")
        self.horizontalLayout_top.addWidget(self.GenerateCode)

        self.verticalLayout.addWidget(self.top_menu)

        # Conteúdo principal
        self.content = QtWidgets.QFrame(self.centralwidget)
        self.content.setStyleSheet("""
        QFrame {
            background-color: #2E3440;
        }
        """)
        self.content.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.content.setObjectName("content")

        # Layout horizontal principal
        self.horizontalLayout_content = QtWidgets.QHBoxLayout(self.content)
        self.horizontalLayout_content.setContentsMargins(0, 0, 0, 0)  # Removendo margens
        self.horizontalLayout_content.setSpacing(0)  # Removendo espaçamento entre widgets
        self.horizontalLayout_content.setObjectName("horizontalLayout_content")

        # Divisão Esquerda (ComboBoxes do lado esquerdo)
        self.left_frame = QtWidgets.QFrame(self.content)
        self.left_frame.setStyleSheet("""
        QFrame {
            background-color: #3B4252;
            border-radius: 10px;
        }
        """)
        self.left_frame.setObjectName("left_frame")
        self.left_layout = QtWidgets.QVBoxLayout(self.left_frame)
        self.left_layout.setContentsMargins(10, 5, 10, 10)
        self.left_layout.setSpacing(2)
        self.left_layout.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTop)

        # Divisão Central (Imagem do ESP32)
        self.center_frame = QtWidgets.QFrame(self.content)
        self.center_frame.setStyleSheet("""
        QFrame {
            background-color: transparent;
        }
        """)
        self.center_frame.setObjectName("center_frame")
        self.center_layout = QtWidgets.QVBoxLayout(self.center_frame)
        self.center_layout.setContentsMargins(0, 0, 0, 0)
        self.center_layout.setSpacing(0)
        self.center_layout.setAlignment(QtCore.Qt.AlignCenter)

        # Imagem do ESP32
        self.esp32Image = QtWidgets.QLabel(self.center_frame)
        pixmap = QtGui.QPixmap(image_path)
        desired_height = 450
        aspect_ratio = pixmap.width() / pixmap.height()
        new_width = int(desired_height * aspect_ratio)
        pixmap = pixmap.scaled(new_width, desired_height, QtCore.Qt.KeepAspectRatio)
        self.esp32Image.setPixmap(pixmap)
        self.esp32Image.setAlignment(QtCore.Qt.AlignCenter)
        self.esp32Image.setObjectName("esp32Image")
        self.center_layout.addWidget(self.esp32Image)

        # Divisão Direita (ComboBoxes do lado direito)
        self.right_frame = QtWidgets.QFrame(self.content)
        self.right_frame.setStyleSheet("""
        QFrame {
            background-color: #3B4252;
            border-radius: 10px;
        }
        """)
        self.right_frame.setObjectName("right_frame")
        self.right_layout = QtWidgets.QVBoxLayout(self.right_frame)
        self.right_layout.setContentsMargins(10, 5, 10, 10)
        self.right_layout.setSpacing(2)
        self.right_layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)

        # Adicionar frames ao layout principal com fatores de esticamento
        self.horizontalLayout_content.addWidget(self.left_frame)
        self.horizontalLayout_content.addWidget(self.center_frame)
        self.horizontalLayout_content.addWidget(self.right_frame)
        self.horizontalLayout_content.setStretch(0, 1)
        self.horizontalLayout_content.setStretch(1, 0)
        self.horizontalLayout_content.setStretch(2, 1)

        self.verticalLayout.addWidget(self.content)
        MainWindow.setCentralWidget(self.centralwidget)

        # Adicionar as ComboBoxes aos frames laterais
        self.add_comboboxes()

        # Adicionar as CheckBoxes para Wi-Fi, Bluetooth e BLE abaixo da imagem
        self.add_checkboxes()

        # Conectar o botão "Generate Code" à função correspondente
        self.GenerateCode.clicked.connect(lambda: self.generate_file_with_selected_pins())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Agendar o ajuste dos layouts após a interface estar pronta
        QtCore.QTimer.singleShot(0, self.adjust_layouts)

        # Janela para exibir o código gerado
        self.code_window = None

    def adjust_layouts(self):
        # Obter a posição da imagem em relação ao widget 'content'
        image_pos = self.esp32Image.mapTo(self.content, QtCore.QPoint(0, 0))
        image_top_y = image_pos.y()

        # Obter a altura de uma ComboBox (com o estilo aplicado)
        combobox_height = self.get_combobox_height()

        # Calcular o deslocamento adicional
        offset = combobox_height * 3

        # Ajustar as margens superiores dos layouts laterais
        self.left_layout.setContentsMargins(10, image_top_y + offset, 10, 10)
        self.right_layout.setContentsMargins(10, image_top_y + offset, 10, 10)

    def get_combobox_height(self):
        # Criar uma ComboBox temporária para obter a altura
        temp_combo = QtWidgets.QComboBox()
        temp_combo.setMaximumHeight(20)
        temp_combo.setStyleSheet("""
        QComboBox {
            min-height: 20px;
            max-height: 20px;
        }
        """)
        temp_combo.adjustSize()
        height = temp_combo.sizeHint().height()
        temp_combo.deleteLater()
        return height

    def add_comboboxes(self):
        left_pins = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26", "D27", "D14", "D12", "D13", "GND1", "VIN"]
        right_pins = ["V3V3", "GND2", "D15", "D2", "D4", "RX2", "TX2", "D5", "D18", "D19", "D21", "RX0", "TX0", "D22", "D23"]

        # Altura das ComboBoxes
        combobox_height = 21

        # Adicionar ComboBoxes para pinos do lado esquerdo
        for pin_name in left_pins:
            combo = QtWidgets.QComboBox()
            combo.setMinimumWidth(150)
            combo.setMaximumHeight(combobox_height)
            combo.setStyleSheet(f"""
            QComboBox {{
                background-color: #4C566A;
                border: 1px solid #434C5E;
                border-radius: 2px;
                padding: 1px;
                color: #D8DEE9;
                min-height: {combobox_height}px;
                max-height: {combobox_height}px;
            }}
            QComboBox:hover {{
                border: 1px solid #81A1C1;
            }}
            QComboBox QAbstractItemView {{
                background-color: #4C566A;
                selection-background-color: #81A1C1;
                color: #ECEFF4;
            }}
            """)
            peripherals = self.get_peripherals_for_pin(pin_name)
            combo.addItems(peripherals)
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

        # Inverter a ordem dos pinos da direita
        right_pins_reversed = list(reversed(right_pins))

        # Adicionar ComboBoxes para pinos do lado direito
        for pin_name in right_pins_reversed:
            combo = QtWidgets.QComboBox()
            combo.setMinimumWidth(150)
            combo.setMaximumHeight(combobox_height)
            combo.setStyleSheet(f"""
            QComboBox {{
                background-color: #4C566A;
                border: 1px solid #434C5E;
                border-radius: 2px;
                padding: 1px;
                color: #D8DEE9;
                min-height: {combobox_height}px;
                max-height: {combobox_height}px;
            }}
            QComboBox:hover {{
                border: 1px solid #81A1C1;
            }}
            QComboBox QAbstractItemView {{
                background-color: #4C566A;
                selection-background-color: #81A1C1;
                color: #ECEFF4;
            }}
            """)
            peripherals = self.get_peripherals_for_pin(pin_name)
            combo.addItems(peripherals)
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
        self.checkboxes_frame.setObjectName("checkboxes_frame")
        self.checkboxes_frame.setStyleSheet("QFrame { background-color: transparent; }")
        self.verticalLayout_checkboxes = QtWidgets.QVBoxLayout(self.checkboxes_frame)
        self.verticalLayout_checkboxes.setContentsMargins(0, 10, 0, 0)
        self.verticalLayout_checkboxes.setSpacing(5)
        self.verticalLayout_checkboxes.setAlignment(QtCore.Qt.AlignCenter)

        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)

        self.checkBox_wifi = QtWidgets.QCheckBox(self.checkboxes_frame)
        self.checkBox_wifi.setFont(font)
        self.checkBox_wifi.setText("Wi-Fi")
        self.checkBox_wifi.setStyleSheet("""
        QCheckBox {
            color: #D8DEE9;
        }
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
        }
        """)
        self.verticalLayout_checkboxes.addWidget(self.checkBox_wifi)

        self.checkBox_bluetooth = QtWidgets.QCheckBox(self.checkboxes_frame)
        self.checkBox_bluetooth.setFont(font)
        self.checkBox_bluetooth.setText("Bluetooth")
        self.checkBox_bluetooth.setStyleSheet("""
        QCheckBox {
            color: #D8DEE9;
        }
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
        }
        """)
        self.verticalLayout_checkboxes.addWidget(self.checkBox_bluetooth)

        self.checkBox_ble = QtWidgets.QCheckBox(self.checkboxes_frame)
        self.checkBox_ble.setFont(font)
        self.checkBox_ble.setText("BLE")
        self.checkBox_ble.setStyleSheet("""
        QCheckBox {
            color: #D8DEE9;
        }
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
        }
        """)
        self.verticalLayout_checkboxes.addWidget(self.checkBox_ble)

        self.center_layout.addWidget(self.checkboxes_frame)

    def get_peripherals_for_pin(self, pin):
        peripherals = [f"Insert_{pin}"]

        gpio_pins = ["D2", "D4", "D5", "D12", "D13", "D14", "D15",
                     "RX2", "TX2", "D18", "D19", "D21", "D22", "D23",
                     "D25", "D26", "D27", "D32", "D33"]
        input_only_pins = ["VP", "VN", "D34", "D35"]
        adc_pins = ["D25", "D26", "D32", "D33", "D34", "D35", "VP", "VN"]
        dac_pins = ["D25", "D26"]
        touch_pins = ["D4", "D2", "D15", "D13", "D12", "D14", "D27", "D33", "D32"]

        if pin in gpio_pins:
            peripherals.extend(["GPIO_Input", "GPIO_Output"])
        if pin in input_only_pins:
            peripherals.append("GPIO_Input")
        if pin in adc_pins:
            peripherals.append("ADC")
        if pin in dac_pins:
            peripherals.append("DAC")
        if pin.startswith("TX") or pin.startswith("RX"):
            peripherals.append("UART")
        if pin == "D21" or pin == "D22":
            peripherals.append("I2C")
        if pin in ["D12", "D13", "D14", "D15"]:
            peripherals.extend(["SPI_Master_HSPI", "SPI_Slave_HSPI"])
        if pin in ["D19", "D23", "D18", "D5"]:
            peripherals.extend(["SPI_Master_VSPI", "SPI_Slave_VSPI"])
        if pin in touch_pins:
            peripherals.append("Touch")
        return peripherals

    def generate_file_with_selected_pins(self):
        project_name = self.lineEdit.text()
        if not project_name:
            QMessageBox.warning(None, "Aviso", "Por favor, insira um nome para o projeto.")
            return

        libraries = set()
        pin_definitions = []
        used_pins = set()
        pin_data = {}
        i2c_selected = False
        peripherals_used = set()
        adc_initialized = set()
        dac_initialized = set()
        spi_hspi_selected = False
        spi_vspi_selected = False

        # Dicionários para mapear pinos SPI
        hspi_pins = {}
        vspi_pins = {}

        for pin in dir(self):
            if pin.startswith("combo_"):
                combo = getattr(self, pin)
                pin_name = pin.replace("combo_", "")
                selected_peripheral = combo.currentText()
                pin_data[pin_name] = selected_peripheral

        # Verificar conflitos de pinos
        for pin_name, peripheral in pin_data.items():
            if peripheral != f"Insert_{pin_name}":
                if pin_name in used_pins:
                    QMessageBox.warning(None, "Conflito de Pinos", f"O pino {pin_name} está configurado para múltiplos periféricos.")
                    return
                else:
                    used_pins.add(pin_name)
                peripherals_used.add(peripheral.split('_')[0])  # Adicionar tipo de periférico

                # Coletar informações sobre SPI HSPI e VSPI
                if "SPI" in peripheral:
                    if "HSPI" in peripheral:
                        spi_hspi_selected = True
                        hspi_pins[pin_name] = peripheral
                    elif "VSPI" in peripheral:
                        spi_vspi_selected = True
                        vspi_pins[pin_name] = peripheral

        # Geração do cabeçalho do código
        header_comment = f"""/* Projeto: {project_name}

   Este código foi gerado automaticamente pela ferramenta ESP32 Tool.

   Instruções para compilação e upload:
   1. Configure o ESP-IDF em seu ambiente.
   2. Copie este código para o arquivo main.c de seu projeto.
   3. No terminal, navegue até o diretório do projeto.
   4. Execute 'idf.py build' para compilar o projeto.
   5. Conecte o ESP32 e execute 'idf.py flash' para carregar o código.
   
   Para mais informações, visite: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/

*/
"""
        code = header_comment + "\n"
        # Adicionar bibliotecas necessárias
        code += "// Bibliotecas necessárias\n"
        code += "#include <stdio.h>\n#include \"freertos/FreeRTOS.h\"\n#include \"freertos/task.h\"\n"
        
        # Adicionar bibliotecas com base nos periféricos selecionados
        for pin_name, peripheral in pin_data.items():
            if peripheral != f"Insert_{pin_name}":
                if "GPIO" in peripheral:
                    libraries.add("#include \"driver/gpio.h\"  // Biblioteca para GPIO")
                if "ADC" in peripheral:
                    libraries.add("#include \"driver/adc.h\"  // Biblioteca para ADC")
                    libraries.add("#include \"esp_adc_cal.h\"  // Biblioteca para calibração do ADC")
                if "DAC" in peripheral:
                    libraries.add("#include \"driver/dac.h\"  // Biblioteca para DAC")
                if "UART" in peripheral:
                    libraries.add("#include \"driver/uart.h\"  // Biblioteca para UART")
                if "I2C" in peripheral:
                    libraries.add("#include \"driver/i2c.h\"  // Biblioteca para I2C")
                if "SPI" in peripheral:
                    libraries.add("#include \"driver/spi_master.h\"  // Biblioteca para SPI")
                if "Touch" in peripheral:
                    libraries.add("#include \"driver/touch_pad.h\"  // Biblioteca para Touch Pad")

        # Adicionar bibliotecas para Wi-Fi, Bluetooth e BLE
        if self.checkBox_wifi.isChecked():
            libraries.add("#include \"esp_wifi.h\"  // Biblioteca para Wi-Fi")
        if self.checkBox_bluetooth.isChecked():
            libraries.add("#include \"esp_bt.h\"  // Biblioteca para Bluetooth")
        if self.checkBox_ble.isChecked():
            libraries.add("#include \"esp_bt.h\"  // Biblioteca para Bluetooth")
            libraries.add("#include \"esp_gap_ble_api.h\"  // Biblioteca para BLE")

        # Adicionar bibliotecas ao código
        if libraries:
            code += "\n".join(sorted(libraries)) + "\n"

        # Definição dos pinos utilizados
        pin_definitions_section = ""
        for pin_name, peripheral in pin_data.items():
            if peripheral != f"Insert_{pin_name}":
                gpio_num = self.get_gpio_number(pin_name)
                if gpio_num is not None:
                    pin_definitions_section += f"#define GPIO_{pin_name} {gpio_num}  // Pino {pin_name} do ESP32\n"

        # Definições adicionais para I2C
        if any(peripheral == "I2C" for peripheral in pin_data.values()):
            i2c_selected = True
            scl_pin = self.get_gpio_number("D22")  # SCL padrão
            sda_pin = self.get_gpio_number("D21")  # SDA padrão
            pin_definitions_section += f"#define I2C_SCL_PIN {scl_pin}  // Pino SCL do I2C\n"
            pin_definitions_section += f"#define I2C_SDA_PIN {sda_pin}  // Pino SDA do I2C\n"

        # Definições adicionais para SPI HSPI
        if spi_hspi_selected:
            # Mapear os pinos HSPI
            hspi_default_pins = {
                "MISO": "D12",
                "MOSI": "D13",
                "CLK": "D14",
                "CS": "D15"
            }
            pin_definitions_section += "\n// Definição dos pinos HSPI\n"
            for role, default_pin in hspi_default_pins.items():
                gpio_num = self.get_gpio_number(default_pin)
                pin_definitions_section += f"#define HSPI_{role}_PIN {gpio_num}  // Pino {role} do HSPI\n"

        # Definições adicionais para SPI VSPI
        if spi_vspi_selected:
            # Mapear os pinos VSPI
            vspi_default_pins = {
                "MISO": "D19",
                "MOSI": "D23",
                "CLK": "D18",
                "CS": "D5"
            }
            pin_definitions_section += "\n// Definição dos pinos VSPI\n"
            for role, default_pin in vspi_default_pins.items():
                gpio_num = self.get_gpio_number(default_pin)
                pin_definitions_section += f"#define VSPI_{role}_PIN {gpio_num}  // Pino {role} do VSPI\n"

        if pin_definitions_section:
            code += "\n// Definição dos pinos utilizados\n" + pin_definitions_section

        code += "\nvoid app_main(void) {\n"

        # Declarar variáveis de configuração uma única vez
        if "GPIO" in peripherals_used or "Touch" in peripherals_used:
            code += "    gpio_config_t io_conf;\n"
        if "ADC" in peripherals_used:
            code += "    adc1_channel_t adc1_channel;\n"
            code += "    adc2_channel_t adc2_channel;\n"
            code += "    esp_adc_cal_characteristics_t adc_chars;\n"
        if "DAC" in peripherals_used:
            code += "    // DAC não requer configurações adicionais\n"
        if "UART" in peripherals_used:
            code += "    uart_config_t uart_config;\n"
        if "I2C" in peripherals_used:
            code += "    i2c_config_t conf;\n"
        if "SPI" in peripherals_used:
            code += "    spi_bus_config_t buscfg;\n"
        code += "\n"

        # Funções de inicialização para ADC e DAC
        if "ADC" in peripherals_used:
            code += "    // Inicialização do ADC\n"
            code += "    adc1_config_width(ADC_WIDTH_BIT_12);\n"
            code += "    esp_adc_cal_characterize(ADC_UNIT_1, ADC_ATTEN_DB_11, ADC_WIDTH_BIT_12, 0, &adc_chars);\n\n"
        if "DAC" in peripherals_used:
            code += "    // Inicialização do DAC\n"
            for pin_name, peripheral in pin_data.items():
                if "DAC" in peripheral:
                    dac_channel = self.get_dac_channel(pin_name)
                    if dac_channel is not None and dac_channel not in dac_initialized:
                        code += f"    dac_output_enable({dac_channel});  // Habilita o DAC no pino {pin_name}\n"
                        dac_initialized.add(dac_channel)
            code += "\n"

        # Código de inicialização dos periféricos
        for pin_name, peripheral in pin_data.items():
            if peripheral != f"Insert_{pin_name}":
                if "GPIO" in peripheral:
                    code += f"    // Configuração do GPIO {pin_name} como {'entrada' if 'Input' in peripheral else 'saída'}\n"
                    code += f"    io_conf.pin_bit_mask = (1ULL << GPIO_{pin_name});  // Seleciona o pino\n"
                    if "Input" in peripheral:
                        code += f"    io_conf.mode = GPIO_MODE_INPUT;  // Modo de entrada\n"
                    elif "Output" in peripheral:
                        code += f"    io_conf.mode = GPIO_MODE_OUTPUT;  // Modo de saída\n"
                    code += f"    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;  // Desabilita pull-up\n"
                    code += f"    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;  // Desabilita pull-down\n"
                    code += f"    io_conf.intr_type = GPIO_INTR_DISABLE;  // Desabilita interrupções\n"
                    code += f"    gpio_config(&io_conf);  // Aplica configurações\n"
                    code += "\n"

                if "ADC" in peripheral:
                    adc_channel = self.get_adc_channel(pin_name)
                    if adc_channel is not None:
                        if adc_channel.startswith("ADC1"):
                            code += f"    // Configuração do ADC1 no pino {pin_name}\n"
                            code += f"    adc1_channel = {adc_channel};\n"
                            code += f"    adc1_config_channel_atten(adc1_channel, ADC_ATTEN_DB_11);\n"
                        elif adc_channel.startswith("ADC2"):
                            code += f"    // Configuração do ADC2 no pino {pin_name}\n"
                            code += f"    adc2_channel = {adc_channel};\n"
                            code += f"    adc2_config_channel_atten(adc2_channel, ADC_ATTEN_DB_11);\n"
                        code += "\n"

                if "DAC" in peripheral:
                    # A inicialização do DAC já foi feita anteriormente
                    pass

                if "UART" in peripheral:
                    uart_num = self.get_uart_number(pin_name)
                    if uart_num is not None:
                        code += f"    // Configuração do UART no pino {pin_name}\n"
                        code += f"    uart_config.baud_rate = 115200;  // Taxa de transmissão\n"
                        code += f"    uart_config.data_bits = UART_DATA_8_BITS;  // 8 bits de dados\n"
                        code += f"    uart_config.parity = UART_PARITY_DISABLE;  // Sem paridade\n"
                        code += f"    uart_config.stop_bits = UART_STOP_BITS_1;  // 1 bit de parada\n"
                        code += f"    uart_config.flow_ctrl = UART_HW_FLOWCTRL_DISABLE;  // Sem controle de fluxo\n"
                        code += f"    uart_param_config({uart_num}, &uart_config);  // Aplica configurações\n"
                        code += "\n"

                if "I2C" in peripheral and i2c_selected:
                    code += f"    // Configuração do I2C\n"
                    code += f"    conf.mode = I2C_MODE_MASTER;  // Modo Mestre\n"
                    code += f"    conf.sda_io_num = I2C_SDA_PIN;  // Pino SDA\n"
                    code += f"    conf.scl_io_num = I2C_SCL_PIN;  // Pino SCL\n"
                    code += f"    conf.sda_pullup_en = GPIO_PULLUP_ENABLE;  // Habilita pull-up no SDA\n"
                    code += f"    conf.scl_pullup_en = GPIO_PULLUP_ENABLE;  // Habilita pull-up no SCL\n"
                    code += f"    conf.master.clk_speed = 100000;  // Velocidade de 100kHz\n"
                    code += f"    // Para modo Slave, altere 'conf.mode = I2C_MODE_SLAVE' e adicione as configurações de slave\n"
                    code += f"    i2c_param_config(I2C_NUM_0, &conf);  // Aplica configurações\n"
                    code += f"    i2c_driver_install(I2C_NUM_0, conf.mode, 0, 0, 0);  // Instala driver I2C\n"
                    code += "\n"
                    i2c_selected = False  # Evitar duplicação

        # Inicialização do HSPI
        if spi_hspi_selected:
            code += f"    // Configuração do HSPI\n"
            code += f"    buscfg.miso_io_num = HSPI_MISO_PIN;  // Pino MISO\n"
            code += f"    buscfg.mosi_io_num = HSPI_MOSI_PIN;  // Pino MOSI\n"
            code += f"    buscfg.sclk_io_num = HSPI_CLK_PIN;   // Pino CLK\n"
            code += f"    buscfg.quadwp_io_num = -1;\n"
            code += f"    buscfg.quadhd_io_num = -1;\n"
            code += f"    buscfg.max_transfer_sz = 4096;\n"
            code += f"    spi_bus_initialize(HSPI_HOST, &buscfg, 1);\n"
            code += "\n"

        # Inicialização do VSPI
        if spi_vspi_selected:
            code += f"    // Configuração do VSPI\n"
            code += f"    buscfg.miso_io_num = VSPI_MISO_PIN;  // Pino MISO\n"
            code += f"    buscfg.mosi_io_num = VSPI_MOSI_PIN;  // Pino MOSI\n"
            code += f"    buscfg.sclk_io_num = VSPI_CLK_PIN;   // Pino CLK\n"
            code += f"    buscfg.quadwp_io_num = -1;\n"
            code += f"    buscfg.quadhd_io_num = -1;\n"
            code += f"    buscfg.max_transfer_sz = 4096;\n"
            code += f"    spi_bus_initialize(VSPI_HOST, &buscfg, 1);\n"
            code += "\n"

        # Adicionar código de inicialização para Wi-Fi, Bluetooth e BLE
        if self.checkBox_wifi.isChecked():
            code += f"    // Configuração do Wi-Fi\n"
            code += f"    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();  // Configurações padrão\n"
            code += f"    esp_wifi_init(&cfg);  // Inicializa Wi-Fi\n"
            code += f"    esp_wifi_set_mode(WIFI_MODE_STA);  // Modo Station\n"
            code += f"    esp_wifi_start();  // Inicia Wi-Fi\n"
            code += f"    // Para configurar SSID e senha, utilize esp_wifi_set_config()\n"
            code += "\n"

        if self.checkBox_bluetooth.isChecked():
            code += f"    // Configuração do Bluetooth\n"
            code += f"    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();  // Configurações padrão\n"
            code += f"    esp_bt_controller_init(&bt_cfg);  // Inicializa controlador BT\n"
            code += f"    esp_bt_controller_enable(ESP_BT_MODE_CLASSIC_BT);  // Habilita Bluetooth clássico\n"
            code += f"    // Adicione código para perfil e serviços Bluetooth\n"
            code += "\n"

        if self.checkBox_ble.isChecked():
            code += f"    // Configuração do BLE\n"
            code += f"    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();  // Configurações padrão\n"
            code += f"    esp_bt_controller_init(&bt_cfg);  // Inicializa controlador BT\n"
            code += f"    esp_bt_controller_enable(ESP_BT_MODE_BLE);  // Habilita BLE\n"
            code += f"    esp_bluedroid_init();  // Inicializa Bluedroid\n"
            code += f"    esp_bluedroid_enable();  // Habilita Bluedroid\n"
            code += f"    // Adicione código para GAP, GATT e perfis BLE\n"
            code += "\n"

        code += "    // Seu código aqui\n"
        code += "}\n"

        # Exibir o código em uma nova janela
        self.show_code_window(code, project_name)

    def show_code_window(self, code, project_name):
        self.code_window = QtWidgets.QWidget()
        self.code_window.setWindowTitle(f"Código Gerado - {project_name}")
        self.code_window.resize(800, 600)
        self.code_window.setStyleSheet("""
        QWidget {
            background-color: #2E3440;
            color: #D8DEE9;
        }
        """)

        layout = QtWidgets.QVBoxLayout(self.code_window)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        self.code_edit = QtWidgets.QTextEdit(self.code_window)
        self.code_edit.setReadOnly(True)
        self.code_edit.setStyleSheet("""
        QTextEdit {
            background-color: #3B4252;
            color: #ECEFF4;
            font-family: Consolas, monospace;
            font-size: 12pt;
            border: 1px solid #4C566A;
            border-radius: 5px;
            padding: 10px;
        }
        """)
        self.code_edit.setText(code)
        layout.addWidget(self.code_edit)

        # Botões de ação
        buttons_layout = QtWidgets.QHBoxLayout()
        buttons_layout.setSpacing(10)

        # Botão para copiar o código
        copy_button = QtWidgets.QPushButton("Copy Code")
        copy_button.setMinimumSize(QtCore.QSize(150, 30))
        copy_button.setStyleSheet("""
        QPushButton {
            background-color: #81A1C1;
            border: none;
            border-radius: 5px;
            color: #ECEFF4;
        }
        QPushButton:hover {
            background-color: #5E81AC;
        }
        """)
        copy_button.clicked.connect(self.copy_code)
        buttons_layout.addWidget(copy_button)

        # Botão para exportar como arquivo .c
        export_button = QtWidgets.QPushButton("Export as .c File")
        export_button.setMinimumSize(QtCore.QSize(150, 30))
        export_button.setStyleSheet("""
        QPushButton {
            background-color: #A3BE8C;
            border: none;
            border-radius: 5px;
            color: #ECEFF4;
        }
        QPushButton:hover {
            background-color: #8FBCBB;
        }
        """)
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
            with open(file_path, "w") as file:
                file.write(code)
            QMessageBox.information(None, "Sucesso", f"Código salvo em {file_path}")

    def get_gpio_number(self, pin_name):
        gpio_mapping = {
            "D2": "2", "D4": "4", "D5": "5", "D12": "12", "D13": "13",
            "D14": "14", "D15": "15", "RX2": "16", "TX2": "17", "D18": "18",
            "D19": "19", "D21": "21", "D22": "22", "D23": "23", "D25": "25",
            "D26": "26", "D27": "27", "D32": "32", "D33": "33", "D34": "34", "D35": "35",
            "VP": "36", "VN": "39", "RX0": "3", "TX0": "1"
        }
        return gpio_mapping.get(pin_name)

    def get_adc_channel(self, pin_name):
        adc_mapping = {
            "D32": "ADC1_CHANNEL_4", "D33": "ADC1_CHANNEL_5",
            "D34": "ADC1_CHANNEL_6", "D35": "ADC1_CHANNEL_7",
            "VP": "ADC1_CHANNEL_0", "VN": "ADC1_CHANNEL_3",
            "D25": "ADC2_CHANNEL_8", "D26": "ADC2_CHANNEL_9"
        }
        return adc_mapping.get(pin_name)

    def get_dac_channel(self, pin_name):
        dac_mapping = {
            "D25": "DAC_CHANNEL_1", "D26": "DAC_CHANNEL_2"
        }
        return dac_mapping.get(pin_name)

    def get_uart_number(self, pin_name):
        uart_mapping = {
            "TX0": "UART_NUM_0", "RX0": "UART_NUM_0",
            "TX2": "UART_NUM_2", "RX2": "UART_NUM_2"
        }
        return uart_mapping.get(pin_name)

    def get_touch_pad_num(self, pin_name):
        touch_pads = {
            "D4": 0, "D0": 1, "D2": 2, "D15": 3, "D13": 4,
            "D12": 5, "D14": 6, "D27": 7, "D33": 8, "D32": 9
        }
        return touch_pads.get(pin_name)

    def retranslateUi(self, MainWindow):
        pass

# Código principal para executar a aplicação
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle("Fusion")

    palette = QtGui.QPalette()
    palette.setColor(QtGui.QPalette.Window, QtGui.QColor("#2E3440"))
    palette.setColor(QtGui.QPalette.WindowText, QtGui.QColor("#D8DEE9"))
    palette.setColor(QtGui.QPalette.Base, QtGui.QColor("#3B4252"))
    palette.setColor(QtGui.QPalette.Text, QtGui.QColor("#ECEFF4"))
    app.setPalette(palette)

    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()

    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
