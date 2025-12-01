import sqlite3
from typing import List, Dict, Any, Optional
from healthmate_ai.core.logger import setup_logger

logger = setup_logger("DoctorDatabaseTool")

class DoctorDatabaseTool:
    """
    A specialized database tool for Doctor Agents to avoid modifying the core DatabaseTool.
    """
    def __init__(self, db_path: str = "healthmate.db"):
        self.db_path = db_path

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def get_doctor_appointments(self, doctor_id: str, date: str) -> List[Dict[str, Any]]:
        """
        Fetches appointments for a specific doctor on a specific date.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Note: The date in appointments table is a full datetime string (e.g., "2023-10-27 09:00")
        # We need to match the date part.
        query = '''
            SELECT a.appointment_id, a.date, a.status, p.patient_id, p.name, p.age, p.gender
            FROM appointments a
            JOIN patients p ON a.patient_id = p.patient_id
            WHERE a.doctor_id = ? AND a.date LIKE ?
            ORDER BY a.date ASC
        '''
        cursor.execute(query, (doctor_id, f"{date}%"))
        rows = cursor.fetchall()
        conn.close()
        
        appointments = []
        for row in rows:
            appointments.append({
                "appointment_id": row[0],
                "time": row[1].split(" ")[1] if " " in row[1] else row[1], # Extract time
                "status": row[2],
                "patient_id": row[3],
                "patient_name": row[4],
                "patient_age": row[5],
                "patient_gender": row[6]
            })
        return appointments

    def get_patient_details_extended(self, patient_id: str) -> Dict[str, Any]:
        """
        Fetches comprehensive patient details including history and reports.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # 1. Basic Info
        cursor.execute('SELECT * FROM patients WHERE patient_id = ?', (patient_id,))
        patient_row = cursor.fetchone()
        
        if not patient_row:
            conn.close()
            return {}

        patient_info = {
            'patient_id': patient_row[0],
            'name': patient_row[1],
            'age': patient_row[2],
            'gender': patient_row[3],
            'phone': patient_row[4],
            'email': patient_row[5]
        }

        # 2. Visit History
        cursor.execute('SELECT * FROM visits WHERE patient_id = ? ORDER BY timestamp DESC', (patient_id,))
        visit_rows = cursor.fetchall()
        visits = []
        for row in visit_rows:
            visits.append({
                'visit_id': row[0],
                'symptoms': row[2],
                'triage_summary': row[3],
                'severity': row[4],
                'department': row[5],
                'timestamp': row[6]
            })

        # 3. Medical Reports
        cursor.execute('SELECT * FROM medical_reports WHERE patient_id = ?', (patient_id,))
        report_rows = cursor.fetchall()
        reports = []
        for row in report_rows:
            reports.append({
                'report_id': row[0],
                'extracted_data': row[2] # This is a JSON string
            })

        conn.close()
        
        return {
            "info": patient_info,
            "visits": visits,
            "reports": reports
        }
