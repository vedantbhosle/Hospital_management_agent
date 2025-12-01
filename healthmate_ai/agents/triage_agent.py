import os
import google.generativeai as genai
from typing import Dict, Any
from healthmate_ai.core.tracing import trace_agent
from healthmate_ai.core.logger import setup_logger

logger = setup_logger("TriageAgent")

class TriageAgent:
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            logger.warning("GEMINI_API_KEY not found. Triage agent will use mock responses.")
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-2.5-flash-lite')

    @trace_agent
    def analyze_symptoms(self, symptoms: str) -> Dict[str, Any]:
        logger.info(f"Analyzing symptoms: {symptoms}")
        
        if not self.api_key:
            return self._mock_analysis(symptoms)

        prompt = f"""
        You are a medical triage assistant. Analyze the following symptoms and provide:
        1. Severity (Low, Medium, High, Critical)
        2. Recommended Department. MUST be one of: [General, Cardiology, Neurology, Orthopedics].
           If the condition is critical/emergency, choose the most relevant specialist (e.g. Cardiology for heart attack) or 'General'.
        3. Brief Summary (1 sentence)

        Symptoms: {symptoms}

        Output JSON format:
        {{
            "severity": "...",
            "department": "...",
            "summary": "..."
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Simple parsing assuming the model returns valid JSON or close to it
            # In production, use structured output parsing or regex
            import json
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3]
            return json.loads(text)
        except Exception as e:
            # Log a clean warning instead of a full error stack trace
            logger.warning(f"LLM Triage unavailable ({str(e)}). Using fallback logic.")
            return self._mock_analysis(symptoms)

    def _mock_analysis(self, symptoms: str) -> Dict[str, Any]:
        # Fallback for testing without API key or if API fails
        symptoms_lower = symptoms.lower()
        
        if any(x in symptoms_lower for x in ["chest pain", "heart", "breathing", "shortness of breath"]):
            return {
                "severity": "Critical",
                "department": "Cardiology",
                "summary": f"Patient reports {symptoms}. Immediate cardiology consultation required."
            }
        elif any(x in symptoms_lower for x in ["headache", "migraine", "dizzy"]):
             return {
                "severity": "Low",
                "department": "Neurology",
                "summary": f"Patient reports {symptoms}. Neurology checkup recommended."
            }
        elif any(x in symptoms_lower for x in ["knee", "bone", "fracture", "leg", "arm", "swollen"]):
             return {
                "severity": "Medium",
                "department": "Orthopedics",
                "summary": f"Patient reports {symptoms}. Orthopedic evaluation recommended."
            }
        
        return {
            "severity": "Medium",
            "department": "General",
            "summary": f"Patient reports {symptoms}. Recommended general checkup."
        }
