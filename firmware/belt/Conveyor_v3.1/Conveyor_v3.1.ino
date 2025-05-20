#include <Servo.h>

const int MOTOR_PIN_A = 4;
const int MOTOR_PIN_B = 5;
const int MOTOR_PIN_PWM = 6;
const int SERVO_PIN = 9;
const int SENSOR_PIN_A = A0;
const int SENSOR_PIN_B = A1;

const int CDS_THRESHOLD_LOW = 70;
const int CDS_THRESHOLD_HIGH = 180;
const int MOTOR_SPEED =254;

bool debugMode = false;
unsigned long lastDebugTime = 0;
const unsigned long DEBUG_INTERVAL = 1000;

#define ROUTE_A 0
#define ROUTE_B 1
#define ROUTE_NONE 2

int currentRoute = ROUTE_A;
int routeLock = ROUTE_NONE;

unsigned long motorStartTime = 0;
unsigned long motorEndTime = 0;
unsigned long remainingTime = 0;
const unsigned long MOTOR_DURATION = 20000;
bool motorRunning = false;

Servo conveyorServo;

bool fullA_state = false;
bool fullB_state = false;
int fullACounter = 0;
int fullBCounter = 0;
const int STABLE_COUNT = 5;

void setup() 
{
  pinMode(MOTOR_PIN_A, OUTPUT);
  pinMode(MOTOR_PIN_B, OUTPUT);
  pinMode(MOTOR_PIN_PWM, OUTPUT);
  Serial.begin(9600);
  conveyorServo.attach(SERVO_PIN);
  conveyorServo.write(70);
  Serial.println("BELT_ROUTE_A");
  Serial.println("벨트 컨트롤러 초기화 완료. 'CDS_VALUE' 명령으로 센서값 확인 가능");
}

void loop() {
  
  reportStatus();

  if (debugMode && (millis() - lastDebugTime > DEBUG_INTERVAL)) {
    reportCDSValues();
    lastDebugTime = millis();
  }

  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');
    command.trim();

    if (command == "BELT_RUN" && !motorRunning) {
      if (decideRoute()) {
        startMotor(MOTOR_DURATION);
      }
    } else if (command == "BELT_STOP" || command == "E") {
      stopMotor();
    } else if (command == "CDS_VALUE") {
      reportCDSValues();
    } else if (command == "DEBUG_ON") {
      debugMode = true;
      Serial.println("DEBUG_MODE:ON");
    } else if (command == "DEBUG_OFF") {
      debugMode = false;
      Serial.println("DEBUG_MODE:OFF");
    } else if (command == "CALIBRATE") {
      calibrateCDS();
    }
  }

  if (motorRunning) {
    if (millis() >= motorEndTime) {
      stopMotor();
    }

    if (isWarehouseFullStable(currentRoute)) {
      unsigned long elapsed = millis() - motorStartTime;
      stopMotor();
      remainingTime = motorEndTime - millis();

      if (currentRoute == ROUTE_A && !isWarehouseFullStable(ROUTE_B)) {
        currentRoute = ROUTE_B;
        routeLock = ROUTE_B;
        conveyorServo.write(90);
        Serial.println("BELT_ROUTE_B");
      } 
      else if (currentRoute == ROUTE_B && !isWarehouseFullStable(ROUTE_A)) {
        currentRoute = ROUTE_A;
        routeLock = ROUTE_A;
        conveyorServo.write(70);
        Serial.println("BELT_ROUTE_A");
      } 
      else {
        Serial.println("BELT_ALL_FULL while Running");
        return;
      }

      delay(1000);
      startMotor(remainingTime);
      Serial.println(remainingTime);
    }
  }
}

void reportCDSValues() {
  int valueA = getAveragedSensor(SENSOR_PIN_A);
  int valueB = getAveragedSensor(SENSOR_PIN_B);
  Serial.print("CDS_VALUE:A=");
  Serial.print(valueA);
  Serial.print(",B=");
  Serial.print(valueB);
  Serial.print(",FULL_A=");
  Serial.print(fullA_state ? "YES" : "NO");
  Serial.print(",FULL_B=");
  Serial.println(fullB_state ? "YES" : "NO");
}

