/* Projeto: Teste-ADC

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
#include "driver/adc.h"  // Biblioteca para ADC
#include "driver/ledc.h"  // Biblioteca para PWM
#include "esp_adc_cal.h"  // Biblioteca para calibração do ADC

// Definição dos pinos utilizados
#define GPIO_D18 18  // Pino D18 do ESP32
#define GPIO_D4 4  // Pino D4 do ESP32

// Configurações do ADC adicionadas manualmente
#define DEFAULT_VREF 1100              // Referência padrão em mV
#define ADC_ATTEN ADC_ATTEN_DB_11      // Atenuação para leitura de 0 a 3.3V
#define ADC_WIDTH ADC_WIDTH_BIT_12     // Resolução do ADC (12 bits)


void app_main(void) {
    // Variáveis para ADC
    // adc1_channel_t adc1_channel;
    adc2_channel_t adc2_channel;
    esp_adc_cal_characteristics_t adc_chars;
    // Variáveis para PWM (LEDC)

    // Inicialização do ADC
    adc1_config_width(ADC_WIDTH_BIT_12);
    esp_adc_cal_characterize(ADC_UNIT_1, ADC_ATTEN_DB_11, ADC_WIDTH_BIT_12, 0, &adc_chars);

    // Configuração do ADC2 no pino D4
    adc2_channel = ADC2_CHANNEL_0;
    adc2_config_channel_atten(adc2_channel, ADC_ATTEN_DB_11);

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

    // Seu código aqui

    while (1) {
        int adc_raw = 0;
        
        // Leitura do valor bruto do ADC
        if (adc2_get_raw(ADC2_CHANNEL_0, ADC_WIDTH, &adc_raw) == ESP_OK) {
            // Mapear o valor do ADC (0 a 4095) para o duty cycle do PWM (0 a 8191)
            int duty_cycle = (adc_raw * 8191) / 4095;

            // Ajustar o duty cycle do PWM no LED
            ledc_set_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0, duty_cycle);
            ledc_update_duty(LEDC_LOW_SPEED_MODE, LEDC_CHANNEL_0);

            // Exibir os valores no console para depuração
            printf("ADC Raw: %d, Duty Cycle: %d\n", adc_raw, duty_cycle);
        } else {
            printf("Erro na leitura do ADC2\n");
        }

        // Delay de 100 ms
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}
