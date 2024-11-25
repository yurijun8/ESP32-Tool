#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_bt.h"
#include "esp_log.h"
#include "esp_spp_api.h"
#include "nvs_flash.h"

#include "esp_bt_main.h"
#include "esp_bt_device.h"
#include "esp_gap_bt_api.h"

#include <inttypes.h>

#define SPP_SERVER_NAME "ESP32_SPP_SERVER"
static const char *TAG = "ESP32_Bluetooth";

static void spp_callback(esp_spp_cb_event_t event, esp_spp_cb_param_t *param) {
    switch (event) {
        case ESP_SPP_INIT_EVT:
            ESP_LOGI(TAG, "ESP_SPP_INIT_EVT");
            esp_bt_dev_set_device_name("ESP32_Bluetooth");
            esp_bt_gap_set_scan_mode(ESP_BT_CONNECTABLE, ESP_BT_GENERAL_DISCOVERABLE);
            esp_spp_start_srv(ESP_SPP_SEC_NONE, ESP_SPP_ROLE_SLAVE, 0, SPP_SERVER_NAME);
            break;
        case ESP_SPP_START_EVT:
            ESP_LOGI(TAG, "ESP_SPP_START_EVT");
            break;
        case ESP_SPP_DATA_IND_EVT:
            ESP_LOGI(TAG, "ESP_SPP_DATA_IND_EVT len=%d handle=%" PRIu32,
                     param->data_ind.len, param->data_ind.handle);
            // Echo dos dados recebidos
            esp_spp_write(param->data_ind.handle, param->data_ind.len, param->data_ind.data);
            break;
        case ESP_SPP_SRV_OPEN_EVT:
            ESP_LOGI(TAG, "Cliente conectado");
            break;
        case ESP_SPP_CLOSE_EVT:
            ESP_LOGI(TAG, "Conexão fechada");
            break;
        default:
            break;
    }
}

void app_main(void) {
    // Inicialização do NVS
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
        ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // Libera memória do BLE se não for usado
    ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_BLE));

    // Configuração e inicialização do controlador BT
    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    bt_cfg.mode = ESP_BT_MODE_CLASSIC_BT; // Definir explicitamente o modo
    ret = esp_bt_controller_init(&bt_cfg);
    if (ret) {
        ESP_LOGE(TAG, "Falha ao inicializar o controlador BT: %s", esp_err_to_name(ret));
        return;
    }

    // Habilitar o controlador BT
    ret = esp_bt_controller_enable(ESP_BT_MODE_CLASSIC_BT);
    if (ret) {
        ESP_LOGE(TAG, "Falha ao habilitar o controlador BT: %s", esp_err_to_name(ret));
        return;
    }

    // Inicialização do Bluedroid
    ret = esp_bluedroid_init();
    if (ret) {
        ESP_LOGE(TAG, "Falha ao inicializar o Bluedroid: %s", esp_err_to_name(ret));
        return;
    }

    // Habilitação do Bluedroid
    ret = esp_bluedroid_enable();
    if (ret) {
        ESP_LOGE(TAG, "Falha ao habilitar o Bluedroid: %s", esp_err_to_name(ret));
        return;
    }

    // Registro do callback SPP
    esp_spp_register_callback(spp_callback);
    esp_spp_init(ESP_SPP_MODE_CB);
}
