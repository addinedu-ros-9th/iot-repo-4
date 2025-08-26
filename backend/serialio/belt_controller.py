import threading
from .serial_controller import SerialController

class BeltController(SerialController):
    """
    컨베이어 벨트의 상태를 관리하고, 시리얼 통신을 통해 벨트를 제어합니다.
    SerialController를 상속받아 안정적인 통신 기능을 사용합니다.
    """
    def __init__(self, serial_interface, facility_status_manager=None):
        super().__init__(serial_interface)
        self.belt_state = "UNKNOWN"  # 벨트의 현재 상태 (RUNNING, STOPPED, EMERGENCY_STOP)
        self.container_full = False # 컨테이너 포화 상태
        self.lock = threading.Lock()
        self.facility_status_manager = facility_status_manager

    def turn_on_belt(self) -> bool:
        """벨트를 작동시키는 명령을 보내고 성공 여부를 반환합니다."""
        with self.lock:
            if self.belt_state == "RUNNING":
                print("[Belt] 이미 작동 중입니다.")
                return True
            
            if self.container_full:
                print("[Belt] 컨테이너가 가득 차서 벨트를 작동할 수 없습니다.")
                self._update_status("STOPPED", "REJECTED_FULL")
                return False

            print("[Belt] 벨트 작동 요청...")
            self._update_status(self.belt_state, "STARTING")

            success = self.send_command_and_wait_ack("BELT", "RUN", retries=3, timeout=3.0)

            if success:
                print("[Belt] 벨트 작동 성공.")
                self._update_status("RUNNING", "IDLE")
            else:
                print("[Belt] 벨트 작동 실패.")
                self._update_status(self.belt_state, "START_FAILED")
            
            return success

    def turn_off_belt(self) -> bool:
        """벨트를 정지시키는 명령을 보내고 성공 여부를 반환합니다."""
        with self.lock:
            if self.belt_state == "STOPPED":
                # 이미 멈춘 상태여도, 외부 요청에 의해 다시 멈춤 명령을 보낼 수 있도록 처리
                pass

            print("[Belt] 벨트 정지 요청...")
            self._update_status(self.belt_state, "STOPPING")

            success = self.send_command_and_wait_ack("BELT", "STOP", retries=3, timeout=3.0)

            if success:
                print("[Belt] 벨트 정지 성공.")
                self._update_status("STOPPED", "IDLE")
            else:
                print("[Belt] 벨트 정지 실패.")
                self._update_status(self.belt_state, "STOP_FAILED")
            
            return success

    def emergency_stop(self) -> bool:
        """벨트를 비상 정지시키는 명령을 보내고 성공 여부를 반환합니다."""
        with self.lock:
            print("[Belt] 비상 정지 요청...")
            self._update_status(self.belt_state, "EMERGENCY_STOPPING")

            success = self.send_command_and_wait_ack("BELT", "EMRSTOP", retries=1, timeout=2.0)

            if success:
                print("[Belt] 비상 정지 성공.")
                self._update_status("EMERGENCY_STOP", "IDLE")
            else:
                print("[Belt] 비상 정지 실패.")
                # 비상 정지는 매우 중요하므로, 실패하더라도 상태는 비상 정지로 변경
                self._update_status("EMERGENCY_STOP", "EMR_STOP_FAILED")
            
            return success

    def handle_message(self, message: str):
        """
        장치로부터 비동기적으로 수신된 메시지(주로 센서 상태)를 처리합니다.
        """
        if not message:
            return

        parsed = self.interface.parse_response(message)
        msg_type = parsed.get("type")

        if msg_type == "BELT":
            new_state = parsed.get("state")
            if self.belt_state != new_state:
                print(f"[Belt] 비동기 상태 변경 감지: {new_state}")
                self._update_status(new_state, "STATUS_UPDATE")

        elif msg_type == "CONTAINER":
            is_full = parsed.get("state") == "FULL"
            if self.container_full != is_full:
                self.container_full = is_full
                print(f"[Belt] 컨테이너 상태 변경 감지: {'포화' if is_full else '비어있음'}")
                if is_full:
                    # 컨테이너가 꽉 차면 벨트는 자동으로 멈춰야 함
                    self.turn_off_belt()
                self._update_status(self.belt_state, "CONTAINER_UPDATE")

    def _update_status(self, state: str, operation: str):
        """
        벨트의 내부 상태를 업데이트하고, 중앙 관리 매니저에 보고합니다.
        """
        old_state = self.belt_state
        self.belt_state = state
        container_status = "FULL" if self.container_full else "EMPTY"

        # 상태가 변경되었거나, 특정 동작이 발생했을 때만 로그 및 보고
        if old_state != state or operation not in ["IDLE", "STATUS_UPDATE"]:
            print(f"[상태 변경] 벨트: {old_state} -> {state}, 컨테이너: {container_status}, 동작: {operation}")
            if self.facility_status_manager:
                self.facility_status_manager.update_belt_status("BELT", state, operation, container_status)