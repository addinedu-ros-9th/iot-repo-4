from .serial_controller import SerialController
from .belt_controller import BeltController
from .gate_controller import GateController
from .dispenser_controller import DispenserController
from .fake_serial import FakeSerial

class DeviceManager:
    def __init__(self, port_map, use_fake=False, fake_devices=None, debug=False, facility_status_manager=None):
        self.controllers = {}
        self.serial_ports = {}
        self.use_fake = use_fake
        self.fake_devices = fake_devices or []
        self.debug = debug
        self.facility_status_manager = facility_status_manager

        for device_id, port_info in port_map.items():
            port = port_info['port']
            baudrate = port_info['baudrate']
            
            if self.use_fake and device_id in self.fake_devices:
                if port not in self.serial_ports:
                    self.serial_ports[port] = FakeSerial(port=port, baudrate=baudrate, debug=self.debug)
                serial_instance = self.serial_ports[port]
            else:
                if port not in self.serial_ports:
                    self.serial_ports[port] = SerialController(port, baudrate, debug=self.debug, facility_status_manager=self.facility_status_manager)
                serial_instance = self.serial_ports[port]

            if "BELT" in device_id:
                self.controllers[device_id] = BeltController(serial_instance)
            elif "GATE" in device_id:
                self.controllers[device_id] = GateController(serial_instance)
            elif "DISPENSER" in device_id:
                self.controllers[device_id] = DispenserController(serial_instance)
        
        print("[DeviceManager 초기화 완료]")

    def get_controller(self, device_id):
        return self.controllers.get(device_id)

    def close_all(self):
        print("[모든 시리얼 포트 종료 중...]")
        for port_controller in self.serial_ports.values():
            try:
                port_controller.close()
            except Exception as e:
                print(f"[경고] 포트 {port_controller.port} 종료 중 오류: {e}")
