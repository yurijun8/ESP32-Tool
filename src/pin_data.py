'''
This is the pin_data module. It contains the data structures and functions for managing pin configurations.
'''

# Mapping of pin names to their corresponding GPIO numbers, ADC channels, DAC channels, UART numbers, and touch sensor numbers.

LEFT_PINS = ["EN", "VP", "VN", "D34", "D35", "D32", "D33", "D25", "D26", "D27", "D14", "D12", "D13", "GND1", "VIN"]
RIGHT_PINS = ["V3V3", "GND2", "D15", "D2", "D4", "RX2", "TX2", "D5", "D18", "D19", "D21", "RX0", "TX0", "D22", "D23"]

GPIO_MAPPING = {
    "D2": "2", "D4": "4", "D5": "5", "D12": "12", "D13": "13",
    "D14": "14", "D15": "15", "RX2": "16", "TX2": "17", "D18": "18",
    "D19": "19", "D21": "21", "D22": "22", "D23": "23", "D25": "25",
    "D26": "26", "D27": "27", "D32": "32", "D33": "33", "D34": "34", "D35": "35",
    "VP": "36", "VN": "39", "RX0": "3", "TX0": "1"
}

ADC_MAPPING = {
    "D32": "ADC1_CHANNEL_4", "D33": "ADC1_CHANNEL_5",
    "D34": "ADC1_CHANNEL_6", "D35": "ADC1_CHANNEL_7",
    "VP": "ADC1_CHANNEL_0", "VN": "ADC1_CHANNEL_3",
    "D25": "ADC2_CHANNEL_8", "D26": "ADC2_CHANNEL_9",
    "D4": "ADC2_CHANNEL_0", "D2": "ADC2_CHANNEL_2",
    "D15": "ADC2_CHANNEL_3", "D13": "ADC2_CHANNEL_4",
    "D12": "ADC2_CHANNEL_5", "D14": "ADC2_CHANNEL_6",
    "D27": "ADC2_CHANNEL_7"
}

DAC_MAPPING = {
    "D25": "DAC_CHANNEL_1", "D26": "DAC_CHANNEL_2"
}

UART_MAPPING = {
    "TX0": "UART_NUM_0", "RX0": "UART_NUM_0",
    "TX2": "UART_NUM_2", "RX2": "UART_NUM_2"
}

TOUCH_MAPPING = {
    "D4": 0, "D2": 2, "D15": 3, "D13": 4,
    "D12": 5, "D14": 6, "D27": 7, "D33": 8, "D32": 9
}

def get_peripherals_for_pin(pin):
    peripherals = [f"Insert_{pin}"]
    gpio_pins = ["D2", "D4", "D5", "D12", "D13", "D14", "D15",
                 "RX2", "TX2", "D18", "D19", "D21", "D22", "D23",
                 "D25", "D26", "D27", "D32", "D33"]
    input_only_pins = ["VP", "VN", "D34", "D35"]
    adc_pins = list(ADC_MAPPING.keys())
    dac_pins = list(DAC_MAPPING.keys())
    touch_pins = list(TOUCH_MAPPING.keys())

    if pin in gpio_pins:
        peripherals.extend(["GPIO_Input", "GPIO_Output", "PWM"])
    if pin in input_only_pins:
        peripherals.append("GPIO_Input")
    if pin in adc_pins:
        peripherals.append("ADC")
    if pin in dac_pins:
        peripherals.append("DAC")
    if pin.startswith("TX") or pin.startswith("RX"):
        peripherals.append("UART")
    if pin in ["D21", "D22"]:
        peripherals.append("I2C")
    if pin in ["D12", "D13", "D14", "D15"]:
        peripherals.extend(["SPI_Master_HSPI", "SPI_Slave_HSPI"])
    if pin in ["D19", "D23", "D18", "D5"]:
        peripherals.extend(["SPI_Master_VSPI", "SPI_Slave_VSPI"])
    if pin in touch_pins:
        peripherals.append("Touch")
    return peripherals