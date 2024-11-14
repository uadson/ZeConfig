import json
import os
import pathlib


try:
    import tomllib
except ImportError:
    import tomli as tomllib


class ConfigDirError(Exception):
    def __init__(self, message="A directory name must be provided"):
        self.message = message
        super().__init__(self.message)


class ZeConfig:
    """
    PT-BR
    ZeConfig é uma classe que gerencia as configurações de uma aplicação,
    facilitando o acesso a dados sensíveis e informações de conexão com
    banco de dados.
    A classe suporta arquivos de configuração em formato TOML e JSON,
    identificando automaticamente o tipo de arquivo e retornando seu
    conteúdo de forma estruturada.

    Parâmetros:
    - settings_file (str): Caminho do arquivo de configuração a ser lido.

    Métodos:
    - get_file_extension() -> str:
        Retorna a extensão do arquivo de configuração.
    - file_reader() -> dict:
        Realiza a leitura do arquivo de configuração e retorna os dados
        lidos.
        Lança um erro caso o tipo de arquivo não seja suportado.
    - config() -> dict:
        Retorna os dados das configurações obtidos a partir do arquivo
        especificado.

    ----------------------------------------------------------------------

    EN
    ZeConfig is a class that manages application configurations,
    making it easier to access sensitive data and database connection
    information.
    The class supports configuration files in TOML and JSON formats,
    automatically identifying the file type and returning its content
    in a structured format.

    Parameters:
    - settings_file (str): Path to the configuration file to be read.

    Methods:
    - get_file_extension() -> str:
        Returns the file extension of the configuration file.
    - file_reader() -> dict:
        Reads the configuration file and returns the data.
        Raises an error if the file type is not supported.
    - config() -> dict:
        Returns configuration data obtained from the specified file.
    """

    def __init__(
        self, 
        settings_file: str, 
        root_path: bool = False,
        config_dir_name: str = '',
        settings_file_path = '',
    ):
        self.settings_file = settings_file
        self.root_path = root_path
        self.config_dir_name = config_dir_name
        self.settings_file_path = settings_file_path

    def __get_file_extension(self):
        file_extension = self.settings_file.split('.')[-1]
        return file_extension

    def get_file_extension(self):
        return self.__get_file_extension()

    def __get_root_path_name(self):
        if self.root_path:
            root_path = pathlib.Path(os.path.abspath(os.getcwd()))
            return root_path.name
        else:
            return None

    def get_root_path_name(self):
        return self.__get_root_path_name()

    def __validate_config_dir_name(self):
        if self.root_path and self.config_dir_name != '':
            root_path = pathlib.Path(os.path.abspath(os.getcwd()))
            
            for dir in os.scandir(self.root_path):
                if dir.is_dir and dir.name == self.config_dir_name:
                    settings_file = self.settings_file
                    self.settings_file = os.path.join(root_path, root_path.name, self.config_dir_name, settings_file)
            return self.settings_file
        elif self.root_path and self.config_dir_name == '':
            raise ConfigDirError
            
        
    def __file_reader(self):
        file_extension = self.__get_file_extension()

        match file_extension:
            case 'toml':
                with open(self.settings_file, 'rb') as file:
                    data = tomllib.load(file)
                return data
            case 'json':
                with open(self.settings_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                return data
            case _:
                raise ValueError('No support to the file type yet')

    def file_reader(self):
        return self.__file_reader()

    def __set_config(self):
        settings_data = self.__file_reader()
        return settings_data

    def config(self):
        return self.__set_config()
