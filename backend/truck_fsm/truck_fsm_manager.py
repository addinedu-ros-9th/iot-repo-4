from .truck_fsm import TruckFSM

class TruckFSMManager:
    def __init__(self, gate_controller, mission_manager, belt_controller, dispenser_controller, truck_status_manager):
        self.fsm = TruckFSM(
            gate_controller=gate_controller,
            mission_manager=mission_manager,
            belt_controller=belt_controller,
            dispenser_controller=dispenser_controller,
            truck_status_manager=truck_status_manager
        )

    def set_commander(self, command_sender):
        self.fsm.set_commander(command_sender)

    def handle_trigger(self, truck_id, event, payload=None):
        try:
            self.fsm.handle_event(truck_id, event, payload)
            print(f"[FSM 매니저] {truck_id}에 이벤트 {event} 처리 완료")
        except Exception as e:
            print(f"[오류] FSM 처리 중 예외 발생: {e}")
