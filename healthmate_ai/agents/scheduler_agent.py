from typing import Dict, Any
from healthmate_ai.tools.scheduling_openapi_tool import SchedulingOpenAPITool
from healthmate_ai.core.tracing import trace_agent
from healthmate_ai.core.logger import setup_logger

logger = setup_logger("SchedulerAgent")

class SchedulerAgent:
    def __init__(self):
        self.scheduler_tool = SchedulingOpenAPITool()

    @trace_agent
    def schedule_appointment(self, patient_id: str, department: str, preferred_date: str) -> Dict[str, Any]:
        logger.info(f"Scheduling appointment for {patient_id} in {department} on {preferred_date}")
        
        # 1. Find doctor
        doctor_id = self.scheduler_tool.get_doctor_for_department(department)
        if not doctor_id:
            return {"status": "failed", "reason": "No doctor available for department"}

        # 2. Check availability (Sequential decision making)
        slots = self.scheduler_tool.get_available_slots(department, preferred_date)
        if not slots:
            # Retry logic: Try next day (simplified)
            logger.info("No slots today, trying next day...")
            # In real app, increment date. Here just fail for simplicity or mock success
            return {"status": "failed", "reason": "No slots available"}

        # 3. Choose earliest slot
        best_slot = slots[0]
        
        # 4. Book
        booking = self.scheduler_tool.book_appointment(doctor_id, preferred_date, best_slot, patient_id)
        logger.info(f"Booked: {booking}")
        return booking
