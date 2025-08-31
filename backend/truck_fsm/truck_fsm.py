from collections import defaultdict
from .truck_state import TruckState, MissionPhase, TruckContext, Direction

class TruckFSM:
    def __init__(self, gate_controller, mission_manager, belt_controller, dispenser_controller, truck_status_manager):
        self.contexts = defaultdict(TruckContext)
        self.command_sender = None
        self.gate_controller = gate_controller
        self.mission_manager = mission_manager
        self.belt_controller = belt_controller
        self.dispenser_controller = dispenser_controller
        self.truck_status_manager = truck_status_manager

    def set_commander(self, command_sender):
        self.command_sender = command_sender

    def _get_or_create_context(self, truck_id):
        return self.contexts[truck_id]

    def handle_event(self, truck_id, event, payload=None):
        context = self._get_or_create_context(truck_id)
        payload = payload or {}
        
        print(f"[FSM] Truck: {truck_id}, State: {context.state}, Event: {event}, Payload: {payload}")

        # 현재 상태와 이벤트를 기반으로 다음 상태 결정
        next_state = self._transitions(context, event, payload)
        
        if next_state is not None:
            print(f"[상태 변경] {truck_id}: {context.state} -> {next_state}")
            context.state = next_state
            # 상태 변경 후 작업 수행
            self._on_state_entry(truck_id, context, event, payload)
        else:
            print(f"[FSM] 처리할 전환 없음: State={context.state}, Event={event}")

    def _transitions(self, context, event, payload):
        # 상태 전환 로직
        # ... (생략)
        return None # 임시

    def _on_state_entry(self, truck_id, context, event, payload):
        # 상태 진입 시 작업
        # ... (생략)
        pass
