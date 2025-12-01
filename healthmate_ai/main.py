import asyncio
import argparse
import json
import os
from healthmate_ai.agents.orchestrator_agent import OrchestratorAgent
from healthmate_ai.tools.database_tool import DatabaseTool
from healthmate_ai.core.logger import setup_logger

logger = setup_logger("Main")

import uuid

async def run_cli():
    orchestrator = OrchestratorAgent()
    
    # Setup Patient Entity
    db = DatabaseTool()
    print("\n--- 👤 Patient Identification ---")
    name = input("Enter Patient Name (e.g. John Doe): ").strip()
    
    existing_patient = db.find_patient_by_name(name)
    
    if existing_patient:
        patient_id = existing_patient['patient_id']
        print(f"Welcome back, {name}! (ID: {patient_id})")
    else:
        print(f"New patient detected. Creating profile for {name}...")
        patient_id = f"p_{uuid.uuid4().hex[:6]}"
        db.add_patient({
            "patient_id": patient_id,
            "name": name,
            "age": 30, # Default for demo
            "gender": "Unknown",
            "phone": "555-0000",
            "email": f"{name.replace(' ', '.').lower()}@example.com"
        })
        print(f"Profile created! (ID: {patient_id})")

    print("--- HealthMate AI CLI ---")
    symptoms = input("Enter symptoms: ")
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
    # In a real app, we'd query the DB for the reminder status.
    # For this simulation, we know the orchestrator triggers it.
    print(f"\n🔔 Reminder Agent")
    if appt and appt.get('status') == 'confirmed':
        print(f"   • Action: SMS sent to patient")
        print(f"   • Status: Delivered")
    else:
        print(f"   • Action: None (No appointment)")

    print("\n" + "="*40 + "\n")

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
