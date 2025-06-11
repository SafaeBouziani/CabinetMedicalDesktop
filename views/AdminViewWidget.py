from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTableWidget,
                              QPushButton, QHBoxLayout, QDialog, QFormLayout,
                              QLineEdit, QComboBox, QDialogButtonBox, QMessageBox,
                              QTableWidgetItem, QLabel)
from PySide6.QtCore import Qt

class AdminView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.user_data = None
        self.setup_ui()
        self.apply_styles()
    
    def apply_styles(self):
        """Apply consistent styling to the interface"""
        self.setStyleSheet("""
            QWidget {
                background-color: #f8f9fa;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 6px;
                font-weight: 500;
                min-width: 100px;
            }
            
            QPushButton:hover {
                background-color: #0056b3;
            }
            
            QPushButton:pressed {
                background-color: #004085;
            }
            
            QPushButton[class="danger"] {
                background-color: #dc3545;
            }
            
            QPushButton[class="danger"]:hover {
                background-color: #c82333;
            }
            
            QPushButton[class="secondary"] {
                background-color: #6c757d;
            }
            
            QPushButton[class="secondary"]:hover {
                background-color: #545b62;
            }
            
            QPushButton[class="success"] {
                background-color: #28a745;
            }
            
            QPushButton[class="success"]:hover {
                background-color: #1e7e34;
            }
            
            QTableWidget {
                background-color: white;
                border: 1px solid #dee2e6;
                border-radius: 8px;
                gridline-color: #dee2e6;
                selection-background-color: #e3f2fd;
            }
            
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #dee2e6;
            }
            
            QHeaderView::section {
                background-color: #f8f9fa;
                padding: 10px;
                border: none;
                border-bottom: 2px solid #dee2e6;
                font-weight: 600;
            }
            
            QTabWidget::pane {
                border: 1px solid #dee2e6;
                background-color: white;
                border-radius: 8px;
            }
            
            QTabBar::tab {
                background-color: #e9ecef;
                padding: 10px 20px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
            }
            
            QTabBar::tab:selected {
                background-color: white;
                border-bottom: 2px solid #007bff;
            }
            
            QComboBox {
                padding: 6px 12px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                background-color: white;
                min-width: 150px;
            }
            
            QComboBox:focus {
                border-color: #007bff;
                outline: none;
            }
            
            QLabel {
                color: #495057;
            }
        """)
    
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Titre de bienvenue
        self.welcome_label = QLabel()
        self.welcome_label.setStyleSheet("""
            font-size: 24px; 
            font-weight: bold; 
            color: #212529;
            padding: 15px 0;
            border-bottom: 2px solid #007bff;
            margin-bottom: 10px;
        """)
        layout.addWidget(self.welcome_label)
        
        # Créer le widget d'onglets
        self.tab_widget = QTabWidget()
        
        # Onglet Utilisateurs
        users_tab = QWidget()
        users_layout = QVBoxLayout()
        users_layout.setSpacing(15)
        users_layout.setContentsMargins(15, 15, 15, 15)
        
        # Filtres d'utilisateurs
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        
        filter_label = QLabel("Filtrer par rôle:")
        filter_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        
        self.role_filter = QComboBox()
        self.role_filter.addItem("Tous", userData=None)
        self.role_filter.addItem("Patients", userData="patient")
        self.role_filter.addItem("Docteurs", userData="doctor")
        self.role_filter.addItem("Admins", userData="admin")
        self.role_filter.currentIndexChanged.connect(
            lambda: self.load_users(self.role_filter.currentData())
        )
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.role_filter)
        filter_layout.addStretch()
        users_layout.addLayout(filter_layout)
        
        # Table des utilisateurs
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels(
            ["ID", "Nom", "Email", "Rôle", "Dernier login", "Actions"]
        )
        
        # Améliorer l'apparence du tableau
        self.users_table.setAlternatingRowColors(True)
        self.users_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.users_table.verticalHeader().setVisible(False)
        
        # Ajuster les largeurs de colonnes
        header = self.users_table.horizontalHeader()
        header.setStretchLastSection(True)
        self.users_table.setColumnWidth(0, 80)   # ID
        self.users_table.setColumnWidth(1, 150)  # Nom
        self.users_table.setColumnWidth(2, 200)  # Email
        self.users_table.setColumnWidth(3, 100)  # Rôle
        self.users_table.setColumnWidth(4, 150)  # Dernier login
        
        users_layout.addWidget(self.users_table)
        
        # Boutons d'action avec meilleur espacement
        users_buttons = QHBoxLayout()
        users_buttons.setSpacing(10)
        
        add_user_btn = QPushButton("➕ Ajouter Utilisateur")
        add_user_btn.setProperty("class", "success")
        add_user_btn.clicked.connect(self.show_add_user_dialog)
        
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.setProperty("class", "secondary")
        refresh_btn.clicked.connect(self.load_users)
        
        users_buttons.addWidget(add_user_btn)
        users_buttons.addWidget(refresh_btn)
        users_buttons.addStretch()
        
        users_layout.addLayout(users_buttons)
        users_tab.setLayout(users_layout)
        
        # Ajouter les onglets
        self.tab_widget.addTab(users_tab, "👥 Utilisateurs")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    
    def load_data(self, user_data):
        self.user_data = user_data
        self.welcome_label.setText(f"🔧 Administration - Bienvenue {user_data.get('name', user_data.get('username'))}")
        self.load_users()

    def show_add_user_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Ajouter un utilisateur")
        dialog.resize(450, 550)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QFormLayout {
                spacing: 12px;
            }
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus, QComboBox:focus {
                border-color: #007bff;
                outline: none;
            }
            QLabel {
                font-weight: 600;
                color: #495057;
            }
        """)
        
        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Champs de saisie
        username_input = QLineEdit()
        username_input.setPlaceholderText("Nom d'utilisateur unique...")
        
        email_input = QLineEdit()
        email_input.setPlaceholderText("adresse@email.com")
        
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setPlaceholderText("Mot de passe sécurisé...")
        
        name_input = QLineEdit()
        name_input.setPlaceholderText("Nom complet...")
        
        age_input = QLineEdit()
        age_input.setPlaceholderText("Âge en années...")
        
        specialty_input = QLineEdit()
        specialty_input.setPlaceholderText("Spécialité médicale...")
        
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
        
        # Boutons avec style amélioré
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Créer")
        buttons.button(QDialogButtonBox.Cancel).setText("Annuler")
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        
        layout.addRow(buttons)
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            # Validation des champs obligatoires
            if not username_input.text().strip():
                QMessageBox.warning(self, "Erreur", "Veuillez saisir un nom d'utilisateur.")
                return
            
            if not email_input.text().strip():
                QMessageBox.warning(self, "Erreur", "Veuillez saisir un email.")
                return
            
            if not password_input.text().strip():
                QMessageBox.warning(self, "Erreur", "Veuillez saisir un mot de passe.")
                return
            
            if not name_input.text().strip():
                QMessageBox.warning(self, "Erreur", "Veuillez saisir le nom complet.")
                return
            
            # Récupérer les valeurs
            new_user = {
                "username": username_input.text().strip(),
                "email": email_input.text().strip(),
                "password": password_input.text().strip(),
                "name": name_input.text().strip(),
                "role": role_combo.currentText()
            }
        
            # Ajouter l'âge si c'est un patient
            if new_user["role"] == "patient":
                try:
                    if age_input.text().strip():
                        new_user["age"] = int(age_input.text().strip())
                    else:
                        QMessageBox.warning(self, "Erreur", "Veuillez saisir l'âge pour un patient.")
                        return
                except ValueError:
                    QMessageBox.warning(self, "Erreur", "L'âge doit être un nombre entier.")
                    return
            
            if new_user["role"] == "doctor":
                if not specialty_input.text().strip():
                    QMessageBox.warning(self, "Erreur", "Veuillez saisir la spécialité pour un docteur.")
                    return
                new_user["specialty"] = specialty_input.text().strip()

            try:
                # Utiliser Database.add_user au lieu de auth_manager.add_user
                self.main_window.database.add_user(new_user, new_user["role"])
                self.main_window.sync_manager.sync_all()
                self.load_users()
                QMessageBox.information(self, "Succès", "Utilisateur créé avec succès.")
            except ValueError as e:
                QMessageBox.warning(self, "Erreur", str(e))

    def show_edit_user_dialog(self, user):
        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier un utilisateur")
        dialog.resize(400, 300)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QFormLayout {
                spacing: 12px;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border-color: #007bff;
                outline: none;
            }
            QLabel {
                font-weight: 600;
                color: #495057;
            }
        """)

        layout = QFormLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        name_input = QLineEdit(user.get("name", ""))
        name_input.setPlaceholderText("Nom complet...")
        
        email_input = QLineEdit(user.get("email", ""))
        email_input.setPlaceholderText("adresse@email.com")
        
        password_input = QLineEdit()
        password_input.setEchoMode(QLineEdit.Password)
        password_input.setPlaceholderText("Laissez vide pour conserver...")

        layout.addRow("Nom complet:", name_input)
        layout.addRow("Email:", email_input)
        layout.addRow("Nouveau mot de passe (optionnel):", password_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Sauvegarder")
        buttons.button(QDialogButtonBox.Cancel).setText("Annuler")
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        dialog.setLayout(layout)

        if dialog.exec_() == QDialog.Accepted:
            if not name_input.text().strip():
                QMessageBox.warning(self, "Erreur", "Veuillez saisir le nom complet.")
                return
            
            if not email_input.text().strip():
                QMessageBox.warning(self, "Erreur", "Veuillez saisir un email.")
                return
            
            updated_data = {
                "name": name_input.text().strip(),
                "email": email_input.text().strip()
            }
            if password_input.text().strip():
                updated_data["password"] = password_input.text().strip()

            try:
                self.main_window.database.update_user(user["_id"], updated_data)
                self.main_window.sync_manager.sync_all()
                self.load_users()
                QMessageBox.information(self, "Succès", "Utilisateur mis à jour avec succès.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la mise à jour: {str(e)}")

    def load_users(self, role_filter=None):
        self.users_table.setRowCount(0)

        try:
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
                
                # Colorer les rôles
                role_item = QTableWidgetItem(user.get("role", ""))
                role = user.get("role", "")
                if role == "admin":
                    role_item.setBackground(Qt.red)
                    role_item.setForeground(Qt.white)
                elif role == "doctor":
                    role_item.setBackground(Qt.blue)
                    role_item.setForeground(Qt.white)
                elif role == "patient":
                    role_item.setBackground(Qt.green)
                    role_item.setForeground(Qt.white)
                self.users_table.setItem(row_index, 3, role_item)
                
                self.users_table.setItem(row_index, 4, QTableWidgetItem(str(user.get("last_login", "Jamais"))))

                # Add Edit & Delete buttons avec style amélioré
                btn_layout = QHBoxLayout()
                btn_layout.setSpacing(5)
                btn_layout.setContentsMargins(5, 2, 5, 2)
                
                edit_btn = QPushButton("✏️")
                edit_btn.setToolTip("Modifier l'utilisateur")
                edit_btn.setMaximumWidth(35)
                
                delete_btn = QPushButton("🗑️")
                delete_btn.setToolTip("Supprimer l'utilisateur")
                delete_btn.setMaximumWidth(35)
                delete_btn.setProperty("class", "danger")
                
                edit_btn.clicked.connect(lambda _, u=user: self.show_edit_user_dialog(u))
                delete_btn.clicked.connect(lambda _, u=user: self.delete_user(u))
                
                btn_widget = QWidget()
                btn_layout.addWidget(edit_btn)
                btn_layout.addWidget(delete_btn)
                btn_widget.setLayout(btn_layout)
                self.users_table.setCellWidget(row_index, 5, btn_widget)
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement: {str(e)}")

    def delete_user(self, user):
        reply = QMessageBox.question(
            self,
            "⚠️ Confirmation",
            f"Êtes-vous sûr de vouloir supprimer l'utilisateur {user.get('name')} ?\n\nCette action est irréversible.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            try:
                self.main_window.database.delete_user(user["_id"])
                self.main_window.sync_manager.delete_user(user["_id"])
                self.load_users()
                QMessageBox.information(self, "✅ Succès", "Utilisateur supprimé avec succès.")
            except Exception as e:
                QMessageBox.critical(self, "❌ Erreur", f"Erreur lors de la suppression: {str(e)}")