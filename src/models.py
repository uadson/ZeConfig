import json
from abc import ABC, abstractmethod

import yaml
from dotenv import dotenv_values

try:
    import tomllib
except ImportError:
    import tomli as tomllib


class ConfigParser(ABC):
    """
    Abstract base class for configuration
    file parses.
    """

    @abstractmethod
    def parse(self, file_path: str) -> dict:
        """
        Parses a configuration file.

        Args:
            file_path (str): Path to the
            configuration file.

        Returns:
            dict: Parsed configuration data.
        """
        pass


class JSONParser(ConfigParser):

    @classmethod
    def parse(cls, file_path: str) -> dict:
        """Parses a JSON configuration file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)


class TOMLParser(ConfigParser):
    
    @classmethod
    def parse(cls, file_path: str) -> dict:
        """Parses a YAML configuration file."""
        with open(file_path, "rb") as file:
            return tomllib.load(file)


class YAMLParser(ConfigParser):
    
    @classmethod
    def parse(cls, file_path: str) -> dict:
        """Parses a YAML configuration file."""
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)


class ENVParser(ConfigParser):
    
    @classmethod
    def parse(cls, file_path: str) -> dict:
        """Parses a .env configuration file."""
        return dotenv_values(file_path)
