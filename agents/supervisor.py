from agents.task_agent import TaskAgent

class SupervisorAgent:
    def __init__(self):
        self.task_agent = TaskAgent()
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

        # Route to task agent (blog/report agents added later)
        if 'blog' in desc.lower():
            # Placeholder for blog agent
            task_data = {
                'description': desc,
                'time': time_str,
                'priority': priority,
                'recurring': recurring,
                'status': 'Pending',
                'ai_response': 'Blog generation not yet implemented'
            }
        else:
            task_data = self.task_agent.process_task(task_id, desc, time_str, priority, recurring)

        self.shared_memory[task_id].update(task_data)
        self.shared_memory[task_id]['status'] = task_data['status']
        return task_data