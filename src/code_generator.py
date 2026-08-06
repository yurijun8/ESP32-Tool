'''
This is the responsible for the code generation of the application. It takes the user inputs and generates the corresponding code for the ESP32 microcontroller.

'''
import os
from jinja2 import Environment, FileSystemLoader
from .pin_data import GPIO_MAPPING, ADC_MAPPING, DAC_MAPPING, UART_MAPPING, TOUCH_MAPPING

def generate_c_code(project_name, pin_data, wifi_checked, bt_checked, ble_checked):
    template_dir = os.path.join(os.path.dirname(__file__), "templates")
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template("main_c.j2")

    libraries = set()
    pin_definitions = []
    peripheral_inits = []
    dac_inits = set()
    pwm_inits = []
    next_pwm_channel = 0

    needs_gpio_conf = False
    needs_adc = False
    needs_uart = False
    needs_i2c = False
    needs_spi = False
    spi_hspi_selected = False
    spi_vspi_selected = False

    for pin_name, peripheral in pin_data.items():
        if peripheral != f"Insert_{pin_name}":
            if "GPIO" in peripheral:
                libraries.add('#include "driver/gpio.h"')
                needs_gpio_conf = True
            if "ADC" in peripheral:
                libraries.add('#include "driver/adc.h"')
                libraries.add('#include "esp_adc_cal.h"')
                needs_adc = True
            if "DAC" in peripheral:
                libraries.add('#include "driver/dac.h"')
            if "UART" in peripheral:
                libraries.add('#include "driver/uart.h"')
            if "I2C" in peripheral:
                libraries.add('#include "driver/i2c.h"')
                needs_i2c = True
            if "SPI" in peripheral:
                libraries.add('#include "driver/spi_master.h"')
                needs_spi = True
                if "HSPI" in peripheral:
                    spi_hspi_selected = True
                elif "VSPI" in peripheral:
                    spi_vspi_selected = True
            if "Touch" in peripheral:
                libraries.add('#include "driver/touch_pad.h"')
                needs_gpio_conf = True
            if "PWM" in peripheral:
                libraries.add('#include "driver/ledc.h"')

    if wifi_checked:
        libraries.add('#include "esp_wifi.h"')
        libraries.add('#include "esp_event.h"')
        libraries.add('#include "esp_netif.h"')
    if bt_checked or ble_checked:
        libraries.add('#include "esp_bt.h"')
        libraries.add('#include "esp_bt_main.h"')
    if ble_checked:
        libraries.add('#include "esp_gap_ble_api.h"')
        libraries.add('#include "esp_gatts_api.h"')
        libraries.add('#include "nvs_flash.h"')

    for pin_name, peripheral in pin_data.items():
        if peripheral != f"Insert_{pin_name}":
            gpio_num = GPIO_MAPPING.get(pin_name)
            if gpio_num:
                pin_definitions.append(f"#define GPIO_{pin_name} {gpio_num}  // Pino {pin_name}")

    if needs_i2c:
        pin_definitions.append(f"#define I2C_SCL_PIN {GPIO_MAPPING.get('D22')}  // Pino SCL do I2C")
        pin_definitions.append(f"#define I2C_SDA_PIN {GPIO_MAPPING.get('D21')}  // Pino SDA do I2C")

    if spi_hspi_selected:
        pin_definitions.append("// Definição dos pinos HSPI")
        hspi_pins = {"MISO": "D12", "MOSI": "D13", "CLK": "D14", "CS": "D15"}
        for role, default_pin in hspi_pins.items():
            pin_definitions.append(f"#define HSPI_{role}_PIN {GPIO_MAPPING.get(default_pin)}")

    if spi_vspi_selected:
        pin_definitions.append("// Definição dos pinos VSPI")
        vspi_pins = {"MISO": "D19", "MOSI": "D23", "CLK": "D18", "CS": "D5"}
        for role, default_pin in vspi_pins.items():
            pin_definitions.append(f"#define VSPI_{role}_PIN {GPIO_MAPPING.get(default_pin)}")

    i2c_done = False
    for pin_name, peripheral in pin_data.items():
        if peripheral != f"Insert_{pin_name}":
            if "GPIO" in peripheral:
                is_input = "Input" in peripheral
                init_code = f"""// Configuração do GPIO {pin_name} como {'entrada' if is_input else 'saída'}
    io_conf.pin_bit_mask = (1ULL << GPIO_{pin_name});
    io_conf.mode = {'GPIO_MODE_INPUT' if is_input else 'GPIO_MODE_OUTPUT'};
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;
    io_conf.intr_type = GPIO_INTR_DISABLE;
    gpio_config(&io_conf);"""
                peripheral_inits.append(init_code)

            elif "ADC" in peripheral:
                adc_ch = ADC_MAPPING.get(pin_name)
                if adc_ch:
                    peripheral_inits.append(f"// Configuração do ADC no pino {pin_name}\n    { 'adc1_channel = ' if 'ADC1' in adc_ch else 'adc2_channel = ' }{adc_ch};\n    { 'adc1_config_channel_atten' if 'ADC1' in adc_ch else 'adc2_config_channel_atten' }({ 'adc1_channel' if 'ADC1' in adc_ch else 'adc2_channel' }, ADC_ATTEN_DB_11);")

            elif "DAC" in peripheral:
                dac_ch = DAC_MAPPING.get(pin_name)
                if dac_ch and dac_ch not in dac_inits:
                    dac_inits.add(f"dac_output_enable({dac_ch});  // Habilita DAC no pino {pin_name}")

            elif "UART" in peripheral:
                uart_num = UART_MAPPING.get(pin_name)
                if uart_num:
                    peripheral_inits.append(f"""// Configuração do UART no pino {pin_name}
    uart_config.baud_rate = 115200;
    uart_config.data_bits = UART_DATA_8_BITS;
    uart_config.parity = UART_PARITY_DISABLE;
    uart_config.stop_bits = UART_STOP_BITS_1;
    uart_config.flow_ctrl = UART_HW_FLOWCTRL_DISABLE;
    uart_param_config({uart_num}, &uart_config);""")

            elif "I2C" in peripheral and not i2c_done:
                peripheral_inits.append("""// Configuração do I2C
    conf.mode = I2C_MODE_MASTER;
    conf.sda_io_num = I2C_SDA_PIN;
    conf.scl_io_num = I2C_SCL_PIN;
    conf.sda_pullup_en = GPIO_PULLUP_ENABLE;
    conf.scl_pullup_en = GPIO_PULLUP_ENABLE;
    conf.master.clk_speed = 100000;
    i2c_param_config(I2C_NUM_0, &conf);
    i2c_driver_install(I2C_NUM_0, conf.mode, 0, 0, 0);""")
                i2c_done = True

            elif "Touch" in peripheral:
                touch_num = TOUCH_MAPPING.get(pin_name, 0)
                peripheral_inits.append(f"""// Inicialização e configuração do Touch Pad no pino {pin_name} (Pad {touch_num})
    touch_pad_init();
    touch_pad_set_voltage(TOUCH_HREF_2P7V, TOUCH_LREF_0P5V, TOUCH_ATTEN_DEFAULT);
    touch_pad_config(TOUCH_PAD_NUM{touch_num}, 0);""")

            elif "PWM" in peripheral:
                if next_pwm_channel < 8:
                    pwm_inits.append(f"""// Configuração do canal PWM para o pino {pin_name}
    ledc_channel_config_t ledc_channel_{next_pwm_channel} = {{
        .channel    = LEDC_CHANNEL_{next_pwm_channel},
        .duty       = 0,
        .gpio_num   = GPIO_{pin_name},
        .speed_mode = LEDC_LOW_SPEED_MODE,
        .hpoint     = 0,
        .timer_sel  = LEDC_TIMER_0
    }};
    ledc_channel_config(&ledc_channel_{next_pwm_channel});""")
                    next_pwm_channel += 1

    context = {
        "project_name": project_name,
        "libraries": sorted(list(libraries)),
        "pin_definitions": pin_definitions,
        "needs_gpio_conf": needs_gpio_conf,
        "needs_adc": needs_adc,
        "needs_uart": needs_uart,
        "needs_i2c": needs_i2c,
        "needs_spi": needs_spi,
        "dac_inits": list(dac_inits),
        "peripheral_inits": peripheral_inits,
        "pwm_inits": pwm_inits,
        "hspi_init": spi_hspi_selected,
        "vspi_init": spi_vspi_selected,
        "wifi_init": wifi_checked,
        "bt_init": bt_checked,
        "ble_init": ble_checked
    }

    return template.render(context)