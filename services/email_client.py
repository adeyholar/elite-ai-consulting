import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailClient:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587, sender_email="adengongo", password="djrnrlbzzsmultwx"):
        """
        Initialize email client with SMTP settings.
        Replace sender_email and password with your Gmail credentials (use an App Password for security).
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.password = password

    def send_email(self, recipient_email, subject, body, attachment_path=None):
        """
        Send an email with optional PDF attachment.
        """
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        msg.attach(MIMEText(body, 'plain'))

        if attachment_path and os.path.exists(attachment_path):
            try:
                logger.info(f"Attempting to attach PDF from: {attachment_path}")
                with open(attachment_path, 'rb') as f:
                    part = MIMEApplication(f.read(), Name=os.path.basename(attachment_path))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment_path)}"'
                    msg.attach(part)
                logger.info(f"Successfully attached PDF: {attachment_path}")
            except Exception as e:
                logger.error(f"Failed to attach PDF {attachment_path}: {e}")
        elif attachment_path:
            logger.error(f"Attachment path {attachment_path} does not exist")

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.password)
                server.send_message(msg)
            return "Email sent successfully"
        except Exception as e:
            return f"Failed to send email: {e}"