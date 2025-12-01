import sys
import os
import uuid
from datetime import datetime

# Add current directory to path
sys.path.append(os.getcwd())

from healthmate_ai.tools.database_tool import DatabaseTool

def seed():
    print("Seeding database...")
    db = DatabaseTool()
    
    # 1. Add Patient
    patient_id = "p_001"
    db.add_patient({
        "patient_id": patient_id,
        "name": "John Doe",
        "age": 45,
        "gender": "Male",
        "phone": "555-1234",
        "email": "john@example.com"
    })
    print(f"Added patient {patient_id}")
    
    # 2. Add Visit
    visit_id = "v_001"
    db.add_visit({
        "visit_id": visit_id,
        "patient_id": patient_id,
        "symptoms": "Chest pain",
        "triage_summary": "Patient reports chest pain. Critical.",
        "severity": "Critical",
        "department": "Cardiology",
        "timestamp": datetime.now().isoformat()
    })
    print(f"Added visit {visit_id}")
    
    # 3. Add Appointment
    today = datetime.now().strftime("%Y-%m-%d")
    appt_id = "appt_001"
    db.add_appointment({
        "appointment_id": appt_id,
        "patient_id": patient_id,
        "doctor_id": "Dr. Smith",
        "date": f"{today} 09:00",
        "status": "confirmed"
    })
    print(f"Added appointment {appt_id} for Dr. Smith on {today}")
    
    # 4. Add Report
    report_id = "r_001"
    db.add_medical_report({
        "report_id": report_id,
        "patient_id": patient_id,
        "extracted_data": {"cholesterol": "high", "bp": "140/90"}
    })
    print(f"Added report {report_id}")
    
    print("Seeding complete.")

if __name__ == "__main__":
    seed()
