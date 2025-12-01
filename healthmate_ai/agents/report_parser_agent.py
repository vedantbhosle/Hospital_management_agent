from typing import Dict, Any
from healthmate_ai.tools.pdf_parser_tool import PDFParserTool
from healthmate_ai.core.tracing import trace_agent
from healthmate_ai.core.logger import setup_logger

logger = setup_logger("ReportParserAgent")

class ReportParserAgent:
    def __init__(self):
        self.pdf_tool = PDFParserTool()

    @trace_agent
    def process_report(self, file_path: str) -> Dict[str, Any]:
        logger.info(f"Processing report: {file_path}")
        try:
            data = self.pdf_tool.parse_report(file_path)
            # In a real agent, we might post-process this data with an LLM
            # to extract specific lab values.
            return {
                "status": "success",
                "data": data
            }
        except Exception as e:
            logger.error(f"Report processing failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
