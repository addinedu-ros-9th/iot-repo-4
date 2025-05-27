/*
 * ESP32 D2 핀 깜빡이기 (Blink) 예제
 * D2 핀은 ESP32 DevKit에서 GPIO 2번에 해당합니다
 */

// LED 핀 정의 (D2는 GPIO 2번 핀)
const int ledPin = 2;  // D2 핀은 ESP32에서 GPIO 2번

// 변수 설정
int ledState = LOW;         // LED 상태 저장 변수
unsigned long previousMillis = 0;  // 마지막으로 LED 상태가 변경된 시간
const long interval = 1000;        // 깜빡임 간격 (밀리초)

void setup() {
  // 시리얼 통신 시작
  Serial.begin(115200);
  Serial.println("ESP32 D2 핀 깜빡이기 예제 시작");
  
  // LED 핀을 출력으로 설정
  pinMode(ledPin, OUTPUT);
}

void loop() {
  // 현재 시간 확인
  unsigned long currentMillis = millis();

  // 설정된 간격마다 LED 상태 변경
  if (currentMillis - previousMillis >= interval) {
    // 마지막 상태 변경 시간 저장
    previousMillis = currentMillis;

    // LED 상태 반전 (켜짐 <-> 꺼짐)
    if (ledState == LOW) {
      ledState = HIGH;
      Serial.println("LED 켜짐");
    } else {
      ledState = LOW;
      Serial.println("LED 꺼짐");
    }

    // 변경된 LED 상태 적용
    digitalWrite(ledPin, ledState);
  }
} 