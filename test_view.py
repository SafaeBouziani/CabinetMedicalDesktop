# test_patient_view.py
import sys
from PySide6.QtWidgets import QApplication
from datetime import datetime

from views.patientView import PatientView

# Mock classes
class MockMongoDB:
    def get_patient_consultations(self, user_id):
        return [
            {
                "date": datetime(2025, 6, 1, 14, 30),
                "doctor": "Dr. Ahmed",
                "motif": "Fever and headache",
                "status": "Completed"
            },
            {
                "date": datetime(2025, 6, 5, 9, 0),
                "doctor": "Dr. Fatima",
                "motif": "Routine Checkup",
                "status": "Scheduled"
            },
        ]

class MockMainWindow:
    def __init__(self):
        self.mongodb = MockMongoDB()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    mock_main_window = MockMainWindow()
    view = PatientView(mock_main_window)
    
    mock_user_data = {
        "user_id": "123456",
        "name": "John Doe"
    }

    view.load_data(mock_user_data)
    view.resize(800, 400)
    view.show()

    sys.exit(app.exec())
