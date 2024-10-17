try:
    import tomllib
except ImportError:
    import tomli as tomllib


class ZeConfig:
    """
        ZeConfig é uma gerenciador de configurações.
        
        Ele identifica as configurações de uma aplição, como conexão com banco de dados,
        dados de registros mais sensíveis e torna mais simples a gestão dos mesmos.
        
        Atributo(s):
        
        settings_file: type(str) = recebe o caminho ao qual está o arquivo de configuração com extensão .toml
        
        Método(s):
        
        config: function() = realiza a leitura do arquivo e retorna os dados lidos.
        
        -------------------------------------------------------------------------------------------------------
        ZeConfig is a configuration manager.

        It identifies the configurations of an application, such as database connection,
        more sensitive registry data and makes their management easier.

        Attribute(s):

        settings_file: type(str) = receives the path to the configuration file with the .toml extension

        Method(s):

        config: function() = reads the file and returns the data read.
    """
    
    def __init__(self, settings_file: str):
        self.settings_file = settings_file

    def config(self):
        with open(self.settings_file, 'rb') as file:
            settings = tomllib.load(file)
        return settings
