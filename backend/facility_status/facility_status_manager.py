import threading
import time
from collections import defaultdict

class FacilityStatusManager:
    def __init__(self, facility_status_db, interval=5):
        self.db = facility_status_db
        self.interval = interval
        self.running = False
        self.thread = None
        self.command_sender = None
        self.truck_status_manager = None
        self.gate_status = self.db.get_all_gate_status() 
        self.belt_status = self.db.get_belt_status()
        self.dispenser_status = self.db.get_dispenser_status()
        print(f"[초기 게이트 상태] {self.gate_status}")

    def set_command_sender(self, command_sender):
        self.command_sender = command_sender

    def set_truck_status_manager(self, truck_status_manager):
        self.truck_status_manager = truck_status_manager

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
            print("[FacilityStatusManager 시작]")

    def _run(self):
        while self.running:
            try:
                self.update_all_status()
            except Exception as e:
                print(f"[오류] FacilityStatusManager 실행 중: {e}")
            time.sleep(self.interval)

    def update_all_status(self):
        print("[상태 업데이트] 모든 시설 상태 업데이트 중...")
        self.gate_status = self.db.get_all_gate_status()
        self.belt_status = self.db.get_belt_status()
        self.dispenser_status = self.db.get_dispenser_status()

    def get_all_facility_status(self):
        return {
            "gate": self.gate_status,
            "belt": self.belt_status,
            "dispenser": self.dispenser_status
        }

    def close(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
        print("[FacilityStatusManager 종료]")