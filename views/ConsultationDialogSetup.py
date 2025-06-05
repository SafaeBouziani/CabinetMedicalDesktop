# views/consultation_dialog.py
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QFormLayout, QLineEdit,
                              QDateTimeEdit, QTextEdit, QComboBox, QPushButton)
from datetime import datetime

class ConsultationDialog(QDialog):
    def __init__(self, main_window, doctor_data, consultation=None):
        super().__init__()
        self.main_window = main_window
        self.doctor_data = doctor_data
        self.consultation = consultation
        self.setup_ui()
    
    def setup_ui(self):
        self.setWindowTitle("Nouvelle Consultation")
        layout = QVBoxLayout()
        
        form_layout = QFormLayout()
        
        self.patient_combo = QComboBox()
        self.load_patients()
        
        self.datetime_edit = QDateTimeEdit()
        self.datetime_edit.setDateTime(datetime.now())
        
        self.motif_edit = QTextEdit()
        
        form_layout.addRow("Patient:", self.patient_combo)
        form_layout.addRow("Date et Heure:", self.datetime_edit)
        form_layout.addRow("Motif:", self.motif_edit)
        
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Enregistrer")
        save_btn.clicked.connect(self.save_consultation)
        cancel_btn = QPushButton("Annuler")
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(form_layout)
        layout.addLayout(buttons_layout)
        
        self.setLayout(layout)
    
    def load_patients(self):
        patients = self.main_window.mongodb.get_patients()
        for patient in patients:
            self.patient_combo.addItem(
                patient['name'],
                userData=patient['_id']
            )
    
    def save_consultation(self):
        patient_id = self.patient_combo.currentData()
        date_time = self.datetime_edit.dateTime().toPython()
        motif = self.motif_edit.toPlainText()
        
        consultation_data = {
            "patient_id": patient_id,
            "doctor_id": self.doctor_data['user_id'],
            "date": date_time,
            "motif": motif,
            "status": "programmé"
        }
        
        try:
            self.main_window.mongodb.add_consultation(consultation_data)
            self.main_window.sync_manager.sync_consultation(consultation_data)
            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))