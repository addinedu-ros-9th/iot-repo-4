from PyQt6.QtWidgets import QWidget, QTableWidgetItem, QMessageBox, QHeaderView
from PyQt6 import uic
import os
import mysql.connector

# 설정 관리를 위해 새로 만든 ConfigManager를 임포트합니다.
from gui.config_manager import config_manager


class SettingsTab(QWidget):
    """
    시스템의 다양한 설정을 관리하는 탭 위젯입니다.
    UI를 통해 사용자가 직접 설정을 변경하고 저장할 수 있습니다.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # UI 파일을 로드합니다. 경로 문제를 피하기 위해 절대 경로를 사용합니다.
        ui_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "ui", "tab_settings.ui")
        uic.loadUi(ui_path, self)
        
        self.init_ui()
        self.load_settings_to_ui()
        
    def init_ui(self):
        """UI의 각 위젯을 초기화하고 시그널-슬롯을 연결합니다."""
        
        # --- 설정 섹션 ---
        self.pushButton_save_settings.clicked.connect(self.save_settings_from_ui)
        self.pushButton_reset_settings.clicked.connect(self.reset_settings)
        
        # --- DB 연결 섹션 ---
        self.pushButton_test_connection.clicked.connect(self.test_db_connection)
        
        # --- 네트워크 섹션 ---
        # 네트워크 설정은 저장 버튼을 누를 때 함께 저장되므로 별도 버튼이 필요 없습니다.
        # self.pushButton_apply_network.clicked.connect(self.apply_network_settings)
        
        # --- 사용자 관리 섹션 ---
        self.pushButton_add_user.clicked.connect(self.add_user)
        self.pushButton_edit_user.clicked.connect(self.edit_user)
        self.pushButton_delete_user.clicked.connect(self.delete_user)
        
        # 사용자 테이블의 컬럼 너비를 조정합니다.
        self.tableWidget_users.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Interactive)
        self.tableWidget_users.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.tableWidget_users.setColumnWidth(0, 300)
        
        self.load_users()

    def load_settings_to_ui(self):
        """ConfigManager에서 설정을 불러와 UI에 적용합니다."""
        config = config_manager.get_config()

        # 일반 설정
        general_config = config.get("general", {})
        self.comboBox_theme.setCurrentText(general_config.get("theme", "라이트 모드"))
        self.comboBox_language.setCurrentText(general_config.get("language", "한국어"))

        # 정책 설정
        policy_config = config.get("policy", {})
        self.spinBox_battery_warning.setValue(policy_config.get("battery_warning_threshold", 20))
        self.spinBox_facility_time_limit.setValue(policy_config.get("facility_time_limit", 8))

        # 서버 설정
        server_config = config.get("server", {})
        self.lineEdit_server_address.setText(server_config.get("server_address", "127.0.0.1"))
        self.lineEdit_api_port.setText(str(server_config.get("api_port", 8000)))
        self.lineEdit_tcp_port.setText(str(server_config.get("tcp_port", 9000)))

        # 데이터베이스 설정
        db_config = config.get("database", {})
        self.lineEdit_db_host.setText(db_config.get("host", "127.0.0.1"))
        self.lineEdit_db_port.setText(str(db_config.get("port", 3306)))
        self.lineEdit_db_user.setText(db_config.get("user", "root"))
        self.lineEdit_db_name.setText(db_config.get("database", "dust"))
        # 비밀번호는 보안을 위해 직접 표시하지 않고, 값이 있으면 마스킹 처리합니다.
        if db_config.get("password"):
            self.lineEdit_db_password.setText("●●●●●●●●")
        else:
            self.lineEdit_db_password.clear()

    def save_settings_from_ui(self):
        """UI의 현재 설정 값들을 ConfigManager를 통해 저장합니다."""
        try:
            # General Settings
            config_manager.update_setting("general", "theme", self.comboBox_theme.currentText())
            config_manager.update_setting("general", "language", self.comboBox_language.currentText())

            # Policy Settings
            config_manager.update_setting("policy", "battery_warning_threshold", self.spinBox_battery_warning.value())
            config_manager.update_setting("policy", "facility_time_limit", self.spinBox_facility_time_limit.value())

            # Server Settings
            config_manager.update_setting("server", "server_address", self.lineEdit_server_address.text())
            config_manager.update_setting("server", "api_port", int(self.lineEdit_api_port.text()))
            config_manager.update_setting("server", "tcp_port", int(self.lineEdit_tcp_port.text()))

            # Database Settings
            config_manager.update_setting("database", "host", self.lineEdit_db_host.text())
            config_manager.update_setting("database", "port", int(self.lineEdit_db_port.text()))
            config_manager.update_setting("database", "user", self.lineEdit_db_user.text())
            config_manager.update_setting("database", "database", self.lineEdit_db_name.text())
            
            # 비밀번호 필드가 마스킹된 상태가 아니라면 (즉, 사용자가 새로 입력했다면) 업데이트
            if not self.lineEdit_db_password.text().startswith("●"):
                config_manager.update_setting("database", "password", self.lineEdit_db_password.text())

            config_manager.save_config()
            
            # API 클라이언트에도 변경된 서버 주소/포트 적용
            self.apply_network_settings_to_client()

            QMessageBox.information(self, "설정 저장", "설정이 성공적으로 저장되었습니다.")

        except ValueError:
            QMessageBox.warning(self, "입력 오류", "포트 번호 등 숫자 필드에 유효한 값을 입력하세요.")
        except Exception as e:
            QMessageBox.critical(self, "오류", f"설정 저장 중 오류가 발생했습니다: {e}")

    def reset_settings(self):
        """모든 설정을 기본값으로 되돌립니다."""
        reply = QMessageBox.question(
            self, 
            "설정 초기화", 
            "모든 설정을 기본값으로 되돌리시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            config_manager.reset_to_defaults()
            self.load_settings_to_ui()
            QMessageBox.information(self, "설정 초기화", "설정이 기본값으로 초기화되었습니다.")

    def apply_network_settings_to_client(self):
        """현재 설정된 네트워크 정보를 API 클라이언트에 적용합니다."""
        try:
            from gui.api_client import api_client
            server_addr = config_manager.get_setting("server", "server_address")
            api_port = config_manager.get_setting("server", "api_port")
            
            api_client.update_config(server_address=server_addr, api_port=api_port)
            print(f"API 클라이언트 설정 업데이트: http://{server_addr}:{api_port}")
        except Exception as e:
            print(f"API 클라이언트 설정 업데이트 실패: {e}")

    def get_db_connection(self, use_ui_values=False):
        """
        데이터베이스 연결을 생성하여 반환합니다.
        use_ui_values가 True이면 UI에 입력된 값으로 연결을 시도합니다. (연결 테스트용)
        """
        try:
            if use_ui_values:
                # 연결 테스트 시에는 UI에 있는 값을 직접 사용
                db_config = {
                    "host": self.lineEdit_db_host.text(),
                    "port": int(self.lineEdit_db_port.text()),
                    "user": self.lineEdit_db_user.text(),
                    "database": self.lineEdit_db_name.text(),
                }
                # 비밀번호 처리: 마스킹 상태가 아니면 UI의 값을, 마스킹 상태면 저장된 값을 사용
                password = self.lineEdit_db_password.text()
                if password.startswith("●"):
                    db_config["password"] = config_manager.get_setting("database", "password")
                else:
                    db_config["password"] = password
            else:
                # 일반적인 경우, 저장된 설정을 사용
                db_config = config_manager.get_config().get("database")

            if not db_config:
                 return None

            conn = mysql.connector.connect(**db_config, connection_timeout=3)
            return conn
        except (ValueError, mysql.connector.Error) as err:
            print(f"DB 연결 실패: {err}")
            return None

    def test_db_connection(self):
        """UI에 입력된 정보로 DB 연결을 테스트합니다."""
        conn = self.get_db_connection(use_ui_values=True)
        if conn:
            QMessageBox.information(self, "연결 테스트", "데이터베이스 연결에 성공했습니다.")
            conn.close()
        else:
            QMessageBox.critical(self, "연결 오류", "데이터베이스 연결에 실패했습니다.\n호스트, 포트, 사용자 이름, 비밀번호를 확인하세요.")

    # =================================================================
    # 사용자 관리 기능 (향후 별도 모듈로 분리 가능)
    # =================================================================

    def load_users(self):
        """데이터베이스에서 사용자 목록을 불러와 테이블에 표시합니다."""
        self.tableWidget_users.setRowCount(0)
        
        try:
            conn = self.get_db_connection(use_ui_values=True) # 현재 설정된 DB 정보로 로드
            if not conn:
                QMessageBox.warning(self, "사용자 로드 실패", "DB에 연결할 수 없어 사용자 목록을 불러올 수 없습니다.")
                return

            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT username, role FROM users ORDER BY id DESC")
            users = cursor.fetchall()
            
            for user in users:
                row_position = self.tableWidget_users.rowCount()
                self.tableWidget_users.insertRow(row_position)
                self.tableWidget_users.setItem(row_position, 0, QTableWidgetItem(user["username"]))
                self.tableWidget_users.setItem(row_position, 1, QTableWidgetItem(user["role"]))
            
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            print(f"사용자 로드 실패: {err}")
            QMessageBox.critical(self, "오류", f"사용자 목록을 불러오는 중 오류가 발생했습니다: {err}")

    def add_user(self):
        """사용자 추가 기능 (미구현)"""
        QMessageBox.information(self, "미구현", "사용자 추가 기능은 아직 구현되지 않았습니다.")
        
    def edit_user(self):
        """사용자 편집 기능 (미구현)"""
        if not self.tableWidget_users.selectedItems():
            QMessageBox.warning(self, "사용자 편집", "편집할 사용자를 선택하세요.")
            return
        QMessageBox.information(self, "미구현", "사용자 편집 기능은 아직 구현되지 않았습니다.")
        
    def delete_user(self):
        """선택된 사용자를 데이터베이스에서 삭제합니다."""
        selected_items = self.tableWidget_users.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "사용자 삭제", "삭제할 사용자를 선택하세요.")
            return
            
        selected_row = selected_items[0].row()
        username = self.tableWidget_users.item(selected_row, 0).text()
        
        reply = QMessageBox.question(
            self, 
            "사용자 삭제", 
            f"사용자 '{username}'을(를) 정말로 삭제하시겠습니까?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, 
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                conn = self.get_db_connection(use_ui_values=True)
                if not conn:
                    QMessageBox.critical(self, "오류", "DB에 연결할 수 없어 사용자를 삭제할 수 없습니다.")
                    return

                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE username = %s", (username,))
                conn.commit()
                
                self.tableWidget_users.removeRow(selected_row)
                QMessageBox.information(self, "삭제 완료", f"사용자 '{username}'이(가) 삭제되었습니다.")

                cursor.close()
                conn.close()
            except mysql.connector.Error as err:
                print(f"사용자 삭제 실패: {err}")
                QMessageBox.critical(self, "오류", f"사용자 삭제 중 오류가 발생했습니다: {err}")