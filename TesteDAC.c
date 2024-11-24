/* Projeto: DACtest

   Este código foi gerado automaticamente pela ferramenta ESP32 Tool.

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
#include "driver/dac.h"  // Biblioteca para DAC
#include "driver/gpio.h"  // Biblioteca para GPIO

// Definição dos pinos utilizados
#define DAC_OUTPUT_CHANNEL DAC_CHANNEL_2 // Pino D26 do ESP32
#define GPIO_D32 32  // Pino D32 do ESP32

// Variáveis globais inseridas
uint8_t dac_value = 0;  // Valor inicial do DAC
float current_voltage = 0.0;

// Constantes inseridas
#define DAC_MAX_VOLTAGE 3.3               // Tensão máxima do DAC (aproximadamente 3.3V)
#define DAC_INCREMENT 0.3                 // Incremento de 0.3V
#define DAC_RESOLUTION 256                // Resolução do DAC (8 bits)

void app_main(void) {
    gpio_config_t io_conf;
    // DAC não requer configurações adicionais

    // Inicialização do DAC
    dac_output_enable(DAC_CHANNEL_2);  // Habilita o DAC no pino D26
    dac_output_voltage(DAC_OUTPUT_CHANNEL, dac_value);

    // Configuração do GPIO D32 como entrada
    io_conf.pin_bit_mask = (1ULL << GPIO_D32);  // Seleciona o pino
    io_conf.mode = GPIO_MODE_INPUT;  // Modo de entrada
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;  // Desabilita pull-up
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;  // Desabilita pull-down
    io_conf.intr_type = GPIO_INTR_DISABLE;  // Desabilita interrupções
    gpio_config(&io_conf);  // Aplica configurações

    // Seu código aqui

    printf("Pressione o botão para aumentar a tensão do DAC em incrementos de %.1fV\n", DAC_INCREMENT);

    while (1) {
        // Verificar o estado do botão
        if (gpio_get_level(GPIO_D32) == 0) {  // Botão pressionado
            // Incrementar o valor do DAC
            if (current_voltage + DAC_INCREMENT <= DAC_MAX_VOLTAGE) {
                current_voltage += DAC_INCREMENT;
                dac_value = (uint8_t)((current_voltage / DAC_MAX_VOLTAGE) * (DAC_RESOLUTION - 1));
                dac_output_voltage(DAC_OUTPUT_CHANNEL, dac_value);

                // Imprimir o valor esperado no terminal
                printf("Tensão atual esperada: %.2fV\n", current_voltage);
            } else {
                printf("Tensão máxima atingida: %.2fV\n", current_voltage);
            }

            // Aguarde enquanto o botão estiver pressionado (evitar múltiplas leituras)
            while (gpio_get_level(GPIO_D32) == 0) {
                vTaskDelay(pdMS_TO_TICKS(50));
            }
        }
        // Pequeno atraso para evitar leitura excessiva
        vTaskDelay(pdMS_TO_TICKS(50));
    }
}

