from pathlib import Path
from typing import Optional


class Settings:
    BASE_DIR: Optional[str] = Path(__file__).resolve().parent


settings: Settings = Settings()
