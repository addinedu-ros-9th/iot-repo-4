import json
import os

class ConfigManager:
    """
    애플리케이션의 설정을 관리하는 싱글턴 클래스.
    설정을 JSON 파일에 저장하고 불러옵니다.
    """
    _instance = None
    _config_file = "config.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
            cls._instance._init_config()
        return cls._instance

    def _init_config(self):
        """설정 파일을 로드하거나, 없는 경우 기본값으로 초기화합니다."""
        self.config = self.get_default_settings()
        if os.path.exists(self._config_file):
            try:
                with open(self._config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # 로드한 설정과 기본 설정을 병합하여 누락된 키를 보충합니다.
                    self._merge_settings(self.config, loaded_config)
            except (json.JSONDecodeError, IOError) as e:
                print(f"설정 파일 로드 오류: {e}. 기본 설정으로 계속합니다.")
        
        self.save_config()

    def _merge_settings(self, target, source):
        """
        재귀적으로 설정을 병합합니다. source의 값이 target을 덮어씁니다.
        source에만 있는 키도 target에 추가됩니다.
        """
        for key, value in source.items():
            if isinstance(value, dict) and key in target and isinstance(target[key], dict):
                self._merge_settings(target[key], value)
            else:
                target[key] = value

    def get_config(self):
        """현재 설정 전체를 반환합니다."""
        return self.config

    def get_setting(self, section, key, default=None):
        """특정 설정 값을 가져옵니다."""
        return self.config.get(section, {}).get(key, default)

    def update_setting(self, section, key, value):
        """특정 설정 값을 업데이트합니다."""
        if section not in self.config:
            self.config[section] = {}
        self.config[section][key] = value

    def save_config(self):
        """현재 설정을 JSON 파일에 저장합니다."""
        try:
            with open(self._config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=4)
        except IOError as e:
            print(f"설정 파일 저장 오류: {e}")

    def reset_to_defaults(self):
        """설정을 기본값으로 되돌립니다."""
        self.config = self.get_default_settings()
        self.save_config()

    def get_default_settings(self):
        """기본 설정값을 반환합니다."""
        return {
            "general": {
                "theme": "라이트 모드",
                "language": "한국어"
            },
            "server": {
                "server_address": "127.0.0.1",
                "api_port": 8000,
                "tcp_port": 9000
            },
            "database": {
                "host": "127.0.0.1",
                "port": 3306,
                "user": "root",
                "password": "",
                "database": "dust"
            },
            "policy": {
                "battery_warning_threshold": 20,
                "facility_time_limit": 8
            }
        }

# 애플리케이션 전체에서 공유할 ConfigManager 인스턴스
config_manager = ConfigManager()
