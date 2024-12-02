class FilenameError(Exception):
    """
    Retorna uma mensagem de erro quando o nome do arquivo de configuração
    não é informado.
    """

    def __init__(self, message='A file name must be provided'):
        self.message = message
        super().__init__(self.message)


class ConfigDirError(Exception):
    def __init__(self, message='A directory name must be provided'):
        self.message = message
        super().__init__(self.message)
