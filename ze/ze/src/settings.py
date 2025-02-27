import os
from pathlib import Path
from typing import Optional


class Settings:
    """Configuration settings for the application's directory structure.

    Provides paths for essential directory locations within the project.

    Attributes:
        BASE_DIR (Optional[str]): Absolute path to the project's base directory,
            derived from this file's location. Initialized at module load time.
        CONF_DIR (Optional[str]): Absolute path to the configuration directory,
            located under the base directory. Defaults to 'configs' subdirectory.

    Note:
        Paths are resolved at class definition time and will not dynamically
        follow file system changes after initialization.
    """

    BASE_DIR: Optional[str] = Path(__file__).resolve().parent
    CONF_DIR: Optional[str] = os.path.join(Path(__file__).resolve().parent, 'configs')


settings: Settings = Settings()
"""Singleton instance of Settings providing configuration paths.

This ready-to-use instance provides immediate access to the predefined
directory paths without requiring explicit class instantiation.
"""
