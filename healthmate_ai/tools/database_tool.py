import sqlite3
import json
from datetime import datetime
from typing import Dict, List, Optional, Any

class DatabaseTool:
    def __init__(self, db_path: str = "healthmate.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self._get_connection()
        cursor = conn.cursor()

        # Patients table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id TEXT PRIMARY KEY,
                name TEXT,
                age INTEGER,
                gender TEXT,
                phone TEXT,
                email TEXT
            )
        ''')

        # Visits table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS visits (
                visit_id TEXT PRIMARY KEY,
                patient_id TEXT,
                symptoms TEXT,
                triage_summary TEXT,
                severity TEXT,
                department TEXT,
                timestamp TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
            )
        ''')

        # Appointments table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                appointment_id TEXT PRIMARY KEY,
                patient_id TEXT,
                doctor_id TEXT,
                date TEXT,
                status TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
            )
        ''')

        # Medical Reports table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS medical_reports (
                report_id TEXT PRIMARY KEY,
                patient_id TEXT,
                extracted_data TEXT,
                FOREIGN KEY(patient_id) REFERENCES patients(patient_id)
            )
        ''')

        # Reminders table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                reminder_id TEXT PRIMARY KEY,
                appointment_id TEXT,
                reminder_date TEXT,
                sent_flag INTEGER DEFAULT 0,
                FOREIGN KEY(appointment_id) REFERENCES appointments(appointment_id)
            )
        ''')

        conn.commit()
        conn.close()

    def add_patient(self, patient_data: Dict[str, Any]):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO patients (patient_id, name, age, gender, phone, email)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            patient_data['patient_id'],
            patient_data['name'],
            patient_data['age'],
            patient_data['gender'],
            patient_data['phone'],
            patient_data['email']
        ))
        conn.commit()
        conn.close()

    def get_patient(self, patient_id: str) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                'patient_id': row[0],
                'name': row[1],
                'age': row[2],
                'gender': row[3],
                'phone': row[4],
                'email': row[5]
            }
        return None

    def find_patient_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM patients WHERE name = ?', (name,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {
                'patient_id': row[0],
                'name': row[1],
                'age': row[2],
                'gender': row[3],
                'phone': row[4],
                'email': row[5]
            }
        return None

    def add_visit(self, visit_data: Dict[str, Any]):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO visits (visit_id, patient_id, symptoms, triage_summary, severity, department, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            visit_data['visit_id'],
            visit_data['patient_id'],
            visit_data['symptoms'],
            visit_data['triage_summary'],
            visit_data['severity'],
            visit_data['department'],
            visit_data.get('timestamp', datetime.now().isoformat())
        ))
        conn.commit()
        conn.close()
    
    def get_patient_history(self, patient_id: str) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM visits WHERE patient_id = ? ORDER BY timestamp DESC', (patient_id,))
        rows = cursor.fetchall()
        conn.close()
        history = []
        for row in rows:
            history.append({
                'visit_id': row[0],
                'patient_id': row[1],
                'symptoms': row[2],
                'triage_summary': row[3],
                'severity': row[4],
                'department': row[5],
                'timestamp': row[6]
            })
        return history

    def add_appointment(self, appointment_data: Dict[str, Any]):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO appointments (appointment_id, patient_id, doctor_id, date, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            appointment_data['appointment_id'],
            appointment_data['patient_id'],
            appointment_data['doctor_id'],
            appointment_data['date'],
            appointment_data['status']
        ))
        conn.commit()
        conn.close()

    def add_medical_report(self, report_data: Dict[str, Any]):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO medical_reports (report_id, patient_id, extracted_data)
            VALUES (?, ?, ?)
        ''', (
            report_data['report_id'],
            report_data['patient_id'],
            json.dumps(report_data['extracted_data'])
        ))
        conn.commit()
        conn.close()

    def add_reminder(self, reminder_data: Dict[str, Any]):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reminders (reminder_id, appointment_id, reminder_date, sent_flag)
            VALUES (?, ?, ?, ?)
        ''', (
            reminder_data['reminder_id'],
            reminder_data['appointment_id'],
            reminder_data['reminder_date'],
            0
        ))
        conn.commit()
        conn.close()

    def get_pending_reminders(self) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        cursor = conn.cursor()
        now = datetime.now().isoformat()
        # Simple check: reminders that are due and not sent
        # For simulation, we might just fetch all unsent
        cursor.execute('SELECT * FROM reminders WHERE sent_flag = 0')
        rows = cursor.fetchall()
        conn.close()
        reminders = []
        for row in rows:
            reminders.append({
                'reminder_id': row[0],
                'appointment_id': row[1],
                'reminder_date': row[2],
                'sent_flag': row[3]
            })
        return reminders

    def mark_reminder_sent(self, reminder_id: str):
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute('UPDATE reminders SET sent_flag = 1 WHERE reminder_id = ?', (reminder_id,))
        conn.commit()
        conn.close()
