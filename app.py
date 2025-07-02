from flask import Flask, render_template, request, jsonify, redirect, url_for
from agents.supervisor import SupervisorAgent

app = Flask(__name__)

# Temporary in-memory task storage (to be replaced with PostgreSQL)
tasks = {}
supervisor = SupervisorAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/request', methods=['GET', 'POST'])
def task_request():
    if request.method == 'POST':
        task_desc = request.form['description']
        time_str = request.form.get('time', '')
        priority = int(request.form.get('priority', 1))
        recurring = 'recurring' in request.form

        # Generate task ID and process with supervisor
        task_id = f"task_{len(tasks)}"
        task_data = supervisor.process_task(task_id, task_desc, time_str, priority, recurring)
        tasks[task_id] = task_data

        # Redirect to status page
        return redirect(url_for('status', task_id=task_id))
    return render_template('request.html')

@app.route('/status/<task_id>')
def status(task_id):
    task = tasks.get(task_id, {'description': 'Not Found', 'status': 'Not Found', 'time': '', 'priority': 1, 'recurring': False, 'ai_response': 'Task not found'})
    return render_template('status.html', task_id=task_id, task=task)

@app.route('/tasks')
def list_tasks():
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)