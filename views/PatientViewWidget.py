# views/patient_view.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
                              QPushButton, QLabel, QTableWidgetItem)

class PatientView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        
        # Informations du patient
        info_layout = QHBoxLayout()
        self.info_label = QLabel()
        info_layout.addWidget(self.info_label)
        
        # Tableau des consultations
        self.consultations_table = QTableWidget()
        self.consultations_table.setColumnCount(5)
        self.consultations_table.setHorizontalHeaderLabels(
            ["Date", "Heure", "Docteur", "Motif", "Statut"]
        )
        
        layout.addLayout(info_layout)
        layout.addWidget(self.consultations_table)
        
        self.setLayout(layout)
    
    def load_data(self, user_data):
        self.user_data = user_data
        self.info_label.setText(f"Patient: {user_data['name']}")
        self.load_consultations()
    
    def load_consultations(self):
        consultations = self.main_window.mongodb.get_patient_consultations(
            self.user_data['user_id']
        )
        self.update_consultations_table(consultations)

# Pour PatientView et DoctorView
def update_consultations_table(self, consultations):
    self.consultations_table.setRowCount(len(consultations))
    for row, consultation in enumerate(consultations):
        date = consultation['date']
        self.consultations_table.setItem(row, 0, QTableWidgetItem(
            date.strftime("%Y-%m-%d")))
        self.consultations_table.setItem(row, 1, QTableWidgetItem(
            date.strftime("%H:%M")))
        self.consultations_table.setItem(row, 2, QTableWidgetItem(
            consultation['motif']))
        self.consultations_table.setItem(row, 3, QTableWidgetItem(
            consultation['status']))