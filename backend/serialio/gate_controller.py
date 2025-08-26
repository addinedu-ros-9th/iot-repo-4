from .serial_controller import SerialController

class GateController(SerialController):
    """
    게이트의 상태를 관리하고, 시리얼 통신을 통해 게이트를 제어합니다.
    SerialController를 상속받아 안정적인 통신 기능을 사용합니다.
    """
    def __init__(self, serial_interface, facility_status_manager=None):
        super().__init__(serial_interface)
        self.gate_states = {"GATE_A": "UNKNOWN", "GATE_B": "UNKNOWN"}
        self.facility_status_manager = facility_status_manager

    def open_gate(self, gate_id: str) -> bool:
        """게이트를 여는 명령을 보내고 성공 여부를 반환합니다."""
        if self.gate_states.get(gate_id) == "OPENED":
            print(f"[{gate_id}] 이미 열려있습니다.")
            return True

        print(f"[{gate_id}] 게이트 열기 요청...")
        self._update_gate_status(gate_id, self.gate_states.get(gate_id, "UNKNOWN"), "OPENING")

        # 부모 클래스의 안정적인 통신 메서드를 사용하여 명령 전송 및 ACK 대기
        success = self.send_command_and_wait_ack(gate_id, "OPEN", retries=3, timeout=5.0)

        if success:
            print(f"[{gate_id}] 게이트 열기 성공.")
            self._update_gate_status(gate_id, "OPENED", "IDLE")
        else:
            print(f"[{gate_id}] 게이트 열기 실패.")
            # 통신 실패 시, 이전 상태로 되돌리고 실패 상태를 보고
            self._update_gate_status(gate_id, self.gate_states.get(gate_id, "UNKNOWN"), "OPEN_FAILED")
        
        return success

    def close_gate(self, gate_id: str) -> bool:
        """게이트를 닫는 명령을 보내고 성공 여부를 반환합니다."""
        if self.gate_states.get(gate_id) == "CLOSED":
            print(f"[{gate_id}] 이미 닫혀있습니다.")
            return True

        print(f"[{gate_id}] 게이트 닫기 요청...")
        self._update_gate_status(gate_id, self.gate_states.get(gate_id, "UNKNOWN"), "CLOSING")

        # 부모 클래스의 안정적인 통신 메서드를 사용하여 명령 전송 및 ACK 대기
        success = self.send_command_and_wait_ack(gate_id, "CLOSE", retries=3, timeout=5.0)

        if success:
            print(f"[{gate_id}] 게이트 닫기 성공.")
            self._update_gate_status(gate_id, "CLOSED", "IDLE")
        else:
            print(f"[{gate_id}] 게이트 닫기 실패.")
            self._update_gate_status(gate_id, self.gate_states.get(gate_id, "UNKNOWN"), "CLOSE_FAILED")

        return success

    def handle_message(self, message: str):
        """
        장치로부터 비동기적으로 수신된 메시지를 처리합니다.
        (예: 센서에 의해 자동으로 상태가 변경되었을 경우)
        """
        if not message:
            return

        parsed = self.interface.parse_response(message)
        if parsed.get("type") == "GATE":
            gate_id = parsed.get("gate_id")
            state = parsed.get("state")
            if gate_id in self.gate_states:
                # 현재 상태와 다른 경우에만 업데이트
                if self.gate_states[gate_id] != state:
                    print(f"[{gate_id}] 비동기 상태 변경 감지: {state}")
                    self._update_gate_status(gate_id, state, "STATUS_UPDATE")

    def _update_gate_status(self, gate_id: str, state: str, operation: str):
        """게이트의 내부 상태를 업데이트하고, 중앙 관리 매니저에 보고합니다."""
        old_state = self.gate_states.get(gate_id)
        self.gate_states[gate_id] = state
        
        # 상태가 실제로 변경되었을 때만 로그를 남기고 보고합니다.
        if old_state != state:
            print(f"[상태 변경] {gate_id}: {old_state} -> {state} (동작: {operation})")
            if self.facility_status_manager:
                self.facility_status_manager.update_gate_status(gate_id, state, operation)
        else:
            # 상태는 같지만 동작(operation)만 변경된 경우 (예: OPENING -> OPEN_FAILED)
            if self.facility_status_manager:
                 self.facility_status_manager.update_gate_status(gate_id, state, operation)