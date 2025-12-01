from healthmate_ai.core.llm_infrastructure import LlmAgent, FunctionTool
from healthmate_ai.tools.doctor_tools_definitions import get_patient_insight
from healthmate_ai.core.logger import setup_logger

logger = setup_logger("PatientInsightAgent")

class PatientInsightAgent:
    """
    LLM-powered agent responsible for providing detailed insights about patients.
    """
    def __init__(self):
        self.agent = LlmAgent(
            name="PatientInsightAgent",
            instruction="""You are a highly knowledgeable medical insight assistant.
            Your role is to assist the doctor by providing comprehensive summaries of patient data.
            
            You have access to `get_patient_insight` to fetch patient details, history, and reports.
            
            When asked about a patient:
            1. Use the tool to get the data.
            2. Synthesize the information into a clear, professional medical summary.
            3. Mention key demographics, recent visit reasons, and any critical findings from reports.
            4. If report data is in JSON format, interpret it for the doctor (e.g., "BP is 140/90, which is elevated").
            
            Maintain a professional, clinical tone.
            """,
            tools=[
                FunctionTool(get_patient_insight)
            ]
        )

    def process_query(self, query: str) -> str:
        """
        Processes a natural language query from the doctor.
        """
        logger.info(f"Processing query: {query}")
        return self.agent.send_message(query)
