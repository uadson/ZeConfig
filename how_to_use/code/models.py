"""
This module provides a class for managing application configurations, 
supporting both TOML and JSON file formats. It includes functionality 
to automatically identify configuration file locations, parse their contents, 
and manage environment-specific settings.
"""

import argparse
import json
import os

try:
    import tomllib
except ImportError:
    import tomli as tomllib

import yaml


class ZeConfig:
    
    def __get_file_extension(self, file, path):
        try:
            ext = file.split(".")[1]
        except:
            ext = file.split(".")
            
        match ext:
            case "toml":
                try: 
                    with open(os.path.join(path, file), 'rb') as f:
                        data = tomllib.load(f)
                        return data
                except tomllib.TOMLDecodeError as error:
                    raise ValueError(
                        f"Error parsing the TOML file {file}: {error}"
                    )
            case "json":
                try:
                    with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                        data = json.load(f)
                        return data
                except json.JSONDecodeError as error:
                    raise ValueError(
                        f"Error parsing the JSON file {file}: {error}"
                    )              
            case "env":
                try:
                    with open(os.path.join(path, file)) as f:
                        for line in f:
                            key, value = line.strip().split("=", 1)
                            os.environ[key] = value
                            return (key, value)
                except Exception as exc:
                    raise ValueError(
                        f"Error parsing the ENV file {file}: {exc}"
                    )
            case "yml":
                try:
                    with open(os.path.join(path, file), "r", encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        return data
                except yaml.YAMLError as error:
                    raise ValueError(
                        f"Error parsing the YML file {file}: {exc}"
                    )
            case _:
                return None
            
    def get_file_extension(self, file, path):
        return self.__get_file_extension(file, path)
    
    def __get_file_location(self):

        files = []

        try:
            for dirname in os.scandir(os.path.dirname(os.getcwd())):
                if dirname.is_dir():
                    for file in os.listdir(dirname.path):
                        ext = self.get_file_extension(file, dirname.path)
                        if ext is not None:
                            print(f"File: {ext} on {dirname.path}")
                elif dirname.is_file():
                    ext = self.get_file_extension(dirname.name, os.path.dirname(os.getcwd()))
                    if ext is not None:
                        print(f"File: {ext} on {os.path.dirname(os.getcwd())}")
            #     if dirname.is_dir():
            #         for file in os.listdir(dirname.path):
            #             if "toml" in file.split(".") or "json" in file.split(".") \
            #                 or "env" in file.split("."):
            #                     files.append(file)                    
            #         return files
            #     elif dirname.is_file():
            #         if  "toml" in dirname.name.split(".") \
            #             or "json" in dirname.name.split(".") \
            #                 or "env" in dirname.name.split("."):
            #                     file.append(file)
            #         return files
            # for dirname in os.scandir(os.getcwd()):
            #     print(dirname)
            # raise FileNotFoundError(
            #     f""" Settings file not found
            #     """
            # )        
        except FileNotFoundError as error:
            print(error)
        except Exception as exc:
            print(exc)
        
    def get_file_location(self):
        return self.__get_file_location()
    
    