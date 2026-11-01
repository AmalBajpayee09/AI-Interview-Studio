"""Settings are exclusively environment sourced, never persisted to SQLite."""
import os
from pathlib import Path

DATA_DIR = Path(os.getenv('STUDIO_DATA_DIR') or str(Path.home() / '.ai-interview-studio')).expanduser()
DB_PATH = DATA_DIR / 'studio.sqlite3'
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://127.0.0.1:11434').rstrip('/')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'qwen2.5:3b')
CLOUD_MODEL = os.getenv('CLOUD_MODEL', 'gpt-4.1-mini')
CLOUD_KEY = os.getenv('OPENAI_API_KEY', '')
ALLOW_CLOUD = os.getenv('ALLOW_CLOUD', 'false').lower() == 'true'
RETENTION_DAYS = max(1, min(3650, int(os.getenv('RETENTION_DAYS', '30'))))
