# ESP32-Tool

### Description

ESP32 Tool is a graphical desktop application built with Python and PyQt5 that simplifies the configuration and generation of starter code for ESP32 peripherals. The tool allows you to select the desired peripherals for each available pin and automatically generates the corresponding C configuration code for the ESP-IDF framework.

### Features

- **Intuitive peripheral selection for available ESP32 pins.**
  
- **Support for various peripherals:**
    - GPIO (Input and Output)
    - PWM (LEDC)
    - ADC (Analog-to-Digital Converter)
    - DAC (Digital-to-Analog Converter)
    - UART
    - I2C (Master/Slave)
    - SPI (Master/Slave - HSPI/VSPI)
    - Touch Pad
    - Toggles for Wi-Fi, Bluetooth, and BLE.
    
- **Automatic C code generation featuring:**
    - Commented header with setup instructions.
    - Modular initialization of selected peripherals using Jinja2 templates.
    - Exporting the generated code as a `.c` file.
    - Copying the generated code directly to the clipboard.
    - Syntax highlighting support in the code preview window.
- **Project Presets:**
    - Save and load your configuration states using JSON preset files.

### Prerequisites

1. **Python 3.7+**
   - Install Python: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **Python Dependencies**
   - Install the required packages with:
     ```bash
     pip install -r requirements.txt
     ```

3. **ESP-IDF**
   - Configured and installed in your development environment.
   - Instructions: [Get Started with ESP-IDF](https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/)

4. **ESP32 Image & Assets**
   - Ensure the board image `esp32-wroom-32.png` is located inside the `src/` directory.

### How to Use

1. **Start the application**
   - Execute the main entry point:
     ```bash
     python main.py
     ```

2. **Configure the peripherals**
   - Enter your project name in the top input field.
   - Select the desired peripherals for each pin using the dropdown menus (ComboBoxes) on the left and right sides of the interface.
   - Toggle Wi-Fi, Bluetooth, or BLE options if needed.
   - Optionally, use the **Save Preset** or **Load Preset** buttons to manage configuration profiles.

3. **Generate the code**
   - Click the **Generate Code** button.
   - The code will be displayed in a new syntax-highlighted window.
   - You can copy it to your clipboard or export it as a `.c` file.

4. **Build and flash the code to the ESP32**
   - Copy the generated code into the `main.c` file of an ESP-IDF project.
   - Build the project:
     ```bash
     idf.py build
     ```
   - Flash the code to your ESP32 board:
     ```bash
     idf.py flash
     ```