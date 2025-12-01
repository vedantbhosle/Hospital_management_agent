from typing import Dict, Any, List
from healthmate_ai.tools.doctor_database_tool import DoctorDatabaseTool

# Initialize the database tool globally for these functions to use
_db_tool = DoctorDatabaseTool()

def get_doctor_schedule(doctor_id: str, date: str) -> Dict[str, Any]:
    """
    Retrieves the schedule for a specific doctor on a given date.

    Args:
        doctor_id: The ID of the doctor (e.g., "Dr. Smith").
        date: The date in YYYY-MM-DD format.

    Returns:
        A dictionary containing the list of appointments.
    """
    appointments = _db_tool.get_doctor_appointments(doctor_id, date)
    return {
        "doctor_id": doctor_id,
        "date": date,
        "appointments": appointments,
        "count": len(appointments)
    }

def get_patient_insight(patient_id: str) -> Dict[str, Any]:
    """
    Retrieves detailed medical insights for a specific patient.

    Args:
        patient_id: The ID of the patient.

    Returns:
        A dictionary with patient info, visit history, and medical reports.
    """
    data = _db_tool.get_patient_details_extended(patient_id)
    if not data:
        return {"error": "Patient not found"}
    return data

def get_patient_list_for_date(doctor_id: str, date: str) -> List[Dict[str, str]]:
    """
    Returns a simple list of patients (ID and Name) that the doctor is seeing on a specific date.
    Useful for quick lookups.

    Args:
        doctor_id: The ID of the doctor.
        date: The date in YYYY-MM-DD format.

    Returns:
        List of dicts with 'patient_id' and 'name'.
    """
    appointments = _db_tool.get_doctor_appointments(doctor_id, date)
    return [{"patient_id": a["patient_id"], "name": a["patient_name"]} for a in appointments]
