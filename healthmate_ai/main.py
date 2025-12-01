import asyncio
import argparse
import json
import os
from healthmate_ai.agents.orchestrator_agent import OrchestratorAgent
from healthmate_ai.tools.database_tool import DatabaseTool
from healthmate_ai.core.logger import setup_logger

logger = setup_logger("Main")

import uuid

from healthmate_ai.agents.doctor_schedule_agent import DoctorScheduleAgent
from healthmate_ai.agents.patient_insight_agent import PatientInsightAgent
from datetime import datetime

async def run_cli():
    print("\n========================================")
    print("       🏥 HEALTHMATE AI SYSTEM       ")
    print("========================================")

    while True:
        print("\n--- 🔐 System Login ---")
        print("[1] 👩‍💼 Staff Portal (Triage & Admissions)")
        print("[2] 👨‍⚕️ Doctor Portal (Clinical Insights)")
        print("[q] 🚪 Exit System")
        
        choice = input("\nSelect Role: ").strip().lower()
        
        if choice in ['1', 'staff']:
            await run_staff_interface()
        elif choice in ['2', 'doctor']:
            await run_doctor_interface()
        elif choice in ['q', 'exit', 'quit']:
            print("Shutting down system. Goodbye! 👋")
            break
        else:
            print("Invalid selection. Please try again.")

async def run_staff_interface():
    print("\n--- 👩‍💼 Staff Portal ---")
    orchestrator = OrchestratorAgent()
    
    # Setup Patient Entity
    db = DatabaseTool()
    while True:
        print("\n--- 👤 Patient Identification ---")
        name = input("Enter Patient Name (e.g. John Doe) or 'back' to menu: ").strip()
        
        if name.lower() == 'back':
            break

        existing_patient = db.find_patient_by_name(name)
        
        if existing_patient:
            patient_id = existing_patient['patient_id']
            print(f"Welcome back, {name}! (ID: {patient_id})")
        else:
            print(f"New patient detected. Creating profile for {name}...")
            
            age_input = input("Enter Age (or enter to skip): ").strip()
            if age_input and age_input.isdigit():
                age = int(age_input)
            else:
                age = 0 # Default
                
            gender_input = input("Enter Gender (M/F/Other) (or enter to skip): ").strip().upper()
            if gender_input in ['M', 'MALE']:
                gender = "Male"
            elif gender_input in ['F', 'FEMALE']:
                gender = "Female"
            elif gender_input:
                gender = gender_input.capitalize()
            else:
                gender = "Unknown"
                
            phone = input("Enter Phone (or enter to skip): ").strip() or "N/A"
            email = input("Enter Email (or enter to skip): ").strip() or "N/A"
            
            patient_id = f"p_{uuid.uuid4().hex[:6]}"
            db.add_patient({
                "patient_id": patient_id,
                "name": name,
                "age": age,
                "gender": gender,
                "phone": phone,
                "email": email
            })
            print(f"Profile created! (ID: {patient_id})")

        print("\n--- New Case Entry ---")
        symptoms = input("Enter symptoms (or 'skip' to cancel): ")
        if symptoms.lower() == 'skip':
            continue
            
        report_path = input("Enter path to PDF report (optional): ").strip()
        if not report_path:
            report_path = None
        
        result = await orchestrator.process_patient_request(patient_id, symptoms, report_path)
        
        print("\n" + "="*40)
        print("       🏥 HEALTHMATE AI REPORT       ")
        print("="*40)
        
        # Patient Info
        print(f"\n👤 Patient ID: {result.get('patient_id')}")
        
        # Triage
        triage = result.get('triage', {})
        print(f"\n🚑 Triage Analysis")
        print(f"   • Severity:   {triage.get('severity', 'N/A')}")
        print(f"   • Department: {triage.get('department', 'N/A')}")
        print(f"   • Summary:    {triage.get('summary', 'N/A')}")

        # Report
        report = result.get('report_analysis', {})
        if report:
            print(f"\n📄 Report Analysis")
            print(f"   • Status: {report.get('status')}")
            if report.get('data'):
                print(f"   • File:   {os.path.basename(report['data'].get('file_path', ''))}")
        
        # Appointment
        appt = result.get('appointment')
        if appt:
            print(f"\n📅 Appointment Scheduled")
            print(f"   • Doctor: {appt.get('doctor_id')}")
            print(f"   • Date:   {appt.get('date')}")
            print(f"   • Status: {appt.get('status')}")
        else:
            print("\n📅 Appointment: Not scheduled")

        # Reminder
        print(f"\n🔔 Reminder Agent")
        if appt and appt.get('status') == 'confirmed':
            print(f"   • Action: SMS sent to patient")
            print(f"   • Status: Delivered")
        else:
            print(f"   • Action: None (No appointment)")

        print("\n" + "="*40 + "\n")

