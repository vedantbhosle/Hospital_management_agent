import asyncio
import sys
import os
# Add parent directory to path to allow importing healthmate_ai package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from healthmate_ai.agents.doctor_schedule_agent import DoctorScheduleAgent
from healthmate_ai.agents.patient_insight_agent import PatientInsightAgent

async def main():
    print("\n--- 👨‍⚕️ Doctor Agent Interface (LLM Powered) ---")
    
    # Initialize Agents
    # Note: In a real app, we might pass the doctor_id to the agent or context
    schedule_agent = DoctorScheduleAgent()
    insight_agent = PatientInsightAgent()
    
    # 1. Doctor Login / Identification
    doctor_id = input("Enter Doctor ID (e.g. Dr. Smith): ").strip()
    if not doctor_id:
        doctor_id = "Dr. Smith" # Default
        
    print(f"\nWelcome, {doctor_id}. I am your AI assistant.")
    print("You can ask me about your schedule or specific patients.")
    
    # 2. Interactive Loop
    while True:
        print("\n" + "-"*30)
        query = input("Ask a question (or type 'exit'): ").strip()
        
        if query.lower() in ['exit', 'quit', 'bye']:
            print("Goodbye!")
            break
            
        if not query:
            continue
            
        # Simple routing logic (in a full multi-agent system, an orchestrator would do this)
        # For now, we'll check keywords to route to the right agent.
        query_lower = query.lower()
        
        if any(x in query_lower for x in ['schedule', 'appointments', 'calendar', 'today', 'patients']):
            # Route to Schedule Agent
            # Context injection: The agent needs to know WHO asks and WHEN
            today = datetime.now().strftime("%Y-%m-%d")
            context_query = f"Doctor ID: {doctor_id}, Date: {today}. Question: {query}"
            print("\n🤖 Schedule Agent is thinking...")
            response = schedule_agent.process_query(context_query)
            print(f"\n{response}")
            
        elif any(x in query_lower for x in ['patient', 'history', 'report', 'details', 'insight']):
            # Route to Insight Agent
            print("\n🤖 Insight Agent is thinking...")
            response = insight_agent.process_query(query)
            print(f"\n{response}")
            
        else:
            # Default to Schedule Agent or ask for clarification
            print("\n🤖 Schedule Agent (Default):")
            response = schedule_agent.process_query(f"Doctor ID: {doctor_id}. Question: {query}")
            print(f"\n{response}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nExiting...")
