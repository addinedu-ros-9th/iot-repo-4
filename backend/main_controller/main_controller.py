from backend.serialio.device_manager import DeviceManager
from backend.serialio.belt_controller import BeltController
from backend.serialio.gate_controller import GateController
from backend.serialio.dispenser_controller import DispenserController

from backend.mission.mission_db import MissionDB
from backend.mission.mission_manager import MissionManager

from backend.truck_status.truck_status_db import TruckStatusDB
from backend.truck_status.truck_status_manager import TruckStatusManager

from backend.tcpio.truck_command_sender import TruckCommandSender
from backend.truck_fsm.truck_fsm_manager import TruckFSMManager
from backend.truck_fsm.truck_controller import TruckController


class MainController:
    def __init__(self, port_map, use_fake=False, fake_devices=None, debug=False, facility_status_manager=None):
        # 디버그 모드 설정
        self.debug = debug
        
        # 시설 상태 관리자 저장
        self.facility_status_manager = facility_status_manager
        
        # 명령 전송자 설정 추적 변수 추가
        self.command_sender_initialized = False
        
        # Serial 연결 및 장치 컨트롤러 생성
        self.device_manager = DeviceManager(
            port_map=port_map, 
            use_fake=use_fake, 
            fake_devices=fake_devices, 
            debug=debug, 
            facility_status_manager=facility_status_manager
        )

        # Mission DB 초기화
        self.mission_db = MissionDB(
            host="localhost",
            user="root",
            password="jinhyuk2dacibul",
            database="dust"
        )
        self.mission_manager = MissionManager(self.mission_db)

        # TruckStatusDB 초기화
        self.status_db = TruckStatusDB(
            host="localhost",
            user="root",
            password="jinhyuk2dacibul",
            database="dust"
        )
        self.truck_status_manager = TruckStatusManager(self.status_db)

        # 장치 컨트롤러 가져오기
        self.belt_controller = self.device_manager.get_controller("BELT")
        
        # 게이트 컨트롤러들 참조
        self.gate_controllers = {
            gate_id: self.device_manager.get_controller(gate_id)
            for gate_id in ["GATE_A", "GATE_B"]
            if self.device_manager.get_controller(gate_id) is not None
        }
        
        # 대표 게이트 컨트롤러 (FSM용)
        if "GATE_A" in self.gate_controllers:
            self.gate_controller = self.gate_controllers["GATE_A"]
        elif "GATE_B" in self.gate_controllers:
            self.gate_controller = self.gate_controllers["GATE_B"]
        else:
            print("[경고] 사용 가능한 게이트 컨트롤러가 없습니다")
            self.gate_controller = None
            
        # 디스펜서 컨트롤러 가져오기
        self.dispenser_controller = self.device_manager.get_controller("DISPENSER")
        if not self.dispenser_controller:
            print("[경고] 디스펜서 컨트롤러를 찾을 수 없습니다")
        
        # FSM 관리자 - 새 버전 사용
        self.truck_fsm_manager = TruckFSMManager(
            gate_controller=self.gate_controller,
            mission_manager=self.mission_manager,
            belt_controller=self.belt_controller,
            dispenser_controller=self.dispenser_controller,
            truck_status_manager=self.truck_status_manager
        )

        # 트럭 컨트롤러 - 새 버전 사용
        self.truck_controller = TruckController(self.truck_fsm_manager)
        self.truck_controller.set_status_manager(self.truck_status_manager)

        # 초기 TruckCommandSender 설정
        self.set_truck_commander({})

        print("[MainController 초기화 완료]")

    # 트럭 명령 전송자 설정
    def set_truck_commander(self, truck_socket_map: dict):
        """트럭 명령 전송자 설정"""
        # 이미 초기화되었는지 확인
        if self.command_sender_initialized and truck_socket_map:
            # truck_socket_map이 비어있지 않은 경우만 업데이트
            commander = TruckCommandSender(truck_socket_map)
            # TCP 서버 참조 설정
            if hasattr(self, 'tcp_server'):
                commander.set_tcp_server(self.tcp_server)
            # 상태 관리자 참조 설정 유지
            if hasattr(self, 'truck_status_manager'):
                commander.set_truck_status_manager(self.truck_status_manager)
            self.truck_fsm_manager.set_commander(commander)
            return
            
        # 최초 설정 또는 맵이 비어있는 초기화인 경우
        commander = TruckCommandSender(truck_socket_map)
        
        # TCP 서버 참조 설정
        if hasattr(self, 'tcp_server'):
            commander.set_tcp_server(self.tcp_server)
            print("[TCP 서버 참조 설정] commander에 tcp_server 참조가 설정되었습니다.")
        
        self.truck_fsm_manager.set_commander(commander)
        
        # 시설 상태 관리자에도 명령 전송자 설정 (최초 한 번만)
        if self.facility_status_manager and not self.command_sender_initialized:
            self.facility_status_manager.set_command_sender(commander)
            
            # 상태 관리자 참조도 설정 - 안전하게 확인
            if hasattr(self, 'truck_status_manager'):
                commander.set_truck_status_manager(self.truck_status_manager)
            
            print("[명령 전송자 설정] facility_status_manager에 명령 전송자 설정 완료")
            self.command_sender_initialized = True

    # 메시지 처리
    def handle_message(self, msg: dict):
        """메시지 처리"""
        sender = msg.get("sender")
        cmd = msg.get("cmd", "").strip().upper()
        payload = msg.get("payload", {})

        print(f"[MainController] sender={sender}, cmd={cmd}")

        # 벨트 수동 제어
        if cmd.startswith("BELT_"):
            self._handle_manual_belt_command(cmd)
            return

        # 게이트 수동 제어
        if cmd.startswith("GATE_"):
            self._handle_manual_gate_command(cmd)
            return
            
        # 디스펜서 수동 제어
        if cmd.startswith("DISPENSER_"):
            self._handle_manual_dispenser_command(cmd)
            return

        # 트럭 메시지 처리
        if sender:
            self.truck_controller.handle_message(msg)
        else:
            print("[경고] sender가 없는 메시지")

    # 수동 벨트 제어 명령 처리
    def _handle_manual_belt_command(self, cmd: str):
        """수동 벨트 제어"""
        print(f"[수동 벨트 제어] CMD: {cmd}")
        if self.belt_controller:
            self.belt_controller.handle_message(cmd)
        else:
            print("[오류] 벨트 컨트롤러를 찾을 수 없습니다")

    # 수동 게이트 제어 명령 처리
    def _handle_manual_gate_command(self, cmd: str):
        """수동 게이트 제어"""
        parts = cmd.split("_")
        if len(parts) == 3:
            gate_id = f"GATE_{parts[1]}"
            action = parts[2]
            
            gate_controller = self.gate_controllers.get(gate_id)
            if gate_controller:
                if action == "OPEN":
                    gate_controller.open_gate(gate_id)
                elif action == "CLOSE":
                    gate_controller.close_gate(gate_id)
            else:
                print(f"[오류] {gate_id} 컨트롤러를 찾을 수 없습니다")
        else:
            print(f"[게이트 명령 포맷 오류] {cmd}")
            
    # 수동 디스펜서 제어 명령 처리
    def _handle_manual_dispenser_command(self, cmd: str):
        """수동 디스펜서 제어"""
        print(f"[수동 디스펜서 제어] CMD: {cmd}")
        parts = cmd.split("_")
        
        if len(parts) >= 2:
            dispenser_id = "DISPENSER"
            action = "_".join(parts[1:])  # DISPENSER_ 이후의 모든 부분을 액션으로 처리
            
            if self.dispenser_controller:
                success = self.dispenser_controller.send_command(dispenser_id, action)
                print(f"[디스펜서 명령 결과] {action}: {'성공' if success else '실패'}")
            else:
                print("[오류] 디스펜서 컨트롤러를 찾을 수 없습니다")
        else:
            print(f"[디스펜서 명령 포맷 오류] {cmd}")

    # 시스템 종료
    def shutdown(self):
        """시스템 종료"""
        print("[시스템 종료 중...]")
        self.mission_db.close()
        self.status_db.close()
        self.device_manager.close_all()
        if self.facility_status_manager:
            self.facility_status_manager.close()
        print("[시스템 종료 완료]")

    # TCP 서버 참조 설정
    def set_tcp_server(self, tcp_server):
        """TCP 서버 참조 설정"""
        self.tcp_server = tcp_server
        print("[TCP 서버 참조 설정] MainController에 tcp_server 참조가 설정되었습니다.")
        
        # 기존 명령 전송자가 있으면 TCP 서버 참조도 설정
        if hasattr(self.truck_fsm_manager, 'command_sender') and self.truck_fsm_manager.command_sender:
            self.truck_fsm_manager.command_sender.set_tcp_server(tcp_server)
            print("[TCP 서버 참조 설정] 기존 command_sender에 tcp_server 참조가 설정되었습니다.")