from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, 
                              QLineEdit, QPushButton, QMessageBox, QLabel)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QIcon

class LoginDialog(QDialog):
    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
        self.user_data = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Connexion")
        self.setFixedSize(400, 250)
        self.setModal(True)
        
        # Style the dialog
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
                border: 1px solid #ddd;
            }
            QLabel {
                font-weight: bold;
                color: #333;
                font-size: 11px;
            }
            QLineEdit {
                padding: 12px;
                border: 2px solid #ddd;
                border-radius: 6px;
                font-size: 13px;
                background-color: white;
                min-height: 16px;
                min-width: 200px;
            }
            QLineEdit:focus {
                border-color: #4a90e2;
                outline: none;
            }
            QPushButton {
                background-color: #4a90e2;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 12px;
                min-height: 20px;
            }
            QPushButton:hover {
                background-color: #357abd;
            }
            QPushButton:pressed {
                background-color: #2968a3;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title_label = QLabel("Connexion")
        title_label.setAlignment(Qt.AlignCenter)
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #2c3e50; margin-bottom: 10px;")
        main_layout.addWidget(title_label)

        # Form layout
        form_layout = QFormLayout()
        form_layout.setSpacing(15)
        form_layout.setLabelAlignment(Qt.AlignLeft)

        # Champs de connexion
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("Entrez votre nom d'utilisateur")
        
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setPlaceholderText("Entrez votre mot de passe")
        
        # Enable Enter key to submit
        self.username_edit.returnPressed.connect(self.try_login)
        self.password_edit.returnPressed.connect(self.try_login)

        form_layout.addRow("Nom d'utilisateur:", self.username_edit)
        form_layout.addRow("Mot de passe:", self.password_edit)

        main_layout.addLayout(form_layout)

        # Bouton de connexion
        login_button = QPushButton("Se connecter")
        login_button.clicked.connect(self.try_login)
        login_button.setDefault(True)  # Makes it the default button (activated by Enter)
        
        main_layout.addWidget(login_button)
        main_layout.addStretch()  # Push content to top

        self.setLayout(main_layout)
        
        # Set focus to username field
        self.username_edit.setFocus()

    def try_login(self):
        username = self.username_edit.text().strip()
        password = self.password_edit.text()
        
        # Basic validation
        if not username:
            QMessageBox.warning(self, "Champ requis", "Veuillez entrer votre nom d'utilisateur.")
            self.username_edit.setFocus()
            return
            
        if not password:
            QMessageBox.warning(self, "Champ requis", "Veuillez entrer votre mot de passe.")
            self.password_edit.setFocus()
            return
        
        try:
            self.user_data = self.auth_manager.login(username, password)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur de connexion", 
                               f"Impossible de se connecter:\n{str(e)}")
            # Clear password field on failed login
            self.password_edit.clear()
            self.password_edit.setFocus()