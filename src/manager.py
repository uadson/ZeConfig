import json
import os

from dotenv import load_dotenv

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from typing import Optional

import yaml

from .settings import settings


class ConfigManager:
    """Manages configuration file loading and
    key retrieval
    """

    _config_data = {}
    _files_checked = False
    _content_files = {}

    @classmethod
    def _load_file(cls, file_path):
        """Reads a configuration file and returns its contents.
        Supports JSON, TOML, YAML and .env files.
        """
        _, ext = os.path.splitext(file_path)
        if ext == '.json':
            with open(file_path, 'r', encoding='utf-8') as file:
                cls._config_data.update(json.load(file))
        elif ext == '.toml':
            with open(file_path, 'r', encoding='utf-8') as file:
                cls._config_data.update(tomllib.load(file))
        elif ext in {'.yaml', '.yml'}:
            with open(file_path, 'r', encoding='utf-8') as file:
                cls._config_data.update(yaml.load(file))
        elif ext == '.env':
            load_dotenv(dotenv_path=file_path)
        else:
            raise ValueError(f'Unsupported file format: {ext}')

    @classmethod
    def _load_files(cls, directory: str):
        """Reads all configuration files in a directory and returns a dictionary
        with the contents of each file.

        If the "configs" directory exists, it will be used. Otherwise, the root
        directory will be used.
        """
        if cls._files_checked:
            return
        cls._files_checked = True

        if os.path.exists('configs'):
            directory = 'configs'

        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            if os.path.isfile(file_path):
                try:
                    cls._load_file(file_path)
                except Exception as exc:
                    raise ValueError(
                        f'Error reading file: {filename}. Details: {exc}'
                    )

    @classmethod
    def get(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        if not cls._files_checked:
            cls._load_files(settings.BASE_DIR)
        cls._load_files(settings.BASE_DIR)

        return cls._config_data.get(key, default)

    # @classmethod
    # def _load_file(cls, file_path):
    #     """Load a single file based on its extension."""
    #     if not os.path.isfile(file_path):
    #         return

    #     if file_path.endswith('.json'):
    #         with open(file_path, 'r', encoding='utf-8') as f:
    #             cls._config_data.update(json.load(f))
    #             return
    #     elif file_path.endswith('.toml'):
    #         with open(file_path, 'r', encoding='utf-8') as f:
    #             content = f.read()
    #             print(f"""
    #                   🔍 TOML FILE CONTENT ({file_path}):\n
    #                   {content}""")
    #             try:
    #                 cls._config_data.update(tomllib.loads(content))
    #             except tomllib.TOMLDecodeError as error:
    #                 raise ValueError(
    #                     f'Erro to load TOML file : {file_path}. Details: {error}'
    #                 )
    #     elif file_path.endswith(('.yml', '.yaml')):
    #         with open(file_path, 'r', encoding='utf-8') as f:
    #             cls._config_data.update(yaml.safe_load(f))
    #     elif file_path.endswith('.env'):
    #         load_dotenv(dotenv_path=file_path, override=True)

    # @classmethod
    # def _load_files(cls):
    #     """Load all configuration files."""
    #     if cls._files_checked:
    #         return
    #     cls._files_checked = True

    #     for entry in os.scandir(settings.BASE_DIR):
    #         file_path = os.path.join(settings.BASE_DIR, entry.name)
    #         if entry.is_file():
    #             cls._load_file(file_path)

    # @classmethod
    # def get(cls, key: str, default: Optional[str] = None) -> Optional[str]:
    #     """
    #     Retrieves a configuration value by key.

    #     Args:
    #         key (str): The key to look up.
    #         defautl (Optional[str]): The default value if
    #         the key is not found.

    #     Returns:
    #         Optional[str]: The value of the key or the
    #         default value.
    #     """

    #     if not cls._files_checked:
    #         cls._load_files()
    #     cls._load_files()

    #     return cls._config_data.get(key, os.getenv(key, default))
