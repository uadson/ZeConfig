"""
This module provides a class for managing application configurations, 
supporting both TOML and JSON file formats. It includes functionality 
to automatically identify configuration file locations, parse their contents, 
and manage environment-specific settings.
"""

import argparse
import os

try:
    import tomllib
except ImportError:
    import tomli as tomllib


class ZeConfig:
    """
    ZeConfig is a class that manages application configurations,
    making it easier to access sensitive data and database connection
    information.

    Attributes:
        settings_file (str): Name of the configuration file.
        env (str): Current environment (e.g., development, staging, production).

    Methods:
        get_file_location(): Retrieves the location of the configuration file.
        get_file_extension(): Returns the file extension of the configuration file.
        file_reader(): Reads and parses the configuration file.
        set_env(env_name: str): Sets the application environment.
        get_env(key: str): Retrieves a specific key's value for the current environment.
    """

    def __init__(self, settings_file: str, project_name: str, env: str = None):
        """
        Initializes the ZeConfig object.

        Args:
            settings_file (str): Name of the configuration file.
            project_name (str): Name of the project for environment variable purposes.
            env (str, optional): Initial environment name. Defaults to detecting 
                                 the environment from CLI arguments or system variables.
        """
        self.settings_file = settings_file
        self.project_name = project_name
        self.env = env or self.__get_env_from_cli_or_variable()

    def __get_env_from_cli_or_variable(self):
        """
        Determines the environment based on CLI arguments or an environment variable.

        Returns:
            str: The name of the environment (e.g., 'development', 'staging', 'production').
        """
        parser = argparse.ArgumentParser(description='Zeconfig CLI Tool')
        parser.add_argument(
            '--dev',
            action='store_true',
            help='Set the enviroment to development',
        )

        parser.add_argument(
            '--staging',
            action='store_true',
            help='Set the enviroment to staging',
        )

        parser.add_argument(
            '--prod',
            action='store_true',
            help='Set the enviroment to production',
        )

        args = parser.parse_args()

        if args.dev:
            os.environ[self.project_name] = 'development'
        elif args.staging:
            os.environ[self.project_name] = 'staging'
        elif args.prod:
            os.environ[self.project_name] = 'production'

        return os.getenv(self.project_name, 'development')

    def __get_file_location(self):
        """
        Locates the configuration file within the current directory or its subdirectories.

        Returns:
            str: The full path to the configuration file.

        Raises:
            FileNotFoundError: If the file cannot be located.
            RuntimeError: If an unexpected error occurs.
        """
        try:
            for dirname in os.scandir(os.getcwd()):
                if dirname.is_dir():
                    if self.settings_file in os.listdir(dirname.path):
                        return os.path.join(dirname.path, self.settings_file)
                elif dirname.is_file():
                    if self.settings_file == dirname.name:
                        return dirname.path
            raise FileNotFoundError(
                f"""
                Settings file '{self.settings_file}' not found
                in the current directory or subdirectores."""
            )
        except FileNotFoundError as exc:
            raise exc

        except Exception as exc:
            raise RuntimeError(
                f'An unexpected error occurred while locating the file: {exc}'
            )

    def get_file_location(self):
        """
        Public method to retrieve the file location.

        Returns:
            str: The full path to the configuration file.
        """
        return self.__get_file_location()

    def __get_file_extension(self):
        """
        Retrieves the file extension of the configuration file.

        Returns:
            str: The file extension.
        """
        try:
            file_path = self.__get_file_location()
            filename = str(file_path).split('/')[-1]
            file_extension = filename.split('.')[-1]
            return file_extension
        except Exception as exc:
            return exc

    def get_file_extension(self):
        """
        Public method to retrieve the file extension.

        Returns:
            str: The file extension.
        """
        return self.__get_file_extension()

    def __file_reader(self):
        """
        Reads and parses the configuration file.

        Returns:
            dict: The parsed data from the configuration file.

        Raises:
            ValueError: If the file format is unsupported or contains parsing errors.
            FileNotFoundError: If the file cannot be located.
            RuntimeError: If an unexpected error occurs during file reading.
        """
        try:
            file_path = self.__get_file_location()
            file_extension = file_path.split('.')[-1]

            if file_extension != 'toml':
                raise ValueError(
                    f"""Unsupported file type: '{file_extension}'.
                    Only TOML files are supported."""
                )

            with open(file_path, 'rb') as file:
                try:
                    data = tomllib.load(file)
                    return data
                except tomllib.TOMLDecodeError as exc:
                    raise ValueError(
                        f"Error parsing the TOML file '{file_path}': {exc} "
                    )
        except FileNotFoundError:
            raise FileNotFoundError(
                f"File '{self.settings_file}' could not be found."
            )
        except Exception as exc:
            raise RuntimeError(
                f'An unexpected error occurred while reading the file: {exc}.'
            )

    def file_reader(self):
        """
        Public method to read and parse the configuration file.

        Returns:
            dict: The parsed data from the configuration file.
        """
        return self.__file_reader()

    def __set_env(self, env_name: str):
        """
        Sets the current environment for the application.

        Args:
            env_name (str): Name of the environment to set.

        Raises:
            KeyError: If the specified environment does not exist in the configuration file.
            RuntimeError: If an unexpected error occurs while setting the environment.
        """
        try:
            data = self.__file_reader()
            if env_name not in data:
                raise KeyError(
                    f"""
                    The environment '{env_name}' does not exist
                    in the configuration file '{self.settings_file}'."""
                )
            self.env = env_name
        except KeyError as exc:
            raise exc
        except Exception as exc:
            raise RuntimeError(
                f"""An unexpected error occurred
                while setting the environment: {exc}"""
            )

    def set_env(self, env_name: str):
        """
        Public method to set the current environment.

        Args:
            env_name (str): Name of the environment to set.
        """
        return self.__set_env(env_name)

    def get_env(self, key: str):
        """
        Retrieves a specific key's value for the current environment.

        Args:
            key (str): The key to retrieve from the environment configuration.

        Returns:
            Any: The value associated with the specified key.

        Raises:
            KeyError: If the environment or key is not found in the configuration file.
            FileNotFoundError: If the configuration file cannot be located.
            RuntimeError: If an unexpected error occurs while accessing the data.
        """
        try:
            data = self.__file_reader()
            if self.env not in data:
                raise KeyError(
                    f"""Environment '{self.env}' not found in
                    the configuration file '{self.settings_file}'."""
                )

            env_data = data[self.env]
            if key not in env_data:
                raise KeyError(
                    f"""Key '{key}' not found in environment '{self.env}'.
                    Check your TOML file."""
                )

            return env_data[key]
        except KeyError as exc:
            raise exc
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Configuration file '{self.settings_file}' not found."
            )
        except Exception as exc:
            raise RuntimeError(
                f"""An unexpected error occurred while accessing
                the environment data: {exc}"""
            )
