#!/usr/bin/env python3
import serial
import time
import sys
import argparse

class GateArduinoTest:
    """
    아두이노 게이트 제어를 테스트하기 위한 클래스입니다.
    이 테스트는 실제 시리얼 포트를 사용하여 아두이노와 통신합니다.
    """
    
    def __init__(self, port="/dev/ttyACM0", baudrate=9600):
        """
        테스트 초기화
        
        Args:
            port (str): 시리얼 포트 경로
            baudrate (int): 통신 속도
        """
        self.port = port
        self.baudrate = baudrate
        self.ser = None
        self.connected = False
        
    def connect(self):
        """시리얼 포트에 연결합니다."""
        try:
            print(f"[시리얼 연결] 포트: {self.port}, 속도: {self.baudrate}...")
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            time.sleep(2)  # 아두이노 재설정을 위한 대기 시간
            self.connected = True
            print("[시리얼 연결 성공]")
            return True
        except Exception as e:
            print(f"[시리얼 연결 실패] {e}")
            return False
            
    def disconnect(self):
        """시리얼 포트 연결을 종료합니다."""
        if self.ser:
            self.ser.close()
            print("[시리얼 연결 종료]")
            self.connected = False
            
    def send_command(self, command):
        """
        명령을 아두이노로 전송합니다.
        
        Args:
            command (str): 전송할 명령
        """
        if not self.connected:
            print("[오류] 시리얼 포트에 연결되어 있지 않습니다.")
            return False
            
        try:
            print(f"[명령 전송] {command}")
            self.ser.write(f"{command}\n".encode())
            return True
        except Exception as e:
            print(f"[명령 전송 실패] {e}")
            return False
            
    def read_response(self, timeout=5, max_responses=10):
        """
        아두이노로부터 응답을 읽습니다.
        
        Args:
            timeout (int): 응답 대기 시간(초)
            max_responses (int): 읽을 최대 응답 수
            
        Returns:
            list: 수신된 응답 목록
        """
        if not self.connected:
            print("[오류] 시리얼 포트에 연결되어 있지 않습니다.")
            return []
            
        responses = []
        start_time = time.time()
        
        while time.time() - start_time < timeout and len(responses) < max_responses:
            if self.ser.in_waiting > 0:
                try:
                    line = self.ser.readline().decode().strip()
                    if line:
                        print(f"[응답 수신] {line}")
                        responses.append(line)
                except Exception as e:
                    print(f"[응답 읽기 실패] {e}")
            else:
                time.sleep(0.1)  # CPU 사용량 감소
                
        return responses
        
    def test_gate_a_open(self):
        """게이트 A 열기 테스트"""
        print("\n==== 게이트 A 열기 테스트 ====")
        self.send_command("GATE_A_OPEN")
        responses = self.read_response(timeout=2)
        if responses:
            return "OPENED" in " ".join(responses)
        return False
        
    def test_gate_a_close(self):
        """게이트 A 닫기 테스트"""
        print("\n==== 게이트 A 닫기 테스트 ====")
        self.send_command("GATE_A_CLOSE")
        responses = self.read_response(timeout=2)
        if responses:
            return "CLOSED" in " ".join(responses)
        return False
        
    def test_gate_b_open(self):
        """게이트 B 열기 테스트"""
        print("\n==== 게이트 B 열기 테스트 ====")
        self.send_command("GATE_B_OPEN")
        responses = self.read_response(timeout=2)
        if responses:
            return "OPENED" in " ".join(responses)
        return False
        
    def test_gate_b_close(self):
        """게이트 B 닫기 테스트"""
        print("\n==== 게이트 B 닫기 테스트 ====")
        self.send_command("GATE_B_CLOSE")
        responses = self.read_response(timeout=2)
        if responses:
            return "CLOSED" in " ".join(responses)
        return False
        
    def test_status_query(self):
        """상태 조회 테스트"""
        print("\n==== 상태 조회 테스트 ====")
        self.send_command("STATUS")
        responses = self.read_response(timeout=2)
        if responses:
            return "STATUS:GATE_A" in " ".join(responses) and "STATUS:GATE_B" in " ".join(responses)
        return False
        
    def test_sequential_operations(self):
        """순차적 작동 테스트"""
        print("\n==== 순차적 작동 테스트 ====")
        
        # 게이트 A 열기
        print("1. 게이트 A 열기")
        self.send_command("GATE_A_OPEN")
        responses = self.read_response(timeout=2)
        success_a_open = "OPENED" in " ".join(responses)
        
        # 게이트 B 열기
        print("2. 게이트 B 열기")
        self.send_command("GATE_B_OPEN")
        responses = self.read_response(timeout=2)
        success_b_open = "OPENED" in " ".join(responses)
        
        # 게이트 B 닫기
        print("3. 게이트 B 닫기")
        self.send_command("GATE_B_CLOSE")
        responses = self.read_response(timeout=2)
        success_b_close = "CLOSED" in " ".join(responses)
        
        # 게이트 A 닫기
        print("4. 게이트 A 닫기")
        self.send_command("GATE_A_CLOSE")
        responses = self.read_response(timeout=2)
        success_a_close = "CLOSED" in " ".join(responses)
        
        return success_a_open and success_b_open and success_b_close and success_a_close
        
    def run_all_tests(self):
        """모든 테스트를 실행합니다."""
        if not self.connect():
            print("[테스트 중단] 시리얼 연결 실패")
            return
            
        try:
            print("\n==== 아두이노 게이트 테스트 시작 ====")
            
            # 초기 상태 확인
            print("\n기본 상태 확인 중...")
            self.send_command("STATUS")
            responses = self.read_response(timeout=2)
            print(f"현재 상태: {responses}")
            
            # 게이트 A 테스트
            print("\n게이트 A 테스트 중...")
            a_open_success = self.test_gate_a_open()
            time.sleep(1)
            a_close_success = self.test_gate_a_close()
            
            # 게이트 B 테스트
            print("\n게이트 B 테스트 중...")
            b_open_success = self.test_gate_b_open()
            time.sleep(1)
            b_close_success = self.test_gate_b_close()
            
            # 순차 테스트
            print("\n순차 테스트 중...")
            sequential_success = self.test_sequential_operations()
            
            # 상태 조회 테스트
            print("\n상태 조회 테스트 중...")
            status_success = self.test_status_query()
            
            # 테스트 결과 출력
            print("\n==== 테스트 결과 ====")
            print(f"게이트 A 열기: {'성공' if a_open_success else '실패'}")
            print(f"게이트 A 닫기: {'성공' if a_close_success else '실패'}")
            print(f"게이트 B 열기: {'성공' if b_open_success else '실패'}")
            print(f"게이트 B 닫기: {'성공' if b_close_success else '실패'}")
            print(f"순차 테스트: {'성공' if sequential_success else '실패'}")
            print(f"상태 조회: {'성공' if status_success else '실패'}")
            
            all_success = all([a_open_success, a_close_success, b_open_success, b_close_success, sequential_success, status_success])
            print(f"\n종합 결과: {'모든 테스트 성공!' if all_success else '일부 테스트 실패'}")
            
        finally:
            self.disconnect()

def main():
    parser = argparse.ArgumentParser(description="아두이노 게이트 제어 테스트")
    parser.add_argument("--port", type=str, default="/dev/ttyACM0", help="시리얼 포트 (기본값: /dev/ttyACM0)")
    parser.add_argument("--baudrate", type=int, default=9600, help="통신 속도 (기본값: 9600)")
    args = parser.parse_args()
    
    tester = GateArduinoTest(port=args.port, baudrate=args.baudrate)
    tester.run_all_tests()

if __name__ == "__main__":
    main() 