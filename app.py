from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/request')
def task_request():
    return render_template('request.html')

@app.route('/status/<task_id>')
def status(task_id):
    return render_template('status.html', task_id=task_id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)