# views/DoctorConsultationView.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                              QPushButton, QLabel, QCalendarWidget, QTableWidgetItem,
                              QMessageBox)
from .ConsultationDialogSetup import ConsultationDialog
from datetime import datetime

class DoctorView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout()
        
        # Panneau gauche - Calendrier et informations
        left_panel = QVBoxLayout()
        
        self.info_label = QLabel("Dr. ")
        left_panel.addWidget(self.info_label)
        
        self.calendar = QCalendarWidget()
        self.calendar.selectionChanged.connect(self.load_day_consultations)
        left_panel.addWidget(self.calendar)
        
        # Panneau droit - Liste des consultations
        right_panel = QVBoxLayout()
        
        # Boutons en haut
        buttons_layout = QHBoxLayout()
        self.add_consultation_btn = QPushButton("Nouvelle Consultation")
        self.add_consultation_btn.clicked.connect(self.show_add_consultation)
        self.refresh_btn = QPushButton("Rafraîchir")
        self.refresh_btn.clicked.connect(self.load_day_consultations)
        
        buttons_layout.addWidget(self.add_consultation_btn)
        buttons_layout.addWidget(self.refresh_btn)
        
        # Tableau des consultations
        self.consultations_table = QTableWidget()
        self.consultations_table.setColumnCount(4)
        self.consultations_table.setHorizontalHeaderLabels(
            ["Heure", "Patient", "Motif", "Statut"]
        )
        self.consultations_table.horizontalHeader().setStretchLastSection(True)
        self.consultations_table.setSelectionBehavior(QTableWidget.SelectRows)
        
        right_panel.addLayout(buttons_layout)
        right_panel.addWidget(self.consultations_table)
        
        # Assembler les panneaux
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        
        layout.addWidget(left_widget, 1)
        layout.addWidget(right_widget, 2)
        
        self.setLayout(layout)
    
    def load_data(self, user_data):
        self.user_data = user_data
        self.info_label.setText(f"Dr. {user_data.get('name', 'Inconnu')} - ID: {user_data.get('user_id', 'N/A')}")
        self.load_day_consultations()
    
    def load_day_consultations(self):
        try:
            date = self.calendar.selectedDate().toPython()
            consultations = self.main_window.mongodb.get_doctor_consultations(
                self.user_data['user_id'],
                date
            )
            self.update_consultations_table(consultations)
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible de charger les consultations : {str(e)}")
    
    def show_add_consultation(self):
        try:
            dialog = ConsultationDialog(self.main_window, self.user_data)
            if dialog.exec_():
                self.load_day_consultations()
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Impossible d'ajouter la consultation : {str(e)}")

    def update_consultations_table(self, consultations):
        self.consultations_table.setRowCount(0)
        self.consultations_table.setRowCount(len(consultations))
        
        for row, consultation in enumerate(consultations):
            try:
                date = consultation['date']
                patient = self.get_patient_name(consultation['patient_id'])
                
                self.consultations_table.setItem(row, 0, QTableWidgetItem(
                    date.strftime("%H:%M")))
                self.consultations_table.setItem(row, 1, QTableWidgetItem(patient))
                self.consultations_table.setItem(row, 2, QTableWidgetItem(
                    consultation.get('motif', '')))
                self.consultations_table.setItem(row, 3, QTableWidgetItem(
                    consultation.get('status', '')))
                
            except Exception as e:
                print(f"Erreur lors de l'ajout de la consultation {row}: {str(e)}")
    
    def get_patient_name(self, patient_id):
        try:
            patient = self.main_window.mongodb.users.find_one({"_id": patient_id})
            return patient.get('name', 'Patient inconnu') if patient else 'Patient inconnu'
        except Exception:
            return 'Patient inconnu'