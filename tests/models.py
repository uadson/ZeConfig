import os

try:
    import tomllib
except ImportError:
    import tomli as tomllib


class ZeconfigMock:
    def __init__(self, settings_file: str, project_name: str):
        self.settings_file = settings_file
        self.project_name = project_name
        self.env = 'development'

    def __get_file_location(self):
        try:
            for dirname in os.scandir(os.getcwd()):
                if dirname.is_dir():
                    if self.settings_file in os.listdir(dirname.path):
                        return os.path.join(dirname.path, self.settings_file)
                elif dirname.is_file():
                    if self.settings_file == dirname.name:
                        return dirname.path
        except Exception as exc:
            return exc

    def get_file_location(self):
        return self.__get_file_location()

    def __get_file_extension(self):
        try:
            file_path = self.__get_file_location()
            filename = str(file_path).split('/')[-1]
            file_extension = filename.split('.')[-1]
            return file_extension
        except Exception as exc:
            return exc

    def get_file_extension(self):
        return self.__get_file_extension()

    def __file_reader(self):
        file_extension = self.__get_file_extension()

        if file_extension == 'toml':
            with open(self.settings_file, 'rb') as file:
                data = tomllib.load(file)
            return data
        else:
            raise ValueError('No support to the file type yet')

    def file_reader(self):
        return self.__file_reader()

    def __set_config(self):
        pass