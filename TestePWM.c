/* Projeto: TestePWM

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
#include "driver/ledc.h"  // Biblioteca para PWM

// Definição dos pinos utilizados
#define GPIO_D18 18  // Pino D18 do ESP32

void app_main(void) {
    // Variáveis para PWM (LEDC)

    // Inicialização do PWM (LEDC)
    // Configuração do timer do LEDC (PWM)
     ledc_timer_config_t ledc_timer = {
        .duty_resolution = LEDC_TIMER_13_BIT, // Resolução do duty cycle
        .freq_hz = 5000,                      // Frequência em Hz
        .speed_mode = LEDC_LOW_SPEED_MODE,    // Modo de velocidade
        .timer_num = LEDC_TIMER_0             // Número do timer
    };
    ledc_timer_config(&ledc_timer);

    // Configuração do canal PWM para o pino D18
    ledc_channel_config_t ledc_channel_0 = {
        .channel    = LEDC_CHANNEL_0,
        .duty       = 0,
        .gpio_num   = GPIO_D18,
        .speed_mode = LEDC_LOW_SPEED_MODE,
        .hpoint     = 0,
        .timer_sel  = LEDC_TIMER_0
    };
    ledc_channel_config(&ledc_channel_0); 
    
    while (1) {
        // Aumentar o brilho gradualmente
        for (int duty = 0; duty <= 8191; duty += 100) {
            ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, duty);
            ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);
            vTaskDelay(pdMS_TO_TICKS(10)); // Aguarda 10ms
        }

        // Diminuir o brilho gradualmente
        for (int duty = 8191; duty >= 0; duty -= 100) {
            ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, duty);
            ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);
            vTaskDelay(pdMS_TO_TICKS(10)); // Aguarda 10ms
        }

        vTaskDelay(pdMS_TO_TICKS(1000)); // Pausa de 1 segundo após ciclo completo
    }
}

