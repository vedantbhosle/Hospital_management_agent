from typing import List, Dict, Any
from healthmate_ai.tools.database_tool import DatabaseTool

class MemoryBank:
    def __init__(self, db_tool: DatabaseTool):
        self.db_tool = db_tool

    def get_patient_context(self, patient_id: str) -> Dict[str, Any]:
        """
        Retrieves comprehensive patient context including:
        - Basic info
        - Past visits
        - Recent medical reports (metadata)
        """
        patient = self.db_tool.get_patient(patient_id)
        if not patient:
            return {}

        history = self.db_tool.get_patient_history(patient_id)
        
        # In a real system, we might also fetch report summaries here
        
        return {
            "patient_info": patient,
            "visit_history": history
        }

    def store_visit_summary(self, visit_data: Dict[str, Any]):
        self.db_tool.add_visit(visit_data)
