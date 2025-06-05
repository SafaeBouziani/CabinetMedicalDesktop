from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTableWidget,
                              QPushButton, QHBoxLayout, QDialog, QFormLayout,
                              QLineEdit, QComboBox, QDialogButtonBox,QMessageBox,QTableWidgetItem)

class AdminView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Créer le widget d'onglets
        self.tab_widget = QTabWidget()
        
        # Onglet Utilisateurs
        users_tab = QWidget()
        users_layout = QVBoxLayout()
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels(
            ["ID", "Nom", "Email", "Rôle", "Dernier login", "Actions"]
        )

        role_filter_layout = QHBoxLayout()
        self.role_filter = QComboBox()
        self.role_filter.addItem("Tous", userData=None)
        self.role_filter.addItem("Patients", userData="patient")
        self.role_filter.addItem("Docteurs", userData="doctor")
        self.role_filter.addItem("Admins", userData="admin")
        self.role_filter.currentIndexChanged.connect(
            lambda: self.load_users(self.role_filter.currentData())
        )
        role_filter_layout.addWidget(self.role_filter)
        users_layout.addLayout(role_filter_layout)

        users_buttons = QHBoxLayout()
        add_user_btn = QPushButton("Ajouter Utilisateur")
        add_user_btn.clicked.connect(self.show_add_user_dialog)
        users_buttons.addWidget(add_user_btn)
        
        users_layout.addWidget(self.users_table)
        users_layout.addLayout(users_buttons)
        users_tab.setLayout(users_layout)

        
        # Ajouter les onglets
        self.tab_widget.addTab(users_tab, "Utilisateurs")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    
    def load_data(self, user_data):
        self.user_data = user_data
        self.load_users()

    def show_add_user_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter un utilisateur")
        
        layout = QFormLayout()
        
        # Champs de saisie
        username_input = QLineEdit()
        email_input = QLineEdit()
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        name_input = QLineEdit()  # Ajout du champ nom
        age_input = QLineEdit()
        specialty_input = QLineEdit() # Ajout du champ âge pour les patients
        
        role_combo = QComboBox()
        role_combo.addItems(["patient", "doctor", "admin"])
        
        layout.addRow("Nom d'utilisateur:", username_input)
        layout.addRow("Nom complet:", name_input)
        layout.addRow("Email:", email_input)
        layout.addRow("Mot de passe:", password_input)
        layout.addRow("Rôle:", role_combo)
        layout.addRow("Âge:", age_input)
        layout.addRow("Spécialité:", specialty_input)
        
        # Fonction pour gérer la visibilité du champ âge
        def on_role_changed():
            age_input.setVisible(role_combo.currentText() == "patient")
            layout.labelForField(age_input).setVisible(role_combo.currentText() == "patient")
            specialty_input.setVisible(role_combo.currentText() == "doctor")
            layout.labelForField(specialty_input).setVisible(role_combo.currentText() == "doctor")

        
        role_combo.currentTextChanged.connect(on_role_changed)
        on_role_changed()  # État initial
        
        # Boutons
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        layout.addRow(buttons)
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            # Récupérer les valeurs
            new_user = {
                "username": username_input.text(),
                "email": email_input.text(),
                "password": password_input.text(),
                "name": name_input.text(),
                "role": role_combo.currentText()
            }
        
        # Ajouter l'âge si c'est un patient
            if new_user["role"] == "patient":
                new_user["age"] = int(age_input.text())
            if new_user["role"] == "doctor":
                new_user["specialty"] = specialty_input.text()

        
            try:
                # Utiliser Database.add_user au lieu de auth_manager.add_user
                self.main_window.database.add_user(new_user, new_user["role"])
                self.main_window.sync_manager.sync_all()
                self.load_users()
            except ValueError as e:
                QMessageBox.warning(self, "Erreur", str(e))

    def show_edit_user_dialog(self, user):
        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier un utilisateur")

        layout = QFormLayout()
        name_input = QLineEdit(user.get("name", ""))
        email_input = QLineEdit(user.get("email", ""))
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)

        layout.addRow("Nom complet:", name_input)
        layout.addRow("Email:", email_input)
        layout.addRow("Nouveau mot de passe (laissez vide pour garder):", password_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            updated_data = {
                "name": name_input.text(),
                "email": email_input.text()
            }
            if password_input.text():
                updated_data["password"] = password_input.text()

            self.main_window.database.update_user(user["_id"], updated_data)
            self.main_window.sync_manager.sync_all()
            self.load_users()


    def load_users(self, role_filter=None):
        self.users_table.setRowCount(0)

        # Fetch users from DB
        if role_filter:
            users = self.main_window.database.get_user_by_role(role_filter)
        else:
            users = self.main_window.database.get_all_users()

        for row_index, user in enumerate(users):
            self.users_table.insertRow(row_index)
            self.users_table.setItem(row_index, 0, QTableWidgetItem(str(user.get("_id"))))
            self.users_table.setItem(row_index, 1, QTableWidgetItem(user.get("name", "")))
            self.users_table.setItem(row_index, 2, QTableWidgetItem(user.get("email", "")))
            self.users_table.setItem(row_index, 3, QTableWidgetItem(user.get("role", "")))
            self.users_table.setItem(row_index, 4, QTableWidgetItem(str(user.get("last_login", ""))))

            # Add Edit & Delete buttons
            btn_layout = QHBoxLayout()
            edit_btn = QPushButton("Modifier")
            delete_btn = QPushButton("Supprimer")
            edit_btn.clicked.connect(lambda _, u=user: self.show_edit_user_dialog(u))
            delete_btn.clicked.connect(lambda _, u=user: self.delete_user(u))
            btn_widget = QWidget()
            btn_layout.addWidget(edit_btn)
            btn_layout.addWidget(delete_btn)
            btn_layout.setContentsMargins(0, 0, 0, 0)
            btn_widget.setLayout(btn_layout)
            self.users_table.setCellWidget(row_index, 5, btn_widget)

    def delete_user(self, user):
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer l'utilisateur {user.get('name')} ?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.main_window.database.delete_user(user["_id"])
            self.main_window.sync_manager.delete_user(user["_id"])
            self.load_users()
