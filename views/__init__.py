# views/__init__.py
from .MainWindowSetup import MainWindow
from .LoginDialogSetup import LoginDialog
from .PatientViewWidget import PatientView
from .DoctorConsultationView import DoctorView
from .AdminViewWidget import AdminView
from .ConsultationDialogSetup import ConsultationDialog

__all__ = [
    'MainWindow',
    'LoginDialog',
    'PatientView',
    'DoctorView',
    'AdminView',
    'ConsultationDialog'
]