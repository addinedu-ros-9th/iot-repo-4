#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
디스펜서 테스트 스크립트
- 디스펜서 하드웨어와 직접 통신하여 모든 기능 테스트
- 명령어 전송 및 응답 확인
- 인터액티브 메뉴 제공
"""

import time
import threading
import argparse
import os
import sys

# 백엔드 코드 사용을 위한 경로 설정
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # 프로젝트 루트 디렉토리
sys.path.append(project_root)  # 프로젝트 루트 디렉토리 추가

try:
    from backend.serialio.serial_interface import SerialInterface
    from backend.serialio.dispenser_controller import DispenserController
except ImportError:
    print("백엔드 모듈을 가져올 수 없습니다. 경로를 확인해주세요.")
    raise

# 테스트용 더미 FacilityStatusManager 및 CommandSender 클래스
class DummyCommandSender:
    def __init__(self):
        self.truck_status_manager = None
        
    def send(self, truck_id, command, payload=None):
        print(f"[▶️ 더미 명령 전송] 트럭: {truck_id}, 명령: {command}, 페이로드: {payload}")
        return True
        
    def set_truck_status_manager(self, truck_status_manager):
        self.truck_status_manager = truck_status_manager
        print(f"[✅ 더미 트럭 상태 관리자 설정] truck_status_manager 설정됨")

class DummyFacilityStatusManager:
    def __init__(self):
        self.command_sender = DummyCommandSender()
        
    def update_dispenser_status(self, dispenser_id, state, position, operation):
        print(f"[▶️ 더미 상태 업데이트] 디스펜서: {dispenser_id}, 상태: {state}, 위치: {position}, 작업: {operation}")
        return True

class DispenserTester:
    def __init__(self, port="/dev/ttyACM2", baudrate=9600, use_fake=False):
        """디스펜서 테스터 초기화"""
        self.port = port
      
        self.baudrate = baudrate
        self.use_fake = use_fake
        self.interface = None
        self.controller = None
        self.running = True
        self.message_listener = None
        self.current_truck_id = "TRUCK_01"  # 기본 트럭 ID
        self.dummy_facility_manager = DummyFacilityStatusManager()  # 더미 매니저

    def initialize(self):
        """디스펜서 연결 초기화"""
        try:
            print(f"[초기화] 디스펜서 연결 시도: {self.port}, 속도: {self.baudrate}")
            self.interface = SerialInterface(
                port=self.port,
                baudrate=self.baudrate,
                use_fake=self.use_fake,
                debug=True
            )
            
            # 컨트롤러 생성 - 더미 facility_status_manager 전달
            self.controller = DispenserController(
                self.interface, 
                facility_status_manager=self.dummy_facility_manager
            )
            
            # 현재 트럭 ID 설정
            self.controller.current_truck_id = self.current_truck_id
            print(f"[✅ 초기화 완료] 디스펜서 컨트롤러 준비됨 (트럭 ID: {self.current_truck_id})")
            
            # 메시지 리스너 시작
            self.start_message_listener()
            
            return True
        except Exception as e:
            print(f"[❌ 초기화 실패] 오류: {e}")
            return False

    def start_message_listener(self):
        """백그라운드에서 메시지 수신 처리"""
        def listener_thread():
            while self.running:
                try:
                    if self.interface and hasattr(self.interface.ser, 'in_waiting') and self.interface.ser.in_waiting > 0:
                        line = self.interface.ser.readline().decode().strip()
                        if line:
                            print(f"[📥 응답] {line}")
                            if self.controller:
                                self.controller.handle_message(line)
                except Exception as e:
                    print(f"[⚠️ 리스너 오류] {e}")
                time.sleep(0.1)
        
        self.message_listener = threading.Thread(target=listener_thread, daemon=True)
        self.message_listener.start()
        print("[✅ 메시지 리스너] 백그라운드 메시지 수신 시작")

    def send_raw_command(self, command):
        """원시 명령어 직접 전송"""
        try:
            if not self.interface:
                print("[❌ 오류] 인터페이스가 초기화되지 않았습니다.")
                return False
                
            print(f"[📤 명령 전송] {command}")
            self.interface.write(command)
            return True
        except Exception as e:
            print(f"[❌ 명령 전송 실패] {e}")
            return False

    def test_open(self):
        """디스펜서 열기 테스트"""
        if not self.controller:
            print("[❌ 오류] 컨트롤러가 초기화되지 않았습니다.")
            return False
            
        print("[🔍 테스트] 디스펜서 열기")
        return self.controller.open_dispenser("DISPENSER")

    def test_close(self):
        """디스펜서 닫기 테스트"""
        if not self.controller:
            print("[❌ 오류] 컨트롤러가 초기화되지 않았습니다.")
            return False
            
        print("[🔍 테스트] 디스펜서 닫기")
        return self.controller.close_dispenser("DISPENSER")

    def test_left_turn(self):
        """디스펜서 왼쪽 회전 테스트"""
        if not self.controller:
            print("[❌ 오류] 컨트롤러가 초기화되지 않았습니다.")
            return False
            
        print("[🔍 테스트] 디스펜서 왼쪽 회전")
        return self.controller.send_direction_command("DISPENSER", "LEFT_TURN")

    def test_right_turn(self):
        """디스펜서 오른쪽 회전 테스트"""
        if not self.controller:
            print("[❌ 오류] 컨트롤러가 초기화되지 않았습니다.")
            return False
            
        print("[🔍 테스트] 디스펜서 오른쪽 회전")
        return self.controller.send_direction_command("DISPENSER", "RIGHT_TURN")

    def test_stop_turn(self):
        """디스펜서 회전 정지 테스트"""
        if not self.controller:
            print("[❌ 오류] 컨트롤러가 초기화되지 않았습니다.")
            return False
            
        print("[🔍 테스트] 디스펜서 회전 정지")
        return self.controller.send_direction_command("DISPENSER", "STOP_TURN")

    def test_route_a(self):
        """디스펜서 A 경로 이동 테스트"""
        if not self.controller:
            print("[❌ 오류] 컨트롤러가 초기화되지 않았습니다.")
            return False
            
        print("[🔍 테스트] 디스펜서 A 경로 이동")
        return self.controller.move_to_route("DISPENSER", "ROUTE_A")

    def test_route_b(self):
        """디스펜서 B 경로 이동 테스트"""
        if not self.controller:
            print("[❌ 오류] 컨트롤러가 초기화되지 않았습니다.")
            return False
            
        print("[🔍 테스트] 디스펜서 B 경로 이동")
        return self.controller.move_to_route("DISPENSER", "ROUTE_B")

    def set_truck_id(self):
        """현재 사용 중인 트럭 ID 변경"""
        if not self.controller:
            print("[❌ 오류] 컨트롤러가 초기화되지 않았습니다.")
            return False
            
        try:
            new_truck_id = input("새 트럭 ID를 입력하세요 (예: TRUCK_01): ")
            if new_truck_id.strip():
                self.current_truck_id = new_truck_id
                self.controller.current_truck_id = new_truck_id
                print(f"[✅ 설정 완료] 트럭 ID가 {new_truck_id}로 변경되었습니다.")
                return True
            else:
                print("[❌ 오류] 유효한 트럭 ID를 입력해주세요.")
                return False
        except Exception as e:
            print(f"[❌ 설정 실패] {e}")
            return False

    def simulate_loaded(self):
        """LOADED 상태 시뮬레이션"""
        if not self.controller:
            print("[❌ 오류] 컨트롤러가 초기화되지 않았습니다.")
            return False
            
        try:
            print("[🔍 테스트] LOADED 상태 시뮬레이션")
            self.controller.handle_message("STATUS:DISPENSER:LOADED")
            return True
        except Exception as e:
            print(f"[❌ 시뮬레이션 실패] {e}")
            return False

    def print_status(self):
        """현재 디스펜서 상태 출력"""
        if not self.controller:
            print("[❌ 오류] 컨트롤러가 초기화되지 않았습니다.")
            return
            
        state = self.controller.dispenser_state.get("DISPENSER", "UNKNOWN")
        position = self.controller.dispenser_position.get("DISPENSER", "UNKNOWN")
        print(f"\n[📊 디스펜서 상태]")
        print(f"상태: {state}")
        print(f"위치: {position}")
        print(f"트럭 ID: {self.current_truck_id}")

    def display_menu(self):
        """메뉴 표시"""
        print("\n" + "="*50)
        print("디스펜서 테스트 메뉴")
        print("="*50)
        print("1. 디스펜서 열기")
        print("2. 디스펜서 닫기")
        print("3. 왼쪽으로 회전")
        print("4. 오른쪽으로 회전")
        print("5. 회전 정지")
        print("6. A 경로로 이동")
        print("7. B 경로로 이동")
        print("8. 상태 확인")
        print("9. 원시 명령어 보내기")
        print("b. LOADED 상태 시뮬레이션")
        print("0. 종료")
        print("="*50)

    def run(self):
        """메인 테스트 루프"""
        if not self.initialize():
            print("[❌ 종료] 초기화에 실패했습니다.")
            return
        
        print("[✅ 테스트 시작] 디스펜서 테스트를 시작합니다.")
        
        while self.running:
            self.display_menu()
            choice = input("선택하세요 (0-9 또는 a-b): ")
            
            if choice == '0':
                self.running = False
                print("[👋 종료] 테스트를 종료합니다.")
                break
            elif choice == '1':
                self.test_open()
            elif choice == '2':
                self.test_close()
            elif choice == '3':
                self.test_left_turn()
            elif choice == '4':
                self.test_right_turn()
            elif choice == '5':
                self.test_stop_turn()
            elif choice == '6':
                self.test_route_a()
            elif choice == '7':
                self.test_route_b()
            elif choice == '8':
                self.print_status()
            elif choice == '9':
                cmd = input("원시 명령어 입력 (예: DISPENSER_DI_OPEN): ")
                self.send_raw_command(cmd)
            elif choice.lower() == 'a':
                self.set_truck_id()
            elif choice.lower() == 'b':
                self.simulate_loaded()
            else:
                print("[❌ 오류] 잘못된 선택입니다.")
            
            # 상태 변화 대기
            time.sleep(0.5)

    def close(self):
        """리소스 정리"""
        self.running = False
        
        if self.message_listener and self.message_listener.is_alive():
            self.message_listener.join(timeout=1)
            
        if self.interface:
            self.interface.close()
            
        print("[✅ 종료] 모든 리소스가 정리되었습니다.")

def parse_arguments():
    """명령줄 인자 파싱"""
    parser = argparse.ArgumentParser(description='디스펜서 테스트 스크립트')
    parser.add_argument('--port', type=str, default='/dev/ttyACM2',
                        help='시리얼 포트 (기본값: /dev/ttyACM2)')
    parser.add_argument('--baudrate', type=int, default=9600,
                        help='전송 속도 (기본값: 9600)')
    parser.add_argument('--fake', action='store_true',
                        help='가상 시리얼 인터페이스 사용 (테스트용)')
    parser.add_argument('--truck-id', type=str, default='TRUCK_01',
                        help='트럭 ID (기본값: TRUCK_01)')
    return parser.parse_args()

def main():
    """메인 함수"""
    args = parse_arguments()
    
    tester = DispenserTester(
        port=args.port,
        baudrate=args.baudrate,
        use_fake=args.fake
    )
    
    # 트럭 ID 설정
    tester.current_truck_id = args.truck_id
    
    try:
        tester.run()
    except KeyboardInterrupt:
        print("\n[👋 종료] 사용자에 의해 테스트가 중단되었습니다.")
    finally:
        tester.close()

if __name__ == "__main__":
    main() 