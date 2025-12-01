from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import random

class SchedulingOpenAPITool:
    """
    Mock implementation of an OpenAPI client for scheduling.
    """
    def __init__(self):
        self.doctors = {
            "cardiology": ["Dr. Smith", "Dr. Jones"],
            "general": ["Dr. Doe", "Dr. White"],
            "neurology": ["Dr. Strange"]
        }

    def get_available_slots(self, department: str, date: str) -> List[str]:
        """
        Returns available time slots for a given department and date.
        """
        if department.lower() not in self.doctors:
            return []
        
        # Mock logic: generate random slots
        slots = ["09:00", "10:00", "11:00", "14:00", "15:00", "16:00"]
        # Randomly remove some slots to simulate unavailability
        return [s for s in slots if random.choice([True, True, False])]

    def book_appointment(self, doctor_id: str, date: str, time: str, patient_id: str) -> Dict[str, Any]:
        """
        Books an appointment.
        """
        # Mock booking confirmation
        return {
            "status": "confirmed",
            "appointment_id": f"apt_{random.randint(1000, 9999)}",
            "doctor_id": doctor_id,
            "date": f"{date} {time}",
            "patient_id": patient_id
        }

    def get_doctor_for_department(self, department: str) -> Optional[str]:
        deps = self.doctors.get(department.lower())
        if deps:
            return deps[0] # Return first doctor for simplicity
        return None
