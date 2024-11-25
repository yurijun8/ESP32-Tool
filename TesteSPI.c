/* Projeto: TesteSPI_ST7735S

   Este código foi gerado automaticamente pela ferramenta ESP32 Tool e modificado para usar o display ST7735S.

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
#include "driver/spi_master.h"
#include "driver/gpio.h"
#include "esp_log.h"

// Definição dos pinos do SPI
#define VSPI_MOSI_PIN 23  // SDA do display
#define VSPI_CLK_PIN 18   // SCL do display
#define VSPI_CS_PIN 5     // CS do display
#define VSPI_DC_PIN 21    // DC do display
#define VSPI_RST_PIN 22   // RES do display

// Tag para logs
static const char *TAG = "ST7735S";

// Comandos do ST7735S
#define CMD_SWRESET 0x01  // Software Reset
#define CMD_SLPOUT  0x11  // Sleep Out
#define CMD_DISPON  0x29  // Display ON
#define CMD_CASET   0x2A  // Column Address Set
#define CMD_RASET   0x2B  // Row Address Set
#define CMD_RAMWR   0x2C  // Write to RAM
#define CMD_MADCTL  0x36  // Memory Data Access Control
#define CMD_COLMOD  0x3A  // Interface Pixel Format

spi_device_handle_t spi;

// Função para enviar comandos via SPI
void spi_send_command(uint8_t cmd) {
    gpio_set_level(VSPI_DC_PIN, 0);  // Seleciona modo comando
    spi_transaction_t t = {
        .length = 8,  // Envia 1 byte (8 bits)
        .tx_buffer = &cmd
    };
    spi_device_polling_transmit(spi, &t);
}

// Função para enviar dados via SPI
void spi_send_data(const uint8_t *data, size_t len) {
    gpio_set_level(VSPI_DC_PIN, 1);  // Seleciona modo dados
    spi_transaction_t t = {
        .length = len * 8,  // Envia 'len' bytes
        .tx_buffer = data
    };
    spi_device_polling_transmit(spi, &t);
}

// Inicialização do ST7735S
void st7735s_init() {
    ESP_LOGI(TAG, "Inicializando ST7735S");

    // Configura pinos RST e DC
    gpio_set_direction(VSPI_RST_PIN, GPIO_MODE_OUTPUT);
    gpio_set_direction(VSPI_DC_PIN, GPIO_MODE_OUTPUT);

    // Realiza reset do display
    gpio_set_level(VSPI_RST_PIN, 0);
    vTaskDelay(pdMS_TO_TICKS(100));
    gpio_set_level(VSPI_RST_PIN, 1);
    vTaskDelay(pdMS_TO_TICKS(100));

    // Sequência de inicialização do ST7735S
    spi_send_command(CMD_SWRESET);  // Software Reset
    vTaskDelay(pdMS_TO_TICKS(150));
    spi_send_command(CMD_SLPOUT);   // Sleep Out
    vTaskDelay(pdMS_TO_TICKS(150));

    // Configurações de controle de memória
    uint8_t madctl = 0xC0;  // Configuração para rotação padrão
    spi_send_command(CMD_MADCTL);
    spi_send_data(&madctl, 1);

    // Configuração do formato de pixel (16 bits por pixel)
    spi_send_command(CMD_COLMOD);
    uint8_t colmod = 0x05;  // 16 bits/pixel
    spi_send_data(&colmod, 1);

    // Liga o display
    spi_send_command(CMD_DISPON);
    ESP_LOGI(TAG, "ST7735S Inicializado");
}

// Função para preencher a tela com uma cor sólida
void st7735s_fill_screen(uint16_t color) {
    uint8_t data[4];

    // Define área de escrita (colunas e linhas para 80x160)
    spi_send_command(CMD_CASET);  // Define coluna
    data[0] = 0x00;  // Início coluna
    data[1] = 0x00;  // Offset início
    data[2] = 0x00;  // Fim coluna
    data[3] = 159;    // Largura 80 (0x4F)
    spi_send_data(data, 4);

    spi_send_command(CMD_RASET);  // Define linha
    data[0] = 0x00;  // Início linha
    data[1] = 0x00;  // Offset início
    data[2] = 0x00;  // Fim linha
    data[3] = 159;   // Altura 160 (0x9F)
    spi_send_data(data, 4);

    spi_send_command(CMD_RAMWR);  // RAM Write

    // Preenche com a cor
    uint8_t pixel[2] = {
        (color >> 8) & 0xFF,  // Byte mais significativo
        color & 0xFF          // Byte menos significativo
    };
    for (int i = 0; i < 80 * 160; i++) {
        spi_send_data(pixel, 2);
    }
}

void app_main(void) {
    // Configuração do SPI
    spi_bus_config_t buscfg = {
        .miso_io_num = -1,              // MISO não utilizado
        .mosi_io_num = VSPI_MOSI_PIN,   // MOSI conectado ao SDA do display
        .sclk_io_num = VSPI_CLK_PIN,    // SCLK conectado ao SCL do display
        .quadwp_io_num = -1,            // Não utilizado
        .quadhd_io_num = -1,            // Não utilizado
        .max_transfer_sz = 4096
    };
    spi_bus_initialize(VSPI_HOST, &buscfg, SPI_DMA_CH_AUTO);

    spi_device_interface_config_t devcfg = {
        .clock_speed_hz = 10 * 1000 * 1000,  // 10 MHz
        .mode = 0,                           // SPI mode 0
        .spics_io_num = VSPI_CS_PIN,         // CS conectado ao CS do display
        .queue_size = 7
    };
    spi_bus_add_device(VSPI_HOST, &devcfg, &spi);

    // Inicializa o display
    st7735s_init();

    // Loop infinito para alternar as cores
    while (1) {
        st7735s_fill_screen(0x0000);  // preto
        vTaskDelay(pdMS_TO_TICKS(1000));

        st7735s_fill_screen(0x8000);  // Vermelho
        vTaskDelay(pdMS_TO_TICKS(1000));

        st7735s_fill_screen(0x0400);  // Verde
        vTaskDelay(pdMS_TO_TICKS(1000));

        st7735s_fill_screen(0x0010);  // Azul
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
