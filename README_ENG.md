![Banner](https://github.com/addinedu-ros-9th/iot-repo-4/blob/main/assets/images/banner_original.png?raw=true)

> **This project implements an IoT-based integrated transportation control system where a small AGV follows RFID tags and communicates with facilities in real-time to execute missions.**  
> **The AGV (truck) is controlled via ESP32 and integrated with gates, belts, and loading stations via an FSM-based central server. A GUI system allows users to visually monitor and control the transportation flow.**

## 🎥 Videos

- [System Overview](https://youtu.be/AI76I9BiS1k?si=EfL9UZIdROXblnkd)  
- [Full Operation Demo](https://youtu.be/LJ2RT1eQdgk)

## 🛻 Presentation

- [Slides](https://docs.google.com/presentation/d/1FL6l2cNho4lIEEreOYMQ6edMlTMGJ92bY9mtO8bmuwk/edit?usp=sharing)

---

## 📚 Table of Contents

| No. | Section |
|-----|---------|
| 1 | Team |
| 2 | Project Overview |
| 3 | Tech Stack |
| 4 | Purpose |
| 5 | Requirements |
| 6 | System Architecture |
| 7 | Database |
| 8 | Communication |
| 9 | Functionality |
| 10 | Technical Challenges |
| 11 | Limitations & Scalability |
| 12 | Directory Structure |

---

# 🚚 IoT-Based Integrated Control System for Small AGVs

## 👥 1. Team

| Name | GitHub | Role |
|------|--------|------|
| **Kim Daein** | [Daeinism](https://github.com/Daeinism) | _(TBD)_ |
| **Lee Gunwoo** | — | _(TBD)_ |
| **Lee Seunghoon** | [leesh0806](https://github.com/leesh0806) | AGV Module & Mechanical Design, AGV Circuit Design, Line Tracing Algorithm, FSM-based Driving Logic, TCP Protocol |
| **Jang Jinhyuk** | [jinhyuk2me](https://github.com/jinhyuk2me) | FSM Logic Implementation, AGV TCP Protocol Design, Facility Serial Control Module, GUI Development (PyQt6), Database Logging System |

---

## 📦 2. Project Overview

`D.U.S.T. (Dynamic Unified Smart Transport)` is an IoT-based control system centered on a small AGV that follows an RFID-tagged route and integrates with logistics facilities like gates, conveyors, and loaders in real-time.

The system unifies FSM-based server control, TCP/Serial communication, and PyQt GUI to offer consistent visualized control of the transportation flow.

### 🧭 Key Features

- AGV autonomously drives along RFID-tagged paths.
- Facilities (gate/belt/loader) respond automatically to server commands.
- FSM-based server makes real-time decisions and controls devices.
- PyQt GUI provides real-time visualization and manual override.

### 🎯 Scope of Implementation

- FSM-based control flow via server
- ESP32-based AGV firmware with sensors
- TCP-based AGV control and status reporting
- Serial-based facility control modules
- PyQt GUI design with tab-based interfaces
- MySQL-based mission/state/log management system

---

## 🤖 3. What is an AGV?

### 🚚 AGV (Automated Guided Vehicle)

AGV refers to an unmanned transport vehicle that automatically follows a preset path without human intervention. It is widely used in logistics, factories, and warehouses.

**Key Characteristics:**
- Path-based autonomous driving via lines, QR, RFID, LiDAR
- Obstacle detection and safety via ultrasonic, IR sensors
- Server/PLC integration for real-time reporting and commands
- Efficient automation for repetitive tasks

### 🛠️ Our AGV System

| Component | Description |
|----------|-------------|
| **MCU** | ESP32-WROOM (Wi-Fi and GPIO control) |
| **Position Detection** | RFID tags at each location |
| **Driving Algorithm** | IR sensor + PID line tracing |
| **Obstacle Detection** | Ultrasonic sensor |
| **Comm Protocol** | TCP over Wi-Fi |
| **State Reporting** | Periodic status to server (battery, FSM state, location) |
| **Auto Charging** | Transitions to charging mode based on battery level |
| **FSM Integration** | Actions based on FSM states like RUN, ARRIVED, etc. |

---

## 🛠️ 4. Project Purpose

The project aims to integrate **all transportation automation components**—AGV, facilities, GUI, and database—into a unified control flow based on **FSM (Finite State Machine)**.

### 🔍 Background

- In industrial sites, it's not enough for AGVs to self-drive. Facility collaboration and integrated control are essential.
- Sensor processing → decision logic → command → UI feedback must be seamless.
- Our project tackles this by building a fully integrated FSM-driven system.

### ✅ Significance

- FSM handles every phase from AGV navigation to loading
- Central server unifies AGV and facility control
- Real-time visualization and manual control via GUI
- Consistent pipeline: sensor input → control logic → UI/DB logging

---

## 🧾 5. Requirements (UR / SR)

System functionality is defined by two categories:

- **User Requirements (UR)**: From the user's perspective.
- **System Requirements (SR)**: Technical implementations that fulfill the URs.

Each item is also labeled with a **Priority**:  
R = Required, O = Optional

### ✅ User Requirements (UR)

| ID | Description | Priority |
|----|-------------|----------|
| UR_01 | The AGV must be able to move to specific locations. | R |
| UR_02 | The AGV must operate autonomously. | O |
| UR_03 | Only authorized users should access the system. | R |
| UR_04 | The user must monitor the AGV’s state in real-time. | R |
| UR_05 | The AGV’s state history must be stored and viewable. | R |
| UR_06 | The status of each facility should be monitorable. | R |
| UR_07 | Only authorized AGVs should access restricted areas. | R |
| UR_08 | There must be an automated loading system. | R |
| UR_09 | The loading system should support manual control. | O |
| UR_10 | The AGV must automatically unload cargo. | R |
| UR_11 | The storage system must be automated. | R |
| UR_12 | Storage selection must consider availability. | O |
| UR_13 | The system must support emergency stop of the storage unit. | R |

> Most required items are implemented in the system. Optional features are partially integrated or included in the design.

---

### ✅ System Requirements (SR)

| ID | Feature | Description |
|-----|---------|-------------|
| SR_01 | AGV Monitoring | Real-time display of AGV location and mission |
| SR_02 | Facility Monitoring | Visualization of gate, belt, loader status |
| SR_03 | User Authorization | Login, permission levels, user management |
| SR_04 | Mission Management | Register/track mission history |
| SR_05 | Central Control | FSM-based unified control of AGVs and facilities |
| SR_06 | AGV Autopilot | Unmanned driving along predefined path |
| SR_07 | Auto Unloading | Automatically unload cargo |
| SR_08 | Position Recognition | RFID-based AGV location detection |
| SR_09 | State Reporting | AGV state updates sent to the server |
| SR_10 | Access Control | Gate restrictions based on AGV ID |
| SR_11 | Auto Gate Control | Automatic gate open/close logic |
| SR_12 | AGV Detection at Loader | Detect AGV arrival at loader |
| SR_13 | Auto Loading at Loader | Perform unloading on server command |
| SR_14 | Manual Loading Control | Allow manual unloading via GUI |
| SR_15 | Belt Transfer Control | Start/stop belt via server |
| SR_16 | Storage Load Detection | Monitor container load state |
| SR_17 | Auto Storage Selection | Choose available container automatically |
| SR_18 | Emergency Stop | Stop AGV on command or full storage |
| SR_19 | Charging Station Support | Automatically switch to charging when needed |

---

### 🔗 UR ↔ SR Mapping

| User Requirement | Linked System Functions |
|------------------|-------------------------|
| UR_01 | SR_06, SR_08 |
| UR_02 | SR_06 |
| UR_03 | SR_03 |
| UR_04 | SR_01, SR_09 |
| UR_05 | SR_04, SR_09 |
| UR_06 | SR_02, SR_15, SR_16 |
| UR_07 | SR_10, SR_11 |
| UR_08 | SR_13 |
| UR_09 | SR_14 |
| UR_10 | SR_07, SR_13 |
| UR_11 | SR_15, SR_16 |
| UR_12 | SR_17 |
| UR_13 | SR_18 |

---

## 🧩 6. System Architecture

### 🧱 Hardware/Software Overview

- **AGV**: Controlled by ESP32, equipped with sensors and motors
- **Facilities**: Arduino-based (gate, belt, dispenser)
- **Server**: FSM-based controller using TCP/Serial communication
- **GUI**: PyQt6-based, REST API for interaction
- **DB**: MySQL used to record status, logs, missions

### 🧠 Server Software Layer

| Module | Role |
|--------|------|
| `MainController` | Oversees FSM and dispatches commands |
| `TruckFSM` | Manages AGV FSM states |
| `FacilityManager` | Controls facility devices |
| `StatusManager` | Collects and saves AGV/facility states |
| `MissionManager` | Handles mission lifecycle |

### ⚙️ Communication Methods

| Type | Direction | Usage |
|------|-----------|-------|
| TCP | AGV ↔ Server | Command/control, status reporting |
| Serial | Server ↔ Facilities | Device control & responses |
| HTTP API | GUI ↔ Server | API calls for control and status |

---

## 🗄️ 7. Database Design

All system states are logged and managed through a modular MySQL schema.

### 📊 Table Structure

**AGV**

| Table | Description |
|-------|-------------|
| `TRUCK` | AGV metadata |
| `BATTERY_STATUS` | Battery/fsm event history |
| `POSITION_STATUS` | AGV location logs |

**Missions**

| Table | Description |
|-------|-------------|
| `MISSIONS` | Mission data with timestamps and progress |

**Facilities**

| Table | Description |
|-------|-------------|
| `FACILITY` | Facility metadata |
| `GATE_STATUS`, `BELT_STATUS`, `CONTAINER_STATUS` | Real-time device state logs |

**Users**

| Table | Description |
|-------|-------------|
| `USERS` | Login credentials and roles |
| `LOGIN_LOGS` | Login attempt logs |

> All modules are integrated through centralized DB logging and are designed for extensibility.

---

## 📡 8. Communication Structure

This system uses a hybrid of **TCP**, **Serial**, and **HTTP API** communication methods to enable real-time interaction among the AGV, server, facilities, and GUI. All message exchanges are aligned with the central FSM server logic.

---

### 🛰 1. AGV ↔ Server (TCP)

#### ✅ Message Format

Supports both:

- **JSON-based messages** (easy debugging and interpretation)
- **Byte-based custom protocol** (lightweight and fast)

#### 🔸 JSON Message Example

<pre><code>{
  "sender": "TRUCK_01",
  "receiver": "SERVER",
  "cmd": "ARRIVED",
  "payload": {
    "position": "CHECKPOINT_A"
  }
}
</code></pre>

#### 🔸 Byte Message Format

| Field        | Size (bytes) | Description                          |
|-------------|----------------|--------------------------------------|
| sender_id   | 1              | Sender ID (e.g., 0x01 = TRUCK)       |
| receiver_id | 1              | Receiver ID (e.g., 0x10 = SERVER)    |
| cmd_id      | 1              | Command code                         |
| payload_len | 1              | Length of the payload                |
| payload     | Variable       | Command-specific data                |

#### 🔹 Common Commands

**From AGV to Server:**
- `ARRIVED`: Notifies location arrival
- `OBSTACLE`: Reports obstacle detection
- `STATUS_UPDATE`: Sends battery, position, FSM state

**From Server to AGV:**
- `MISSION_ASSIGNED`: Assigns mission to AGV
- `RUN` / `STOP`: Controls driving state
- `GATE_OPENED`: Notifies that gate is opened

> All FSM state transitions are triggered based on these messages.

---

### ⚙️ 2. Server ↔ Facility (Serial)

#### ✅ Facility Devices

- Gate Controller
- Belt Controller
- Dispenser Controller

#### 🔸 Communication Flow

- **Send**: Server → Facility (commands)
- **Receive**: Facility → Server (status feedback)

#### 🔸 Sample Commands

| Command           | Description              |
|------------------|--------------------------|
| `GATE_A_OPEN`     | Opens Gate A             |
| `BELT_RUN`        | Starts conveyor belt     |
| `DISPENSER_OPEN`  | Drops cargo via dispenser|

---

### 🌐 3. GUI ↔ Server (HTTP REST API)

#### ✅ API Information

- **Base URL**: `/api`
- **Protocol**: HTTP
- **Content-Type**: `application/json`

#### 🔸 Major API Endpoints

| Method | Endpoint                                  | Description                      |
|--------|-------------------------------------------|----------------------------------|
| GET    | `/api/trucks`                             | Retrieves all AGV states         |
| GET    | `/api/trucks/{truck_id}`                  | Retrieves a specific AGV state   |
| POST   | `/api/missions`                           | Registers a new mission          |
| POST   | `/api/facilities/gates/{id}/control`      | Opens/closes a specific gate     |
| POST   | `/api/facilities/belt/control`            | Starts/stops the conveyor belt   |

#### 🔸 Example Requests

**Mission Registration**
<pre><code>{
  "mission_id": "MISSION_001",
  "cargo_type": "SAND",
  "cargo_amount": 100.0,
  "source": "LOAD_A",
  "destination": "BELT"
}
</code></pre>

**AGV State Response**
<pre><code>{
  "TRUCK_01": {
    "battery": {"level": 87.0, "is_charging": false},
    "position": {"location": "CHECKPOINT_A", "status": "IDLE"},
    "fsm_state": "IDLE"
  }
}
</code></pre>

---

### ✅ Summary of Communication Methods

| Component        | Method         | Description                                    |
|------------------|----------------|------------------------------------------------|
| AGV ↔ Server     | TCP (JSON/Byte)| Real-time command and state synchronization   |
| Facility ↔ Server| Serial         | Device control and status feedback            |
| GUI ↔ Server     | HTTP API       | Manual mission registration and monitoring    |

> All channels are synchronized through the central FSM logic, ensuring consistent operation across components.

---

## ⚙️ 9. Feature Overview

### 🚚 AGV-Related Functions

| Feature | Description |
|--------|-------------|
| **Autonomous Driving** | The AGV follows a pre-tagged path by detecting RFID tags and driving via PID-controlled IR line tracing. |
| **Position Recognition** | Detects checkpoints via RFID and sends location updates to the server. |
| **Battery Monitoring** | Reports current battery level and FSM state periodically to the server. |
| **Mission Execution** | Automatically starts mission on assignment and transitions between FSM states. |
| **Obstacle Avoidance** | Detects obstacles via ultrasonic sensors and stops accordingly. |
| **Socket Auto Registration** | Unregistered AGVs are temporarily assigned a `TEMP_` socket and remapped to real IDs. |
| **FSM Recovery Handling** | FSM state mismatches are automatically corrected to ensure stable flows. |

---

### 🏗 Facility Control Functions

| Feature | Description |
|--------|-------------|
| **Gate Control** | Opens only for registered AGVs and blocks unregistered access. |
| **Belt Operation** | Automatically starts/stops depending on commands or safety checks. |
| **Cargo Drop Function** | Loads/unloads automatically when AGV arrives; can be manually triggered. |
| **Storage Status Detection** | Detects container saturation via sensors and reports to server. |
| **Auto Storage Selection** | Chooses available container based on current load. |
| **Belt Safety Logic** | Prevents belt operation if containers are full. |

---

### 🖥 Central Control Server

| Feature | Description |
|--------|-------------|
| **FSM-Based Control Flow** | Manages AGV and facility state transitions using FSM. |
| **TCP / Serial Communication** | Handles message exchange with AGVs (TCP) and facilities (Serial). |
| **Mission Management** | Registers, assigns, and tracks cargo missions. |
| **State Collection and Logging** | Periodically logs all AGV/facility status to MySQL DB. |
| **Emergency Stop & Manual Override** | Supports instant server-side intervention. |
| **Dispenser Location Auto-Correction** | Fixes AGV position using dispenser status if location is unclear. |
| **Structured Serial Parser** | Converts messages like `ACK:GATE_A_OPENED` into JSON format. |
| **Custom Byte Protocol** | Lightweight, header+payload formatted binary messages. |
| **Idle/Charge Mode Logic** | AGVs automatically switch state if no mission is queued. |

---

## 🧠 10. Technical Issues & Solutions

This system encountered and overcame two major challenges:

---

### 🚧 Issue 1: Communication Delay (JSON overhead)

- **Problem**:  
  Using JSON in the ESP32 loop caused long parse times, which disrupted PID control loop cycles and affected line-tracking performance.

- **Solution**:  
  Replaced JSON with a custom lightweight Byte protocol for key control messages.

- **Result**:
  - Faster loop cycles
  - Lower parsing overhead
  - Improved tracking accuracy

#### Comparison:

| Format | Example | Size |
|--------|---------|------|
| JSON | <pre><code>{"cmd": "RUN", "payload": {...}}</code></pre> | ~60–100 bytes |
| Byte | <pre><code>[0x01][0x01][0xA1]...</code></pre> | ~3–5 bytes |

---

### ⚠️ Issue 2: RFID Caused PWM Instability

- **Problem**:  
  RFID reading caused delays during PID control, resulting in unstable PWM output and deviation in straight-line movement.

- **Solution**:  
  Temporarily paused PID updates (~0.5s) during RFID read; held previous PWM value constant.

- **Result**:
  - Stable PID control during RFID access
  - Improved straight-line accuracy

---

> ✅ Both issues were solved structurally (not just code-level) to ensure high-frequency real-time control in an embedded system context.

---

## 🧱 11. Implementation Constraints & Scalability

| Current State | Limitation | Potential Improvement |
|---------------|------------|------------------------|
| Single-AGV FSM & GUI | Current GUI and mission queue are bound to a single FSM context. | Support multiple AGVs using `contexts[truck_id]` and `TruckFSMManager`. Extend GUI and queue logic for concurrent simulation. |
| Simulated Battery Level | No real voltage/current sensor; uses estimated values. | Integrate INA226 for real-time battery measurement. Enables energy-aware route planning and smart charging. |
| Basic Facility ACK | Only checks for ACK response; no retry mechanism. | Add timeout/retry logic and error logging for robust control. |
| No Persistent Settings | Comm configs and device registration reset on restart. | Store config in JSON/MySQL for persistent setup across reboots. |

> The system is designed with modularity and future expansion in mind. Most constraints can be lifted with additional implementation.

---

## 📁 12. Directory Structure

The project is organized by functional modules such as server, firmware, GUI, assets, and documentation.

<pre><code>
iot_dust/
├── backend/                 # 💡 Python modules for backend logic
│   ├── auth/               # User authentication
│   ├── mission/            # Mission registration and tracking
│   ├── truck_fsm/          # AGV FSM logic
│   ├── tcpio/              # TCP handling for AGVs
│   ├── serialio/           # Serial control for facilities
│   ├── rest_api/           # Flask-based HTTP API for GUI
│   ├── main_controller/    # 🚀 Central FSM entry point
│   ├── truck_status/       # Battery, position logs
│   └── facility_status/    # Facility state logging
│
├── gui/                    # 🖥 PyQt6 GUI
│   ├── tabs/               # Tab-specific behavior
│   ├── ui/                 # .ui files from Qt Designer
│   └── main_windows/       # Main windows for Admin/Operator
│
├── firmware/               # 🔌 Firmware code for ESP32/Arduino
│   ├── truck/              # AGV driving + sensors
│   ├── gate/               # Gate firmware
│   ├── belt/               # Conveyor belt firmware
│   └── dispenser/          # Dispenser controller
│
├── run/                    # ▶️ Launch scripts
│   ├── run_main_server.py  # Start backend server
│   └── run_gui.py          # Start GUI system
│
├── tests/                  # 🧪 Unit test scripts
├── assets/                 # 📷 Images, GIFs, diagrams, ERD
├── documents/              # 📄 Design docs, slides, protocol specs
└── README.md               # 📘 Project overview
</code></pre>

---





