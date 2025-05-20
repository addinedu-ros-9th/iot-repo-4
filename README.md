![배너](https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/banner.png?raw=true)

> **이 프로젝트는 RFID 태그를 따라 주행하는 소형 AGV가 설비와 실시간으로 통신하며 미션을 수행하는, IoT 기반 통합 운송 관제 시스템입니다.**  
> **트럭(AGV)은 ESP32로 제어되며, 게이트/벨트/적재소 등 설비와 FSM 기반 서버를 통해 실시간 통합 제어됩니다. GUI 시스템은 운송 흐름을 시각적으로 모니터링하고 제어할 수 있도록 구현되었습니다..**

[시스템 소개 영상](https://youtu.be/AI76I9BiS1k?si=EfL9UZIdROXblnkd)

[전체 구동 영상](https://youtu.be/LJ2RT1eQdgk)

---

## 📚 목차


| 순서 | 항목 |
|------|------|
| **1** | **팀 구성** |
| **2** | **프로젝트 개요** |
| **3** | **기술 스택** |
| **4** | **프로젝트 목적** |
| **5** | **요구사항 정의** |
| **6** | **시스템 구성** |
| **7** | **데이터베이스 구성** |
| **8** | **통신 구조** |
| **9** | **기능 설명** |
| **10** | **기술적 문제 및 해결** |
| **11** | **구현 제약 및 확장 가능성** |
| **12** | **디렉토리 구조** |


---

# 🚚 IoT 기반 소형 AGV 통합 관제 시스템


## 👥 1. 팀 구성

<table>
  <thead>
    <tr>
      <th>이름</th>
      <th>GitHub</th>
      <th>역할</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><strong>김대인</strong></td>
      <td>
        <a href="https://github.com/Daeinism">
          <img src="https://img.shields.io/badge/github-Daeinism-181717?style=flat-square&logo=github&logoColor=white">
        </a>
      </td>
      <td>
        (작성 예정)
      </td>
    </tr>
    <tr>
      <td><strong>이건우</strong></td>
      <td><span style="color: gray;">-</span></td>
      <td>
        (작성 예정)
      </td>
    </tr>
    <tr>
      <td><strong>이승훈</strong></td>
      <td>
        <a href="https://github.com/leesh0806">
          <img src="https://img.shields.io/badge/github-leesh0806-181717?style=flat-square&logo=github&logoColor=white">
        </a>
      </td>
      <td>
        AGV모듈 개발 및 기구설계<br>
        AGV 회로 설계<br>
        라인주행 제어 알고리즘 구현<br>
        AGV FSM상태기반 주행제어 구현<br>
        AGV TCP통신 명령 송수신 프로토콜 제작<br>
      </td>
    </tr>
    <tr>
      <td><strong>장진혁</strong></td>
      <td>
        <a href="https://github.com/jinhyuk2me">
          <img src="https://img.shields.io/badge/github-jinhyuk2me-181717?style=flat-square&logo=github&logoColor=white">
        </a>
      </td>
      <td>
        FSM 제어 흐름 및 상태 전이 구현<br>
        AGV TCP 통신 구조 설계 및 명령 송수신 구현<br>
        설비 시리얼 제어 모듈 개발 (게이트, 벨트, 적재소)<br>
        GUI 시스템 개발 (PyQt6 기반, 탭별 기능 구현)<br>
        DB 테이블 설계 및 상태 로그 저장 시스템 구축<br>
      </td>
    </tr>
  </tbody>
</table>

---

## 📦 2. 프로젝트 개요

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/gui/main_monitoring_1.gif?raw=true" width="45%" style="margin-right:10px;">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/facilities/gate_1.gif?raw=true" width="45%">
</p>

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/facilities/belt_2.gif?raw=true" width="45%" style="margin-right:10px;">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/facilities/load_1.gif?raw=true" width="45%">
</p>

> ⏰ **프로젝트 기간**: 2025.05.03 ~ 2025.05.15

`D.U.S.T. (Dynamic Unified Smart Transport)`는 RFID 기반 위치 인식을 바탕으로 경로를 따라 주행하는 소형 AGV를 중심으로, 게이트, 컨베이어 벨트, 적재소 등 물류 설비를 실시간으로 통합 제어하는 IoT 기반 운송 관제 시스템입니다.

이 시스템은 FSM(Finite State Machine) 기반의 서버 제어 흐름과 TCP/Serial 통신, 그리고 PyQt 기반 GUI 관제 화면을 통합하여, 운송 흐름을 일관되게 제어하고 시각화할 수 있도록 설계되었습니다.

### 🧭 주요 특징

- AGV는 RFID 태그를 인식하며 지정된 경로를 자동 주행
- 설비(게이트/벨트/적재소)는 서버 명령에 따라 자동 응답 및 작동
- FSM 기반 서버가 AGV 상태와 설비 동작을 실시간으로 판단하고 명령 전송
- PyQt 기반 GUI를 통해 전체 흐름을 시각적으로 모니터링하고, 사용자가 수동으로 제어할 수 있도록 구현

### 🎯 구현 범위

- 서버 FSM 기반 상태 제어 흐름 설계 및 구현
- ESP32 기반 소형 AGV 펌웨어 개발 및 센서 연동
- TCP 통신 기반 AGV 제어 및 상태 보고 구조 구현
- Serial 통신 기반 설비 제어 모듈 설계 및 구현
- PyQt GUI 기반 관제 인터페이스 설계 (탭별 기능 구성)
- MySQL 기반 상태/미션/로그 관리 시스템 구축
  
---

## 🤖 AGV란? & 프로젝트 AGV 소개

### 🚚 AGV란? (Automated Guided Vehicle)

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/agv.jpg?raw=true" width="90%">
</p>

AGV는 **사람의 개입 없이 자동으로 지정된 경로를 따라 이동하며 작업을 수행하는 무인 운반 차량**을 의미합니다. 산업 현장에서는 물류 이송, 자재 공급, 제품 이동 등 다양한 작업에 사용되며, 다음과 같은 특징을 가집니다:

- **경로 기반 자율 주행**: 선, QR, RFID, LiDAR 등 다양한 방식으로 경로를 인식하고 이동  
- **안전성 확보**: 초음파, IR, 라이다 등의 센서를 통해 장애물 감지 및 비상 정지  
- **중앙 제어 연동**: 서버 또는 PLC 기반 시스템과 연동되어 상태 보고 및 명령 수행  
- **자동화 효율성**: 반복 작업을 안정적으로 수행하여 인력 비용 절감 및 작업 효율 증가

### 🛠️ 본 프로젝트의 소형 AGV

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/truck/truck_3.jpg?raw=true" width="90%">
</p>

이번 프로젝트에서 구현된 AGV는 **ESP32 기반의 경량 무인 차량**으로, 다음과 같은 구성 요소와 기능을 포함합니다:

| 항목 | 설명 |
|------|------|
| **제어 MCU** | ESP32-WROOM (Wi-Fi 통신 및 GPIO 제어) |
| **위치 인식** | RFID 태그를 통해 각 지점 도착 여부 판단 |
| **주행 알고리즘** | IR 센서 기반 라인트레이서 + PID 제어 방식 |
| **장애물 감지** | 초음파 센서로 전방 장애물 인식 후 자동 정지 |
| **통신 방식** | Wi-Fi 기반 TCP 클라이언트 (서버와 양방향 메시지 송수신) |
| **상태 보고** | 현재 위치, 배터리 상태, FSM 상태를 주기적으로 서버에 전송 |
| **자동 충전 전환** | 미션 종료 후 대기소 도착 시, 배터리 잔량에 따라 충전 상태로 자동 진입 |
| **FSM 기반 동작 흐름** | RUN, ARRIVED, START_LOADING, EMERGENCY 등 서버 FSM 상태에 따라 행동 결정 |

---

## 🛠️ 3. 기술 스택

| 분류 | 기술 구성 | |
|------|-----------|--|
| **개발 환경** | Linux (Ubuntu 24.04) | ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=white) ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=Ubuntu&logoColor=white) |
| **MCU 및 펌웨어** | ESP32-WROOM, Arduino IDE | ![ESP32](https://img.shields.io/badge/ESP32-WROOM-E7352C?style=for-the-badge&logo=espressif&logoColor=white) ![Arduino](https://img.shields.io/badge/Arduino-00979D?style=for-the-badge&logo=arduino&logoColor=white) |
| **프로그래밍 언어** | Python 3.12, C++ | ![Python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![C++](https://img.shields.io/badge/c++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white) |
| **관제 UI** | PyQt6 | ![PyQt6](https://img.shields.io/badge/PyQt6-41CD52?style=for-the-badge&logo=qt&logoColor=white) |
| **DB 연동** | MySQL | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white) |
| **버전 관리** | Git, GitHub | ![Git](https://img.shields.io/badge/git-F05032?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-181717?style=for-the-badge&logo=github&logoColor=white) |
| **협업 툴** | Confluence, Slack, Jira | ![Confluence](https://img.shields.io/badge/confluence-172B4D?style=for-the-badge&logo=confluence&logoColor=white) ![Slack](https://img.shields.io/badge/slack-4A154B?style=for-the-badge&logo=slack&logoColor=white) ![Jira](https://img.shields.io/badge/Jira-0052CC?style=for-the-badge&logo=Jira&logoColor=white) |

---

## 🎯 4. 프로젝트 목적 / 필요성

본 프로젝트는 **소형 AGV(Automated Guided Vehicle)** 를 기반으로, **물류 자동화 시나리오의 흐름을 단일 제어 구조로 통합**하는 데 목적이 있습니다.

단순한 주행 제어나 센서 통신 구현을 넘어, AGV 이동부터 설비 제어, 상태 모니터링, 사용자 인터페이스까지 모든 흐름을 FSM 기반으로 통합 제어하는 것을 핵심 목표로 삼았습니다.

### 🔍 추진 배경

- 산업 현장에서는 AGV가 **정해진 경로를 따라 자율 주행하며**, 다양한 설비(게이트, 벨트, 저장소)와 **연동되는 시스템**이 점점 요구되고 있습니다.
- 이런 시스템은 단순 하드웨어 구성만으로는 구현이 어렵고, **센서 데이터 처리 → 판단 로직 → 제어 명령 → 시각화 UI**까지 전체 흐름이 유기적으로 연결되어야 합니다.
- 본 프로젝트는 이러한 구성 요소를 직접 설계 및 개발하며, **작동 흐름 전체가 일관된 FSM 구조로 제어되는 통합 관제 시스템**을 구현하였습니다.

### ✅ 핵심 의의

- **소형 AGV의 경로 주행부터 미션 처리까지 FSM으로 구성**
- **중앙 제어 서버가 AGV와 설비를 실시간으로 판단 및 제어**
- **GUI에서 실시간 상태 모니터링 및 수동 개입 가능**
- **센서 입력 → 제어 명령 → UI 반영 → DB 기록까지 전 과정 일관성 유지**

---


## 🧾 5. 요구사항 정의 (UR / SR)

본 시스템의 기능은 사용자 관점에서의 요구사항(**User Requirement, UR**)과  이를 만족시키기 위한 시스템 관점의 요구사항(**System Requirement, SR**)으로 나뉘며, 각 항목은 구현된 기능 기준으로 우선순위(Priority)를 함께 정의하였습니다.

### ✅ User Requirement (UR)
RFID 인식 직전에 약 0.5초간 PID 제어를 일시 정지하고, 기존 PWM 출력을 유지하는 방식으로 주행 안정성을 확보했습니다.
| ID | 요구사항 내용 | 우선순위 |
|----|----------------|---------|
| UR_01 | AGV는 특정 장소로 이동할 수 있어야 한다. | R |
| UR_02 | 이동에 사용되는 AGV는 무인 주행이 가능해야 한다. | O |
| UR_03 | 권한 있는 사용자만 시스템에 접속할 수 있어야 한다. | R |
| UR_04 | AGV 이동 단계별 상태를 실시간으로 모니터링할 수 있어야 한다. | R |
| UR_05 | AGV의 상태 기록을 저장하고 조회할 수 있어야 한다. | R |
| UR_06 | 각 시설의 상태를 모니터링할 수 있어야 한다. | R |
| UR_07 | AGV 출입은 허가된 AGV에 한해 이루어져야 한다. | R |
| UR_08 | 자동화된 적재 시설이 존재해야 한다. | R |
| UR_09 | 적재 시설은 수동 제어도 가능해야 한다. | O |
| UR_10 | AGV는 자동으로 화물을 적하할 수 있어야 한다. | R |
| UR_11 | 화물 저장소가 자동화되어 있어야 한다. | R |
| UR_12 | 저장소는 가용성을 고려해 자동으로 선택되어야 한다. | O |
| UR_13 | 저장소는 상황에 따라 동작을 정지할 수 있어야 한다. | R |

> 우선순위(R: Required / O: Optional)는 개발 당시의 시스템 구조 설계 기준이며, 대부분의 필수 요구사항은 이번 구현에 포함되어 있으며, 일부 선택 항목도 기본 동작 구조 내 포함되어 있습니다.

---

### ✅ System Requirement (SR)

| ID | 기능명 | 설명 |
|-----|--------|------|
| SR_01 | AGV 모니터링 기능 | AGV의 위치, 상태, 미션 진행 상황을 실시간 확인 |
| SR_02 | 시설 모니터링 기능 | 게이트, 벨트, 적재소 등 주요 시설 상태 시각화 |
| SR_03 | 사용자 권한 관리 기능 | 로그인, 접근 권한 설정 및 사용자 정보 관리 |
| SR_04 | 작업 관리 기능 | 미션 등록, 실행, 로그 기록 및 조회 기능 |
| SR_05 | 중앙 통제 기능 | AGV와 시설을 통합 제어하는 FSM 기반 중앙 서버 |
| SR_06 | AGV 자동 주행 기능 | 지정 경로에 따라 무인 주행 및 장애물 정지 |
| SR_07 | 화물 적하 기능 | 적재 완료 후 화물을 자동으로 하역 |
| SR_08 | 위치 인식 기능 | RFID 기반으로 AGV 위치 판단 및 상태 연동 |
| SR_09 | 상태 보고 기능 | 미션, 위치, 배터리 등의 상태를 서버에 실시간 송신 |
| SR_10 | 출입 제어 기능 | AGV 출입 여부를 게이트에서 확인 및 제한 |
| SR_11 | 게이트 자동 제어 기능 | AGV 통과 여부에 따라 자동 개폐 수행 |
| SR_12 | 적재소 AGV 감지 기능 | AGV 도착 여부 인식 및 응답 처리 |
| SR_13 | 적재소 자동 제어 기능 | 서버 명령에 따라 화물 적하 자동 수행 |
| SR_14 | 적재소 수동 제어 기능 | 수동으로 화물 투하 명령을 내릴 수 있음 (GUI 포함) |
| SR_15 | 벨트 이송 제어 기능 | 중앙 서버 명령에 따라 벨트 작동 및 정지 |
| SR_16 | 저장소 적재량 감지 기능 | 컨테이너의 실시간 적재 상태 모니터링 |
| SR_17 | 저장소 선택 자동화 기능 | 저장소 가용성에 따라 자동으로 저장 대상 결정 |
| SR_18 | 자동 정지 기능 | 중앙 명령 또는 저장소 포화 시 운송 흐름 정지 |
| SR_19 | 충전소 기능 | 배터리 상태에 따라 자동 충전 또는 대기 상태 전환 |

---

### 🔗 UR ↔ SR 매핑 관계
70
| 사용자 요구사항 (UR) | 관련 시스템 기능 (SR) |
|----------------------|------------------------|
| UR_01 AGV는 특정 장소로 이동할 수 있어야 한다. | SR_06, SR_08 |
| UR_02 이동에 사용되는 AGV는 무인 주행이 가능해야 한다. | SR_06 |
| UR_03 권한 있는 사용자만 시스템에 접속할 수 있어야 한다. | SR_03 |
| UR_04 AGV 이동 단계별 상태를 실시간으로 모니터링할 수 있어야 한다. | SR_01, SR_09 |
| UR_05 AGV의 상태 기록을 저장하고 조회할 수 있어야 한다. | SR_04, SR_09 |
| UR_06 각 시설의 상태를 모니터링할 수 있어야 한다. | SR_02, SR_15, SR_16 |
| UR_07 AGV 출입은 허가된 AGV에 한해 이루어져야 한다. | SR_10, SR_11 |
| UR_08 자동화된 적재 시설이 존재해야 한다. | SR_13 |
| UR_09 적재 시설은 수동 제어도 가능해야 한다. | SR_14 |
| UR_10 AGV는 자동으로 화물을 적하할 수 있어야 한다. | SR_07, SR_13 |
| UR_11 화물 저장소가 자동화되어 있어야 한다. | SR_15, SR_16 |
| UR_12 저장소는 가용성을 고려해 자동으로 선택되어야 한다. | SR_17 |
| UR_13 저장소는 상황에 따라 동작을 정지할 수 있어야 한다. | SR_18 |

---

## 🧩 6. 시스템 구성

## 6-1 시스템 아키텍처

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/system_architecture/system.png?raw=true" width="85%">
</p>

이 시스템은 AGV, 서버, 설비, GUI가 유기적으로 연결된 IoT 기반 통합 제어 구조로 설계되었습니다.

### 🧱 통신 구조

- **TCP 통신**: AGV ↔ 서버 (양방향 실시간 명령/상태 보고)
- **시리얼 통신**: 서버 ↔ 설비 컨트롤러 (게이트/벨트/적재소)
- **HTTP API**: GUI ↔ 서버 API 서버 (Flask 기반 REST 호출)

### 🧠 서버 소프트웨어 계층

| 구성 요소 | 역할 |
|-----------|------|
| **MainController** | 전체 FSM 흐름 제어 및 명령 분배 |
| **TruckFSM** | AGV 상태 전이 FSM 처리 |
| **FacilityManager** | 설비 명령 라우팅 및 제어 |
| **StatusManager** | 상태 수집 및 DB 반영 |
| **MissionManager** | 미션 등록/변경/기록 처리 |

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/system_architecture/sw.png?raw=true" width="85%">
</p>

### 🏗 하드웨어 구성

- AGV: ESP32 제어, 센서 장착, DC 모터 구동
- 설비: 아두이노 기반 (게이트/벨트/디스펜서)
- 충전소: 배터리 상태 감지 및 응답용 구성

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/system_architecture/hw.png?raw=true" width="85%">
</p>

---

## 6-2. 시스템 시퀀스

### 1. 시스템 전체 흐름
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/scenario/system.png?raw=true" width="85%">
</p>

### 2. 배터리 상태 변화
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/scenario/battery.png?raw=true" width="85%">
</p>

### 3. **로그인 & 미션 등록**
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/scenario/login.png?raw=true" width="85%">
</p>

### 4. **장애물 감지 및 비상 중단**
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/scenario/obstacle.png?raw=true" width="85%">
</p>

### 5. **벨트 제어 및 경로 관리**
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/scenario/belt.png?raw=true" width="85%">
</p>

---

## 6-3. FSM기반 상태제어 흐름

AGV는 FSM(Finite State Machine)을 기반으로 동작하며, 제어 서버에서의 상태 판단, 설비 응답 처리, 통신 흐름, GUI 반영까지 하나의 FSM 구조 안에서 통합적으로 제어됩니다.

아래는 서버 FSM에서 제어되는 AGV 상태 흐름을 시각화한 다이어그램입니다.

```mermaid
stateDiagram-v2
    [*] --> IDLE

    IDLE --> ASSIGNED : ASSIGN_MISSION
    ASSIGNED --> MOVING : RUN

    MOVING --> WAITING : ARRIVED (e.g. GATE_A)
    WAITING --> LOADING : START_LOADING (at LOAD_A/B)
    WAITING --> UNLOADING : START_UNLOADING (at BELT)

    LOADING --> MOVING : FINISH_LOADING
    UNLOADING --> MOVING : FINISH_UNLOADING

    MOVING --> IDLE : ARRIVED @ STANDBY + NO MISSION
    MOVING --> CHARGING : START_CHARGING
    CHARGING --> IDLE : FINISH_CHARGING

    [*] --> EMERGENCY : EMERGENCY_TRIGGERED
    EMERGENCY --> IDLE : RESET
```

---

## 🗄️ 7. 데이터베이스 구성 및 출처

본 시스템은 AGV, 미션, 설비, 사용자, 상태 기록 등 주요 항목을 MySQL 기반으로 테이블화하여 관리하며, 각 항목은 기능별로 나뉜 **모듈형 테이블 구조**로 구성되어 있습니다.

### 🧠 ERD (Entity Relationship Diagram)

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/erd/erd.png?raw=true" width="85%">
</p>
※ 시스템 내 모든 구성요소가 DB 기반으로 통합 관리됨

### 📊 테이블 그룹별 구성

#### 🚚 AGV 관련

| 테이블명 | 설명 |
|----------|------|
| `TRUCK` | AGV 기본 정보 (ID, 이름 등) |
| `BATTERY_STATUS` | AGV의 배터리 잔량, FSM 상태, 이벤트 유형, 시점 기록 |
| `POSITION_STATUS` | AGV 위치, 상태, 시간 기록 (FSM 기준) |

#### 📦 임무(Mission) 관련

| 테이블명 | 설명 |
|----------|------|
| `MISSIONS` | 화물 종류, 수량, 출발지/도착지, 미션 상태 및 타임스탬프 기록 |
- AGV와 1:N 관계를 가지며, 미션 진행 단계를 시간 순으로 관리합니다.

#### 🏗 설비 관련

| 테이블명 | 설명 |
|----------|------|
| `FACILITY` | 시설 기본 정보 (게이트, 벨트, 컨테이너 등) |
| `GATE_STATUS` | 게이트 A/B 개폐 여부 및 타임스탬프 |
| `BELT_STATUS` | 컨베이어 벨트 작동 여부 |
| `CONTAINER_STATUS` | 컨테이너 A/B의 포화 여부 상태 기록 |

#### 👤 사용자 관련

| 테이블명 | 설명 |
|----------|------|
| `USERS` | 사용자 계정, 비밀번호, 역할(role) 등 로그인 정보 |
| `LOGIN_LOGS` | 로그인 시도, 성공/실패 여부, 시각 기록 |

### 🔄 데이터 흐름 및 활용 방식

- **AGV → 서버 (TCP)**  
  → 배터리 잔량, 위치, FSM 상태 주기적 보고 → `BATTERY_STATUS`, `POSITION_STATUS`

- **GUI → 서버 (API)**  
  → 미션 등록 요청 / 수동 제어 → `MISSIONS` / `FACILITY` 상태 갱신

- **시설 컨트롤러 → 서버 (Serial)**  
  → 벨트 작동, 게이트 개폐, 포화 상태 보고 → `GATE_STATUS`, `BELT_STATUS`, `CONTAINER_STATUS`

- **서버 내부 FSM**  
  → 이벤트 기반으로 상태 변경 기록 및 DB 반영 → 트리거형 상태 저장 구조

### ✅ 설계 특징 요약

- **모듈별 책임 분리**  
  → AGV/미션/설비/사용자 정보를 명확히 분리하여 구조화

- **상태 기반 기록 구조**  
  → `BATTERY_STATUS`, `POSITION_STATUS`, `GATE_STATUS` 등은 모두 시계열 기반 로그 테이블로 설계되어  
     제어 흐름을 추적하거나 문제 발생 시 원인 분석이 가능합니다.

- **가독성 높은 확장형 설계**  
  → 시설 종류(FACILITY)와 관련 상태 테이블을 분리 설계하여 향후 장치 추가 시 구조 유지 가능

> 미션 생성부터 AGV 운행, 설비 동작, 상태 기록까지 모든 흐름이 하나의 제어 구조로 연결되어 있으며, 관련 데이터는 단일 DB에서 통합 관리할 수 있도록 설계되었습니다.

---

## 📡 8. 통신 구조

본 시스템은 AGV, 설비, GUI 간의 실시간 상호작용을 위해 **TCP 통신**, **Serial 통신**, **HTTP API 통신**의 세 가지 방식을 조합하여 구현되었습니다.

각 통신 방식은 독립적이지만, **중앙 서버의 FSM 제어 흐름에 따라 긴밀히 연결**되어 작동합니다.

### 🛰 1. AGV ↔ 중앙 서버: **TCP 통신**

#### ✅ 메시지 포맷

- **2가지 형식 지원**:
  - JSON 기반 메시지 (디버깅, 해석 용이)
  - Byte 기반 메시지 (경량/고속 전송)

#### 🔸 JSON 메시지 예시

```json
{
  "sender": "TRUCK_01",
  "receiver": "SERVER",
  "cmd": "ARRIVED",
  "payload": {
    "position": "CHECKPOINT_A"
  }
}
```

#### 🔸 Byte 메시지 포맷 (Header + Payload 구조)

| 필드        | 크기(byte) | 설명                            |
|-------------|-------------|---------------------------------|
| sender_id   | 1           | 송신자 ID (e.g., 0x01 = TRUCK)  |
| receiver_id | 1           | 수신자 ID (e.g., 0x10 = SERVER) |
| cmd_id      | 1           | 명령 코드                       |
| payload_len | 1           | 페이로드 길이                   |
| payload     | 가변        | 명령어별 데이터                 |

#### 🔹 주요 명령 예시

**AGV → 서버**

- `ARRIVED` (0x01): 위치 도착 알림  
- `OBSTACLE` (0x02): 장애물 감지 보고  
- `STATUS_UPDATE` (0x03): 배터리/위치 상태 보고  
- `START_LOADING`, `FINISH_UNLOADING` 등

**서버 → AGV**

- `MISSION_ASSIGNED` (0x10): 미션 할당  
- `RUN` / `STOP`: 주행 시작/정지  
- `GATE_OPENED`: 게이트 개방 알림

> FSM 상태 전이는 이 메시지 흐름에 따라 자동 수행됩니다.

### ⚙️ 2. 설비 ↔ 중앙 서버: **Serial 통신**

#### ✅ 설비 구성

- Gate Controller (게이트 개폐)  
- Belt Controller (벨트 작동)  
- Dispenser Controller (자원 투하)

#### 🔸 명령 방식

- **송신**: 서버 → 설비 (명령어 전송)  
- **수신**: 설비 → 서버 (상태 회신)

#### 🔸 예시 명령어

| 명령        | 설명              |
|-------------|-------------------|
| `GATE_A_OPEN`    | 게이트 A 개방     |
| `BELT_RUN`   | 벨트 작동 시작    |
| `DISPENSER_OPEN` | 자원 투하 실행 |

### 🌐 3. GUI ↔ 중앙 서버: **HTTP REST API**

#### ✅ 기본 정보

- Base URL: `/api`
- Protocol: HTTP  
- Content-Type: `application/json`

#### 🔸 주요 API 엔드포인트

| 메서드 | 엔드포인트                              | 설명                          |
|--------|------------------------------------------|-------------------------------|
| GET    | `/api/trucks`                            | 모든 AGV 상태 조회           |
| GET    | `/api/trucks/{truck_id}`                 | 특정 AGV 상태 조회           |
| POST   | `/api/missions`                          | 미션 생성                     |
| POST   | `/api/facilities/gates/{id}/control`     | 게이트 열기/닫기              |
| POST   | `/api/facilities/belt/control`           | 벨트 시작/정지                |

#### 🔸 예시 요청/응답

**미션 생성 요청**
```json
{
  "mission_id": "MISSION_001",
  "cargo_type": "SAND",
  "cargo_amount": 100.0,
  "source": "LOAD_A",
  "destination": "BELT"
}
```

**AGV 상태 응답**
```json
{
  "TRUCK_01": {
    "battery": {"level": 87.0, "is_charging": false},
    "position": {"location": "CHECKPOINT_A", "status": "IDLE"},
    "fsm_state": "IDLE"
  }
}
```

### ✅ 통신 방식 비교 요약

| 구성          | 방식           | 역할 및 특징                            |
|---------------|----------------|-----------------------------------------|
| AGV ↔ 서버   | TCP (JSON/Byte)| 명령 송수신 / 상태 보고 (실시간 FSM 연동) |
| 설비 ↔ 서버   | Serial         | 명령 기반 제어 및 상태 회신             |
| GUI ↔ 서버    | HTTP API       | 미션 등록, 상태 조회, 수동 제어 기능     |

> 각 통신 구조는 독립적으로 작동하지만, 중앙 서버의 FSM 흐름에 따라 유기적으로 동기화되어 작동합니다.

---


 ## ⚙️ 9. 기능 설명
 

### 🚚 AGV 관련 기능

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/truck/truck_1.gif?raw=true" width="45%" style="margin-right:10px;">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/truck/truck_2.gif?raw=true" width="45%">
</p>

| 기능 | 설명 |
|------|------|
| **자동 주행** | AGV는 ESP32로 제어되며, RFID 태그를 따라 지정된 경로를 자동으로 주행합니다. |
| **위치 인식 및 보고** | RFID 태그를 인식해 현재 위치를 판단하고, 서버에 위치를 주기적으로 송신합니다. |
| **배터리 상태 모니터링** | 배터리 잔량 및 FSM 상태를 서버에 주기적으로 보고하며, 충전 필요 여부를 판단합니다. |
| **미션 수행** | 서버로부터 미션을 할당받고, 상태에 따라 FSM 전이 및 도착 후 하역을 자동 수행합니다. |
| **충돌 방지** | 초음파 센서를 통해 장애물을 감지하고 정지하도록 구현되어 있습니다. |
| **AGV 소켓 자동 등록** | 미등록 상태의 AGV도 TEMP 소켓으로 임시 등록되며, 정상적인 ID로 자동 재매핑됩니다. |
| **FSM 상태 회복 처리** | AGV FSM은 상태 불일치 시에도 강제로 상태를 보정하여 정상 흐름을 유지합니다. |

---

### 🏗 시설 제어 기능

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/facilities/gate_1.gif?raw=true" width="30%" style="margin-right:10px;">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/facilities/load_1.gif?raw=true" width="30%" style="margin-right:10px;">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/facilities/belt_1.gif?raw=true" width="30%">
</p>

| 기능 | 설명 |
|------|------|
| **게이트 제어** | 등록된 AGV 접근 시 자동 개방, 미등록 AGV 접근 시 차단됩니다. |
| **벨트 작동 제어** | 서버 명령 또는 조건에 따라 컨베이어 벨트가 자동으로 작동/정지됩니다. |
| **화물 적하 기능** | AGV 도착 시 적재소가 감지하여 자동 투하 명령을 수행하며, GUI에서 수동 전환도 가능합니다. |
| **저장소 상태 감지** | 센서를 통해 저장소의 포화 여부를 감지하고, 서버에 상태를 보고합니다. |
| **저장소 자동 선택** | 컨테이너 A/B 중 가용 공간이 있는 저장소를 자동으로 선택하여 적하를 수행합니다. |
| **벨트 안전 제어 로직** | 컨테이너가 포화 상태일 경우, 벨트는 자동으로 작동을 거부하며 안전 상태를 유지합니다. |

---

### 🖥 중앙 제어 서버 기능

| 기능 | 설명 |
|------|------|
| **FSM 기반 제어 흐름** | AGV와 시설의 상태를 FSM으로 관리하며, 상태에 따라 명령을 자동 전송합니다. |
| **TCP / Serial 통신 처리** | AGV와는 TCP로, 시설과는 Serial로 통신하며 양방향 명령/상태 처리를 수행합니다. |
| **미션 관리 시스템** | 미션 생성, 할당, 상태 변경, 완료 여부 등을 종합 관리합니다. |
| **상태 수집 및 기록** | 모든 AGV/설비의 실시간 상태를 주기적으로 수집하여 DB에 기록합니다. |
| **비상 정지 및 우선 제어** | 서버에서 수동 명령으로 AGV/설비에 즉시 제어 명령을 내릴 수 있습니다. |
| **디스펜서 위치 보정** | DISPENSER_LOADED 이벤트 시, AGV 위치 누락을 디스펜서 상태로 자동 보정합니다. |
| **시리얼 응답 파싱 구조화** | 예: ACK:GATE_A_OPENED 형식의 문자열 응답을 구조화된 JSON으로 변환하여 FSM 로직과 연계합니다. |
| **커스텀 프로토콜 구조화** | JSON 기반 메시지 외에도 `Header + Payload` 형식의 Byte 메시지를 지원. 명령어 ID, 송수신자 ID, 페이로드 길이, 내용 등으로 구조화하여 통신 효율 향상 |
| **미션 없음 시 자동 상태 전환** | 미션 큐가 비었을 경우, AGV이 STANDBY에 있다면 자동으로 충전 상태 진입 또는 IDLE 유지 결정 |

#### 🔧 고급 제어 기능 요약

| 고급 기능 | 설명 |
|-----------|------|
| **TEMP 소켓 자동 등록** | AGV이 등록되지 않은 상태로 TCP 연결 시, `TEMP_포트번호`로 임시 등록한 뒤 실제 AGV ID로 자동 전환합니다. |
| **FSM 상태 불일치 자동 보정** | 서버 재시작 등으로 상태가 어긋나도, FSM이 현재 위치와 이벤트에 따라 적절한 상태로 자동 전이됩니다. |
| **적재 위치 유효성 검증 및 재지시** | 잘못된 위치에 도착 시, 미션 정보와 대조하여 다시 올바른 적재 위치로 RUN 명령을 보냅니다. |
| **미션 없음 시 자동 충전 전환** | 미션이 없고 STANDBY에 있을 경우, 배터리가 100%가 아니면 자동으로 충전 상태로 전환됩니다. |

---

### 🧑‍💼 사용자 인터페이스

#### Login Window
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/gui/login.png?raw=true" width="30%">
</p>

#### Main Monitoring 탭
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/gui/main_monitoring_1.gif?raw=true" width="90%">
</p>
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/gui/main_monitoring_2.gif?raw=true" width="90%">
</p>

#### Mission Management 탭
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/gui/mission%20management.gif?raw=true" width="90%">
</p>

#### Event Log 탭
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/gui/event%20log.gif?raw=true" width="90%">
</p>

#### Settings 탭
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/gui/settings.gif?raw=true" width="90%">
</p>


| 기능            | 설명                                                                                                                                         |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| **메인 모니터링 탭** | 전체 맵을 통해 AGV의 위치와 진행 상황을 실시간으로 시각화합니다. 사용자는 FSM 상태, 현재 위치, 미션 흐름을 직관적으로 확인하고, 필요한 경우 직접 제어할 수 있습니다.                      |
| **미션 관리 탭**   | AGV가 수행할 미션을 수동으로 등록하거나 삭제할 수 있으며, 현재 진행 중인 미션의 상세 정보도 확인 가능합니다. 이 기능은 AGV FSM 흐름에 직접 영향을 미칩니다. 사용자는 GUI를 통해 미션 생성 → 배정 → 완료까지의 흐름을 제어할 수 있습니다. |
| **이벤트 로그 탭**  | AGV와 설비의 상태 변화, 명령 수행, 센서 감지, 오류 발생 등의 주요 이벤트를 실시간으로 확인할 수 있어, AGV 운영 상태를 정밀하게 추적할 수 있습니다.                                                  |
| **Setting 탭** | AGV ID, 설비 포트, 통신 설정 등을 구성하여 AGV 및 제어 서버 간 통신 환경을 설정합니다. 해당 설정은 실제 운행에 적용되는 구성으로, 시스템 시작 시 필수로 지정해야 하는 항목들입니다.                              |
| **로그인 기능**    | 사용자 로그인 후 권한에 따라 기능 접근이 달라지며, 관리자/오퍼레이터 권한에 따라 미션 제어, 설정 변경, 긴급 정지 등 주요 기능 사용 여부가 결정됩니다. 이는 실제 AGV 제어의 안전성과 보안성을 보장하기 위한 구조입니다.            |



---

## 🧪 10. 기술적 문제 및 해결

본 프로젝트에서는 실제 구현 과정에서 다양한 기술적 문제가 발생했으며, 이를 직접 해결해나가는 과정을 통해 시스템의 안정성과 응답 속도를 향상시켰습니다.

### 🧠 1. 통신 지연 및 처리 속도 문제

- **문제**:  
  AGV ↔ 서버 간 TCP 통신을 JSON 기반으로 설계했으나, 문자열 파싱 시간이 길어지고 `loop()` 처리 속도가 느려져 정밀한 주행 타이밍을 방해하는 문제가 발생했습니다.

- **해결**:  
  주요 명령에 대해서는 커스텀 바이트 메시지 프로토콜로 전환하여 메시지 크기를 줄이고 파싱 시간을 단축함으로써 주행 제어 명령에 대한 응답 속도를 크게 향상시켰습니다.
  
> ✅ 실제 통신 구조는 JSON + Byte 혼합 구조로 설계되어 유연성과 실시간성을 동시에 확보하였습니다.


### 🚗 2. RFID 리딩 중 PWM 불안정 문제

- **문제**:  
  RFID 태그 인식 시 센서 리딩 연산이 길어져 PID 루프 내 PWM 출력이 급격히 튀는 문제가 발생했습니다. 이는 주행 안정성을 해치고, 직선 주행 시 궤도가 흔들리는 현상을 유발했습니다.

- **해결**:  
  RFID 인식 직전에 약 0.5초간 PID 제어를 일시 정지하고, 기존 PWM 출력을 유지하는 방식으로 주행 안정성을 확보했습니다.
  
> ✅ RFID 기반 위치 인식과 주행 제어를 충돌 없이 병행하기 위한 타이밍 제어 기법을 적용하였습니다.


---

 ## 🧱 11. 구현 제약 및 확장 가능성

| 현재 상태 | 구현 한계 | 개선 가능성 |
|------------|------------|-------------|
| AGV 1대 기반 FSM + GUI 구조 | 현재 GUI와 미션 큐가 하나의 FSM 흐름에만 연결되어 있어, 다중 AGV 운용에 제약이 있습니다. | `contexts[truck_id]`, `TruckFSMManager` 구조를 활용해 다중 FSM 병렬 운용 가능. GUI 시각화 및 큐 구조 확장 시, 다중 AGV 운용 시뮬레이션 가능 |
| 배터리 상태 가상값 기반 운영 | 실제 전류/전압 센서 미연동, 잔량은 시뮬레이션 값으로 처리됨 | `INA226` 등 센서 연동 시 실시간 잔량 측정 가능. 향후 에너지 기반 경로 최적화 및 스마트 충전 로직으로 확장 가능 |
| 설비 제어는 기본적인 양방향 구조 | ACK 수신 여부만 단순 확인하며, 미수신 시 재시도 없음 | 설비 명령에 대해 타임아웃 기반 재전송 및 오류 기록 기능 추가 시 신뢰성 강화 가능 |
| 설정 저장 기능 미구현 | 통신 설정, 장치 등록 등이 세션 내 임시 저장. 재시작 시 초기화됨 | JSON 또는 MySQL 기반 설정 저장 구조 적용 시 운영 환경 유지 및 빠른 재가동 가능 |

---

## 📁 12. 디렉토리 구조

본 프로젝트는 **서버, 펌웨어, GUI, 시각 자료, 테스트, 문서**까지 전체 시스템을 구성하는 모든 요소를 기능 단위로 디렉토리화하여 구성하였습니다.

```
iot_dust/
├── backend/                 # 💡 서버 로직 및 기능별 Python 모듈
│   ├── auth/               # 사용자 인증 기능 (로그인/권한)
│   ├── mission/            # 미션 등록 및 상태 관리
│   ├── truck_fsm/          # 서버 FSM 흐름 중 AGV 관련 상태 전이 로직
│   ├── tcpio/              # AGV와의 TCP 통신 수신/응답 처리
│   ├── serialio/           # 설비(Gate, Belt 등) 제어용 시리얼 통신 모듈
│   ├── rest_api/           # Flask 기반 GUI API 서버
│   ├── main_controller/    # 🚀 전체 FSM 흐름 및 제어 통합 (진입점)
│   ├── truck_status/       # AGV 상태 기록 (배터리, 위치 등)
│   └── facility_status/    # 설비 상태 기록 모듈
│
├── gui/                    # 🖥 PyQt6 기반 관제 인터페이스
│   ├── tabs/               # 각 탭별 UI 및 동작 구현
│   ├── ui/                 # Qt Designer로 제작한 .ui 파일들
│   └── main_windows/       # GUI 진입점 (관리자/오퍼레이터 전용 메인 창)
│
├── firmware/               # 🔌 MCU 기반 펌웨어 코드 (Arduino/ESP32)
│   ├── truck/              # AGV 센서/주행/RFID 관련 펌웨어
│   ├── gate/               # 게이트 개폐 펌웨어
│   ├── belt/               # 컨베이어 벨트 제어 펌웨어
│   └── dispenser/          # 적재소(디스펜서) 제어 펌웨어
│
├── run/                    # ▶️ 실행 스크립트 디렉토리
│   ├── run_main_server.py  # 서버 실행 진입점
│   └── run_gui.py          # GUI 실행 진입점
│
├── tests/                  # 🧪 주요 기능 단위 테스트 코드 모음
├── assets/                 # 📷 시연 GIF, 시스템 구조도, ERD, GUI 캡처 등
├── documents/              # 📄 발표자료, 설계 문서, 통신 명세서 등 문서
└── README.md               # 📘 프로젝트 소개 문서

```

---
