# 🏥 HealthMate AI

HealthMate AI is a comprehensive, multi-agent healthcare assistant designed to streamline patient management and clinical workflows. It features a unified CLI with role-based access for both **Staff** and **Doctors**, powered by Google's Gemini LLM.

## ✨ Key Features

### 🔐 Unified Role-Based System
*   **Single Entry Point**: One command to access the entire system.
*   **Staff Portal**:
    *   **Patient Management**: Register new patients with detailed profiles (Age, Gender, Contact) or lookup existing ones.
    *   **Smart Triage**: AI-powered symptom analysis to determine severity and department.
    *   **Workflow Automation**: Automatically parses reports, books appointments, and sends SMS reminders.
*   **Doctor Portal**:
    *   **Conversational Interface**: Chat with your clinical data using natural language.
    *   **Schedule Management**: Ask "What is my schedule today?" to see appointments.
    *   **Patient Insights**: Ask "Tell me about John Doe" to get a summarized medical history.

### 🤖 Intelligent Agents
1.  **Triage Agent** (`gemini-2.5-flash-lite`): Analyzes symptoms and routes to Cardiology, Neurology, Orthopedics, or General.
2.  **Orchestrator Agent**: Coordinates the end-to-end patient journey.
3.  **Doctor Schedule Agent**: Retrieves and summarizes doctor appointments.
4.  **Patient Insight Agent**: Synthesizes patient history and medical reports.
5.  **Reminder Agent**: Background process for patient engagement.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r healthmate_ai/requirements.txt
```

### 2. Set API Key
You need a Google Gemini API key for the AI features.
```bash
export GEMINI_API_KEY="your_api_key_here"
```

### 3. Run the System
```bash
export PYTHONPATH=$PYTHONPATH:.
python healthmate_ai/main.py --cli
```

## 📖 Usage Guide

### 👩‍💼 Staff Workflow
1.  **Login**: Select Option `[1] Staff Portal`.
2.  **Identify Patient**: Enter a name.
    *   *New Patient*: You will be prompted for Age, Gender, Phone, Email. (Press Enter to skip/default).
    *   *Existing Patient*: System retrieves their ID automatically.
3.  **Process Case**: Enter symptoms (e.g., "severe chest pain") and optional PDF report path.
4.  **View Results**: The system generates a report, books a doctor, and sends a reminder.
5.  **Loop**: The system returns to patient identification for the next case.

### 👨‍⚕️ Doctor Workflow
1.  **Login**: Select Option `[2] Doctor Portal`.
2.  **Identify**: Enter your Doctor ID (e.g., "Dr. Smith").
3.  **Interact**:
    *   *"What is my schedule?"*
    *   *"Who is my first patient?"*
    *   *"Show me the history for [Patient Name]"*

## 📂 Project Structure

*   `healthmate_ai/main.py`: **Main Entry Point** (CLI & Auth Logic).
*   `healthmate_ai/agents/`:
    *   `triage_agent.py`: Symptom analysis.
    *   `doctor_schedule_agent.py`: Doctor interactions.
    *   `patient_insight_agent.py`: Patient summaries.
    *   `orchestrator_agent.py`: Workflow coordination.
*   `healthmate_ai/tools/`:
    *   `database_tool.py`: SQLite database manager.
    *   `scheduling_openapi_tool.py`: Mock appointment booking.
*   `healthmate_ai/core/`: Logging, Tracing, and LLM setup.

## 🏗️ Architecture
The system uses a **Hub-and-Spoke** architecture where the `OrchestratorAgent` manages the patient flow, while specialized `LlmAgents` handle the doctor's conversational queries. All data is persisted in a local SQLite database (`healthmate.db`).
