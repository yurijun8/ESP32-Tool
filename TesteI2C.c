
/* Projeto: I2CT - Leitura BMP280 via I2C

   Este código foi gerado automaticamente pela ferramenta ESP32 Tool e atualizado para usar o BMP280.

   Instruções para compilação e upload:
   1. Configure o ESP-IDF em seu ambiente.
   2. Copie este código para o arquivo main.c de seu projeto.
   3. No terminal, navegue até o diretório do projeto.
   4. Execute 'idf.py build' para compilar o projeto.
   5. Conecte o ESP32 e execute 'idf.py flash' para carregar o código.
   
   Para mais informações, visite: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/
*/

// Bibliotecas necessárias
#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2c.h"
#include "esp_log.h"
#include <inttypes.h>  // Para usar PRId32

// Definição dos pinos utilizados
#define I2C_SCL_PIN 22  // Pino SCL do I2C
#define I2C_SDA_PIN 21  // Pino SDA do I2C
#define BMP280_ADDRESS 0x37  // Endereço I2C do BMP280

// Registradores do BMP280
#define BMP280_REG_ID 0xD0
#define BMP280_REG_TEMP_PRESS_CALIB 0x88
#define BMP280_REG_CTRL_MEAS 0xF4
#define BMP280_REG_CONFIG 0xF5
#define BMP280_REG_PRESS_MSB 0xF7

static const char *TAG = "BMP280";

// Função para inicializar o BMP280
void bmp280_init() {
    uint8_t chip_id;

    // Lê o ID do sensor (0x58 para BMP280)
    i2c_master_write_read_device(I2C_NUM_0, BMP280_ADDRESS, (uint8_t[]){BMP280_REG_ID}, 1, &chip_id, 1, 1000 / portTICK_PERIOD_MS);
    ESP_LOGI(TAG, "BMP280 Chip ID: 0x%02X", chip_id);

    if (chip_id != 0x58) {
        ESP_LOGE(TAG, "ID incorreto. Verifique conexões e endereços!");
        return;
    }

    // Configurações iniciais do sensor
    uint8_t config_data[2];

    // Configura o sensor: oversampling e modo normal
    config_data[0] = BMP280_REG_CTRL_MEAS;
    config_data[1] = 0x27;  // Temperatura x1, Pressão x1, Modo Normal
    i2c_master_write_to_device(I2C_NUM_0, BMP280_ADDRESS, config_data, 2, 1000 / portTICK_PERIOD_MS);

    // Configura o filtro e o tempo de espera
    config_data[0] = BMP280_REG_CONFIG;
    config_data[1] = 0xA0;  // Filtro x4, tempo de espera 1ms
    i2c_master_write_to_device(I2C_NUM_0, BMP280_ADDRESS, config_data, 2, 1000 / portTICK_PERIOD_MS);
}

// Função para ler pressão e temperatura
void bmp280_read() {
    uint8_t data[6];
    int32_t adc_pressure, adc_temperature;

    // Lê os dados de pressão e temperatura
    i2c_master_write_read_device(I2C_NUM_0, BMP280_ADDRESS, (uint8_t[]){BMP280_REG_PRESS_MSB}, 1, data, 6, 1000 / portTICK_PERIOD_MS);

    // Combina os bytes em valores de 20 bits para pressão e temperatura
    adc_pressure = (int32_t)(((uint32_t)data[0] << 16) | ((uint32_t)data[1] << 8) | (uint32_t)data[2]) >> 4;
    adc_temperature = (int32_t)(((uint32_t)data[3] << 16) | ((uint32_t)data[4] << 8) | (uint32_t)data[5]) >> 4;

    // Use PRId32 para formatar corretamente int32_t
    ESP_LOGI(TAG, "ADC Pressure: %" PRId32 ", ADC Temperature: %" PRId32, adc_pressure, adc_temperature);

    // Conversão para valores reais (simplificado, ajustes adicionais podem ser feitos usando os coeficientes de calibração do BMP280)
    float pressure = adc_pressure / 256.0;
    float temperature = adc_temperature / 5120.0;

    ESP_LOGI(TAG, "Pressão: %.2f Pa, Temperatura: %.2f °C", pressure, temperature);
}

// Função principal
void app_main(void) {
    i2c_config_t conf;

    // Configuração do I2C
    conf.mode = I2C_MODE_MASTER;  // Modo Mestre
    conf.sda_io_num = I2C_SDA_PIN;  // Pino SDA
    conf.scl_io_num = I2C_SCL_PIN;  // Pino SCL
    conf.sda_pullup_en = GPIO_PULLUP_ENABLE;  // Habilita pull-up no SDA
    conf.scl_pullup_en = GPIO_PULLUP_ENABLE;  // Habilita pull-up no SCL
    conf.master.clk_speed = 100000;  // Velocidade de 100kHz
    i2c_param_config(I2C_NUM_0, &conf);  // Aplica configurações
    i2c_driver_install(I2C_NUM_0, conf.mode, 0, 0, 0);  // Instala driver I2C

    // Inicializa o BMP280
    bmp280_init();

    // Loop para leitura contínua
    while (1) {
        bmp280_read();
        vTaskDelay(2000 / portTICK_PERIOD_MS);
    }
}
