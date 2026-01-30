import subprocess
from pathlib import Path
from config import settings

RAW_DIR = Path("/app/volume/sast/raw")
FORMATTED_DIR = Path("/app/volume/sast/formatted")
AI_DIR = Path("/app/volume/sast/ai_analysis")

settings.validate()

print("Se passou é pq deu certo")
