from pathlib import Path
from typing import Optional

from .core import get_file_data
from .settings import settings


class ConfigManager:
    """Central configuration management handler with lazy-loaded file parsing.

    Implements a singleton-like pattern to manage application configuration through
    various file formats. Automatically searches for configuration files in either
    CONF_DIR or BASE_DIR locations defined in settings.

    Class Attributes:
        _files_checked (bool): Flag indicating if configuration files have been loaded
        _config_data (Dict): Cache storing combined configuration data
        _config_files (List): Collection of discovered configuration filenames
    """

    _files_checked = False
    _config_data = {}
    _config_files = []

    @classmethod
    def _load_config_files(cls):
        """Load configuration files from predefined directories.

        Searches configuration directories in this order:
        1. Primary configuration directory (CONF_DIR from settings)
        2. Fallback to base directory (BASE_DIR from settings)

        Note:
            Executes only once per class lifecycle (idempotent operation).
            Modifies class attributes _config_files and _config_data in-place.
        """

        if cls._files_checked:
            return

        cls._files_checked = True

        if Path(settings.CONF_DIR).exists():
            path = Path(settings.CONF_DIR)
            get_file_data(cls._config_files, cls._config_data, path)
        elif Path(settings.BASE_DIR).exists():
            path = Path(settings.BASE_DIR)
            get_file_data(cls._config_files, cls._config_data, path)

    @classmethod
    def get(cls, key: str, default: Optional[str] = None) -> Optional[str]:
        """Retrieve configuration value with error handling and lazy initialization.

        Args:
            key: Configuration key to look up
            default: Fallback value if key not found (default: None)

        Returns:
            Configuration value as string if found, default value if provided

        Raises:
            ValueError: When key is not found and no default is provided

        Note:
            Automatically triggers configuration loading on first access.
            Uses colorama for colored terminal error messages.
        """
        if not cls._files_checked:
            cls._load_config_files()
        cls._load_config_files()

        if cls._config_data.get(key, default) is None:
            raise ValueError(f"""Key: '{key}' not found or file non exists""")
        return cls._config_data.get(key, default)