void calibrateCDS() {
  Serial.println("CALIBRATING_START");
  
  int minA = 1023, maxA = 0;
  int minB = 1023, maxB = 0;
  
  for (int i = 0; i < 50; i++) {
    int valueA = analogRead(SENSOR_PIN_A);
    int valueB = analogRead(SENSOR_PIN_B);
    
    minA = min(minA, valueA);
    maxA = max(maxA, valueA);
    minB = min(minB, valueB);
    maxB = max(maxB, valueB);
    
    Serial.print(".");
    delay(100);
  }
  Serial.println();
  
  int thresholdLowA = (int)(minA + (maxA-minA) * 0.3);
  int thresholdHighA = (int)(minA + (maxA-minA) * 0.7);
  int thresholdLowB = (int)(minB + (maxB-minB) * 0.3);
  int thresholdHighB = (int)(minB + (maxB-minB) * 0.7);
  
  Serial.print("CALIBRATION_RESULT:A=");
  Serial.print(minA);
  Serial.print("-");
  Serial.print(maxA);
  Serial.print(",B=");
  Serial.print(minB);
  Serial.print("-");
  Serial.println(maxB);
  
  Serial.print("SUGGESTED_THRESHOLDS:LOW=");
  Serial.print(thresholdLowA);
  Serial.print(",HIGH=");
  Serial.println(thresholdHighA);
}

bool decideRoute() {
  if (routeLock != ROUTE_NONE) {
    currentRoute = routeLock;
    return true;
  }

  bool fullA = isWarehouseFullStable(ROUTE_A);
  bool fullB = isWarehouseFullStable(ROUTE_B);

  if (!fullA) {
    currentRoute = ROUTE_A;
    routeLock = ROUTE_A;
  } else if (!fullB) {
    currentRoute = ROUTE_B;
    routeLock = ROUTE_B;
  } else {
    Serial.println("BELT_ALL_FULL at beginning");
    return false;
  }

  if (currentRoute == ROUTE_A) {
    conveyorServo.write(50);
    Serial.println("BELT_ROUTE_A");
  } else {
    conveyorServo.write(130);
    Serial.println("BELT_ROUTE_B");
    delay(800);
  }

  return true;
}

void startMotor(unsigned long duration) {
  digitalWrite(MOTOR_PIN_A, HIGH);
  digitalWrite(MOTOR_PIN_B, LOW);
  analogWrite(MOTOR_PIN_PWM, MOTOR_SPEED);
  motorStartTime = millis();
  motorEndTime = motorStartTime + duration;
  motorRunning = true;
  
  Serial.print("DURATION_MS:");
  Serial.println(duration);
  Serial.println("BELT_RUNNING");
}

void stopMotor() {
  digitalWrite(MOTOR_PIN_A, LOW);
  digitalWrite(MOTOR_PIN_B, LOW);
  analogWrite(MOTOR_PIN_PWM, 0);
  motorRunning = false;
  Serial.println("BELT_STOPPED");
}

int getAveragedSensor(int pin) {
  long sum = 0;
  for (int i = 0; i < 10; i++) {
    sum += analogRead(pin);
    delay(2);
  }
  return sum / 10;
}

bool isWarehouseFullStable(int route) {
  int value = 0;
  if (route == ROUTE_A) {
    value = getAveragedSensor(SENSOR_PIN_A);
    if (value < CDS_THRESHOLD_LOW) {
      if (fullACounter < STABLE_COUNT) fullACounter++;
    } else if (value > CDS_THRESHOLD_HIGH) {
      if (fullACounter > 0) fullACounter--;
    }
    fullA_state = (fullACounter >= STABLE_COUNT);
    return fullA_state;
  } else {
    value = getAveragedSensor(SENSOR_PIN_B);
    if (value < CDS_THRESHOLD_LOW) {
      if (fullBCounter < STABLE_COUNT) fullBCounter++;
    } else if (value > CDS_THRESHOLD_HIGH) {
      if (fullBCounter > 0) fullBCounter--;
    }
    fullB_state = (fullBCounter >= STABLE_COUNT);
    return fullB_state;
  }
}

unsigned long lastReportTime = 0;
const unsigned long REPORT_INTERVAL = 300;

void reportStatus() {
  static bool lastAState = false;
  static bool lastBState = false;


  

  if (millis() - lastReportTime < REPORT_INTERVAL) return;

  

  bool aNow = isWarehouseFullStable(ROUTE_A);
  bool bNow = isWarehouseFullStable(ROUTE_B);

  if (aNow != lastAState || bNow != lastBState) {
    
    if (aNow != lastAState)
      Serial.println(aNow ? "BELT_A_FULL" : "BELT_A_EMPTY");
    if (bNow != lastBState)
      Serial.println(bNow ? "BELT_B_FULL" : "BELT_B_EMPTY");

    lastAState = aNow;
    lastBState = bNow;
    lastReportTime = millis();
  }
}

