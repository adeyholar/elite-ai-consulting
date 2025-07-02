import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import os
import logging
from typing import cast  # Import cast for explicit type assertion

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailClient:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587, sender_email="your.email@gmail.com"):
        """
        Initialize email client with SMTP settings.
        Password is loaded from environment variable EMAIL_PASSWORD.
        Replace sender_email with your Gmail address.
        Raises ValueError if EMAIL_PASSWORD is not set.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.password = os.getenv("EMAIL_PASSWORD")
        if self.password is None:
            raise ValueError("Environment variable EMAIL_PASSWORD not set. Please set it before running the application.")
        # The cast below explicitly tells Pylance that self.password is a string here.
        # This is already present, but the issue might be how Pylance tracks it across methods.
        self.password = cast(str, self.password)

    def send_email(self, recipient_email, subject, body, attachment_path=None, html_body=None):
        """
        Send an email with optional PDF attachment and HTML body.
        """
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject

        # Attach plain text body if provided
        if body:
            msg.attach(MIMEText(body, 'plain'))

        # Attach HTML body if provided
        if html_body:
            msg.attach(MIMEText(html_body, 'html'))

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
                # Explicitly assert the type here for Pylance, even though it's checked in __init__
                # This ensures Pylance understands it's a string at this point.
                server.login(self.sender_email, cast(str, self.password))
                server.send_message(msg)
            return "Email sent successfully!"
        except smtplib.SMTPException as e:
            logger.error(f"Failed to send email: {e}")
            return f"Failed to send email: {e}"
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            return f"Email configuration error: {e}"
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return f"An unexpected error occurred: {e}"