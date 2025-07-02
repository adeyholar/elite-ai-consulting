from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Temporary in-memory task storage (to be replaced with PostgreSQL)
tasks = {}

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

        # Generate a unique task ID
        task_id = f"task_{len(tasks)}"
        tasks[task_id] = {
            'description': task_desc,
            'time': time_str,
            'priority': priority,
            'recurring': recurring,
            'status': 'Pending'
        }

        # Return JSON for testing (later, we'll redirect or process with agents)
        return jsonify({'task_id': task_id, 'status': 'Task submitted', 'description': task_desc})
    return render_template('request.html')

@app.route('/status/<task_id>')
def status(task_id):
    task = tasks.get(task_id, {'description': 'Not Found', 'status': 'Not Found', 'time': '', 'priority': 1, 'recurring': False})
    return render_template('status.html', task_id=task_id, task=task)

@app.route('/tasks')
def list_tasks():
    return jsonify(tasks)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)