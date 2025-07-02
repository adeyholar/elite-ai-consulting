from agents.task_agent import TaskAgent
from agents.blog_agent import BlogAgent
from agents.report_agent import ReportAgent

class SupervisorAgent:
    def __init__(self):
        self.task_agent = TaskAgent()
        self.blog_agent = BlogAgent()
        self.report_agent = ReportAgent()
        self.shared_memory = {}  # Shared context for agents

    def process_task(self, task_id, desc, time_str, priority, recurring):
        """
        Route task to appropriate agent based on description.
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
        return task_data