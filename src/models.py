import json
from abc import ABC, abstractmethod

from dotenv import dotenv_values

try:
    import tomllib
except ImportError:
    import tomli as tomllib
from pathlib import Path

import yaml


class ConfigParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> dict:
        pass


class JSONParser(ConfigParser):
    def parse(self, file_path: str) -> dict:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)


class TOMLParser(ConfigParser):
    def parse(self, file_path: str) -> dict:
        return tomllib.load(file_path)


class YAMLParser(ConfigParser):
    def parse(self, file_path: str) -> dict:
        with open(file_path, "r", encoding="utf-8") as file:
            return yaml.safe_load(file)


class EnvParser(ConfigParser):
    def parse(self, file_path: str) -> dict:
        return dotenv_values(file_path)


class ParserFactory:
    _parsers = {
        ".json": JSONParser,
        ".toml": TOMLParser,
        ".yml": YAMLParser,
        ".yaml": YAMLParser,
        ".env": EnvParser,
    }

    @staticmethod
    def get_parser(file_path: str) -> ConfigParser:
        ext = Path(file_path).suffix
        parser_class = ParserFactory._parsers.get(ext)
