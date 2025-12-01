import os
import inspect
import google.generativeai as genai
from typing import List, Callable, Dict, Any, Optional
from healthmate_ai.core.logger import setup_logger

logger = setup_logger("LlmInfrastructure")

class ToolContext:
    """
    Context passed to tools, allowing them to request confirmation or access shared state.
    """
    def __init__(self):
        self.tool_confirmation = None # Placeholder for confirmation logic

    def request_confirmation(self, hint: str, payload: Dict[str, Any]):
        # Simulation of requesting confirmation
        logger.info(f"Tool requested confirmation: {hint}")
        # In a real app, this would pause execution and wait for user input.
        # For this simulation, we'll just log it.

class FunctionTool:
    """
    Wraps a python function to be used by the LLM.
    """
    def __init__(self, func: Callable):
        self.func = func
        self.name = func.__name__
        self.doc = func.__doc__ or ""

    def to_gemini_tool(self):
        """
        Returns the function in a format suitable for Gemini's tools list.
        Gemini Python SDK handles callable directly.
        """
        return self.func

class LlmAgent:
    """
    An agent powered by an LLM that can use tools.
    """
    def __init__(self, name: str, model_name: str = "gemini-2.5-flash-lite", instruction: str = "", tools: List[FunctionTool] = []):
        self.name = name
        self.instruction = instruction
        self.tools = tools
        self.tool_map = {t.name: t.func for t in tools}
        
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            logger.warning("GEMINI_API_KEY not found. Agent will not work correctly.")
        else:
            genai.configure(api_key=api_key)
            
        self.model = genai.GenerativeModel(
            model_name=model_name,
            tools=[t.to_gemini_tool() for t in tools],
            system_instruction=instruction
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)

    def send_message(self, message: str) -> str:
        """
        Sends a message to the agent and returns the response.
        """
        logger.info(f"[{self.name}] User: {message}")
        try:
            response = self.chat.send_message(message)
            text = response.text
            logger.info(f"[{self.name}] Agent: {text}")
            return text
        except Exception as e:
            logger.error(f"[{self.name}] Error: {e}")
            return f"I encountered an error: {str(e)}"
