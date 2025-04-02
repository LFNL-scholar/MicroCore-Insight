#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED 宽度
#define SCREEN_HEIGHT 64 // OLED 高度
#define OLED_RESET 4
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

int progress = 0;  // 进度（0 - 100）
bool isProgressComplete = false;  // 标记进度是否完成


void setup() {
    Serial.begin(115200);
    display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
    display.clearDisplay();
    display.display();
    
}

void loop() {
  display.clearDisplay();

  if(!isProgressComplete){
      draw_title("Progress");
      draw_progress_bar(progress);

      // 模拟进度条的速度，随机增速（控制更新步伐不一致）
      int increment = random(1, 5);  // 随机在1到5之间增加进度
      progress += increment;

      // 进度条达到100时重置
      if (progress >= 100) {
          progress = 100;
          isProgressComplete = true;
      }

      delay(random(50, 200));  // 随机延迟，模拟进度条不规则的更新速度
    
    }else{
      // 进度条完成后，显示主页
      draw_title("Home");  // 传入不同的标题
      display.setTextSize(1);
      display.setTextColor(SSD1306_WHITE);
      display.setCursor((SCREEN_WIDTH - 6 * 14) / 2, SCREEN_HEIGHT / 2);
      display.print("Welcome to Home");
    }

    display.display();
}

// 绘制标题
void draw_title(const char* title) {
    display.setTextSize(1);
    display.setTextColor(SSD1306_WHITE);
    
    int textWidth = 8 * strlen(title);  // 计算文本宽度（假设每个字符约 8 像素宽）
    
    display.setCursor((SCREEN_WIDTH - textWidth) / 2, 5); // 居中
    display.print(title);
}

// 绘制进度条和百分比
void draw_progress_bar(int percentage) {
    int barWidth = 100;  // 进度条宽度
    int barHeight = 10;  // 进度条高度
    int x = (SCREEN_WIDTH - barWidth) / 2; // 居中
    int y = (SCREEN_HEIGHT - barHeight) / 2; // 居中

    // 画进度条背景框
    display.drawRect(x, y, barWidth, barHeight, SSD1306_WHITE);
    
    // 填充进度
    int fillWidth = (percentage * barWidth) / 100;
    display.fillRect(x + 1, y + 1, fillWidth, barHeight - 2, SSD1306_WHITE);
    
    // 显示百分比（居中放在进度条下方）
    display.setTextSize(1);
    display.setCursor((SCREEN_WIDTH - 6 * 4) / 2, y + barHeight + 5);
    display.print(percentage);
    display.print("%");
}

