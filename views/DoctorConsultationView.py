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
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Titre de bienvenue
        self.welcome_label = QLabel()
        self.welcome_label.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(self.welcome_label)
        
        # Créer le widget d'onglets
        self.tab_widget = QTabWidget()
        
        # Onglet Consultations
        consultations_tab = QWidget()
        consultations_layout = QVBoxLayout()
        
        # Filtres de consultation
        filter_layout = QHBoxLayout()
        self.status_filter = QComboBox()
        self.status_filter.addItem("Toutes", userData=None)
        self.status_filter.addItem("Programmées", userData="programmé")
        self.status_filter.addItem("En cours", userData="en_cours")
        self.status_filter.addItem("Terminées", userData="terminé")
        self.status_filter.addItem("Annulées", userData="annulé")
        self.status_filter.currentIndexChanged.connect(
            lambda: self.load_consultations(self.status_filter.currentData())
        )
        
        filter_layout.addWidget(QLabel("Filtrer par statut:"))
        filter_layout.addWidget(self.status_filter)
        filter_layout.addStretch()
        consultations_layout.addLayout(filter_layout)
        
        # Table des consultations
        self.consultations_table = QTableWidget()
        self.consultations_table.setColumnCount(7)
        self.consultations_table.setHorizontalHeaderLabels([
            "ID", "Patient", "Date", "Motif", "Statut", "Diagnostic", "Actions"
        ])
        
        # Boutons d'action
        consultations_buttons = QHBoxLayout()
        add_consultation_btn = QPushButton("Nouvelle Consultation")
        add_consultation_btn.clicked.connect(self.show_add_consultation_dialog)
        refresh_btn = QPushButton("Actualiser")
        refresh_btn.clicked.connect(self.load_consultations)
        
        consultations_buttons.addWidget(add_consultation_btn)
        consultations_buttons.addWidget(refresh_btn)
        consultations_buttons.addStretch()
        
        consultations_layout.addWidget(self.consultations_table)
        consultations_layout.addLayout(consultations_buttons)
        consultations_tab.setLayout(consultations_layout)
        
        # Ajouter l'onglet
        self.tab_widget.addTab(consultations_tab, "Consultations")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    
    def load_data(self, user_data):
        self.user_data = user_data
        self.welcome_label.setText(f"Bienvenue Dr. {user_data.get('name', user_data.get('username'))}")
        self.load_consultations()
    
    def show_add_consultation_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Nouvelle Consultation")
        dialog.resize(400, 500)
        
        layout = QFormLayout()
        
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
        
        # Statut
        status_combo = QComboBox()
        status_combo.addItems(["programmé", "en_cours", "terminé", "annulé"])
        
        # Diagnostic (optionnel)
        diagnostic_input = QTextEdit()
        diagnostic_input.setMaximumHeight(100)
        
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
        
        # Boutons
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
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
        dialog.resize(400, 500)
        
        layout = QFormLayout()
        
        # Informations patient (lecture seule)
        patient = self.main_window.database.get_user_by_id(consultation.get('patient_id'))
        patient_label = QLabel(f"{patient.get('name', 'N/A')} ({patient.get('email', 'N/A')})")
        
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
                self.consultations_table.setItem(row_index, 4, 
                    QTableWidgetItem(consultation.get('status', '')))
                
                # Diagnostic
                diagnostic = consultation.get('diagnostic', '')
                if diagnostic:
                    diagnostic = diagnostic[:30] + "..." if len(diagnostic) > 30 else diagnostic
                self.consultations_table.setItem(row_index, 5, 
                    QTableWidgetItem(diagnostic or "Non défini"))
                
                # Boutons d'action
                btn_layout = QHBoxLayout()
                edit_btn = QPushButton("Modifier")
                delete_btn = QPushButton("Supprimer")
                view_btn = QPushButton("Détails")
                
                edit_btn.clicked.connect(lambda _, c=consultation: self.show_edit_consultation_dialog(c))
                delete_btn.clicked.connect(lambda _, c=consultation: self.delete_consultation(c))
                view_btn.clicked.connect(lambda _, c=consultation: self.show_consultation_details(c))
                
                btn_widget = QWidget()
                btn_layout.addWidget(view_btn)
                btn_layout.addWidget(edit_btn)
                btn_layout.addWidget(delete_btn)
                btn_layout.setContentsMargins(0, 0, 0, 0)
                btn_widget.setLayout(btn_layout)
                
                self.consultations_table.setCellWidget(row_index, 6, btn_widget)
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def show_consultation_details(self, consultation):
        dialog = QDialog(self)
        dialog.setWindowTitle("Détails de la Consultation")
        dialog.resize(500, 400)
        
        layout = QVBoxLayout()
        
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
INFORMATIONS GÉNÉRALES
Patient: {patient_info}
Date: {date_str}
Statut: {consultation.get('status', 'Non défini')}
Créée le: {consultation.get('created_at', 'Non définie')}

MOTIF DE CONSULTATION
{consultation.get('motif', 'Non défini')}

DIAGNOSTIC
{consultation.get('diagnostic', 'Non défini')}

PRESCRIPTIONS
{prescriptions_text}
        """
        
        details_text.setPlainText(details_content.strip())
        
        layout.addWidget(details_text)
        
        # Bouton Fermer
        close_btn = QPushButton("Fermer")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.setLayout(layout)
        dialog.exec_()
    
    def delete_consultation(self, consultation):
        patient = self.main_window.database.get_user_by_id(consultation.get('patient_id'))
        patient_name = patient.get('name', 'Patient inconnu') if patient else 'Patient inconnu'
        
        reply = QMessageBox.question(
            self,
            "Confirmation",
            f"Êtes-vous sûr de vouloir supprimer la consultation avec {patient_name} ?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                self.main_window.database.delete_consultation(consultation['_id'])
                self.load_consultations()
                QMessageBox.information(self, "Succès", "Consultation supprimée avec succès.")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression: {str(e)}")