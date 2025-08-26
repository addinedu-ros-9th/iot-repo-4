import threading
from .truck_fsm import TruckFSM
from .truck_state import TruckContext

class TruckFSMManager:
    """
    모든 트럭의 FSM(상태 머신)과 상태(Context)를 총괄 관리합니다.
    다중 AGV가 안정적으로 동작하도록 공유 자원(설비)에 대한 접근을 제어합니다.
    """
    def __init__(self, gate_controller, mission_manager, belt_controller=None, dispenser_controller=None, truck_status_manager=None):
        # 각 트럭의 상태(Context)를 저장하는 딕셔너리
        self.contexts = {}
        
        # 공유 자원(설비)에 대한 Lock 생성
        self.gate_lock = threading.Lock()
        self.belt_lock = threading.Lock()
        self.dispenser_lock = threading.Lock()

        # 상태 전이 로직을 처리할 FSM 엔진 (단일 인스턴스)
        self.fsm = TruckFSM(
            gate_controller=gate_controller,
            belt_controller=belt_controller,
            dispenser_controller=dispenser_controller,
            mission_manager=mission_manager,
            # FSM이 공유 자원을 잠글 수 있도록 Lock 전달
            locks={
                'gate': self.gate_lock,
                'belt': self.belt_lock,
                'dispenser': self.dispenser_lock
            }
        )
        self.truck_status_manager = truck_status_manager
        self.command_sender = None
        print("[TruckFSMManager] 초기화 완료")

    def set_command_sender(self, command_sender):
        """TCP 서버로부터 받은 command_sender를 FSM과 다른 모듈에 설정합니다."""
        self.command_sender = command_sender
        self.fsm.command_sender = command_sender
        if self.fsm.mission_manager:
            self.fsm.mission_manager.set_command_sender(command_sender)

    def handle_event(self, truck_id, event, payload=None):
        """
        특정 트럭에 대한 이벤트를 처리합니다.
        해당 트럭의 Context를 찾아 FSM 엔진에 전달합니다.
        """
        context = self._get_or_create_context(truck_id)
        return self.fsm.handle_event(context, event, payload)

    def handle_trigger(self, truck_id, cmd, payload=None):
        """
        외부(주로 API)로부터의 명령(트리거)을 처리합니다.
        내부적으로는 FSM 이벤트로 변환하여 처리합니다.
        """
        print(f"[FSMManager] 트리거 수신: {truck_id}, 명령: {cmd}")
        # 트리거를 FSM 이벤트로 변환하여 처리
        return self.handle_event(truck_id, cmd, payload)

    def update_truck_status(self, truck_id, position, battery_level, is_charging=False):
        """트럭의 물리적 상태(위치, 배터리)를 업데이트합니다."""
        context = self._get_or_create_context(truck_id)
        
        if battery_level is not None:
            context.battery_level = battery_level
            context.is_charging = is_charging

        # 위치가 변경되었을 경우, ARRIVED 이벤트를 발생시켜 FSM이 상태를 변경하도록 함
        if position and context.position != position:
            self.handle_event(truck_id, "ARRIVED", {"position": position})

    def get_all_truck_statuses(self):
        """모든 트럭의 현재 상태를 요약하여 반환합니다."""
        statuses = {}
        for truck_id, context in self.contexts.items():
            statuses[truck_id] = {
                "state": context.state.value,
                "position": context.position,
                "mission_id": context.mission_id,
                "mission_phase": context.mission_phase.value if context.mission_phase else None,
                "battery": {
                    "level": context.battery_level,
                    "is_charging": context.is_charging
                }
            }
        return statuses

    def get_truck_context(self, truck_id):
        """특정 트럭의 전체 Context 객체를 반환합니다."""
        return self._get_or_create_context(truck_id)

    def _get_or_create_context(self, truck_id):
        """truck_id에 해당하는 Context를 가져오거나, 없으면 새로 생성합니다."""
        if truck_id not in self.contexts:
            print(f"[FSMManager] 새로운 트럭 감지: {truck_id}. 새 Context를 생성합니다.")
            self.contexts[truck_id] = TruckContext(truck_id)
        return self.contexts[truck_id]