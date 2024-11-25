#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_bt.h"
#include "esp_log.h"
#include "nvs_flash.h"

#include "esp_gap_ble_api.h"
#include "esp_gatts_api.h"
#include "esp_bt_main.h"

#include <string.h> // Para usar memcpy

#define GATTS_TAG "ESP32_BLE"

/// Definições do Serviço e Característica
#define GATTS_SERVICE_UUID_TEST   0x00FF
#define GATTS_CHAR_UUID_TEST      0xFF01
#define GATTS_NUM_HANDLE_TEST     4

#define GATTS_DEMO_CHAR_VAL_LEN_MAX 0x40
#define CHAR_DECLARATION_SIZE       (sizeof(uint8_t))
#define SVC_INST_ID                 0

// UUIDs para serviços e características
static const uint16_t primary_service_uuid            = ESP_GATT_UUID_PRI_SERVICE;
static const uint16_t character_declaration_uuid      = ESP_GATT_UUID_CHAR_DECLARE;
static const uint16_t character_client_config_uuid    = ESP_GATT_UUID_CHAR_CLIENT_CONFIG;

static const uint8_t char_prop_read_write_notify = ESP_GATT_CHAR_PROP_BIT_READ | ESP_GATT_CHAR_PROP_BIT_WRITE | ESP_GATT_CHAR_PROP_BIT_NOTIFY;

// Valores iniciais
static uint8_t ccc[2] = {0x00, 0x00};

// Variáveis para UUIDs de serviço e característica
static uint16_t GATTS_SERVICE_UUID = GATTS_SERVICE_UUID_TEST;
static uint16_t GATTS_CHAR_UUID = GATTS_CHAR_UUID_TEST;

static uint8_t adv_service_uuid128[16] = {
    /* LSB <--------------------------------------------------------------------------------> MSB */
    0xFB, 0x34, 0x9B, 0x5F, 0x80, 0x00, 0x00, 0x80,
    0x00, 0x10, 0x00, 0x00, 0xFF, 0x00, 0x00, 0x00,
};

// Dados de anúncio
static esp_ble_adv_data_t adv_data = {
    .set_scan_rsp = false,
    .include_name = true,
    .include_txpower = false,
    .min_interval = 0x0006, // Intervalo mínimo de conexão
    .max_interval = 0x0010, // Intervalo máximo de conexão
    .appearance = 0x00,
    .manufacturer_len = 0,  // Sem dados do fabricante
    .p_manufacturer_data =  NULL,
    .service_data_len = 0,
    .p_service_data = NULL,
    .service_uuid_len = sizeof(adv_service_uuid128),
    .p_service_uuid = adv_service_uuid128,
    .flag = (ESP_BLE_ADV_FLAG_GEN_DISC | ESP_BLE_ADV_FLAG_BREDR_NOT_SPT),
};

// Parâmetros de anúncio
static esp_ble_adv_params_t adv_params = {
    .adv_int_min        = 0x20,
    .adv_int_max        = 0x40,
    .adv_type           = ADV_TYPE_IND,
    .own_addr_type      = BLE_ADDR_TYPE_PUBLIC,
    //.peer_addr          = {0},
    //.peer_addr_type     = BLE_ADDR_TYPE_PUBLIC,
    .channel_map        = ADV_CHNL_ALL,
    .adv_filter_policy  = ADV_FILTER_ALLOW_SCAN_ANY_CON_ANY,
};

// Índices para os handles
enum {
    IDX_SVC,
    IDX_CHAR_DECL,
    IDX_CHAR_VAL,
    IDX_CHAR_CFG,
    HRS_IDX_NB,
};

static uint16_t handle_table[GATTS_NUM_HANDLE_TEST];

static esp_gatts_attr_db_t gatt_db[GATTS_NUM_HANDLE_TEST] =
{
    // Serviço Primário
    [IDX_SVC] = {
        {ESP_GATT_AUTO_RSP},
        {
            .uuid_length = ESP_UUID_LEN_16,
            .uuid_p = (uint8_t *)&primary_service_uuid,
            .perm = ESP_GATT_PERM_READ,
            .max_length = sizeof(uint16_t),
            .length = sizeof(GATTS_SERVICE_UUID),
            .value = (uint8_t *)&GATTS_SERVICE_UUID
        }
    },

    // Característica Declaração
    [IDX_CHAR_DECL] = {
        {ESP_GATT_AUTO_RSP},
        {
            .uuid_length = ESP_UUID_LEN_16,
            .uuid_p = (uint8_t *)&character_declaration_uuid,
            .perm = ESP_GATT_PERM_READ,
            .max_length = CHAR_DECLARATION_SIZE,
            .length = CHAR_DECLARATION_SIZE,
            .value = (uint8_t *)&char_prop_read_write_notify
        }
    },

    // Característica Valor
    [IDX_CHAR_VAL] = {
        {ESP_GATT_AUTO_RSP},
        {
            .uuid_length = ESP_UUID_LEN_16,
            .uuid_p = (uint8_t *)&GATTS_CHAR_UUID,
            .perm = ESP_GATT_PERM_READ | ESP_GATT_PERM_WRITE,
            .max_length = GATTS_DEMO_CHAR_VAL_LEN_MAX,
            .length = sizeof("ESP32"),
            .value = (uint8_t *)"ESP32"
        }
    },

    // Cliente Configuração de Característica (para notificações/indicações)
    [IDX_CHAR_CFG] = {
        {ESP_GATT_AUTO_RSP},
        {
            .uuid_length = ESP_UUID_LEN_16,
            .uuid_p = (uint8_t *)&character_client_config_uuid,
            .perm = ESP_GATT_PERM_READ | ESP_GATT_PERM_WRITE,
            .max_length = sizeof(uint16_t),
            .length = sizeof(ccc),
            .value = (uint8_t *)ccc
        }
    },
};

