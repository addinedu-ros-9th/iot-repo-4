from .protocol import dust_proto_res

class TruckCommandSender:
    def __init__(self, truck_socket_map):
        self.truck_sockets = truck_socket_map
        self.tcp_server = None
        self.truck_status_manager = None

    def set_tcp_server(self, tcp_server):
        self.tcp_server = tcp_server

    def set_truck_status_manager(self, truck_status_manager):
        self.truck_status_manager = truck_status_manager

    def send(self, truck_id, command, payload=None):
        if self.tcp_server:
            print(f"[명령 전송] Truck: {truck_id}, Command: {command}, Payload: {payload}")
            # 상태 DB 업데이트
            if self.truck_status_manager:
                self.truck_status_manager.update_truck_command(truck_id, command, payload)
            
            # TCP 서버를 통해 전송
            return self.tcp_server.send_to_client(truck_id, command, payload)
        else:
            print(f"[경고] TCP 서버가 설정되지 않아 명령을 보낼 수 없습니다.")
            return False