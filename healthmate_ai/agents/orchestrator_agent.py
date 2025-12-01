import asyncio
import uuid
from datetime import datetime
from typing import Dict, Any, Optional

from healthmate_ai.agents.triage_agent import TriageAgent
from healthmate_ai.agents.report_parser_agent import ReportParserAgent
from healthmate_ai.agents.scheduler_agent import SchedulerAgent
from healthmate_ai.agents.reminder_agent import ReminderAgent
from healthmate_ai.tools.database_tool import DatabaseTool
from healthmate_ai.core.session_memory import SessionMemory
from healthmate_ai.core.memory_bank import MemoryBank
from healthmate_ai.core.tracing import trace_agent
from healthmate_ai.core.logger import setup_logger

logger = setup_logger("OrchestratorAgent")

class OrchestratorAgent:
    def __init__(self):
        self.db_tool = DatabaseTool()
        self.session = SessionMemory()
        self.memory_bank = MemoryBank(self.db_tool)
        
        self.triage_agent = TriageAgent()
        self.report_agent = ReportParserAgent()
        self.scheduler_agent = SchedulerAgent()
        # Reminder agent is usually a background process, but we can trigger it here for simulation
        self.reminder_agent = ReminderAgent(self.db_tool)

    @trace_agent
    async def process_patient_request(self, 
                                      patient_id: str, 
                                      symptoms: str, 
                                      report_path: Optional[str] = None) -> Dict[str, Any]:
        
        logger.info(f"Starting workflow for patient {patient_id}")
        
        # 1. Load Context
        context = self.memory_bank.get_patient_context(patient_id)
        self.session.add_message("system", f"Loaded context for {patient_id}")

        # 2. Parallel Execution: Triage & Report Parsing
        tasks = [self._run_triage(symptoms)]
        if report_path:
            tasks.append(self._run_report_parsing(report_path))
        
        results = await asyncio.gather(*tasks)
        triage_result = results[0]
        report_result = results[1] if report_path else None

        # 3. Store Visit Data
        visit_id = str(uuid.uuid4())
        self.db_tool.add_visit({
            "visit_id": visit_id,
            "patient_id": patient_id,
            "symptoms": symptoms,
            "triage_summary": triage_result.get("summary"),
            "severity": triage_result.get("severity"),
            "department": triage_result.get("department"),
            "timestamp": datetime.now().isoformat()
        })

        # 4. Sequential Execution: Scheduling
        appointment = None
        if triage_result.get("department"):
            # Auto-schedule for today for simplicity
            today = datetime.now().strftime("%Y-%m-%d")
            appointment = self.scheduler_agent.schedule_appointment(
                patient_id, 
                triage_result["department"], 
                today
            )
            
            if appointment and appointment.get("status") == "confirmed":
                self.db_tool.add_appointment(appointment)
                # Schedule reminder
                self.db_tool.add_reminder({
                    "reminder_id": str(uuid.uuid4()),
                    "appointment_id": appointment["appointment_id"],
                    "reminder_date": today # Mock: remind immediately
                })

        # 5. Trigger Reminder Cycle (Simulation)
        self.reminder_agent.run_cycle()

        # 6. Final Summary
        summary = {
            "patient_id": patient_id,
            "triage": triage_result,
            "report_analysis": report_result,
            "appointment": appointment
        }
        
        logger.info("Workflow completed.")
        return summary

    async def _run_triage(self, symptoms: str):
        return self.triage_agent.analyze_symptoms(symptoms)

    async def _run_report_parsing(self, path: str):
        return self.report_agent.process_report(path)
