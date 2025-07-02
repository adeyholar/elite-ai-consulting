# Elite AI Consulting

A professional AI-powered consulting platform built with Flask, Ollama, and a multi-agent system. This project supports task management, blog generation, and report creation, leveraging local LLMs for privacy and performance.

## Features
- **Web Interface**: Client-facing portal for task submission and status tracking (Flask-based).
- **Multi-Agent System**: Supervisor, task, blog, and report agents process tasks using `llama3.2:latest` for efficiency.
- **Local LLM Integration**: Uses native Ollama installation on `D:\AI\Models\Ollama` with GPU acceleration (RTX 4060).
- **PDF Generation**: Generates professional PDF reports for tasks and analyses.
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

3. **Install Native Ollama**:
   - Install Ollama natively on `D:\AI\Models\Ollama` using the downloaded installer.
   - Set environment variable: `OLLAMA_MODELS=D:\VM\OllamaModels`.
   - Pull models: `D:\AI\Models\Ollama\ollama.exe pull llama3.2:latest`.
   - Run Ollama: `D:\AI\Models\Ollama\ollama.exe run llama3.2:latest`.

4. **Run Flask App**:
   ```bash
   python app.py
   ```
   - Visit `http://localhost:5000` to access the web interface.

## Usage
- **Submit Tasks**: Go to `/request` to submit tasks (e.g., “Plan a meeting”, “Generate a blog post”, “Generate a report on productivity”).
- **View Status**: Check task details at `/status/<task_id>`.
- **Download Reports**: Click “Download Report” for PDF files.
- **List Tasks**: View all tasks at `/tasks` (JSON).

## Project Structure
```
elite-ai-consulting/
├── agents/
│   ├── supervisor.py
│   ├── task_agent.py
│   ├── blog_agent.py
│   ├── report_agent.py
├── services/
│   ├── ollama_client.py
│   ├── pdf_generator.py
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
- Implement email client for task, blog, and report notifications (Lesson 7).
- Add PostgreSQL for task persistence (Lesson 10).
- Deploy to cloud (Lesson 15).