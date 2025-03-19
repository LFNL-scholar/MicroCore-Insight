#include <Wire.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128  
#define SCREEN_HEIGHT 64  
#define OLED_RESET    -1   
#define SCREEN_ADDRESS 0x3C 

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void setup() {
    Wire.begin();
    Serial.begin(115200);
  
    if (!display.begin(SSD1306_SWITCHCAPVCC, SCREEN_ADDRESS)) {
        Serial.println("OLED 初始化失败！");
        while (1);
    }

    display.clearDisplay();
}

void loop() {
    for (int progress = 0; progress <= 100; progress++) {
        display.clearDisplay();
        
        // 绘制进度条外框
        display.drawRect(10, 25, 100, 10, SSD1306_WHITE);

        // 绘制进度条填充
        display.fillRect(10, 25, progress, 10, SSD1306_WHITE);

        // 显示百分比
        display.setTextSize(1);
        display.setTextColor(SSD1306_WHITE);
        display.setCursor(50, 45);
        display.print(progress);
        display.print(" %");

        display.display();
        delay(50); // 控制进度速度
    }
}