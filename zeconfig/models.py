import json
import os
import pathlib

try:
    import tomllib
except ImportError:
    import tomli as tomllib

from .exc import FilenameError


class ZeConfig:
    """
    PT-BR
    ZeConfig é uma classe que gerencia as configurações de uma aplicação,
    facilitando o acesso a dados sensíveis e informações de conexão com
    banco de dados.
    A classe suporta arquivos de configuração em formato TOML e JSON,
    identificando automaticamente o tipo de arquivo e retornando seu
    conteúdo de forma estruturada.

    ----------------------------------------------------------------------

    EN
    ZeConfig is a class that manages application configurations,
    making it easier to access sensitive data and database connection
    information.
    The class supports configuration files in TOML and JSON formats,
    automatically identifying the file type and returning its content
    in a structured format.

    """

    def __init__(self, root_path=False):
        self.root_path = root_path

    @staticmethod
    def __get_file_extension(filename: str):
        """
        Obtêm e retorna a extensão do arquivo.
        """
        if not filename:
            raise FilenameError()

        file_extension = filename.split('.')[-1]
        return file_extension

    def get_file_extension(self, filename: str):
        return self.__get_file_extension(filename=filename)

    def __get_root_path_name(self):
        """
        Obtém o nome do diretório raiz do caminho atual,
        se `root_path` estiver configurado.
        """
        if self.root_path:
            root_path = pathlib.Path(os.path.abspath(os.getcwd()))
            return root_path.name
        else:
            return None

    def get_root_path_name(self):
        return self.__get_root_path_name()

    # def __validate_config_dir_name(self):
    #     if self.root_path and self.config_dir_name != '':
    #         root_path = pathlib.Path(os.path.abspath(os.getcwd()))

    #         for dir in os.scandir(self.root_path):
    #             if dir.is_dir and dir.name == self.config_dir_name:
    #                 settings_file = self.settings_file
    #                 self.settings_file = os.path.join(
    #                       root_path,
    #                       root_path.name,
    #                       self.config_dir_name,
    #                       settings_file)
    #         return self.settings_file
    #     elif self.root_path and self.config_dir_name == '':
    #         raise ConfigDirError

    def __file_reader(self, filename: str):
        file_extension = self.__get_file_extension(filename=filename)

        match file_extension:
            case 'toml':
                with open(filename, 'rb') as file:
                    data = tomllib.load(file)
                return data
            case 'json':
                with open(filename, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                return data
            case _:
                raise ValueError('No support to the file type yet')

    def file_reader(self, filename: str):
        return self.__file_reader(filename=filename)

    def __set_config(self, project_name: str, filename: str):
        settings_data = self.__file_reader(filename=filename)
        return settings_data

    def config(self, project_name: str, filename: str):
        return self.__set_config(project_name=project_name, filename=filename)
