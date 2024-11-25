/* Projeto: UART Loopback Teste

   Este código foi gerado automaticamente pela ferramenta ESP32 Tool e atualizado para realizar um teste de loopback na UART2.

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
#include "driver/uart.h"
#include "string.h"

// Definição dos pinos utilizados
#define GPIO_RX2 16  // Pino RX2 do ESP32
#define GPIO_TX2 17  // Pino TX2 do ESP32
#define BUF_SIZE 1024  // Tamanho do buffer UART

void app_main(void) {
    // Configuração da UART
    uart_config_t uart_config = {
        .baud_rate = 115200,                // Taxa de transmissão
        .data_bits = UART_DATA_8_BITS,      // 8 bits de dados
        .parity = UART_PARITY_DISABLE,      // Sem paridade
        .stop_bits = UART_STOP_BITS_1,      // 1 bit de parada
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE // Sem controle de fluxo
    };
    uart_param_config(UART_NUM_2, &uart_config);
    uart_set_pin(UART_NUM_2, GPIO_TX2, GPIO_RX2, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE);
    uart_driver_install(UART_NUM_2, BUF_SIZE, BUF_SIZE, 0, NULL, 0);

    // Mensagem para o teste
    const char *test_message = "Teste UART Loopback\n";
    uint8_t data[BUF_SIZE];

    while (1) {
        // Envia a mensagem pela UART
        uart_write_bytes(UART_NUM_2, test_message, strlen(test_message));
        printf("Mensagem enviada: %s", test_message);  // Log quando a mensagem for enviada

        // Lê os dados recebidos
        int len = uart_read_bytes(UART_NUM_2, data, BUF_SIZE, 1000 / portTICK_PERIOD_MS);
        if (len > 0) {
            data[len] = '\0';  // Finaliza a string
            printf("Recebido: %s", data);  // Imprime os dados recebidos
        }

        vTaskDelay(pdMS_TO_TICKS(1000));  // Delay de 1 segundo
    }
}
