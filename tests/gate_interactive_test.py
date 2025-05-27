#!/usr/bin/env python3
"""
게이트 제어 대화형 테스트 스크립트
사용자가 키보드 입력으로 게이트를 직접 제어할 수 있는 프로그램
"""

import serial
import time
import sys
import argparse
import os

# ANSI 색상 코드
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class GateInteractiveTest:
    """게이트 제어 대화형 테스트 클래스"""
    
    def __init__(self, port="/dev/ttyACM0", baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.connected = False
        self.exit_flag = False
        
        # 게이트 상태 추적
        self.gates = {
            "GATE_A": "CLOSED",
            "GATE_B": "CLOSED"
        }
    
    def connect(self):
        """시리얼 포트에 연결"""
        try:
            print(f"{Colors.YELLOW}[시리얼 연결] 포트: {self.port}, 속도: {self.baudrate}...{Colors.ENDC}")
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # 아두이노 재설정 대기
            self.connected = True
            print(f"{Colors.GREEN}[시리얼 연결 성공]{Colors.ENDC}")
            return True
        except Exception as e:
            print(f"{Colors.RED}[시리얼 연결 실패] {e}{Colors.ENDC}")
            return False
    
    def disconnect(self):
        """시리얼 포트 연결 종료"""
        if self.ser:
            self.ser.close()
            print(f"{Colors.YELLOW}[시리얼 연결 종료]{Colors.ENDC}")
            self.connected = False
    
    def send_command(self, command):
        """명령 전송"""
        if not self.connected:
            print(f"{Colors.RED}[오류] 시리얼 포트에 연결되어 있지 않습니다.{Colors.ENDC}")
            return False
        
        try:
            print(f"{Colors.BLUE}[명령 전송] {command}{Colors.ENDC}")
            self.ser.write(f"{command}\n".encode())
            return True
        except Exception as e:
            print(f"{Colors.RED}[명령 전송 실패] {e}{Colors.ENDC}")
            return False
    
    def read_responses(self, timeout=2):
        """응답 읽기"""
        if not self.connected:
            return []
        
        responses = []
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode().strip()
                    if line:
                        if line.startswith("STATUS:GATE_"):
                            parts = line.split(":")
                            if len(parts) >= 3:
                                gate_id = parts[1]
                                state = parts[2]
                                self.gates[gate_id] = state
                                print(f"{Colors.CYAN}[상태 업데이트] {gate_id}: {state}{Colors.ENDC}")
                        else:
                            print(f"{Colors.GREEN}[응답 수신] {line}{Colors.ENDC}")
                        responses.append(line)
                except Exception as e:
                    print(f"{Colors.RED}[응답 읽기 실패] {e}{Colors.ENDC}")
            else:
                time.sleep(0.1)
        
        return responses
    
    def show_status(self):
        """현재 게이트 상태 표시"""
        self.send_command("STATUS")
        responses = self.read_responses()
        
        print("\n" + "=" * 40)
        print(f"{Colors.BOLD}현재 게이트 상태:{Colors.ENDC}")
        print("-" * 40)
        
        for gate, state in self.gates.items():
            color = Colors.GREEN if state == "OPENED" else Colors.RED
            print(f"{gate}: {color}{state}{Colors.ENDC}")
        
        print("=" * 40 + "\n")
    
    def show_help(self):
        """도움말 표시"""
        print("\n" + "=" * 50)
        print(f"{Colors.BOLD}{Colors.HEADER}게이트 제어 대화형 테스트 도움말{Colors.ENDC}")
        print("-" * 50)
        print(f"{Colors.BOLD}1{Colors.ENDC} - 게이트 A 열기")
        print(f"{Colors.BOLD}2{Colors.ENDC} - 게이트 A 닫기")
        print(f"{Colors.BOLD}3{Colors.ENDC} - 게이트 B 열기")
        print(f"{Colors.BOLD}4{Colors.ENDC} - 게이트 B 닫기")
        print(f"{Colors.BOLD}s{Colors.ENDC} - 상태 확인")
        print(f"{Colors.BOLD}t{Colors.ENDC} - 자가 테스트 실행")
        print(f"{Colors.BOLD}h{Colors.ENDC} - 도움말 표시")
        print(f"{Colors.BOLD}q{Colors.ENDC} - 종료")
        print("=" * 50 + "\n")
    
    def process_command(self, key):
        """키 입력 처리"""
        if key == '1':
            self.send_command("GATE_A_OPEN")
            self.read_responses()
        elif key == '2':
            self.send_command("GATE_A_CLOSE")
            self.read_responses()
        elif key == '3':
            self.send_command("GATE_B_OPEN")
            self.read_responses()
        elif key == '4':
            self.send_command("GATE_B_CLOSE")
            self.read_responses()
        elif key == 's':
            self.show_status()
        elif key == 't':
            self.send_command("SELF_TEST")
            self.read_responses(timeout=10)  # 테스트는 시간이 더 걸림
        elif key == 'h':
            self.show_help()
        elif key == 'q':
            print(f"{Colors.YELLOW}종료합니다...{Colors.ENDC}")
            self.exit_flag = True
        else:
            print(f"{Colors.YELLOW}알 수 없는 명령입니다. 'h'를 입력하여 도움말을 확인하세요.{Colors.ENDC}")
    
    def run(self):
        """대화형 테스트 실행"""
        if not self.connect():
            print(f"{Colors.RED}[오류] 시리얼 연결에 실패했습니다.{Colors.ENDC}")
            return
        
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f"{Colors.BOLD}{Colors.HEADER}게이트 제어 대화형 테스트{Colors.ENDC}")
            print(f"{Colors.CYAN}포트: {self.port}, 속도: {self.baudrate}{Colors.ENDC}")
            self.show_help()
            
            # 초기 상태 확인
            self.show_status()
            
            # 메인 루프
            while not self.exit_flag:
                key = input(f"{Colors.BOLD}명령 입력> {Colors.ENDC}").lower()
                self.process_command(key)
                
                # 응답 처리 (명령이 없어도 응답을 읽음)
                if self.ser and self.ser.in_waiting > 0:
                    self.read_responses(timeout=0.5)
            
        except KeyboardInterrupt:
            print(f"\n{Colors.YELLOW}사용자에 의해 중단되었습니다.{Colors.ENDC}")
        finally:
            self.disconnect()

def main():
    parser = argparse.ArgumentParser(description="게이트 제어 대화형 테스트")
    parser.add_argument("--port", type=str, default="/dev/ttyACM0", help="시리얼 포트 (기본값: /dev/ttyACM0)")
    parser.add_argument("--baudrate", type=int, default=9600, help="통신 속도 (기본값: 9600)")
    args = parser.parse_args()
    
    tester = GateInteractiveTest(port=args.port, baudrate=args.baudrate)
    tester.run()

if __name__ == "__main__":
    main() 