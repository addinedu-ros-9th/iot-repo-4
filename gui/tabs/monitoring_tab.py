from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGraphicsScene, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsTextItem, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QDialog, QGridLayout, QPushButton, QLabel, QComboBox
from PyQt6.QtGui import QPen, QBrush, QColor, QPainterPath, QPixmap
from PyQt6.QtCore import Qt, QTimer, QSize, QPointF
from PyQt6 import uic
import os

from gui.api_client import api_client

class TruckIcon(QGraphicsPixmapItem):
    """맵에 표시되는 트럭 아이콘 GrahpicsItem"""
    def __init__(self, truck_id, parent=None):
        super().__init__(parent)
        self.truck_id = truck_id
        self.setPixmap(QPixmap("gui/assets/truck.png").scaled(30, 30, Qt.AspectRatioMode.KeepAspectRatio))
        self.setOffset(-15, -15)  # 아이콘의 중심점을 기준으로 위치 조정
        self.setZValue(10) # 다른 아이템들보다 위에 보이도록 설정

class MonitoringTab(QWidget):
    """메인 모니터링 탭 클래스"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui", "tab_monitoring.ui")
        uic.loadUi(ui_path, self)

        self.node_coords = {}
        self.truck_icons = {}  # 다중 트럭 아이콘을 관리하는 딕셔너리
        self.selected_truck_id = None

        self.setup_map()
        self.setup_controls()
        self.setup_update_timer()
        
    def setup_map(self):
        """맵 경로와 고정 시설물을 QGraphicsScene에 그립니다."""
        self.scene = QGraphicsScene(self)
        self.graphicsView_map.setScene(self.scene)
        self.scene.setSceneRect(0, 0, 800, 400)
        
        # 경로 및 노드 좌표 정의 (이전과 동일)
        left, top = 0, 80
        right, bottom = 600, 320
        width, height = right - left, bottom - top
        self.node_coords = {
            "STANDBY": QPointF(left + width * 0.1, bottom),
            "CHECKPOINT_A": QPointF(left + width * 0.3, bottom),
            "GATE_A": QPointF(left + width * 0.5, bottom),
            "CHECKPOINT_B": QPointF(left + width * 0.7, bottom),
            "LOAD_B": QPointF(right, bottom - height * 0.3),
            "LOAD_A": QPointF(right, top + height * 0.3),
            "CHECKPOINT_C": QPointF(left + width * 0.7, top),
            "GATE_B": QPointF(left + width * 0.5, top),
            "CHECKPOINT_D": QPointF(left + width * 0.3, top),
            "BELT": QPointF(left, top + height * 0.3)
        }
        # ... (이하 맵을 그리는 코드는 이전과 동일하여 생략) ...

    def setup_controls(self):
        """UI 컨트롤(버튼 등)의 이벤트를 연결합니다."""
        # self.button_new_mission.clicked.connect(self.open_new_mission_dialog)
        pass # 필요한 컨트롤 연결

    def setup_update_timer(self):
        """모든 UI 정보를 주기적으로 업데이트하는 메인 타이머를 설정합니다."""
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_all_ui_elements)
        self.timer.start(500)  # 0.5초마다 모든 정보 업데이트

    def update_all_ui_elements(self):
        """API를 호출하여 모든 트럭 및 시설물 정보를 업데이트합니다."""
        try:
            # FSM 매니저로부터 모든 트럭의 최신 상태를 가져옵니다.
            all_statuses = api_client.get_all_truck_statuses()
            if not all_statuses:
                return

            self._update_truck_icons(all_statuses)
            self._update_info_panels(all_statuses)

        except Exception as e:
            print(f"[UI] UI 업데이트 중 오류 발생: {e}")

    def _update_truck_icons(self, all_statuses):
        """맵 위의 트럭 아이콘들을 생성, 이동, 삭제합니다."""
        current_truck_ids = set(all_statuses.keys())
        existing_truck_ids = set(self.truck_icons.keys())

        # 새로 추가된 트럭 아이콘 생성
        for truck_id in current_truck_ids - existing_truck_ids:
            new_icon = TruckIcon(truck_id)
            self.truck_icons[truck_id] = new_icon
            self.scene.addItem(new_icon)
            print(f"[UI] 새로운 트럭 아이콘 생성: {truck_id}")

        # 없어진 트럭 아이콘 삭제
        for truck_id in existing_truck_ids - current_truck_ids:
            icon_to_remove = self.truck_icons.pop(truck_id)
            self.scene.removeItem(icon_to_remove)
            print(f"[UI] 트럭 아이콘 삭제: {truck_id}")

        # 모든 트럭 위치 업데이트
        for truck_id, status in all_statuses.items():
            position_name = status.get("position")
            if position_name in self.node_coords:
                coords = self.node_coords[position_name]
                self.truck_icons[truck_id].setPos(coords)

    def _update_info_panels(self, all_statuses):
        """사이드 정보 패널(상태, 배터리, 미션)의 내용을 업데이트합니다."""
        # 현재 선택된 트럭이 없으면, 첫 번째 트럭을 선택
        if self.selected_truck_id is None and all_statuses:
            self.selected_truck_id = list(all_statuses.keys())[0]
        
        # 선택된 트럭이 더 이상 존재하지 않으면, 선택 해제
        if self.selected_truck_id not in all_statuses:
            self.selected_truck_id = None
            # 정보 패널 클리어 로직 추가 가능
            return

        # 선택된 트럭의 정보 가져오기
        selected_truck_data = all_statuses.get(self.selected_truck_id, {})

        # FSM 상태 업데이트
        fsm_state = selected_truck_data.get("state", "UNKNOWN")
        self.label_fsm_state.setText(fsm_state)

        # 위치 정보 업데이트
        position = selected_truck_data.get("position", "UNKNOWN")
        self.label_truck_position.setText(position)

        # 배터리 정보 업데이트
        battery_info = selected_truck_data.get("battery", {})
        level = battery_info.get("level", 0)
        is_charging = battery_info.get("is_charging", False)
        self.progressBar_battery.setValue(int(level))
        self.progressBar_battery.setFormat(f"{level:.0f}% {'(충전중)' if is_charging else ''}")

        # 미션 정보 업데이트
        mission_id = selected_truck_data.get("mission_id", "없음")
        mission_phase = selected_truck_data.get("mission_phase", "")
        self.label_mission_info.setText(f"ID: {mission_id} ({mission_phase})")

# 이 파일이 직접 실행될 때를 위한 간단한 테스트 코드 (선택 사항)
if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication, QMainWindow
    app = QApplication(sys.argv)
    window = QMainWindow()
    monitoring_tab = MonitoringTab()
    window.setCentralWidget(monitoring_tab)
    window.show()
    sys.exit(app.exec())