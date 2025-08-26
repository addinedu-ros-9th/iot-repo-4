import threading
import time
from typing import Optional

class SerialController:
    """
    시리얼 장치와의 통신을 제어하는 기본 클래스입니다.
    명령 전송, 비동기 메시지 폴링, 안정적인 통신을 위한 재시도 로직을 포함합니다.
    """
    def __init__(self, serial_interface):
        self.interface = serial_interface
        self.running = False
        self.polling_thread: Optional[threading.Thread] = None

    def start_polling(self):
        """백그라운드에서 시리얼 포트를 주기적으로 확인하는 폴링 스레드를 시작합니다."""
        if self.polling_thread and self.polling_thread.is_alive():
            print(f"[{self.__class__.__name__}] 이미 폴링 스레드가 실행 중입니다.")
            return
        
        self.running = True
        self.polling_thread = threading.Thread(target=self._poll_serial_loop, daemon=True)
        self.polling_thread.start()
        print(f"[{self.__class__.__name__}] 시리얼 폴링을 시작합니다.")

    def stop_polling(self):
        """실행 중인 폴링 스레드를 중지합니다."""
        if not self.running:
            return
            
        self.running = False
        if self.polling_thread:
            self.polling_thread.join(timeout=1)
        print(f"[{self.__class__.__name__}] 시리얼 폴링을 중지했습니다.")

    def _poll_serial_loop(self):
        """
        폴링 스레드의 메인 루프.
        지속적으로 시리얼 응답을 확인하고, 메시지가 있으면 handle_message를 호출합니다.
        """
        device_name = self.__class__.__name__
        print(f"[{device_name}] 폴링 루프 시작.")
        while self.running:
            try:
                # 장치로부터 비동기적으로 들어오는 메시지를 확인 (타임아웃을 짧게 설정)
                line = self.interface.read_response(timeout=0.5)
                if line:
                    self.handle_message(line)
            except Exception as e:
                print(f"[{device_name}] 폴링 중 오류 발생: {e}")
            time.sleep(0.05)  # CPU 사용량 조절
        print(f"[{device_name}] 폴링 루프 종료.")

    def handle_message(self, message: str):
        """
        폴링 루프에서 수신된 메시지를 처리하는 메서드입니다.
        자식 클래스에서 각 장치에 맞게 반드시 재정의해야 합니다.
        """
        raise NotImplementedError("자식 클래스에서 이 메서드를 구현해야 합니다.")

    def send_command_and_wait_ack(self, target: str, action: str, retries: int = 3, timeout: float = 2.0) -> bool:
        """
        명령을 전송하고, 지정된 시간 동안 ACK(응답)를 기다립니다.
        응답이 없으면 지정된 횟수만큼 재시도합니다.

        Args:
            target (str): 명령 대상 (예: "GATE_A")
            action (str): 수행할 동작 (예: "OPEN")
            retries (int): 재시도 횟수
            timeout (float): 각 시도에 대한 응답 대기 시간 (초)

        Returns:
            bool: ACK 수신 성공 시 True, 아니면 False
        """
        command_str = f"{target.upper()}_{action.upper()}"
        
        for attempt in range(retries):
            print(f"[{self.__class__.__name__}] 명령 전송 ({attempt + 1}/{retries}): {command_str}")
            try:
                # 1. 명령 전송
                self.interface.send_command(target, action)
                
                # 2. ACK 대기
                # ACK 형식은 'ACK:명령어' 또는 'ACK:명령어:결과'를 기대합니다.
                response = self.interface.read_response(timeout=timeout)
                
                # 3. ACK 확인
                if response and "ACK" in response and command_str in response:
                    print(f"[{self.__class__.__name__}] 명령 성공 (ACK 수신): {response}")
                    return True
                elif response:
                    print(f"[{self.__class__.__name__}] 예상치 못한 응답 수신: {response}")
                    # 예상치 못한 응답이라도 일단 수신은 되었으므로, 폴링 핸들러에 처리를 위임할 수 있습니다.
                    self.handle_message(response)
                else:
                    print(f"[{self.__class__.__name__}] 응답 시간 초과 ({timeout}초)")

            except Exception as e:
                print(f"[{self.__class__.__name__}] 명령 전송 중 오류 발생: {e}")

            # 재시도 전 잠시 대기
            time.sleep(0.5)

        print(f"[{self.__class__.__name__}] 명령 실패: {command_str} (총 {retries}회 시도)")
        return False

    def send_command(self, target: str, action: str):
        """
        단순히 명령을 전송하고 응답을 기다리지 않습니다. (Fire and Forget)
        ACK 확인이 필요 없는 경우에 사용합니다.
        """
        try:
            self.interface.send_command(target, action)
        except Exception as e:
            print(f"[{self.__class__.__name__}] 단순 명령 전송 오류: {e}")

    def close(self):
        """컨트롤러와 시리얼 인터페이스를 안전하게 종료합니다."""
        self.stop_polling()
        if hasattr(self.interface, 'close'):
            self.interface.close()
        print(f"[{self.__class__.__name__}] 종료됨")