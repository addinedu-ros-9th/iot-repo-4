from .truck_status_db import TruckStatusDB

class TruckStatusManager:
    def __init__(self, db: TruckStatusDB):
        self.db = db

    def update_truck_status(self, truck_id: str, event: str, payload: dict):
        """트럭 상태를 DB에 업데이트합니다."""
        try:
            # 이벤트에 따라 적절한 DB 메서드 호출
            if event == "STATUS_UPDATE":
                self.db.update_battery_status(truck_id, payload.get('battery'))
                self.db.update_position(truck_id, payload.get('position'))
            elif event == "OBSTACLE_DETECTED":
                self.db.update_obstacle_status(truck_id, payload.get('obstacle'))
            # 기타 이벤트 처리...
            print(f"[상태 관리자] {truck_id}의 상태 업데이트 완료: {event}")
        except Exception as e:
            print(f"[오류] 트럭 상태 업데이트 중: {e}")

    def update_truck_command(self, truck_id: str, command: str, payload: dict):
        """FSM에서 트럭으로 보낸 명령을 DB에 기록합니다."""
        try:
            self.db.update_last_command(truck_id, command, payload)
            print(f"[상태 관리자] {truck_id}의 마지막 명령 업데이트: {command}")
        except Exception as e:
            print(f"[오류] 트럭 명령 업데이트 중: {e}")

    def get_truck_status(self, truck_id: str):
        """특정 트럭의 전체 상태를 가져옵니다."""
        return self.db.get_truck_status(truck_id)

    def get_all_truck_status(self):
        """모든 트럭의 상태를 가져옵니다."""
        return self.db.get_all_truck_statuses()

    def get_fsm_state(self, truck_id: str):
        """트럭의 FSM 상태를 가져옵니다."""
        return self.db.get_fsm_state(truck_id)