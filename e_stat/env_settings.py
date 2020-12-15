import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(verbose=True)

dotenv_path = Path(__file__) / ".env"
load_dotenv(dotenv_path)

app_id = os.environ.get("app_id")
