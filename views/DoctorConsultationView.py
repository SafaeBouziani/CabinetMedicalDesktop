# views/DoctorConsultationView.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTableWidget,
                              QPushButton, QHBoxLayout, QDialog, QFormLayout,
                              QLineEdit, QComboBox, QDialogButtonBox, QMessageBox,
                              QTableWidgetItem, QTextEdit, QDateTimeEdit, QLabel)
from PySide6.QtCore import QDateTime, Qt
from datetime import datetime
from models.ConsultationModel import Consultation

class DoctorView(QWidget):
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
        
        # Onglet Consultations
        consultations_tab = QWidget()
        consultations_layout = QVBoxLayout()
        consultations_layout.setSpacing(15)
        consultations_layout.setContentsMargins(15, 15, 15, 15)
        
        # Filtres de consultation
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(15)
        
        filter_label = QLabel("Filtrer par statut:")
        filter_label.setStyleSheet("font-weight: 600; font-size: 14px;")
        
        self.status_filter = QComboBox()
        self.status_filter.addItem("Toutes", userData=None)
        self.status_filter.addItem("Programmées", userData="programmé")
        self.status_filter.addItem("En cours", userData="en_cours")
        self.status_filter.addItem("Terminées", userData="terminé")
        self.status_filter.addItem("Annulées", userData="annulé")
        self.status_filter.currentIndexChanged.connect(
            lambda: self.load_consultations(self.status_filter.currentData())
        )
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.status_filter)
        filter_layout.addStretch()
        consultations_layout.addLayout(filter_layout)
        
        # Table des consultations
        self.consultations_table = QTableWidget()
        self.consultations_table.setColumnCount(7)
        self.consultations_table.setHorizontalHeaderLabels([
            "ID", "Patient", "Date", "Motif", "Statut", "Diagnostic", "Actions"
        ])
        
        # Améliorer l'apparence du tableau
        self.consultations_table.setAlternatingRowColors(True)
        self.consultations_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.consultations_table.verticalHeader().setVisible(False)
        
        # Ajuster les largeurs de colonnes
        header = self.consultations_table.horizontalHeader()
        header.setStretchLastSection(True)
        self.consultations_table.setColumnWidth(0, 80)   # ID
        self.consultations_table.setColumnWidth(1, 150)  # Patient
        self.consultations_table.setColumnWidth(2, 130)  # Date
        self.consultations_table.setColumnWidth(3, 200)  # Motif
        self.consultations_table.setColumnWidth(4, 100)  # Statut
        self.consultations_table.setColumnWidth(5, 150)  # Diagnostic
        
        consultations_layout.addWidget(self.consultations_table)
        
        # Boutons d'action avec meilleur espacement
        consultations_buttons = QHBoxLayout()
        consultations_buttons.setSpacing(10)
        
        add_consultation_btn = QPushButton("➕ Nouvelle Consultation")
        add_consultation_btn.setProperty("class", "success")
        add_consultation_btn.clicked.connect(self.show_add_consultation_dialog)
        
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.setProperty("class", "secondary")
        refresh_btn.clicked.connect(self.load_consultations)
        
        consultations_buttons.addWidget(add_consultation_btn)
        consultations_buttons.addWidget(refresh_btn)
        consultations_buttons.addStretch()
        
        consultations_layout.addLayout(consultations_buttons)
        consultations_tab.setLayout(consultations_layout)
        
        # Ajouter l'onglet
        self.tab_widget.addTab(consultations_tab, "📋 Consultations")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    
    def load_data(self, user_data):
        self.user_data = user_data
        self.welcome_label.setText(f"👨‍⚕️ Bienvenue Dr. {user_data.get('name', user_data.get('username'))}")
        self.load_consultations()
    
    def show_add_consultation_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nouvelle Consultation")
        dialog.resize(450, 550)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QFormLayout {
                spacing: 12px;
            }
            QTextEdit, QLineEdit, QComboBox, QDateTimeEdit {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 13px;
            }
            QTextEdit:focus, QLineEdit:focus, QComboBox:focus, QDateTimeEdit:focus {
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
        
        # Sélection du patient
        patient_combo = QComboBox()
        patients = self.main_window.database.get_user_by_role("patient")
        patient_combo.addItem("Sélectionner un patient", userData=None)
        for patient in patients:
            patient_combo.addItem(
                f"{patient.get('name', '')} ({patient.get('email', '')})", 
                userData=str(patient['_id'])
            )
        
        # Date et heure
        datetime_edit = QDateTimeEdit()
        datetime_edit.setDateTime(QDateTime.currentDateTime())
        datetime_edit.setCalendarPopup(True)
        
        # Motif
        motif_input = QTextEdit()
        motif_input.setMaximumHeight(80)
        motif_input.setPlaceholderText("Décrivez le motif de la consultation...")
        
        # Statut
        status_combo = QComboBox()
        status_combo.addItems(["programmé", "en_cours", "terminé", "annulé"])
        
        # Diagnostic (optionnel)
        diagnostic_input = QTextEdit()
        diagnostic_input.setMaximumHeight(100)
        diagnostic_input.setPlaceholderText("Diagnostic (optionnel)...")
        
        # Prescriptions (optionnel)
        prescriptions_input = QTextEdit()
        prescriptions_input.setMaximumHeight(100)
        prescriptions_input.setPlaceholderText("Une prescription par ligne...")
        
        layout.addRow("Patient:", patient_combo)
        layout.addRow("Date et heure:", datetime_edit)
        layout.addRow("Motif:", motif_input)
        layout.addRow("Statut:", status_combo)
        layout.addRow("Diagnostic:", diagnostic_input)
        layout.addRow("Prescriptions:", prescriptions_input)
        
        # Boutons avec style amélioré
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Créer")
        buttons.button(QDialogButtonBox.Cancel).setText("Annuler")
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            if not patient_combo.currentData():
                QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un patient.")
                return
            
            if not motif_input.toPlainText().strip():
                QMessageBox.warning(self, "Erreur", "Veuillez saisir le motif de consultation.")
                return
            
            # Préparer les prescriptions
            prescriptions = []
            if prescriptions_input.toPlainText().strip():
                prescriptions = [p.strip() for p in prescriptions_input.toPlainText().split('\n') if p.strip()]
            
            consultation_data = {
                "patient_id": patient_combo.currentData(),
                "doctor_id": str(self.user_data['_id']),
                "date": datetime_edit.dateTime().toPython(),
                "motif": motif_input.toPlainText().strip(),
                "status": status_combo.currentText(),
                "diagnostic": diagnostic_input.toPlainText().strip() or None,
                "prescriptions": prescriptions,
                "created_at": datetime.utcnow()
            }
            
            try:
                self.main_window.database.add_consultation(consultation_data)
                self.load_consultations()
                QMessageBox.information(self, "Succès", "Consultation créée avec succès.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la création: {str(e)}")
    
    def show_edit_consultation_dialog(self, consultation):
        dialog = QDialog(self)
        dialog.setWindowTitle("Modifier la Consultation")
        dialog.resize(450, 550)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QFormLayout {
                spacing: 12px;
            }
            QTextEdit, QLineEdit, QComboBox, QDateTimeEdit {
                padding: 8px;
                border: 1px solid #ced4da;
                border-radius: 4px;
                font-size: 13px;
            }
            QTextEdit:focus, QLineEdit:focus, QComboBox:focus, QDateTimeEdit:focus {
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
        
        # Informations patient (lecture seule)
        patient = self.main_window.database.get_user_by_id(consultation.get('patient_id'))
        patient_label = QLabel(f"{patient.get('name', 'N/A')} ({patient.get('email', 'N/A')})")
        patient_label.setStyleSheet("color: #6c757d; font-style: italic;")
        
        # Date et heure
        datetime_edit = QDateTimeEdit()
        if consultation.get('date'):
            if isinstance(consultation['date'], datetime):
                datetime_edit.setDateTime(QDateTime.fromSecsSinceEpoch(int(consultation['date'].timestamp())))
            else:
                datetime_edit.setDateTime(QDateTime.currentDateTime())
        else:
            datetime_edit.setDateTime(QDateTime.currentDateTime())
        datetime_edit.setCalendarPopup(True)
        
        # Motif
        motif_input = QTextEdit()
        motif_input.setMaximumHeight(80)
        motif_input.setPlainText(consultation.get('motif', ''))
        
        # Statut
        status_combo = QComboBox()
        status_combo.addItems(["programmé", "en_cours", "terminé", "annulé"])
        current_status = consultation.get('status', 'programmé')
        status_index = status_combo.findText(current_status)
        if status_index >= 0:
            status_combo.setCurrentIndex(status_index)
        
        # Diagnostic
        diagnostic_input = QTextEdit()
        diagnostic_input.setMaximumHeight(100)
        diagnostic_input.setPlainText(consultation.get('diagnostic', ''))
        
        # Prescriptions
        prescriptions_input = QTextEdit()
        prescriptions_input.setMaximumHeight(100)
        prescriptions_input.setPlaceholderText("Une prescription par ligne...")
        if consultation.get('prescriptions'):
            prescriptions_input.setPlainText('\n'.join(consultation['prescriptions']))
        
        layout.addRow("Patient:", patient_label)
        layout.addRow("Date et heure:", datetime_edit)
        layout.addRow("Motif:", motif_input)
        layout.addRow("Statut:", status_combo)
        layout.addRow("Diagnostic:", diagnostic_input)
        layout.addRow("Prescriptions:", prescriptions_input)
        
        # Boutons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Sauvegarder")
        buttons.button(QDialogButtonBox.Cancel).setText("Annuler")
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addRow(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec_() == QDialog.Accepted:
            if not motif_input.toPlainText().strip():
                QMessageBox.warning(self, "Erreur", "Veuillez saisir le motif de consultation.")
                return
            
            # Préparer les prescriptions
            prescriptions = []
            if prescriptions_input.toPlainText().strip():
                prescriptions = [p.strip() for p in prescriptions_input.toPlainText().split('\n') if p.strip()]
            
            updated_data = {
                "date": datetime_edit.dateTime().toPython(),
                "motif": motif_input.toPlainText().strip(),
                "status": status_combo.currentText(),
                "diagnostic": diagnostic_input.toPlainText().strip() or None,
                "prescriptions": prescriptions
            }
            
            try:
                self.main_window.database.update_consultation(consultation['_id'], updated_data)
                self.load_consultations()
                QMessageBox.information(self, "Succès", "Consultation mise à jour avec succès.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la mise à jour: {str(e)}")
    
    def load_consultations(self, status_filter=None):
        self.consultations_table.setRowCount(0)
        
        try:
            # Récupérer les consultations du médecin connecté
            consultations = self.main_window.database.get_consultations_by_doctor(
                str(self.user_data['_id']), status_filter
            )
            
            for row_index, consultation in enumerate(consultations):
                self.consultations_table.insertRow(row_index)
                
                # ID
                self.consultations_table.setItem(row_index, 0, 
                    QTableWidgetItem(str(consultation.get('_id', ''))))
                
                # Patient
                patient = self.main_window.database.get_user_by_id(consultation.get('patient_id'))
                patient_name = patient.get('name', 'Patient inconnu') if patient else 'Patient inconnu'
                self.consultations_table.setItem(row_index, 1, 
                    QTableWidgetItem(patient_name))
                
                # Date
                date_str = "Non définie"
                if consultation.get('date'):
                    if isinstance(consultation['date'], datetime):
                        date_str = consultation['date'].strftime("%d/%m/%Y %H:%M")
                    else:
                        date_str = str(consultation['date'])
                self.consultations_table.setItem(row_index, 2, 
                    QTableWidgetItem(date_str))
                
                # Motif
                motif = consultation.get('motif', '')[:50] + "..." if len(consultation.get('motif', '')) > 50 else consultation.get('motif', '')
                self.consultations_table.setItem(row_index, 3, 
                    QTableWidgetItem(motif))
                
                # Statut
                status_item = QTableWidgetItem(consultation.get('status', ''))
                # Colorer les statuts
                status = consultation.get('status', '')
                if status == 'terminé':
                    status_item.setBackground(Qt.green)
                elif status == 'en_cours':
                    status_item.setBackground(Qt.yellow)
                elif status == 'annulé':
                    status_item.setBackground(Qt.red)
                self.consultations_table.setItem(row_index, 4, status_item)
                
                # Diagnostic
                diagnostic = consultation.get('diagnostic', '')
                if diagnostic:
                    diagnostic = diagnostic[:30] + "..." if len(diagnostic) > 30 else diagnostic
                self.consultations_table.setItem(row_index, 5, 
                    QTableWidgetItem(diagnostic or "Non défini"))
                
                # Boutons d'action avec meilleur espacement
                btn_layout = QHBoxLayout()
                btn_layout.setSpacing(5)
                btn_layout.setContentsMargins(5, 2, 5, 2)
                
                view_btn = QPushButton("👁️")
                view_btn.setToolTip("Voir les détails")
                view_btn.setMaximumWidth(35)
                view_btn.setProperty("class", "secondary")
                
                edit_btn = QPushButton("✏️")
                edit_btn.setToolTip("Modifier")
                edit_btn.setMaximumWidth(35)
                
                delete_btn = QPushButton("🗑️")
                delete_btn.setToolTip("Supprimer")
                delete_btn.setMaximumWidth(35)
                delete_btn.setProperty("class", "danger")
                
                edit_btn.clicked.connect(lambda _, c=consultation: self.show_edit_consultation_dialog(c))
                delete_btn.clicked.connect(lambda _, c=consultation: self.delete_consultation(c))
                view_btn.clicked.connect(lambda _, c=consultation: self.show_consultation_details(c))
                
                btn_widget = QWidget()
                btn_layout.addWidget(view_btn)
                btn_layout.addWidget(edit_btn)
                btn_layout.addWidget(delete_btn)
                btn_widget.setLayout(btn_layout)
                
                self.consultations_table.setCellWidget(row_index, 6, btn_widget)
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def show_consultation_details(self, consultation):
        dialog = QDialog(self)
        dialog.setWindowTitle("Détails de la Consultation")
        dialog.resize(550, 450)
        dialog.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QTextEdit {
                background-color: #f8f9fa;
                border: 1px solid #dee2e6;
                border-radius: 6px;
                padding: 15px;
                font-family: 'Consolas', monospace;
                font-size: 13px;
                line-height: 1.5;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Informations détaillées
        details_text = QTextEdit()
        details_text.setReadOnly(True)
        
        # Récupérer les informations du patient
        patient = self.main_window.database.get_user_by_id(consultation.get('patient_id'))
        patient_info = f"{patient.get('name', 'N/A')} ({patient.get('email', 'N/A')})" if patient else "Patient inconnu"
        
        # Date formatée
        date_str = "Non définie"
        if consultation.get('date'):
            if isinstance(consultation['date'], datetime):
                date_str = consultation['date'].strftime("%d/%m/%Y à %H:%M")
            else:
                date_str = str(consultation['date'])
        
        # Prescriptions formatées
        prescriptions_text = "Aucune"
        if consultation.get('prescriptions'):
            prescriptions_text = '\n'.join([f"• {p}" for p in consultation['prescriptions']])
        
        details_content = f"""
📋 INFORMATIONS GÉNÉRALES
═══════════════════════════════════════════════════════════════
👤 Patient: {patient_info}
📅 Date: {date_str}
🏷️ Statut: {consultation.get('status', 'Non défini')}
⏰ Créée le: {consultation.get('created_at', 'Non définie')}

💬 MOTIF DE CONSULTATION
═══════════════════════════════════════════════════════════════
{consultation.get('motif', 'Non défini')}

🔍 DIAGNOSTIC
═══════════════════════════════════════════════════════════════
{consultation.get('diagnostic', 'Non défini')}

💊 PRESCRIPTIONS
═══════════════════════════════════════════════════════════════
{prescriptions_text}
        """
        
        details_text.setPlainText(details_content.strip())
        
        layout.addWidget(details_text)
        
        # Bouton Fermer avec style
        close_btn = QPushButton("✖️ Fermer")
        close_btn.setProperty("class", "secondary")
        close_btn.clicked.connect(dialog.accept)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def delete_consultation(self, consultation):
        patient = self.main_window.database.get_user_by_id(consultation.get('patient_id'))
        patient_name = patient.get('name', 'Patient inconnu') if patient else 'Patient inconnu'
        
        reply = QMessageBox.question(
            self,
            "⚠️ Confirmation",
            f"Êtes-vous sûr de vouloir supprimer la consultation avec {patient_name} ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.main_window.database.delete_consultation(consultation['_id'])
                self.load_consultations()
                QMessageBox.information(self, "✅ Succès", "Consultation supprimée avec succès.")
            except Exception as e:
                QMessageBox.critical(self, "❌ Erreur", f"Erreur lors de la suppression: {str(e)}")