from healthmate_ai.core.llm_infrastructure import LlmAgent, FunctionTool
from healthmate_ai.tools.doctor_tools_definitions import get_doctor_schedule, get_patient_list_for_date
from healthmate_ai.core.logger import setup_logger

logger = setup_logger("DoctorScheduleAgent")

class DoctorScheduleAgent:
    """
    LLM-powered agent responsible for helping the doctor know their schedule.
    """
    def __init__(self):
        self.agent = LlmAgent(
            name="DoctorScheduleAgent",
            instruction="""You are a helpful and efficient assistant for a doctor. 
            Your primary goal is to help the doctor manage and understand their daily schedule.
            
            You have access to tools to fetch the schedule and list patients.
            
            When asked about the schedule:
            1. Use `get_doctor_schedule` to retrieve the appointments.
            2. Provide a clear, chronological summary of the day.
            3. Highlight any critical information (though currently we only have basic status).
            4. If the schedule is empty, inform the doctor politely.
            
            Be concise, professional, and friendly.
            """,
            tools=[
                FunctionTool(get_doctor_schedule),
                FunctionTool(get_patient_list_for_date)
            ]
        )

    def process_query(self, query: str) -> str:
        """
        Processes a natural language query from the doctor.
        """
        logger.info(f"Processing query: {query}")
        return self.agent.send_message(query)
