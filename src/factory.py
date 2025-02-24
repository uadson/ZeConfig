from pathlib import Path

from models import (
    ConfigParser,
    JSONParser,
    TOMLParser,
    YAMLParser,
    ENVParser
)


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