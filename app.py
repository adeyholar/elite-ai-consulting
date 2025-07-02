from flask import Flask, render_template, request, jsonify, redirect, url_for, send_from_directory
from agents.supervisor import SupervisorAgent
import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Database configuration from environment variables
DB_CONFIG = {
    'dbname': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST', 'localhost'),  # Default to localhost if not set
    'port': os.getenv('DB_PORT', '5432')  # Default to 5432 if not set
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)  # type: ignore
    return conn

# Initialize SupervisorAgent
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
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO tasks (description, time, priority, recurring) VALUES (%s, %s, %s, %s) RETURNING id",
                    (task_desc, time_str, priority, recurring))
        task_id = f"task_{cur.fetchone()[0]}"
        conn.commit()
        cur.close()
        conn.close()

        task_data = supervisor.process_task(task_id, task_desc, time_str, priority, recurring)

        # Redirect to status page
        return redirect(url_for('status', task_id=task_id))
    return render_template('request.html')

@app.route('/status/<task_id>')
def status(task_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM tasks WHERE id = %s", (int(task_id.replace('task_', '')),))
    task = cur.fetchone()
    cur.close()
    conn.close()
    if task:
        task['ai_response'] = supervisor.shared_memory.get(task_id, {}).get('ai_response', 'Task not processed yet')
        task['status'] = supervisor.shared_memory.get(task_id, {}).get('status', 'Processing')
        task['generated_at'] = supervisor.shared_memory.get(task_id, {}).get('generated_at', '')
        task['pdf_path'] = supervisor.shared_memory.get(task_id, {}).get('pdf_path', '')
    else:
        task = {'description': 'Not Found', 'status': 'Not Found', 'time': '', 'priority': 1, 'recurring': False, 'ai_response': 'Task not found'}
    return render_template('status.html', task_id=task_id, task=task)

@app.route('/tasks')
def list_tasks():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, description, time, priority, recurring FROM tasks")
    tasks = cur.fetchall()
    cur.close()
    conn.close()
    for task in tasks:
        task_id = f"task_{task['id']}"
        task['ai_response'] = supervisor.shared_memory.get(task_id, {}).get('ai_response', 'Task not processed yet')
        task['status'] = supervisor.shared_memory.get(task_id, {}).get('status', 'Processing')
        task['generated_at'] = supervisor.shared_memory.get(task_id, {}).get('generated_at', '')
        task['pdf_path'] = supervisor.shared_memory.get(task_id, {}).get('pdf_path', '')
    return jsonify(tasks)

@app.route('/reports/<path:filename>')
def serve_report(filename):
    # Serve from the reports directory relative to the app root
    return send_from_directory(os.path.join(app.root_path, 'reports'), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)