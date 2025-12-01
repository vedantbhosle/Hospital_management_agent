import time
from typing import List
from healthmate_ai.tools.database_tool import DatabaseTool
from healthmate_ai.tools.notification_tool import NotificationTool
from healthmate_ai.core.tracing import trace_agent
from healthmate_ai.core.logger import setup_logger

logger = setup_logger("ReminderAgent")

class ReminderAgent:
    def __init__(self, db_tool: DatabaseTool):
        self.db_tool = db_tool
        self.notifier = NotificationTool()

    @trace_agent
    def run_cycle(self):
        """
        Runs a single cycle of checking and sending reminders.
        """
        logger.info("Running reminder cycle...")
        pending = self.db_tool.get_pending_reminders()
        
        for reminder in pending:
            self._process_reminder(reminder)

    def _process_reminder(self, reminder):
        # In a real app, we'd fetch patient details to get phone/email
        # Here we mock it
        logger.info(f"Processing reminder {reminder['reminder_id']}")
        
        success = self.notifier.send_sms("555-0123", f"Reminder for appointment {reminder['appointment_id']}")
        
        if success:
            self.db_tool.mark_reminder_sent(reminder['reminder_id'])
            logger.info(f"Reminder {reminder['reminder_id']} sent and marked.")

    def start_loop(self, interval=60):
        """
        Starts the infinite loop (blocking).
        """
        while True:
            self.run_cycle()
            time.sleep(interval)
