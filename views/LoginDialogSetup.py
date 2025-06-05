from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, 
                              QLineEdit, QPushButton, QMessageBox)

class LoginDialog(QDialog):
    def __init__(self, auth_manager):
        super().__init__()
        self.auth_manager = auth_manager
        self.user_data = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Connexion")
        layout = QFormLayout()

        # Champs de connexion
        self.username_edit = QLineEdit()
        self.password_edit = QLineEdit()
        self.password_edit.setEchoMode(QLineEdit.Password)

        layout.addRow("Nom d'utilisateur:", self.username_edit)
        layout.addRow("Mot de passe:", self.password_edit)

        # Bouton de connexion
        login_button = QPushButton("Se connecter")
        login_button.clicked.connect(self.try_login)
        layout.addRow(login_button)

        self.setLayout(layout)

    def try_login(self):
        username = self.username_edit.text()
        password = self.password_edit.text()
        
        try:
            self.user_data = self.auth_manager.login(username, password)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))