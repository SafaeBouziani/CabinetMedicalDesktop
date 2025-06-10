# views/MainWindowSetup.py
from ConfigManagement import Config
from PySide6.QtWidgets import QMainWindow, QStackedWidget, QMessageBox
from views.LoginDialogSetup import LoginDialog
from views.PatientViewWidget import PatientView
from views.DoctorConsultationView import DoctorView
from views.AdminViewWidget import AdminView

class MainWindow(QMainWindow):
    def __init__(self, mongodb, neo4j, sync_manager, auth_manager,database):
        super().__init__()
        self.mongodb = mongodb
        self.neo4j = neo4j
        self.sync_manager = sync_manager
        self.auth_manager = auth_manager
        self.database = database
        self.token = None
        self.user_data = None
        self.setup_ui()
        self.show_login()
    
    def setup_ui(self):
        self.setWindowTitle(Config.APP_NAME)
        self.setGeometry(80, 80,
                        Config.WINDOW_SIZE['width'], 
                        Config.WINDOW_SIZE['height'])
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Créer les différentes vues
        self.patient_view = PatientView(self)
        self.doctor_view = DoctorView(self)
        self.admin_view = AdminView(self)
        
        # Ajouter les vues au stacked widget
        self.stacked_widget.addWidget(self.patient_view)
        self.stacked_widget.addWidget(self.doctor_view)
        self.stacked_widget.addWidget(self.admin_view)
    
    def show_login(self):
        login_dialog = LoginDialog(self.auth_manager)
        if login_dialog.exec_():
            self.user_data = login_dialog.user_data
            print("User data received:", self.user_data)
            self.show_appropriate_view()
        else:
            self.close()

    def show_appropriate_view(self):
        try:
            role = self.user_data['role']
            if role == 'patient':
                self.stacked_widget.setCurrentWidget(self.patient_view)
                self.patient_view.load_data(self.user_data)
            elif role == 'doctor':
                self.stacked_widget.setCurrentWidget(self.doctor_view)
                self.doctor_view.load_data(self.user_data)
            elif role == 'admin':
                self.stacked_widget.setCurrentWidget(self.admin_view)
                self.admin_view.load_data(self.user_data)
            else:
                raise ValueError(f"Unknown role: {role}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur de redirection: {e}")
            self.close()