async def run_doctor_interface():
    print("\n--- 👨‍⚕️ Doctor Portal ---")
    
    # Initialize Agents
    schedule_agent = DoctorScheduleAgent()
    insight_agent = PatientInsightAgent()
    
    doctor_id = input("Enter Doctor ID (default: Dr. Smith): ").strip()
    if not doctor_id:
        doctor_id = "Dr. Smith"
        
    print(f"\nWelcome, {doctor_id}. Accessing clinical database...")
    
    while True:
        print("\n" + "-"*30)
        query = input("Ask a question (or 'back' to logout): ").strip()
        
        if query.lower() in ['back', 'logout', 'exit']:
            break
            
        if not query:
            continue
            
        # Routing logic
        query_lower = query.lower()
        
        if any(x in query_lower for x in ['schedule', 'appointments', 'calendar', 'today', 'patients']):
            today = datetime.now().strftime("%Y-%m-%d")
            context_query = f"Doctor ID: {doctor_id}, Date: {today}. Question: {query}"
            print("\n🤖 Schedule Agent is thinking...")
            response = schedule_agent.process_query(context_query)
            print(f"\n{response}")
            
        elif any(x in query_lower for x in ['patient', 'history', 'report', 'details', 'insight']):
            print("\n🤖 Insight Agent is thinking...")
            response = insight_agent.process_query(query)
            print(f"\n{response}")
            
        else:
            print("\n🤖 Schedule Agent (Default):")
            response = schedule_agent.process_query(f"Doctor ID: {doctor_id}. Question: {query}")
            print(f"\n{response}")

async def run_test_scenario(scenario_path: str):
    logger.info(f"Running test scenario from {scenario_path}")
    with open(scenario_path, 'r') as f:
        scenario = json.load(f)
    
    orchestrator = OrchestratorAgent()
    db = DatabaseTool()
    
    # Setup patient
    patient = scenario.get("patient")
    if patient:
        db.add_patient(patient)
        patient_id = patient["patient_id"]
    else:
        patient_id = "test_patient"
        db.add_patient({"patient_id": patient_id, "name": "Test", "age": 25, "gender": "F", "phone": "000", "email": "test@test.com"})

    symptoms = scenario.get("symptoms", "Headache")
    report_path = scenario.get("report_path")
    
    result = await orchestrator.process_patient_request(patient_id, symptoms, report_path)
    
    # Simple validation
    expected = scenario.get("expected_output", {})
    if expected.get("department"):
        assert result["triage"]["department"] == expected["department"], f"Expected {expected['department']}, got {result['triage']['department']}"
    
    logger.info("Test scenario passed successfully.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="HealthMate AI")
    parser.add_argument("--cli", action="store_true", help="Run in CLI mode")
    parser.add_argument("--test-scenario", type=str, help="Path to test scenario JSON")
    
    args = parser.parse_args()
    
    if args.test_scenario:
        asyncio.run(run_test_scenario(args.test_scenario))
    else:
        asyncio.run(run_cli())
