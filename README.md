![배너](https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/banner.png?raw=true)

<p align="center">
  <a href="https://docs.google.com/presentation/d/1-bRbadY4XmSBsaMfYFJiN6WQ00letQ_9P2LTwLdzEXg/edit?usp=sharing">
    <img src="https://img.shields.io/badge/PRESENTATION-GoogleSlides-yellow?style=for-the-badge&logo=google-slides&logoColor=white" alt="발표자료">
  </a>
  <a href="https://youtu.be/hftyShwyZxk">
    <img src="https://img.shields.io/badge/DEMO-YouTube-red?style=for-the-badge&logo=youtube&logoColor=white" alt="시스템 구동 영상">
  </a>
</p>

# 📚 목차

- [1. 프로젝트 개요](#1-프로젝트-개요)
- [2. 프로젝트 목적](#2-프로젝트-목적)
- [3. 시스템 설계](#3-시스템-설계)
- [4. 주요 기능](#4-주요-기능)
- [5. 기술적 문제 및 해결](#5-기술적-문제-및-해결)
- [6. 구현 제약 및 확장 가능성](#6-구현-제약-및-확장-가능성)
- [7. 기술 스택](#7-기술-스택)
- [8. 팀 구성](#8-팀-구성)

---

# 1. 프로젝트 개요
> ⏰ 프로젝트 기간: 2025.05.03 ~ 2025.05.15

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/gui/main_monitoring_1.gif?raw=true" width="45%" style="margin-right:10px;">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/facilities/load_1.gif?raw=true" width="45%">
</p>

`D.U.S.T. (Dynamic Unified Smart Transport)`는 `RFID 기반 위치 인식`을 바탕으로 경로를 따라 주행하는 `AGV`와 게이트, 컨베이어 벨트, 적재소 등 `물류 설비`를 실시간으로 `통합 제어`하는 IoT 기반 운송 관제 시스템입니다.

---

# 2. 프로젝트 목적

산업 현장에서는 `AGV(Automated Guided Vehicle)`가 **정해진 경로를 따라 자율 주행하며**, 다양한 설비(게이트, 벨트, 저장소)와 **연동되는 시스템**이 점점 요구되고 있습니다.

따라서 본 프로젝트는 `AGV`를 기반으로, **물류 자동화 시나리오의 흐름을 단일 제어 구조로 통합**하는 데 목적이 있습니다.

---

# 3. 시스템 설계

## 시스템 아키텍처

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/system_architecture/sys_archi.png?raw=true" width="80%">
</p>

## ER 다이어그램

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/erd/erd.png?raw=true" width="50%">
</p>

---

# 4. 주요 기능
 
## 🚚 AGV 관련 기능

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/truck/truck_1.gif?raw=true" width="45%" style="margin-right:10px;">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/truck/truck_2.gif?raw=true" width="45%">
</p>

- `자동 주행` : `ESP32` 제어를 통한 `RFID` 경로 기반 주행 
- `위치 인식 및 보고` : RFID 태그 → 위치 판단 및 서버 송신
- `배터리 모니터링` : 잔량 및 FSM 상태 → 주기적 서버 보고
- `미션 수행` : 서버 미션 수신 → FSM 전이 + 자동 하역
- `충돌 방지` : 초음파 센서 기반 정지 처리

---

## 🏗 시설 제어 기능

<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/facilities/gate_1.gif?raw=true" width="30%" style="margin-right:10px;">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/facilities/load_1.gif?raw=true" width="30%" style="margin-right:10px;">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/facilities/belt_1.gif?raw=true" width="30%">
</p>

- `게이트 제어` : 등록 AGV → 자동 개방 / 미등록 AGV → 차단
- `벨트 작동 제어` : 서버 명령 또는 조건 → 자동 작동/정지
- `화물 적하 기능` : AGV 도착 시 자동 투하 / GUI 수동 전환 가능
- `저장소 상태 감지` : 센서로 포화 여부 감지 → 서버 보고
- `저장소 자동 선택` : 컨테이너 A/B 중 여유 공간 선택
- `벨트 안전 제어 로직` : 포화 상태일 경우 벨트 작동 거부 → 안전 유지

---

## 🖥 중앙 제어 서버 기능

- `FSM 제어` : AGV/설비 상태 기반 명령 자동 전송
- `상태 기록` : AGV/설비 상태 주기 수집 및 저장
- `비상 제어` : 수동 명령으로 긴급 정지 및 제어
- `자동 소켓 등록` : 미등록 AGV → TEMP → 실 ID 매핑
- `자동 충전 전환` : 미션 없음 + 배터리 부족 시 충전 상태로 전환
  
---

## 🧑‍💼 사용자 인터페이스

### Main Monitoring 탭
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/gui/main_monitoring_1.gif?raw=true" width="45%">
</p>
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/gui/main_monitoring_2.gif?raw=true" width="45%">
</p>

### Mission Management 탭
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/gui/mission%20management.gif?raw=true" width="45%">
</p>

### Event Log 탭
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/gui/event%20log.gif?raw=true" width="45%">
</p>

### Settings 탭
<p align="center">
  <img src="https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/gui/settings.gif?raw=true" width="45%">
</p>

- `메인 모니터링 탭` : AGV 위치 및 FSM 상태 실시간 시각화 + 수동 제어 가능
- `미션 관리 탭` : 미션 수동 등록/삭제 + 전체 흐름 관리 (생성 → 배정 → 완료)
- `이벤트 로그 탭` : 상태 변화, 명령 수행, 센서 감지 등 이벤트 실시간 추적
- `Setting 탭` : AGV ID, 포트, 통신 등 시스템 운용 설정
- `로그인 기능` : 권한 기반 기능 접근 제어 (관리자 / 오퍼레이터)

---

# 5. 기술적 문제 및 해결

본 프로젝트에서는 실제 구현 과정에서 다양한 기술적 문제가 발생했으며, 
이를 직접 해결해나가는 과정을 통해 시스템의 안정성과 응답 속도를 향상시켰습니다.
- `통신 지연` : JSON 파싱 지연 → 주요 명령은 바이트 프로토콜로 전환하여 응답 속도 향상
- `PWM 불안정` : RFID 리딩 시 제어 루프 충돌 → 리딩 중 PID 일시 정지로 주행 안정성 확보

---

# 6. 구현 제약 및 확장 가능성

- `단일 AGV FSM 구조` : 현재 FSM/GUI는 1대 AGV만 지원 → 다중 FSM 확장 가능
- `배터리 가상값 사용` : 잔량은 시뮬레이션 값 기반 → `INA226` 센서 연동 시 실시간 측정 및 최적화 가능
- `설비 단순 응답 처리` : ACK 여부만 확인, 재시도 없음 → 타임아웃 기반 재전송 + 오류 로그로 신뢰성 개선
- `설정 저장 미지원` : 설정값 세션 내 유지 → JSON/MySQL 기반 설정 저장 시 재시작 후 복원 가능

---

# 7. 기술 스택

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

# 8. 팀 구성

### 🧑‍💼 김대인 [`@Daeinism`](https://github.com/Daeinism)
- 프로젝트 총괄  
- 자원 분배기 기구 및 펌웨어 제작  
- 차단기 기구 및 펌웨어 제작

### 🧑‍💼 이건우 [`@DigitalNomad230`](https://github.com/DigitalNomad230)
- 프로젝트 기술문서 검토 및 관리
- 자원저장센터 기구 및 펌웨어 제작
- 컨테이너 적재량 연동 센터가동 로직 구현

### 🧑‍💼 이승훈 [`@leesh0806`](https://github.com/leesh0806)
- AGV 모듈 개발 및 기구설계  
- AGV 회로 설계  
- 라인주행 제어 알고리즘 구현  
- AGV FSM 상태기반 주행제어 구현  
- AGV TCP 통신 명령 송수신 프로토콜 제작

### 🧑‍💼 장진혁 [`@jinhyuk2me`](https://github.com/jinhyuk2me)
- 메인 서버 설계 및 구현
- GUI 설계 및 구현
- 시스템 아키텍처 설계 
- 통신 인터페이스 설계 
- 데이터베이스 구축 및 관리
