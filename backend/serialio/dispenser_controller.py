from .serial_controller import SerialController

class DispenserController:
    def __init__(self, serial_controller: SerialController):
        self.serial_controller = serial_controller
        self.device_id = "DISPENSER"

    def send_command(self, dispenser_id: str, command: str) -> bool:
        """디스펜서에 명령을 전송합니다."""
        full_command = f"{command}"
        print(f"[디스펜서] 명령 전송: {full_command}")
        if self.serial_controller:
            return self.serial_controller.send_command(self.device_id, full_command)
        else:
            print(f"[오류] 시리얼 컨트롤러가 설정되지 않았습니다.")
            return False
