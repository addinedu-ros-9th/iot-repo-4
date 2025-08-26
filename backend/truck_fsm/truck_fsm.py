from .truck_state import TruckState, MissionPhase, Direction
import time
import threading

class TruckFSM:
    """
    트럭의 상태 전이 로직을 정의하는 순수 엔진 클래스입니다.
    외부로부터 트럭의 현재 상태(Context)와 이벤트를 받아 다음 상태를 결정하고, 
    필요한 액션을 수행합니다.
    """
    def __init__(self, command_sender=None, gate_controller=None, belt_controller=None, dispenser_controller=None, mission_manager=None, locks=None):
        self.command_sender = command_sender
        self.gate_controller = gate_controller
        self.belt_controller = belt_controller
        self.dispenser_controller = dispenser_controller
        self.mission_manager = mission_manager
        
        # Manager로부터 공유 자원 Lock을 전달받음
        self.locks = locks if locks else {
            'gate': threading.Lock(),
            'belt': threading.Lock(),
            'dispenser': threading.Lock()
        }
        
        # 상태 전이 테이블 정의
        self.transitions = self._define_transitions()

    def handle_event(self, context, event, payload=None):
        """
        특정 트럭(Context)에 대한 이벤트를 처리하고 상태를 전이시킵니다.
        """
        if payload is None: payload = {}
        current_state = context.state

        # (현재 상태, 이벤트) 또는 (모든 상태, 이벤트)에 해당하는 전이 규칙을 찾음
        key = (current_state, event)
        global_key = (None, event)
        transition = self.transitions.get(key) or self.transitions.get(global_key)

        if not transition:
            print(f"[FSM] {context.truck_id}: 상태({current_state})에서 이벤트({event})에 대한 전이 규칙을 찾을 수 없습니다.")
            return False

        # 조건 확인
        condition = transition.get("condition")
        if condition and not condition(self, context, payload):
            print(f"[FSM] {context.truck_id}: 이벤트({event})의 조건이 충족되지 않아 전이를 중단합니다.")
            return False

        # 액션 실행
        action = transition.get("action")
        if action:
            try:
                action(self, context, payload)
            except Exception as e:
                print(f"[FSM] {context.truck_id}: 액션 실행 중 오류 발생 - {e}")
                import traceback
                traceback.print_exc()
                return False

        # 상태 변경
        next_state = transition.get("next_state")
        if next_state:
            context.state = next_state
            print(f"[FSM] {context.truck_id}: 상태 전이 {current_state} -> {next_state}")
        
        return True

    # ------------------- 상태 전이 테이블 정의 ------------------- #

    def _define_transitions(self):
        """FSM의 모든 상태 전이 규칙을 정의합니다."""
        return {
            # (현재 상태, 이벤트): {다음 상태, 액션, 조건}
            (TruckState.IDLE, "ASSIGN_MISSION"): {
                "next_state": TruckState.MOVING,
                "action": self._action_assign_mission,
                "condition": self._cond_can_accept_mission
            },
            (TruckState.IDLE, "START_CHARGING"): {
                "next_state": TruckState.CHARGING,
                "action": self._action_start_charging,
                "condition": self._cond_needs_charging
            },
            (TruckState.MOVING, "ARRIVED"): {
                "next_state": TruckState.WAITING,
                "action": self._action_handle_arrival
            },
            (TruckState.WAITING, "START_LOADING"): {
                "next_state": TruckState.LOADING,
                "action": self._action_start_loading,
                "condition": self._cond_is_at_loading_area
            },
            (TruckState.LOADING, "FINISH_LOADING"): {
                "next_state": TruckState.MOVING,
                "action": self._action_finish_loading
            },
            (TruckState.WAITING, "START_UNLOADING"): {
                "next_state": TruckState.UNLOADING,
                "action": self._action_start_unloading,
                "condition": self._cond_is_at_unloading_area
            },
            (TruckState.UNLOADING, "FINISH_UNLOADING"): {
                "next_state": TruckState.IDLE,
                "action": self._action_finish_unloading
            },
            (TruckState.CHARGING, "FINISH_CHARGING"): {
                "next_state": TruckState.IDLE,
                "action": self._action_finish_charging,
                "condition": self._cond_is_fully_charged
            },
            (None, "EMERGENCY"): {
                "next_state": TruckState.EMERGENCY,
                "action": self._action_handle_emergency
            },
            (TruckState.EMERGENCY, "RESET"): {
                "next_state": TruckState.IDLE,
                "action": self._action_reset_from_emergency
            },
        }

    # ------------------- 액션 메서드 (이름 변경: _action_*) ------------------- #

    def _action_assign_mission(self, context, payload):
        mission_id = payload.get("mission_id")
        source = payload.get("source", "LOAD_A")
        context.mission_id = mission_id
        context.mission_phase = MissionPhase.TO_LOADING
        context.loading_target = source
        context.target_position = "CHECKPOINT_A"
        print(f"[FSM] {context.truck_id}: 미션({mission_id}) 할당. {source}에서 적재 후 이동 시작.")
        self.command_sender.send(context.truck_id, "RUN", {"target": context.target_position})

    def _action_handle_arrival(self, context, payload):
        position = payload.get("position")
        context.position = position
        print(f"[FSM] {context.truck_id}: {position}에 도착.")

        # 게이트 제어
        if position == "CHECKPOINT_A":
            with self.locks['gate']:
                self.gate_controller.open_gate("GATE_A")
        elif position == "CHECKPOINT_B":
            with self.locks['gate']:
                self.gate_controller.close_gate("GATE_A")
        # ... 다른 게이트 로직 ...

        # 목적지 도착 여부 확인
        if position == context.loading_target:
            self.handle_event(context, "START_LOADING")
        elif position == "BELT":
            self.handle_event(context, "START_UNLOADING")
        else:
            # 다음 목적지로 계속 이동
            self._update_target_and_run(context)

    def _action_start_loading(self, context, payload):
        print(f"[FSM] {context.truck_id}: 적재 위치({context.position})에서 적재 시작.")
        with self.locks['dispenser']:
            self.dispenser_controller.open_dispenser(context.truck_id)

    def _action_finish_loading(self, context, payload):
        print(f"[FSM] {context.truck_id}: 적재 완료. 하역지로 이동 시작.")
        context.mission_phase = MissionPhase.TO_UNLOADING
        self._update_target_and_run(context)

    def _action_start_unloading(self, context, payload):
        print(f"[FSM] {context.truck_id}: 하역 위치({context.position})에서 하역 시작.")
        with self.locks['belt']:
            self.belt_controller.turn_on_belt()

    def _action_finish_unloading(self, context, payload):
        print(f"[FSM] {context.truck_id}: 하역 완료. 대기 장소로 복귀.")
        if self.mission_manager:
            self.mission_manager.complete_mission(context.mission_id)
        context.mission_id = None
        context.mission_phase = MissionPhase.RETURNING
        self._update_target_and_run(context)

    def _action_start_charging(self, context, payload):
        context.is_charging = True
        print(f"[FSM] {context.truck_id}: 충전 시작.")
        self.command_sender.send(context.truck_id, "START_CHARGING")

    def _action_finish_charging(self, context, payload):
        context.is_charging = False
        print(f"[FSM] {context.truck_id}: 충전 완료.")
        self.command_sender.send(context.truck_id, "CHARGING_COMPLETED")
        # 충전 완료 후 새 미션 확인
        self.handle_event(context, "ASSIGN_MISSION")

    def _action_handle_emergency(self, context, payload):
        print(f"[FSM] {context.truck_id}: 비상 정지 발동.")
        self.command_sender.send(context.truck_id, "STOP")
        with self.locks['belt']:
            self.belt_controller.emergency_stop()

    def _action_reset_from_emergency(self, context, payload):
        print(f"[FSM] {context.truck_id}: 비상 상태 해제.")
        if context.mission_id and self.mission_manager:
            self.mission_manager.cancel_mission(context.mission_id)
        context.mission_id = None
        context.mission_phase = MissionPhase.NONE

    # ------------------- 조건 메서드 (이름 변경: _cond_*) ------------------- #

    def _cond_can_accept_mission(self, context, payload):
        return (context.mission_id is None and 
                not context.is_charging and 
                context.battery_level > 30)

    def _cond_is_at_loading_area(self, context, payload):
        return context.position == context.loading_target

    def _cond_is_at_unloading_area(self, context, payload):
        return context.position == "BELT"

    def _cond_needs_charging(self, context, payload):
        return context.battery_level <= 30

    def _cond_is_fully_charged(self, context, payload):
        return context.battery_level >= 100

    # ------------------- Helper 메서드 ------------------- #

    def _update_target_and_run(self, context):
        """컨텍스트를 기반으로 다음 목적지를 계산하고 이동 명령을 전송합니다."""
        # 이 부분은 경로 관리 로직이 필요합니다. 지금은 간단하게 처리합니다.
        if context.mission_phase == MissionPhase.TO_UNLOADING:
            context.target_position = "BELT"
        elif context.mission_phase == MissionPhase.RETURNING:
            context.target_position = "STANDBY"
        else:
            context.target_position = None # 경로의 끝

        if context.target_position:
            print(f"[FSM] {context.truck_id}: 다음 목적지({context.target_position})로 이동 명령.")
            self.command_sender.send(context.truck_id, "RUN", {"target": context.target_position})
        else:
            print(f"[FSM] {context.truck_id}: 모든 경로 완료.")