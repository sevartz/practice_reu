import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent

load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

LOGINOM_BASE_URL = os.getenv("LOGINOM_BASE_URL", "https://edu.loginom.dev")
LOGINOM_PACKAGE = os.getenv("LOGINOM_PACKAGE", "instacart_ws_serebryakov_i_arina")

NVIDIA_API_KEY = os.getenv("NVIDIA_API_KEY") or os.getenv("nvidia_api", "")
NVIDIA_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
NVIDIA_MODEL = "moonshotai/kimi-k2.6"

FLASK_SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "dev-secret-change-me")

CACHE_DB = os.getenv("CACHE_DB", str(BASE_DIR / "cache.db"))

MOCK_LOGINOM = os.getenv("MOCK_LOGINOM", "0") == "1"
