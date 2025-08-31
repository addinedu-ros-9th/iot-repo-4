from .serial_controller import SerialController

class GateController:
    def __init__(self, serial_controller: SerialController):
        self.serial_controller = serial_controller

    def open_gate(self, gate_id: str):
        command = f"{gate_id}_OPEN"
        print(f"[게이트] 명령 전송: {command}")
        if self.serial_controller:
            self.serial_controller.send_command(gate_id, command)
        else:
            print(f"[오류] 시리얼 컨트롤러가 설정되지 않았습니다.")

    def close_gate(self, gate_id: str):
        command = f"{gate_id}_CLOSE"
        print(f"[게이트] 명령 전송: {command}")
        if self.serial_controller:
            self.serial_controller.send_command(gate_id, command)
        else:
            print(f"[오류] 시리얼 컨트롤러가 설정되지 않았습니다.")