static void gatts_profile_event_handler(esp_gatts_cb_event_t event,
                                        esp_gatt_if_t gatts_if,
                                        esp_ble_gatts_cb_param_t *param);

static void gap_event_handler(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param) {
    switch (event) {
        case ESP_GAP_BLE_ADV_DATA_SET_COMPLETE_EVT:
            esp_ble_gap_start_advertising(&adv_params);
            break;
        case ESP_GAP_BLE_ADV_START_COMPLETE_EVT:
            ESP_LOGI(GATTS_TAG, "Anúncio iniciado");
            break;
        case ESP_GAP_BLE_ADV_STOP_COMPLETE_EVT:
            ESP_LOGI(GATTS_TAG, "Anúncio parado");
            break;
        default:
            break;
    }
}

static void gatts_profile_event_handler(esp_gatts_cb_event_t event,
                                        esp_gatt_if_t gatts_if,
                                        esp_ble_gatts_cb_param_t *param) {
    switch (event) {
        case ESP_GATTS_REG_EVT:
            ESP_LOGI(GATTS_TAG, "Registro de GATT");
            esp_ble_gap_set_device_name("ESP32_BLE");
            esp_ble_gap_config_adv_data(&adv_data);
            esp_ble_gatts_create_attr_tab(gatt_db, gatts_if, GATTS_NUM_HANDLE_TEST, SVC_INST_ID);
            break;
        case ESP_GATTS_CREAT_ATTR_TAB_EVT:
            if (param->add_attr_tab.status != ESP_GATT_OK){
                ESP_LOGE(GATTS_TAG, "Erro ao criar a tabela de atributos, erro=0x%x", param->add_attr_tab.status);
            } else {
                memcpy(handle_table, param->add_attr_tab.handles, sizeof(handle_table));
                esp_ble_gatts_start_service(handle_table[IDX_SVC]);
            }
            break;
        case ESP_GATTS_CONNECT_EVT:
            ESP_LOGI(GATTS_TAG, "ESP_GATTS_CONNECT_EVT, conn_id=%d", param->connect.conn_id);
            break;
        case ESP_GATTS_DISCONNECT_EVT:
            ESP_LOGI(GATTS_TAG, "ESP_GATTS_DISCONNECT_EVT, reason=0x%x", param->disconnect.reason);
            // Reiniciar anúncio após desconexão
            esp_ble_gap_start_advertising(&adv_params);
            break;
        case ESP_GATTS_READ_EVT:
            ESP_LOGI(GATTS_TAG, "Leitura da Característica");
            break;
        case ESP_GATTS_WRITE_EVT:
            ESP_LOGI(GATTS_TAG, "Escrita na Característica");
            if (param->write.handle == handle_table[IDX_CHAR_VAL]) {
                // Processar os dados recebidos
                ESP_LOGI(GATTS_TAG, "Dados recebidos: %.*s", param->write.len, param->write.value);

                // Exemplo: Enviar uma resposta (eco)
                esp_ble_gatts_send_indicate(gatts_if, param->write.conn_id, handle_table[IDX_CHAR_VAL],
                                            param->write.len, param->write.value, false);
            }
            break;
        default:
            break;
    }
}

void app_main(void) {
    esp_err_t ret;

    // Inicialização do NVS
    ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES ||
        ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    // Inicialização do Bluetooth
    ESP_ERROR_CHECK(esp_bt_controller_mem_release(ESP_BT_MODE_CLASSIC_BT));

    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    bt_cfg.mode = ESP_BT_MODE_BLE; // Definir o modo BLE
    ret = esp_bt_controller_init(&bt_cfg);
    if (ret) {
        ESP_LOGE(GATTS_TAG, "Falha ao inicializar o controlador BT: %s", esp_err_to_name(ret));
        return;
    }

    ret = esp_bt_controller_enable(ESP_BT_MODE_BLE);
    if (ret) {
        ESP_LOGE(GATTS_TAG, "Falha ao habilitar o controlador BT: %s", esp_err_to_name(ret));
        return;
    }

    ret = esp_bluedroid_init();
    if (ret) {
        ESP_LOGE(GATTS_TAG, "Falha ao inicializar o Bluedroid: %s", esp_err_to_name(ret));
        return;
    }

    ret = esp_bluedroid_enable();
    if (ret) {
        ESP_LOGE(GATTS_TAG, "Falha ao habilitar o Bluedroid: %s", esp_err_to_name(ret));
        return;
    }

    // Registro dos callbacks
    ret = esp_ble_gap_register_callback(gap_event_handler);
    if (ret){
        ESP_LOGE(GATTS_TAG, "Falha ao registrar o callback GAP: %s", esp_err_to_name(ret));
        return;
    }

    ret = esp_ble_gatts_register_callback(gatts_profile_event_handler);
    if (ret){
        ESP_LOGE(GATTS_TAG, "Falha ao registrar o callback GATTS: %s", esp_err_to_name(ret));
        return;
    }

    ret = esp_ble_gatts_app_register(0);
    if (ret){
        ESP_LOGE(GATTS_TAG, "Falha ao registrar o aplicativo GATTS: %s", esp_err_to_name(ret));
        return;
    }
}
