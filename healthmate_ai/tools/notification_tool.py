from healthmate_ai.core.logger import setup_logger

logger = setup_logger("NotificationTool")

class NotificationTool:
    def send_email(self, to_email: str, subject: str, body: str):
        # Simulation
        logger.info(f"Sending EMAIL to {to_email}")
        logger.info(f"Subject: {subject}")
        logger.info(f"Body: {body}")
        return True

    def send_sms(self, phone_number: str, message: str):
        # Simulation
        logger.info(f"Sending SMS to {phone_number}")
        logger.info(f"Message: {message}")
        return True
