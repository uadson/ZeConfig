import os

from src.factory import ParserFactory

from typing import List, AnyStr, Dict


def parse_data(
    config_data: Dict,
    path: AnyStr,
    file: AnyStr,
):
    """Parse a configuration file and update the configuration data dictionary.
    
    Args:
        config_data (Dict): Dictionary containing existing configuration data 
        to be updated with new parsed data.
        path (AnyStr): Directory path where the configuration file is located.
        file (AnyStr): Name of the configuration file to parse.
        
    Note:
        Uses the appropriate parser from ParserFactory based on the file extension.
        Modifies the config_data dictionary in-place with parsed results.
    """
    file_path = os.path.join(
        path, file
    )
    parser = ParserFactory.get_parser(file)
    config_data.update(
        parser.parse(file_path)
    )


def get_file_data(
    config_files: List,
    config_data:  Dict,
    path: AnyStr
):
    """Collect and process configuration files from a directory.
    
    Scans the specified directory for files, adds them to the config_files list,
    and parses supported file formats to update configuration data.
    
    Args:
        config_files (List): List to be populated with filenames found in the directory.
        config_data (Dict): Dictionary to store aggregated configuration data.
        path (AnyStr): Path of the directory to scan for configuration files.
        
    Note:
        Processes files with the following extensions: .json, .toml, .yaml, .yml.
        Skips files with unsupported extensions.
    """
    
    for entry in os.scandir(path):
        if entry.is_file():
            config_files.append(entry.name)
    
    for file in config_files:
        if file.endswith(".json"):
            parse_data(config_data, path, file)
        elif file.endswith(".toml"):
            parse_data(config_data, path, file)
        elif file.endswith((".yaml", ".yml")):
            parse_data(config_data, path, file)
        elif file.endswith(".env") or file.startswith(".env"):
            parse_data(config_data, path, file)
