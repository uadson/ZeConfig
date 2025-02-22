import json
from abc import ABC, abstractmethod
from pathlib import Path

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
        return tomllib.load(file_path)


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


class ParserFactory:
    """Factory class that returns the correct parser
    based on the file extension.
    """

    _parsers = {
        '.json': JSONParser,
        '.toml': TOMLParser,
        '.yml': YAMLParser,
        '.yaml': YAMLParser,
        '.env': ENVParser,
    }

    @staticmethod
    def get_parser(file_path: str) -> ConfigParser:
        """
        Returns the appropriate parser for the given
        file extension.

        Args:
            file_path (str): Path to the configuration
            file.

        Returns:
            ValueError: If the file extension is not
            supported.
        """

        ext = Path(file_path).suffix
        parser_class = ParserFactory._parsers.get(ext)

        if not parser_class:
            raise ValueError(f"Unsupported file extension: '{ext}'.")

        return parser_class()
