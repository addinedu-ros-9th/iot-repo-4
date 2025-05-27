import unittest
import time
import sys
import os

# 현재 스크립트의 디렉토리를 기준으로 상위 경로를 모듈 검색 경로에 추가
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.serialio.fake_serial import FakeSerial
from backend.serialio.serial_interface import SerialInterface
from backend.serialio.gate_controller import GateController

class GateTest(unittest.TestCase):
    """게이트 제어 시스템 테스트 클래스"""

    def setUp(self):
        """각 테스트 전에 실행되는 설정 메서드"""
        # 가상 시리얼 인터페이스 생성 (디버그 모드 활성화)
        self.fake_serial = FakeSerial(name="TEST_SERIAL", debug=True)
        self.serial_interface = SerialInterface(port="TEST_PORT", baudrate=9600, use_fake=True, debug=True)
        self.serial_interface.ser = self.fake_serial  # 가짜 시리얼 객체 직접 할당
        
        # 게이트 컨트롤러 생성
        self.gate_controller = GateController(self.serial_interface)

    def tearDown(self):
        """각 테스트 후에 실행되는 정리 메서드"""
        # 시리얼 인터페이스 종료
        if hasattr(self.fake_serial, 'close'):
            self.fake_serial.close()
        if hasattr(self.serial_interface, 'close'):
            self.serial_interface.close()

    def test_gate_a_open_close(self):
        """게이트 A 열기/닫기 테스트"""
        print("\n==== 게이트 A 열기/닫기 테스트 ====")
        
        # 게이트 A 초기 상태 확인
        self.assertEqual(self.gate_controller.gate_states["GATE_A"], "CLOSED")
        
        # 게이트 A 열기
        print("게이트 A 열기 명령 전송")
        result = self.gate_controller.open_gate("GATE_A")
        self.assertTrue(result, "게이트 A 열기 명령이 실패했습니다.")
        self.assertEqual(self.gate_controller.gate_states["GATE_A"], "OPENED")
        
        # 잠시 대기
        time.sleep(1)
        
        # 게이트 A 닫기
        print("게이트 A 닫기 명령 전송")
        result = self.gate_controller.close_gate("GATE_A")
        self.assertTrue(result, "게이트 A 닫기 명령이 실패했습니다.")
        self.assertEqual(self.gate_controller.gate_states["GATE_A"], "CLOSED")

    def test_gate_b_open_close(self):
        """게이트 B 열기/닫기 테스트"""
        print("\n==== 게이트 B 열기/닫기 테스트 ====")
        
        # 게이트 B 초기 상태 확인
        self.assertEqual(self.gate_controller.gate_states["GATE_B"], "CLOSED")
        
        # 게이트 B 열기
        print("게이트 B 열기 명령 전송")
        result = self.gate_controller.open_gate("GATE_B")
        self.assertTrue(result, "게이트 B 열기 명령이 실패했습니다.")
        self.assertEqual(self.gate_controller.gate_states["GATE_B"], "OPENED")
        
        # 잠시 대기
        time.sleep(1)
        
        # 게이트 B 닫기
        print("게이트 B 닫기 명령 전송")
        result = self.gate_controller.close_gate("GATE_B")
        self.assertTrue(result, "게이트 B 닫기 명령이 실패했습니다.")
        self.assertEqual(self.gate_controller.gate_states["GATE_B"], "CLOSED")

    def test_sequential_operations(self):
        """게이트 A와 B를 순차적으로 제어하는 테스트"""
        print("\n==== 게이트 순차 제어 테스트 ====")
        
        # 게이트 A 열기
        print("1. 게이트 A 열기")
        result = self.gate_controller.open_gate("GATE_A")
        self.assertTrue(result)
        self.assertEqual(self.gate_controller.gate_states["GATE_A"], "OPENED")
        
        # 잠시 대기
        time.sleep(0.5)
        
        # 게이트 B 열기
        print("2. 게이트 B 열기")
        result = self.gate_controller.open_gate("GATE_B")
        self.assertTrue(result)
        self.assertEqual(self.gate_controller.gate_states["GATE_B"], "OPENED")
        
        # 잠시 대기
        time.sleep(0.5)
        
        # 게이트 B 닫기
        print("3. 게이트 B 닫기")
        result = self.gate_controller.close_gate("GATE_B")
        self.assertTrue(result)
        self.assertEqual(self.gate_controller.gate_states["GATE_B"], "CLOSED")
        
        # 잠시 대기
        time.sleep(0.5)
        
        # 게이트 A 닫기
        print("4. 게이트 A 닫기")
        result = self.gate_controller.close_gate("GATE_A")
        self.assertTrue(result)
        self.assertEqual(self.gate_controller.gate_states["GATE_A"], "CLOSED")

    def test_error_handling(self):
        """오류 처리 테스트"""
        print("\n==== 오류 처리 테스트 ====")
        
        # 잘못된 게이트 ID로 명령 시도
        print("잘못된 게이트 ID로 열기 명령 시도")
        result = self.gate_controller.open_gate("GATE_X")
        self.assertFalse(result, "잘못된 게이트 ID로 명령을 보냈는데 성공했습니다.")
        
        # 이미 열린 게이트를 열기 시도
        print("게이트 A 열기")
        self.gate_controller.open_gate("GATE_A")
        print("이미 열린 게이트 A를 다시 열기 시도")
        result = self.gate_controller.open_gate("GATE_A")
        self.assertTrue(result, "이미 열린 게이트에 대한 중복 명령이 실패했습니다.")
        
        # 이미 닫힌 게이트를 닫기 시도
        print("게이트 A 닫기")
        self.gate_controller.close_gate("GATE_A")
        print("이미 닫힌 게이트 A를 다시 닫기 시도")
        result = self.gate_controller.close_gate("GATE_A")
        self.assertTrue(result, "이미 닫힌 게이트에 대한 중복 명령이 실패했습니다.")

if __name__ == "__main__":
    unittest.main() 