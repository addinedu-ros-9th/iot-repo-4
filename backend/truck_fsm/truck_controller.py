from .truck_fsm_manager import TruckFSMManager

class TruckController:
    def __init__(self, fsm_manager: TruckFSMManager):
        self.fsm_manager = fsm_manager
        self.truck_status_manager = None

    def set_status_manager(self, truck_status_manager):
        self.truck_status_manager = truck_status_manager

    def handle_message(self, msg: dict):
        truck_id = msg.get("sender")
        cmd = msg.get("cmd")
        payload = msg.get("payload", {})

        if not truck_id or not cmd:
            print(f"[컨트롤러] 잘못된 메시지 수신: {msg}")
            return

        # 상태 DB 업데이트
        if self.truck_status_manager:
            self.truck_status_manager.update_truck_status(truck_id, cmd, payload)

        # FSM에 트리거 전달
        if self.fsm_manager:
            self.fsm_manager.handle_trigger(truck_id, cmd, payload)
        else:
            print(f"[경고] FSM Manager가 설정되지 않았습니다.")