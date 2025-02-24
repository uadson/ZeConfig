import json

class ConfigManager:
    """Manages configuration file loading and
    key retrieval
    """

    _config_data = {}
    _files_checked = False
    _config_files = []
    
    @classmethod
    def add_config_file(cls, file_path):
        """Adds a configuration file to the list to be loaded."""
        cls._config_files.append(file_path)
        
    @classmethod
    def _load_files(cls):
        """Load all configuration files."""
        if cls._files_checked:
            return
        cls._files_checked = True
        
        for file_path in cls._config_files:
            cls._load_file(file_path)
        
    @classmethod
    def _load_file(cls, file_path):
        """Load a single file based on its extension."""
        if file_path.endswith('.json'):
            with open(file_path, 'r', encoding='utf-8') as f:
                cls._config_data.update(json.load(f))
        elif file_path.endswith('.toml'):
            with open(file_path, 'rb') as f:
                cls._config_data.update(tomllib.load(f))
        elif file_path.endswith(('.yml', '.yaml')):
            with open(file_path, 'r', encoding='utf-8') as f:
                cls._config_data.update(yaml.safe_load(f))
        elif file_path.endswith('.env'):
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=file_path, override=True)
        
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

        return cls._config_data.get(key, os.getenv(key, default))
