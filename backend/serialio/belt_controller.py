from .serial_controller import SerialController

class BeltController:
    def __init__(self, serial_controller: SerialController):
        self.serial_controller = serial_controller
        self.device_id = "BELT"

    def handle_message(self, message: str):
        print(f"[컨베이어] 메시지 수신: {message}")
        if self.serial_controller:
            self.serial_controller.send_command(self.device_id, message)
        else:
            print(f"[오류] 시리얼 컨트롤러가 설정되지 않았습니다.")
