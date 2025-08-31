import socket
import threading
import time

class TCPClient:
    def __init__(self, host, port, on_message_received=None, on_disconnected=None, client_id=None):
        self.host = host
        self.port = port
        self.on_message_received = on_message_received
        self.on_disconnected = on_disconnected
        self.client_id = client_id
        self.sock = None
        self.running = False
        self.thread = None

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.running = True
            self.thread = threading.Thread(target=self.receive_loop, daemon=True)
            self.thread.start()
            print(f"[TCP 클라이언트] {self.host}:{self.port}에 연결되었습니다.")
            return True
        except socket.error as e:
            print(f"[연결 오류] {e}")
            return False

    def receive_loop(self):
        while self.running:
            try:
                data = self.sock.recv(1024)
                if data:
                    if self.on_message_received:
                        self.on_message_received(self.client_id, data)
                else:
                    # 연결이 끊어진 경우
                    self.disconnect()
                    break
            except socket.error as e:
                print(f"[수신 오류] {e}")
                self.disconnect()
                break

    def send(self, message):
        if self.sock and self.running:
            try:
                self.sock.sendall(message)
                return True
            except socket.error as e:
                print(f"[전송 오류] {e}")
                return False
        return False

    def disconnect(self):
        if self.running:
            self.running = False
            if self.sock:
                self.sock.close()
                self.sock = None
            if self.on_disconnected:
                self.on_disconnected(self.client_id)
            print(f"[연결 종료] {self.host}:{self.port} 연결이 종료되었습니다.")
