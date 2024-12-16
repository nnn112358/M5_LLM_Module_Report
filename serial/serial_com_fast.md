## 目的

従来、Module LLMからのUART信号の受信にQCGA画像で200msかかっていた。
これを高速化した。

LLM  Moduleのmp4をuart経由でCore S3に表示してみた。QVGAで受信に200ms、描画に40ms。やはり遅いっすね…
https://x.com/nnn112358/status/1860208779780063613

I tried before, AX630C does support up to 2Mbps, but there will be bit error in transmission for long time.
https://x.com/HanxiaoM/status/1864932394375221594





```M5StackCoreS3SE_receive.cpp
#include <M5Unified.h>
#include "driver/uart.h"
#include "driver/gpio.h"
#include "esp_log.h"

static const char* TAG = "UART_DMA";
static const int UART_NUM = UART_NUM_2;
static const int BUF_SIZE = 16384;
static QueueHandle_t uart_queue;
static QueueHandle_t display_queue;

struct ImageData {
  uint8_t* buffer;
  size_t length;
  uint32_t frame_number;
  unsigned long read_time;  // 読み取り時間を追加
};

void setup_uart() {
  uart_config_t uart_config = {
    .baud_rate = 2000000,
    .data_bits = UART_DATA_8_BITS,
    .parity = UART_PARITY_DISABLE,
    .stop_bits = UART_STOP_BITS_1,
    .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
    .source_clk = UART_SCLK_APB,
  };

  const int uart_rx_pin = 18;
  const int uart_tx_pin = 17;

  ESP_ERROR_CHECK(uart_driver_install(UART_NUM, BUF_SIZE * 2, BUF_SIZE * 2, 30, &uart_queue, ESP_INTR_FLAG_IRAM));
  ESP_ERROR_CHECK(uart_param_config(UART_NUM, &uart_config));
  ESP_ERROR_CHECK(uart_set_pin(UART_NUM, uart_tx_pin, uart_rx_pin, UART_PIN_NO_CHANGE, UART_PIN_NO_CHANGE));

  ESP_ERROR_CHECK(uart_set_rx_timeout(UART_NUM, 1));
  ESP_ERROR_CHECK(uart_set_rx_full_threshold(UART_NUM, 100));
  ESP_ERROR_CHECK(uart_set_tx_empty_threshold(UART_NUM, 10));

  uint8_t pattern[3] = { 0xFF, 0xD8, 0xEA };
  ESP_ERROR_CHECK(uart_enable_pattern_det_baud_intr(UART_NUM, pattern[0], 3, 1, 0, 0));
}

void uart_task(void* parameter) {

  static const uint8_t packet_begin[3] = { 0xFF, 0xD8, 0xEA };
  uint8_t* temp_buffer = (uint8_t*)heap_caps_malloc(BUF_SIZE, MALLOC_CAP_DMA);
  uint8_t header[10];

  // 時間測定用の変数
  unsigned long start_time;
  unsigned long header_read_time;
  unsigned long data_read_time;

  if (!temp_buffer) {
    ESP_LOGE(TAG, "Failed to allocate temporary buffer");
    vTaskDelete(NULL);
    return;
  }

  while (1) {
    uart_event_t event;
    if (xQueueReceive(uart_queue, (void*)&event, pdMS_TO_TICKS(10))) {
      switch (event.type) {
        case UART_DATA:
          {
            // ヘッダー読み取り開始時間
            start_time = millis();
            // まずヘッダーのみを読み取り
            int header_size = uart_read_bytes(UART_NUM, header, 10, pdMS_TO_TICKS(50));
            header_read_time = millis() - start_time;

            if (header_size == 10 && header[0] == packet_begin[0] && header[1] == packet_begin[1] && header[2] == packet_begin[2]) {

              uint32_t jpeg_length = (uint32_t)(header[4] << 16) | (header[5] << 8) | header[6];
              uint32_t frame_number = (uint32_t)(header[7] << 16) | (header[8] << 8) | header[9];

              char buffer[100];  // メッセージを格納するのに十分な大きさのバッファを確保
              sprintf(buffer, "Header read in %lu ms, frame: %u, length: %u",
                      header_read_time, frame_number, jpeg_length);
              Serial.println(buffer);


              if (jpeg_length > BUF_SIZE) {

                char buffer[100];  // メッセージを格納するのに十分な大きさのバッファを確保
                sprintf(buffer, "Image too large: %d", jpeg_length);
                Serial.println(buffer);
                
                uart_flush_input(UART_NUM);
                continue;
              }

              // 事前にメモリを確保
              uint8_t* display_buffer = (uint8_t*)heap_caps_malloc(jpeg_length, MALLOC_CAP_DMA);
              if (!display_buffer) {
                ESP_LOGE(TAG, "Failed to allocate display buffer");
                continue;
              }

              size_t total_read = 0;
              bool read_success = true;
              unsigned long start_time = millis();

              // より大きなチャンクサイズでデータを読み込む
              while (total_read < jpeg_length) {
                size_t remaining = jpeg_length - total_read;
                size_t chunk_size = min(remaining, (size_t)1024);  // より大きなチャンクサイズ

                int bytes_read = uart_read_bytes(UART_NUM,
                                                 display_buffer + total_read,
                                                 chunk_size,
                                                 pdMS_TO_TICKS(100));

                if (bytes_read <= 0) {
                  read_success = false;
                  break;
                }
                total_read += bytes_read;
              }
              data_read_time = millis() - start_time;

              if (read_success && total_read == jpeg_length) {


                char buffer[100];  // メッセージを格納するのに十分な大きさのバッファを確保
                sprintf(buffer, "Data read in %lu ms, bytes read: %u",
                        data_read_time, total_read);
                Serial.println(buffer);

                ImageData img_data = {
                  .buffer = display_buffer,
                  .length = jpeg_length,
                  .frame_number = frame_number,
                                    .read_time = data_read_time  // 読み取り時間を保存

                };

                if (xQueueSend(display_queue, &img_data, pdMS_TO_TICKS(10)) != pdTRUE) {
                  Serial.println("Failed to send to display queue");

                  heap_caps_free(display_buffer);
                }
              } else {

                char buffer[100];  // メッセージを格納するのに十分な大きさのバッファを確保
                sprintf(buffer, "Failed to read complete frame in %lu ms", data_read_time);
                Serial.println(buffer);
                heap_caps_free(display_buffer);
              }
            }
            break;
          }

        case UART_FIFO_OVF:
        case UART_BUFFER_FULL:
          ESP_LOGW(TAG, "Buffer overflow/full, flushing");
          uart_flush(UART_NUM);
          xQueueReset(uart_queue);
          break;

        case UART_BREAK:
        case UART_PARITY_ERR:
        case UART_FRAME_ERR:
          uart_flush_input(UART_NUM);
          break;
      }
    }
    taskYIELD();  // より効率的なタスク切り替え
  }

  heap_caps_free(temp_buffer);
}
// ディスプレイ描画タスク
void display_task(void* parameter) {
  uint32_t last_frame_number = 0;

  while (1) {
    ImageData img_data;
    if (xQueueReceive(display_queue, &img_data, pdMS_TO_TICKS(10)) == pdTRUE) {
        unsigned long start_time = millis();
        M5.Lcd.drawJpg(img_data.buffer, img_data.length);
        unsigned long draw_time = millis() - start_time;

        ESP_LOGI(TAG, "Frame %u drawn in %lu ms", img_data.frame_number, draw_time);

        char buffer[512];
        sprintf(buffer, "Frame %u drawn in %lu ms", img_data.frame_number, draw_time);
        Serial.println(buffer);

        last_frame_number = img_data.frame_number;
      heap_caps_free(img_data.buffer);
    }
    vTaskDelay(pdMS_TO_TICKS(1));
  }
}

void setup() {
  M5.begin();
  M5.Display.setTextSize(1);
  M5.Display.setTextScroll(true);
  M5.Lcd.setTextFont(&fonts::efontJA_16);
  M5.Log.setLogLevel(m5::log_target_display, ESP_LOG_INFO);

  display_queue = xQueueCreate(3, sizeof(ImageData));

  setup_uart();
  Serial.begin(115200);
  M5.Display.printf(">>  ModuleLLM..\n");
  Serial.println("ModuleLLM");

  // UARTタスクを高優先度で作成
  xTaskCreatePinnedToCore(
    uart_task,
    "uart_task",
    8192,
    NULL,
    configMAX_PRIORITIES - 1,  // 最高優先度
    NULL,
    0);

  // ディスプレイタスクを作成
  xTaskCreatePinnedToCore(
    display_task,
    "display_task",
    8192,
    NULL,
    1,
    NULL,
    1);
}

void loop() {
  M5.update();
  vTaskDelay(pdMS_TO_TICKS(10));
}
```


