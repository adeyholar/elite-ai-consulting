from agents.task_agent import TaskAgent
from agents.blog_agent import BlogAgent
from agents.report_agent import ReportAgent
from services.email_client import EmailClient
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

class SupervisorAgent:
    def __init__(self):
        self.task_agent = TaskAgent()
        self.blog_agent = BlogAgent()
        self.report_agent = ReportAgent()
        self.email_client = EmailClient()  # Initialize with your email credentials
        self.shared_memory = {}  # Temporary until fully replaced by DB
        # Load environment variables from .env file
        load_dotenv()
        # Database configuration from environment variables
        self.DB_CONFIG = {
            'dbname': os.getenv('DB_NAME'),
            'user': os.getenv('DB_USER'),
            'password': os.getenv('DB_PASSWORD'),
            'host': os.getenv('DB_HOST', 'localhost'),  # Default to localhost if not set
            'port': os.getenv('DB_PORT', '5432')  # Default to 5432 if not set
        }

    def get_db_connection(self):
        conn = psycopg2.connect(**self.DB_CONFIG)  # type: ignore
        return conn

    def process_task(self, task_id, desc, time_str, priority, recurring):
        """
        Route task to appropriate agent based on description and send email notification.
        """
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (description, time, priority, recurring) VALUES (%s, %s, %s, %s) RETURNING id",
                    (desc, time_str, priority, recurring))
        task_id_db = f"task_{cur.fetchone()[0]}"
        conn.commit()
        cur.close()
        conn.close()

        self.shared_memory[task_id_db] = {
            'description': desc,
            'time': time_str,
            'priority': priority,
            'recurring': recurring,
            'status': 'Processing'
        }

        # Route to appropriate agent
        if 'blog' in desc.lower():
            task_data = self.blog_agent.generate_blog(desc)
        elif 'report' in desc.lower():
            task_data = self.report_agent.generate_report(task_id_db, desc)
        else:
            task_data = self.task_agent.process_task(task_id_db, desc, time_str, priority, recurring)

        self.shared_memory[task_id_db].update(task_data)
        self.shared_memory[task_id_db]['status'] = task_data['status']

        # Update database with task status and response
        conn = self.get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE tasks 
            SET status = %s, ai_response = %s, generated_at = %s, pdf_path = %s 
            WHERE id = %s
        """, (task_data['status'], task_data['ai_response'], task_data.get('generated_at'), task_data.get('pdf_path'), int(task_id_db.replace('task_', ''))))
        conn.commit()
        cur.close()
        conn.close()

        # Send HTML email notification
        recipient = "adecisco_associate@yahoo.com"  # Update this line with the actual recipient email
        subject = f"Task {task_id_db} Completed: {desc}"
        body = f"Task {task_id_db} has been completed.\nStatus: {task_data['status']}\nDetails: {task_data['ai_response']}"
        html_body = f"""
        <html>
          <body>
            <h2>Task Completion Notification</h2>
            <p><strong>Task ID:</strong> {task_id_db}</p>
            <p><strong>Description:</strong> {desc}</p>
            <p><strong>Status:</strong> {task_data['status']}</p>
            <p><strong>Details:</strong> {task_data['ai_response']}</p>
            <p>This is an automated message from Elite AI Consulting.</p>
          </body>
        </html>
        """
        attachment = task_data.get('pdf_path') if 'pdf_path' in task_data else None
        email_status = self.email_client.send_email(recipient, subject, body, attachment, html_body)
        print(f"Email status: {email_status}")

        return task_data