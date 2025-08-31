import socket
import threading
from .protocol import dust_proto_req, dust_proto_res

class TCPServer:
    def __init__(self, host, port, main_controller=None):
        self.host = host
        self.port = port
        self.main_controller = main_controller
        self.clients = {}
        self.server_socket = None
        self.running = False
        self.lock = threading.Lock()

    def start(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        print(f"[TCP 서버] {self.host}:{self.port}에서 시작됨")

        thread = threading.Thread(target=self.accept_clients, daemon=True)
        thread.start()

    def accept_clients(self):
        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                print(f"[클라이언트 연결] {addr}에서 새로운 클라이언트가 연결되었습니다.")
                # 클라이언트 ID는 주소와 포트로 임시 지정
                client_id = f"{addr[0]}:{addr[1]}"
                
                with self.lock:
                    self.clients[client_id] = client_socket
                
                # MainController에 트럭 소켓 맵 업데이트 알림
                if self.main_controller:
                    self.main_controller.set_truck_commander(self.get_truck_sockets())
                
                thread = threading.Thread(target=self.handle_client, args=(client_socket, client_id), daemon=True)
                thread.start()
            except OSError:
                break

    def handle_client(self, client_socket, client_id):
        while self.running:
            try:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                # 데이터 처리 로직
                self.process_data(data, client_id)

            except ConnectionResetError:
                print(f"[연결 오류] {client_id}와 연결이 초기화되었습니다.")
                break
            except Exception as e:
                print(f"[오류] 클라이언트 {client_id} 처리 중 오류: {e}")
                break
        
        self.remove_client(client_id)

    def process_data(self, data, client_id):
        # 프로토콜 처리
        header, payload = dust_proto_req.unpack(data)
        sender, receiver, cmd, _ = header
        
        # 클라이언트 ID 업데이트 (최초 메시지 수신 시)
        if client_id.startswith("192.168"): # 임시 ID인 경우
            new_client_id = f"TRUCK_{sender:02d}"
            with self.lock:
                if client_id in self.clients:
                    socket = self.clients.pop(client_id)
                    self.clients[new_client_id] = socket
                    client_id = new_client_id
            
            # MainController에 트럭 소켓 맵 업데이트 알림
            if self.main_controller:
                self.main_controller.set_truck_commander(self.get_truck_sockets())

        # MainController로 메시지 전달
        if self.main_controller:
            msg = {
                "sender": f"TRUCK_{sender:02d}",
                "cmd": cmd,
                "payload": payload
            }
            self.main_controller.handle_message(msg)

    def send_to_client(self, client_id, command, payload=None):
        with self.lock:
            client_socket = self.clients.get(client_id)
        
        if client_socket:
            try:
                # DUST 프로토콜에 따라 패킹
                packed_data = dust_proto_res.pack(command, payload or {})
                client_socket.sendall(packed_data)
                return True
            except socket.error as e:
                print(f"[전송 오류] {client_id}에 메시지 전송 실패: {e}")
                self.remove_client(client_id)
                return False
        return False

    def remove_client(self, client_id):
        with self.lock:
            if client_id in self.clients:
                self.clients.pop(client_id)
                print(f"[클라이언트 연결 종료] {client_id} 연결이 종료되었습니다.")
                # MainController에 트럭 소켓 맵 업데이트 알림
                if self.main_controller:
                    self.main_controller.set_truck_commander(self.get_truck_sockets())

    def stop(self):
        self.running = False
        with self.lock:
            for sock in self.clients.values():
                sock.close()
        if self.server_socket:
            self.server_socket.close()
        print("[TCP 서버] 서버가 종료되었습니다.")

    def get_connected_clients(self):
        with self.lock:
            return list(self.clients.keys())

    def get_truck_sockets(self):
        """TRUCK으로 시작하는 ID를 가진 소켓만 반환"""
        with self.lock:
            return {k: v for k, v in self.clients.items() if k.startswith("TRUCK")}