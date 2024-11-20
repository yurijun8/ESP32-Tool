/* Projeto: TesteLED 

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
#include "driver/gpio.h"  // Biblioteca para GPIO

// Definição dos pinos utilizados
#define GPIO_D15 15  // Pino D15 do ESP32
#define GPIO_D2 2  // Pino D2 do ESP32

void app_main(void) {
    gpio_config_t io_conf;

    // Configuração do GPIO D15 como saída
    io_conf.pin_bit_mask = (1ULL << GPIO_D15);  // Seleciona o pino
    io_conf.mode = GPIO_MODE_OUTPUT;  // Modo de saída
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;  // Desabilita pull-up
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;  // Desabilita pull-down
    io_conf.intr_type = GPIO_INTR_DISABLE;  // Desabilita interrupções
    gpio_config(&io_conf);  // Aplica configurações

    // Configuração do GPIO D2 como entrada
    io_conf.pin_bit_mask = (1ULL << GPIO_D2);  // Seleciona o pino
    io_conf.mode = GPIO_MODE_INPUT;  // Modo de entrada
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;  // Desabilita pull-up
    io_conf.pull_down_en = GPIO_PULLDOWN_DISABLE;  // Desabilita pull-down
    io_conf.intr_type = GPIO_INTR_DISABLE;  // Desabilita interrupções
    gpio_config(&io_conf);  // Aplica configurações

    // Seu código aqui

     int led_state = 0; 
    while (1) {
        
        int button_state = gpio_get_level(GPIO_D2);

        if (button_state == 0) { // Botão pressionado (nivel baixo)
            // Alterna o estado do LED
            led_state = !led_state;
            gpio_set_level(GPIO_D15, led_state);
            // Aguarda para evitar múltiplos acionamentos
            vTaskDelay(pdMS_TO_TICKS(200));  // Debouncing
        }
        // Pequeno atraso para evitar leitura excessiva
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}

