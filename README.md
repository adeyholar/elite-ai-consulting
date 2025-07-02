# Elite AI Consulting

A professional AI-powered consulting platform built with Flask, Ollama, and a multi-agent system. This project supports task management, blog generation, and report creation, leveraging local LLMs for privacy and performance.

## Features
- **Web Interface**: Client-facing portal for task submission and status tracking (Flask-based).
- **Multi-Agent System**: Supervisor and task agents process tasks using `llama3.2:latest` and `llama3.3:70b`.
- **Local LLM Integration**: Uses Ollama for AI-driven responses with GPU acceleration.
- **Scalable Architecture**: Designed for future PostgreSQL integration and cloud deployment.

## Setup
1. **Clone Repository**:
   ```bash
   git clone https://github.com/adeyholar/elite-ai-consulting.git
   cd elite-ai-consulting
   ```

2. **Set Up Conda Environment**:
   ```bash
   conda create -n ai_consulting-3.12 python=3.12 -y
   conda activate ai_consulting-3.12
   pip install -r requirements.txt
   ```

3. **Run Ollama**:
   ```bash
   docker run -d -p 11434:11434 --name ollama --gpus all ollama/ollama
   docker exec ollama ollama pull llama3.2:latest
   docker exec ollama ollama run llama3.2:latest
   ```

4. **Run Flask App**:
   ```bash
   python app.py
   ```
   - Visit `http://localhost:5000` to access the web interface.

## Usage
- **Submit Tasks**: Go to `/request` to submit tasks (e.g., “Plan a meeting” or “Generate a blog post”).
- **View Status**: Check task details at `/status/<task_id>`.
- **List Tasks**: View all tasks at `/tasks` (JSON).

## Project Structure
```
elite-ai-consulting/
├── agents/
│   ├── supervisor.py
│   ├── task_agent.py
├── services/
│   ├── ollama_client.py
├── templates/
│   ├── index.html
│   ├── request.html
│   ├── status.html
├── static/
│   ├── css/style.css
├── app.py
├── config.py
├── requirements.txt
```

## Next Steps
- Implement blog and report agents (Lessons 6-7).
- Add PostgreSQL for task persistence (Lesson 10).
- Deploy to cloud (Lesson 15).