from pathlib import Path
from typing import Optional

try:
    import tomllib
except ImportError:
    import tomli as tomllib

import json

import yaml
from dotenv import load_dotenv


class ConfigManager:
    """Manages configuration file loading and
    key retrieval
    """

    # Configuration cache
    _config_data = {}
    # Ensures files are loaded only once
    _files_checked = False

    _default_files = [
        str(Path(__file__).parent.parent / 'config.json'),
        str(Path(__file__).parent.parent / 'config.toml'),
        str(Path(__file__).parent.parent / 'config.yml'),
        str(Path(__file__).parent.parent / '.env'),
    ]

    @classmethod
    def _load_file(cls, file_path):
        """Load a single file based on its extension."""
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                cls._config_data.update(json.load(f))
        elif file_path.endswith('.toml'):
            with open(file_path, 'r', encoding='utf-8') as f:
                cls._config_data.update(tomllib.load(f))
        elif file_path.endswith(('.yml', '.yaml')):
            with open(file_path, 'r', encoding='utf-8') as f:
                cls._config_data.update(yaml.safe_load(f))
        elif file_path.endswith('.env'):
            load_dotenv(dotenv_path=file_path)

    @classmethod
    def _load_files(cls):
        """Load all configuration files."""
        if cls._files_checked:
            return
        cls._files_checked = True

        # Load .env and other files in order of preference
        for file_path in cls._default_files:
            if Path(file_path).exists():
                cls._load_file(file_path)

    @classmethod
    def get(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Retrieves a configuration value by key.

        Args:
            key (str): The key to look up.
            defautl (Optional[str]): The default value if
            the key is not found.

        Returns:
            Optional[str]: The value of the key or the
            default value.
        """

        if not cls._files_checked:
            cls._load_files()

        return cls._config_data.get(key, default)

config = ConfigManager()
print(config.get("DATABASE_URL"))