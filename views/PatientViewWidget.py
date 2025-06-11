# views/PatientViewWidget.py
from PySide6.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTableWidget,
                              QPushButton, QHBoxLayout, QDialog, QFormLayout,
                              QLineEdit, QComboBox, QDialogButtonBox, QMessageBox,
                              QTableWidgetItem, QTextEdit, QDateTimeEdit, QLabel)
from PySide6.QtCore import QDateTime, Qt
from PySide6.QtGui import QColor  # Add this import
from datetime import datetime

class PatientView(QWidget):
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
            
            QPushButton[class="secondary"] {
                background-color: #6c757d;
            }
            
            QPushButton[class="secondary"]:hover {
                background-color: #545b62;
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
        
        # Onglet Mes Consultations
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
        self.consultations_table.setColumnCount(6)
        self.consultations_table.setHorizontalHeaderLabels([
            "ID", "Médecin", "Date", "Motif", "Statut", "Actions"
        ])
        
        # Améliorer l'apparence du tableau
        self.consultations_table.setAlternatingRowColors(True)
        self.consultations_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.consultations_table.verticalHeader().setVisible(False)
        
        # Ajuster les largeurs de colonnes
        header = self.consultations_table.horizontalHeader()
        header.setStretchLastSection(True)
        self.consultations_table.setColumnWidth(0, 80)   # ID
        self.consultations_table.setColumnWidth(1, 150)  # Médecin
        self.consultations_table.setColumnWidth(2, 130)  # Date
        self.consultations_table.setColumnWidth(3, 250)  # Motif
        self.consultations_table.setColumnWidth(4, 100)  # Statut
        
        consultations_layout.addWidget(self.consultations_table)
        
        # Bouton d'actualisation
        consultations_buttons = QHBoxLayout()
        consultations_buttons.setSpacing(10)
        
        refresh_btn = QPushButton("🔄 Actualiser")
        refresh_btn.setProperty("class", "secondary")
        refresh_btn.clicked.connect(self.load_consultations)
        
        consultations_buttons.addWidget(refresh_btn)
        consultations_buttons.addStretch()
        
        consultations_layout.addLayout(consultations_buttons)
        consultations_tab.setLayout(consultations_layout)
        
        # Ajouter l'onglet
        self.tab_widget.addTab(consultations_tab, "📋 Mes Consultations")
        
        layout.addWidget(self.tab_widget)
        self.setLayout(layout)
    
    def load_data(self, user_data):
        self.user_data = user_data
        self.welcome_label.setText(f"👤 Bienvenue {user_data.get('name', user_data.get('username'))}")
        self.load_consultations()
    
    def load_consultations(self, status_filter=None):
        self.consultations_table.setRowCount(0)
        
        try:
            # Récupérer les consultations du patient connecté
            consultations = self.main_window.database.get_consultations_by_patient(
                str(self.user_data['_id'])
            )
            
            # Filtrer par statut si nécessaire
            if status_filter:
                consultations = [c for c in consultations if c.get('status') == status_filter]
            
            for row_index, consultation in enumerate(consultations):
                self.consultations_table.insertRow(row_index)
                
                # ID
                self.consultations_table.setItem(row_index, 0, 
                    QTableWidgetItem(str(consultation.get('_id', ''))))
                
                # Médecin
                doctor = self.main_window.database.get_user_by_id(consultation.get('doctor_id'))
                doctor_name = f"Dr. {doctor.get('name', 'Médecin inconnu')}" if doctor else 'Médecin inconnu'
                self.consultations_table.setItem(row_index, 1, 
                    QTableWidgetItem(doctor_name))
                
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
                motif = consultation.get('motif', '')
                if len(motif) > 50:
                    motif = motif[:50] + "..."
                self.consultations_table.setItem(row_index, 3, 
                    QTableWidgetItem(motif))
                
                # Statut
                status_item = QTableWidgetItem(consultation.get('status', ''))
                # Colorer les statuts
                status = consultation.get('status', '')
                if status == 'terminé':
                    status_item.setBackground(QColor('lightgreen'))
                elif status == 'en_cours':
                    status_item.setBackground(QColor('yellow'))
                elif status == 'annulé':
                    status_item.setBackground(QColor('lightcoral'))
                elif status == 'programmé':
                    status_item.setBackground(QColor('lightblue'))  # Fixed this line
                self.consultations_table.setItem(row_index, 4, status_item)
                
                # Bouton d'action (uniquement visualisation)
                btn_layout = QHBoxLayout()
                btn_layout.setSpacing(5)
                btn_layout.setContentsMargins(5, 2, 5, 2)
                
                view_btn = QPushButton("👁️ Voir")
                view_btn.setToolTip("Voir les détails")
                view_btn.setProperty("class", "secondary")
                view_btn.clicked.connect(lambda _, c=consultation: self.show_consultation_details(c))
                
                btn_widget = QWidget()
                btn_layout.addWidget(view_btn)
                btn_layout.addStretch()
                btn_widget.setLayout(btn_layout)
                
                self.consultations_table.setCellWidget(row_index, 5, btn_widget)
                
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors du chargement: {str(e)}")
    
    def show_consultation_details(self, consultation):
        dialog = QDialog(self)
        dialog.setWindowTitle("Détails de la Consultation")
        dialog.resize(550, 500)
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
        
        # Récupérer les informations du médecin
        doctor = self.main_window.database.get_user_by_id(consultation.get('doctor_id'))
        doctor_info = f"Dr. {doctor.get('name', 'N/A')} ({doctor.get('email', 'N/A')})" if doctor else "Médecin inconnu"
        
        # Date formatée
        date_str = "Non définie"
        if consultation.get('date'):
            if isinstance(consultation['date'], datetime):
                date_str = consultation['date'].strftime("%d/%m/%Y à %H:%M")
            else:
                date_str = str(consultation['date'])
        
        # Prescriptions formatées
        prescriptions_text = "Aucune prescription"
        if consultation.get('prescriptions'):
            prescriptions_text = '\n'.join([f"• {p}" for p in consultation['prescriptions']])
        
        # Statut avec emoji
        status_emoji = {
            'programmé': '📅',
            'en_cours': '⏳',
            'terminé': '✅',
            'annulé': '❌'
        }
        status_display = f"{status_emoji.get(consultation.get('status', ''), '📋')} {consultation.get('status', 'Non défini')}"
        
        details_content = f"""
📋 INFORMATIONS GÉNÉRALES
═══════════════════════════════════════════════════════════════
👨‍⚕️ Médecin: {doctor_info}
📅 Date: {date_str}
🏷️ Statut: {status_display}
⏰ Créée le: {consultation.get('created_at', 'Non définie')}

💬 MOTIF DE CONSULTATION
═══════════════════════════════════════════════════════════════
{consultation.get('motif', 'Non défini')}

🔍 DIAGNOSTIC
═══════════════════════════════════════════════════════════════
{consultation.get('diagnostic', 'Pas encore de diagnostic')}

💊 PRESCRIPTIONS
═══════════════════════════════════════════════════════════════
{prescriptions_text}
        """
        
        details_text.setPlainText(details_content.strip())
        
        layout.addWidget(details_text)
        
        # Bouton Fermer
        close_btn = QPushButton("✖️ Fermer")
        close_btn.setProperty("class", "secondary")
        close_btn.clicked.connect(dialog.accept)
        
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        layout.addLayout(btn_layout)
        
        dialog.setLayout(layout)
        dialog.exec_()

'''# views/patient_view.py
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem,
    QLabel, QGroupBox, QHeaderView, QFrame
)
from PySide6.QtGui import QFont, QIcon
from PySide6.QtCore import Qt
from datetime import datetime
import traceback
from neo4j_consultation_service import ConsultationService  # Assuming this is the correct import path for your service

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
        self.title = QLabel("👨‍⚕️ Dashboard Patient ")
        self.title.setObjectName("Header")
        main_layout.addWidget(self.title)

        # Patient Info Box
        info_box = QGroupBox("Informations Patient ")
        info_layout = QVBoxLayout()
        self.info_label = QLabel("Loading...")
        self.info_label.setFont(QFont("Arial", 13))
        info_layout.addWidget(self.info_label)
        info_box.setLayout(info_layout)
        main_layout.addWidget(info_box)

        # Consultations Table
        table_box = QGroupBox("Consultations ")
        table_layout = QVBoxLayout()

        self.consultations_table = QTableWidget()
        self.consultations_table.setColumnCount(5)
        self.consultations_table.setHorizontalHeaderLabels(
            ["Date", "Heure", "Docteur", "Motif", "Status"]
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
        self.info_label.setText(f"<b>Name:</b> {user_data['name']}<br><b>ID:</b> {user_data['_id']}")
        self.load_consultations()

    
    def load_consultations(self):
        try:
            user_id = str(self.user_data["_id"])
            user_name = self.user_data.get("name", "Nom inconnu")
            print(f"[DEBUG] Loading consultations for user_id = {user_id}, name = {user_name}")
            
            service = ConsultationService(self.main_window.database.mongodb)
            consultations = service.get_consultations(user_id)

            # Inject current user's name in case it's needed
            for c in consultations:
                if "patient" not in c:
                    c["patient"] = user_name

            print(f"[DEBUG] Retrieved consultations: {consultations}")
            self.update_consultations_table(consultations)
        except Exception as e:
            print(f"[ERROR] Erreur lors du chargement des consultations : {e}")
            traceback.print_exc()
            
    def update_consultations_table(self, consultations):
        self.consultations_table.setRowCount(len(consultations))

        for row, consultation in enumerate(consultations):
            # 1. Parse date safely
            date_value = consultation["date"]
            if isinstance(date_value, str):
                try:
                    date = datetime.fromisoformat(date_value)
                except ValueError:
                    print(f"[WARN] Invalid date format: {date_value}")
                    date = datetime.now()
            else:
                date = date_value.to_native() if hasattr(date_value, 'to_native') else date_value

            # 2. Set each column
            self.consultations_table.setItem(row, 0, QTableWidgetItem(date.strftime("%Y-%m-%d")))  # Date
            self.consultations_table.setItem(row, 1, QTableWidgetItem(date.strftime("%H:%M")))     # Heure
            self.consultations_table.setItem(row, 2, QTableWidgetItem(consultation.get("doctor", "N/A")))  # Docteur
            self.consultations_table.setItem(row, 3, QTableWidgetItem(consultation.get("motif", "—")))      # Motif

            # 3. Status with color coding
            status_text = consultation.get("status", "Inconnu").lower()
            status_item = QTableWidgetItem(status_text.capitalize())

            if "complet" in status_text:
                status_item.setBackground(Qt.green)
            elif "programmé" in status_text or "schedul" in status_text:
                status_item.setBackground(Qt.yellow)
            elif "annul" in status_text or "cancel" in status_text:
                status_item.setBackground(Qt.red)

            self.consultations_table.setItem(row, 4, status_item)  # Status
'''