CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    time TEXT,
    priority INTEGER NOT NULL,
    recurring BOOLEAN NOT NULL,
    status TEXT,
    ai_response TEXT,
    generated_at TIMESTAMP,
    pdf_path TEXT
);