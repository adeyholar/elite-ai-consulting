from agents.task_agent import TaskAgent
from agents.blog_agent import BlogAgent
from agents.report_agent import ReportAgent
from services.email_client import EmailClient

class SupervisorAgent:
    def __init__(self):
        self.task_agent = TaskAgent()
        self.blog_agent = BlogAgent()
        self.report_agent = ReportAgent()
        self.email_client = EmailClient()  # Initialize with your email credentials
        self.shared_memory = {}  # Shared context for agents

    def process_task(self, task_id, desc, time_str, priority, recurring):
        """
        Route task to appropriate agent based on description and send email notification.
        """
        self.shared_memory[task_id] = {
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
            task_data = self.report_agent.generate_report(task_id, desc)
        else:
            task_data = self.task_agent.process_task(task_id, desc, time_str, priority, recurring)

        self.shared_memory[task_id].update(task_data)
        self.shared_memory[task_id]['status'] = task_data['status']

        # Send HTML email notification (replace with your recipient email)
        recipient = "adecisco_associate@yahoo.com"  # Update this line with the actual recipient email
        subject = f"Task {task_id} Completed: {desc}"
        body = f"Task {task_id} has been completed.\nStatus: {task_data['status']}\nDetails: {task_data['ai_response']}"
        # HTML version of the email
        html_body = f"""
        <html>
          <body>
            <h2>Task Completion Notification</h2>
            <p><strong>Task ID:</strong> {task_id}</p>
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