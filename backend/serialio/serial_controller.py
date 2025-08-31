import serial
import threading
import time

class SerialController:
    def __init__(self, port, baudrate, debug=False, facility_status_manager=None):
        self.port = port
        self.baudrate = baudrate
        self.debug = debug
        self.facility_status_manager = facility_status_manager
        self.ser = None
        self.thread = None
        self.running = False
        self.lock = threading.Lock()
        
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self.running = True
            self.thread = threading.Thread(target=self.read_from_port, daemon=True)
            self.thread.start()
            print(f"[시리얼] {self.port}에 연결되었습니다.")
        except serial.SerialException as e:
            print(f"[시리얼 오류] {self.port}: {e}")
            self.ser = None

    def read_from_port(self):
        while self.running and self.ser:
            try:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        if self.debug:
                            print(f"[시리얼 수신] {self.port}: {line}")
                        # 여기서 facility_status_manager를 통해 상태 업데이트
                        if self.facility_status_manager:
                            self.facility_status_manager.update_facility_status(line)
            except serial.SerialException as e:
                print(f"[시리얼 오류] {self.port}에서 읽는 중 오류: {e}")
                self.running = False
            except Exception as e:
                print(f"[오류] {self.port} 처리 중 예외: {e}")
            time.sleep(0.1)

    def send_command(self, device_id, command):
        if self.ser and self.ser.is_open:
            with self.lock:
                try:
                    full_command = f"{command}\n"
                    self.ser.write(full_command.encode('utf-8'))
                    if self.debug:
                        print(f"[시리얼 송신] {self.port} -> {device_id}: {command}")
                    return True
                except serial.SerialException as e:
                    print(f"[시리얼 오류] {self.port}에 쓰는 중 오류: {e}")
                    return False
        else:
            print(f"[경고] {self.port} 포트가 열려있지 않습니다.")
            return False

    def close(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
        if self.ser and self.ser.is_open:
            self.ser.close()
            print(f"[시리얼] {self.port} 연결이 종료되었습니다.")
