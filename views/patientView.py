# views/patient_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QGroupBox, QHeaderView, QFrame
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from datetime import datetime

class PatientView(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.setup_ui()

    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f5f7fa;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
                color: #000000;
            }

            QLabel#Header {
                font-size: 22px;
                font-weight: bold;
                color: #2c3e50;
                margin-bottom: 10px;
            }

            QGroupBox {
                background-color: white;
                border-radius: 10px;
                padding: 15px;
                margin-top: 10px;
                box-shadow: 0px 4px 10px rgba(0,0,0,0.05);
                border: 1px solid #e0e0e0;
            }

            QGroupBox::title {
                font-weight: bold;
                color: #34495e;
                padding-left: 5px;
            }

            QTableWidget {
                background-color: white;
                border: none;
                border-radius: 5px;
            }

            QHeaderView::section {
                background-color: #3498db;
                color: white;
                padding: 8px;
                font-weight: bold;
                border: none;
            }

            QTableWidget::item {
                padding: 10px;
            }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 20, 30, 20)
        main_layout.setSpacing(20)

        # Title
        self.title = QLabel("👨‍⚕️ Patient Dashboard")
        self.title.setObjectName("Header")
        main_layout.addWidget(self.title)

        # Patient Info Box
        info_box = QGroupBox("Patient Information")
        info_layout = QVBoxLayout()
        self.info_label = QLabel("Loading...")
        self.info_label.setFont(QFont("Arial", 13))
        info_layout.addWidget(self.info_label)
        info_box.setLayout(info_layout)
        main_layout.addWidget(info_box)

        # Consultations Table
        table_box = QGroupBox("Consultation History")
        table_layout = QVBoxLayout()

        self.consultations_table = QTableWidget()
        self.consultations_table.setColumnCount(5)
        self.consultations_table.setHorizontalHeaderLabels(
            ["Date", "Time", "Doctor", "Reason", "Status"]
        )
        self.consultations_table.horizontalHeader().setStretchLastSection(True)
        self.consultations_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.consultations_table.verticalHeader().setVisible(False)
        self.consultations_table.setAlternatingRowColors(True)

        table_layout.addWidget(self.consultations_table)
        table_box.setLayout(table_layout)
        main_layout.addWidget(table_box)

    def load_data(self, user_data):
        self.user_data = user_data
        self.info_label.setText(f"<b>Name:</b> {user_data['name']}<br><b>ID:</b> {user_data['user_id']}")
        self.load_consultations()

    def load_consultations(self):
        consultations = self.main_window.mongodb.get_patient_consultations(
            self.user_data['user_id']
        )
        self.update_consultations_table(consultations)

    def update_consultations_table(self, consultations):
        self.consultations_table.setRowCount(len(consultations))
        for row, consultation in enumerate(consultations):
            date = consultation["date"]

            self.consultations_table.setItem(row, 0, QTableWidgetItem(date.strftime("%Y-%m-%d")))
            self.consultations_table.setItem(row, 1, QTableWidgetItem(date.strftime("%H:%M")))
            self.consultations_table.setItem(row, 2, QTableWidgetItem(consultation["doctor"]))
            self.consultations_table.setItem(row, 3, QTableWidgetItem(consultation["motif"]))

            # Color-code status
            status_item = QTableWidgetItem(consultation["status"])
            status = consultation["status"].lower()
            if "completed" in status:
                status_item.setBackground(Qt.green)
            elif "scheduled" in status:
                status_item.setBackground(Qt.yellow)
            elif "canceled" in status:
                status_item.setBackground(Qt.red)
            self.consultations_table.setItem(row, 4, status_item)
