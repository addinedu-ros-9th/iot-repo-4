import threading
import time
from .serial_controller import SerialController

class DispenserController(SerialController):
    """
    화물 분배기(Dispenser)의 상태를 관리하고 제어합니다.
    문 개폐, 경로 이동과 같은 물리적 동작과 화물 적재 프로세스를 관리합니다.
    """
    def __init__(self, serial_interface, facility_status_manager=None):
        super().__init__(serial_interface)
        self.state = "UNKNOWN"      # 현재 상태 (OPENED, CLOSED, LOADING, LOADED)
        self.position = "UNKNOWN"   # 현재 위치 (ROUTE_A, ROUTE_B)
        self.operation = "IDLE"     # 현재 동작 (OPENING, CLOSING, MOVING 등)
        self.lock = threading.Lock()
        self.facility_status_manager = facility_status_manager
        self.current_truck_id = None # 현재 상호작용 중인 트럭 ID

    def open_dispenser(self, truck_id: str) -> bool:
        """디스펜서를 열고 적재 프로세스를 시작합니다."""
        with self.lock:
            if self.state == "OPENED":
                print("[Dispenser] 이미 열려있습니다.")
                return True

            print(f"[Dispenser] {truck_id}를 위해 열기 요청...")
            self.current_truck_id = truck_id
            self._update_status("OPENING")

            success = self.send_command_and_wait_ack("DISPENSER", "DI_OPEN", retries=3, timeout=5.0)

            if success:
                print("[Dispenser] 열기 성공. 적재 대기 상태로 전환합니다.")
                self._update_status("OPENED", "LOADING")
                # 10초 후에도 LOADED 신호가 없으면 타임아웃 처리
                threading.Timer(10.0, self._loading_timeout).start()
            else:
                print("[Dispenser] 열기 실패.")
                self._update_status("CLOSED", "OPEN_FAILED")
            
            return success

    def close_dispenser(self) -> bool:
        """디스펜서를 닫습니다."""
        with self.lock:
            if self.state == "CLOSED":
                print("[Dispenser] 이미 닫혀있습니다.")
                return True

            print("[Dispenser] 닫기 요청...")
            self._update_status("CLOSING")

            success = self.send_command_and_wait_ack("DISPENSER", "DI_CLOSE", retries=3, timeout=5.0)

            if success:
                print("[Dispenser] 닫기 성공.")
                self._update_status("CLOSED", "IDLE")
            else:
                print("[Dispenser] 닫기 실패.")
                self._update_status("OPENED", "CLOSE_FAILED") # 실패 시 이전 상태로 복귀
            
            return success

    def move_to_route(self, route: str) -> bool:
        """디스펜서를 지정된 경로(ROUTE_A 또는 ROUTE_B)로 이동시킵니다."""
        with self.lock:
            if self.position == route:
                print(f"[Dispenser] 이미 {route}에 위치합니다.")
                return True

            print(f"[Dispenser] {route}로 이동 요청...")
            self._update_status("MOVING")
            
            command = f"DI_LOC_{route}"
            success = self.send_command_and_wait_ack("DISPENSER", command, retries=3, timeout=10.0)

            if success:
                print(f"[Dispenser] {route}로 이동 성공.")
                self.position = route
                self._update_status("IDLE")
            else:
                print(f"[Dispenser] {route}로 이동 실패.")
                self._update_status("MOVE_FAILED")
            
            return success

    def handle_message(self, message: str):
        """
        장치로부터 비동기적으로 수신된 메시지를 처리합니다.
        주로 "LOADED"와 같은 센서 기반 상태 변경을 처리합니다.
        """
        if not message:
            return

        parsed = self.interface.parse_response(message)
        msg_type = parsed.get("type")
        
        if msg_type == "DISPENSER":
            new_state = parsed.get("state")
            new_position = parsed.get("position")

            if new_position and self.position != new_position:
                self.position = new_position
                print(f"[Dispenser] 비동기 위치 변경 감지: {new_position}")
                self._update_status("IDLE")

            if new_state == "LOADED" and self.state != "LOADED":
                print("[Dispenser] 적재 완료 신호 수신.")
                self._update_status("LOADED")
                self._on_loading_complete()
            elif new_state and self.state != new_state:
                 self._update_status(new_state)

    def _on_loading_complete(self):
        """적재 완료 후 후속 조치를 처리합니다."""
        print("[Dispenser] 적재 완료 후속 조치 시작.")
        
        # 1. 디스펜서를 닫습니다.
        self.close_dispenser()
        
        # 2. 트럭에 적재 완료 및 출발 명령을 보냅니다.
        if self.current_truck_id and self.facility_status_manager:
            truck_id = self.current_truck_id
            command_sender = self.facility_status_manager.command_sender
            
            if command_sender:
                # 1초 후 FINISH_LOADING 전송
                threading.Timer(1.0, command_sender.send, args=[truck_id, "FINISH_LOADING", {"position": self.position}]).start()
                # 1.5초 후 RUN 전송
                threading.Timer(1.5, command_sender.send, args=[truck_id, "RUN", {"target": "CHECKPOINT_C"}]).start()
                print(f"[Dispenser] {truck_id}에 적재 완료 및 출발 명령 예약 완료.")
            
            self.current_truck_id = None # 처리 완료 후 트럭 ID 초기화

    def _loading_timeout(self):
        """적재 시간 초과 시 호출됩니다."""
        with self.lock:
            # state가 여전히 LOADING일 경우 (즉, LOADED 신호를 못 받았을 경우) 타임아웃 처리
            if self.state == "OPENED" and self.operation == "LOADING":
                print("[Dispenser] 적재 시간 초과! 강제 완료 처리합니다.")
                self._update_status("LOADED", "TIMED_OUT")
                self._on_loading_complete()

    def _update_status(self, operation: str, state: str = None):
        """
        디스펜서의 상태와 동작을 업데이트하고 중앙 관리 매니저에 보고합니다.
        """
        # 상태(state)가 명시적으로 주어지면 업데이트
        if state:
            self.state = state
        
        self.operation = operation
        
        print(f"[상태 변경] 디스펜서: {self.state}, 위치: {self.position}, 동작: {self.operation}")
        if self.facility_status_manager:
            self.facility_status_manager.update_dispenser_status(
                "DISPENSER", self.state, self.position, self.operation
            )