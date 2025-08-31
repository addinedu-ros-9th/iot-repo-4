from flask import Blueprint, jsonify, request
from backend.tcpio.tcp_server import TCPServer

system_api = Blueprint('system_api', __name__)

# TCP 서버 인스턴스를 저장할 전역 변수
tcp_server_instance = None

def set_tcp_server_instance(server_instance):
    """TCP 서버 인스턴스를 설정하는 함수"""
    global tcp_server_instance
    tcp_server_instance = server_instance
    print("[INFO] system_api에 TCP 서버 인스턴스가 설정되었습니다.")

@system_api.route('/connections', methods=['GET'])
def get_connections():
    """현재 연결된 클라이언트 목록 반환"""
    if tcp_server_instance:
        clients = tcp_server_instance.get_connected_clients()
        return jsonify(clients)
    return jsonify({"error": "TCP server not initialized"}), 500

@system_api.route('/send', methods=['POST'])
def send_message():
    """특정 클라이언트에게 메시지 전송"""
    data = request.json
    client_id = data.get('client_id')
    message = data.get('message')
    
    if not client_id or not message:
        return jsonify({"error": "client_id and message are required"}), 400

    if tcp_server_instance:
        success = tcp_server_instance.send_to_client(client_id, message)
        if success:
            return jsonify({"status": "Message sent"})
        else:
            return jsonify({"error": "Client not found or connection closed"}), 404
    
    return jsonify({"error": "TCP server not initialized"}), 500