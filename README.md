# HealthMate AI

HealthMate AI is a Python-based multi-agent healthcare assistant designed to automate patient triage, report extraction, appointment scheduling, and reminders. It implements Google ADK concepts such as multi-agent orchestration, parallel execution, and tool-based interactions.

## Features

- **Triage Agent**: Analyzes symptoms using LLM (Gemini) to determine severity and recommended department.
- **Report Parser Agent**: Extracts medical data from PDF reports.
- **Scheduler Agent**: Checks doctor availability and books appointments sequentially.
- **Reminder Agent**: Sends automated reminders for upcoming appointments.
- **Orchestrator Agent**: Manages the end-to-end patient workflow.
- **Memory System**: Maintains session state and long-term patient history.
- **Observability**: Built-in tracing and structured logging.

## Architecture

The system follows a hub-and-spoke architecture where the **OrchestratorAgent** coordinates specialized agents:

1.  **Triage** and **Report Parsing** run in parallel.
2.  **Scheduling** happens sequentially based on triage results.
3.  **Reminders** are triggered asynchronously.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r healthmate_ai/requirements.txt
    pip install fpdf  # For sample generation
    ```

2.  **Environment Variables**:
    Set your Gemini API key (optional, mock mode used if missing):
    ```bash
    export GEMINI_API_KEY="your_api_key_here"
    ```

## Usage

### CLI Mode
Run the interactive CLI:
```bash
export PYTHONPATH=$PYTHONPATH:.
python healthmate_ai/main.py --cli
```

### Run Evaluation
Run the end-to-end test scenario:
```bash
export PYTHONPATH=$PYTHONPATH:.
python healthmate_ai/main.py --test-scenario healthmate_ai/evaluation/end_to_end_eval.json
```

### Generate Sample Data
Create a sample medical report PDF:
```bash
python create_sample_pdf.py
```

## Directory Structure

- `healthmate_ai/agents`: Agent implementations.
- `healthmate_ai/tools`: Tool implementations (DB, PDF, Notification, Scheduling).
- `healthmate_ai/core`: Core runtime (Memory, Tracing, Logger).
- `healthmate_ai/evaluation`: Test scenarios.
