/* Projeto: TesteTouch

   Este código foi gerado automaticamente pela ferramenta ESP32 Tool e modificado para implementar o ciclo de LEDs com base no sensor Touch, incluindo valores de leitura detalhados no terminal.

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
#include "driver/gpio.h"      // Biblioteca para GPIO
#include "driver/touch_pad.h" // Biblioteca para Touch Pad

// Definição dos pinos utilizados
#define GPIO_D19 19              // Pino D19 do ESP32 (LED 1)
#define GPIO_D21 21              // Pino D21 do ESP32 (LED 2)
#define TOUCH_D2 2 // Pino D2 do ESP32 (Sensor Touch)

// Estados do ciclo
typedef enum {
    STATE_LED1_ON,
    STATE_LED2_ON,
    STATE_BOTH_ON,
    STATE_BOTH_OFF
} led_state_t;

void app_main(void) {
    gpio_config_t io_conf;

    // Configuração do GPIO D19 como saída
    io_conf.pin_bit_mask = (1ULL << GPIO_D19); // Seleciona o pino
    io_conf.mode = GPIO_MODE_OUTPUT;          // Modo de saída
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE; // Desabilita pull-up
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE; // Desabilita pull-down
    io_conf.intr_type = GPIO_INTR_DISABLE;    // Desabilita interrupções
    gpio_config(&io_conf); // Aplica configurações

    // Configuração do GPIO D21 como saída
    io_conf.pin_bit_mask = (1ULL << GPIO_D21); // Seleciona o pino
    gpio_config(&io_conf); // Aplica configurações

    // Inicialização do Touch Pad
    touch_pad_init(); // Inicializa o módulo de touch pad
    touch_pad_set_voltage(TOUCH_HVOLT_2V7, TOUCH_LVOLT_0V5, TOUCH_HVOLT_ATTEN_1V);
    touch_pad_config(TOUCH_D2, -1); // Configura o sensor Touch
    touch_pad_filter_start(10); // Inicia o filtro para estabilizar a leitura

    // Variáveis para valores de toque
    uint16_t raw_value_touch = 0, filtered_value = 0, val = 0;

    // Inicializa o estado
    led_state_t state = STATE_BOTH_OFF;

    printf("Touch Pad inicializado. Monitorando valores...\n");

    // Loop principal
    while (1) {
        // Lê os valores do sensor
        touch_pad_read_raw_data(TOUCH_D2, &raw_value_touch);
        touch_pad_read_filtered(TOUCH_D2, &filtered_value);
        touch_pad_read(TOUCH_D2, &val);

        // Exibe os valores detalhados no terminal
    
        // Verifica se o toque foi detectado
        if (val < (filtered_value * 0.2)) { // 20% do valor filtrado como threshold
            vTaskDelay(50 / portTICK_PERIOD_MS); // Debounce
            touch_pad_read(TOUCH_D2, &val);

            if (val < (filtered_value * 0.2)) { // Confirma o toque
             printf("Touch value: %d, Raw: %d, Filtered: %d\n", val, raw_value_touch, filtered_value);
                // Alterna entre os estados
                switch (state) {
                    case STATE_BOTH_OFF:
                        gpio_set_level(GPIO_D19, 1); // Liga LED1
                        gpio_set_level(GPIO_D21, 0); // Garante que LED2 está apagado
                        state = STATE_LED1_ON;
                        break;

                    case STATE_LED1_ON:
                        gpio_set_level(GPIO_D19, 0); // Apaga LED1
                        gpio_set_level(GPIO_D21, 1); // Liga LED2
                        state = STATE_LED2_ON;
                        break;

                    case STATE_LED2_ON:
                        gpio_set_level(GPIO_D19, 1); // Liga LED1
                        gpio_set_level(GPIO_D21, 1); // Liga LED2
                        state = STATE_BOTH_ON;
                        break;

                    case STATE_BOTH_ON:
                        gpio_set_level(GPIO_D19, 0); // Apaga LED1
                        gpio_set_level(GPIO_D21, 0); // Apaga LED2
                        state = STATE_BOTH_OFF;
                        break;
                }

                printf("Touch detectado! Estado atual: %d\n", state);
                vTaskDelay(300 / portTICK_PERIOD_MS); // Aguarda para evitar múltiplas detecções
            }
        }

    }
}
