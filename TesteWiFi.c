/* Projeto: HTTP Client

   Este código foi gerado automaticamente pela ferramenta ESP32 Tool e atualizado para testar a comunicação como cliente HTTP.

   Instruções para compilação e upload:
   1. Configure o ESP-IDF em seu ambiente.
   2. Copie este código para o arquivo main.c de seu projeto.
   3. No terminal, navegue até o diretório do projeto.
   4. Execute 'idf.py build' para compilar o projeto.
   5. Conecte o ESP32 e execute 'idf.py flash' para carregar o código.

   Para mais informações, visite: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/get-started/
*/

#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_netif.h"
#include "esp_http_client.h"

#define WIFI_SSID "ClaroWiFi"  // Substitua pelo nome da sua rede Wi-Fi
#define WIFI_PASS "yuri5252"  // Substitua pela senha da sua rede Wi-Fi

static const char *TAG = "HTTP_CLIENT";

static void http_client_task(void *pvParameters);

// Evento de Wi-Fi
static void wifi_event_handler(void *arg, esp_event_base_t event_base, int32_t event_id, void *event_data) {
    if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_START) {
        esp_wifi_connect();
    } else if (event_base == WIFI_EVENT && event_id == WIFI_EVENT_STA_DISCONNECTED) {
        ESP_LOGI(TAG, "Desconectado. Tentando reconectar...");
        esp_wifi_connect();
    } else if (event_base == IP_EVENT && event_id == IP_EVENT_STA_GOT_IP) {
        ip_event_got_ip_t *event = (ip_event_got_ip_t *)event_data;
        ESP_LOGI(TAG, "Conectado com IP: " IPSTR, IP2STR(&event->ip_info.ip));
        xTaskCreate(&http_client_task, "http_client_task", 8192, NULL, 5, NULL);
    }
}

// Inicialização do Wi-Fi
void wifi_init() {
    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());
    esp_netif_create_default_wifi_sta();

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    esp_event_handler_instance_t instance_any_id;
    esp_event_handler_instance_t instance_got_ip;
    ESP_ERROR_CHECK(esp_event_handler_instance_register(WIFI_EVENT, ESP_EVENT_ANY_ID, &wifi_event_handler, NULL, &instance_any_id));
    ESP_ERROR_CHECK(esp_event_handler_instance_register(IP_EVENT, IP_EVENT_STA_GOT_IP, &wifi_event_handler, NULL, &instance_got_ip));

    wifi_config_t wifi_config = {
        .sta = {
            .ssid = WIFI_SSID,
            .password = WIFI_PASS,
            .threshold.authmode = WIFI_AUTH_WPA2_PSK,
        },
    };

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_STA));
    ESP_ERROR_CHECK(esp_wifi_set_config(ESP_IF_WIFI_STA, &wifi_config));
    ESP_ERROR_CHECK(esp_wifi_start());
}

// Função para fazer uma requisição HTTP GET
static void http_client_task(void *pvParameters) {
    esp_http_client_config_t config = {
        .url = "http://httpbin.org/get",  // URL do servidor HTTP
        .method = HTTP_METHOD_GET
    };

    esp_http_client_handle_t client = esp_http_client_init(&config);
    esp_err_t err = esp_http_client_perform(client);

    if (err == ESP_OK) {
        int status_code = esp_http_client_get_status_code(client);
        int content_length = esp_http_client_get_content_length(client);
        ESP_LOGI(TAG, "Código HTTP: %d", status_code);
        ESP_LOGI(TAG, "Tamanho da resposta: %d bytes", content_length);

        // Lê a resposta
        char buffer[1024];
        int bytes_read = esp_http_client_read(client, buffer, sizeof(buffer) - 1);
        if (bytes_read > 0) {
            buffer[bytes_read] = '\0';  // Finaliza a string
            ESP_LOGI(TAG, "Resposta:\n%s", buffer);
        }
    } else {
        ESP_LOGE(TAG, "Falha na requisição HTTP: %s", esp_err_to_name(err));
    }

    esp_http_client_cleanup(client);
    vTaskDelete(NULL);  // Encerra a tarefa
}

void app_main(void) {
    ESP_ERROR_CHECK(nvs_flash_init());
    wifi_init();
}
