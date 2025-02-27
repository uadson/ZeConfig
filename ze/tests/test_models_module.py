from ze.src.models import ENVParser, JSONParser, TOMLParser, YAMLParser


def test_model_json_parser(json_file):
    """
    Tests the JSONParser's ability to correctly parse a JSON file.

    Args:
        json_file (tuple): A tuple containing the file path of the JSON file
        and the expected data after parsing.
    """
    file_path, expected_data = json_file
    assert JSONParser.parse(file_path) == expected_data


def test_toml_parser(toml_file):
    """
    Tests the TOMLParser's ability to correctly parse a TOML file.

    Args:
        toml_file (tuple): A tuple containing the file path of the TOML file
        and the expected data after parsing.
    """
    file_path, expected_data = toml_file
    assert TOMLParser.parse(file_path) == expected_data


def test_yaml_parser(yaml_file):
    """
    Tests the YAMLParser's ability to correctly parse a YAML file.

    Args:
        yaml_file (tuple): A tuple containing the file path of the YAML file
         and the expected configuration after parsing.
    """
    file_path, expected_conf = yaml_file
    assert YAMLParser.parse(file_path) == expected_conf


def test_env_parser(env_file):
    """
    Tests the ENVParser's ability to correctly parse an environment file
    (assumed to be similar to TOML in this case).

    Args:
        toml_file (tuple): A tuple containing the file path of the environment file
        (treated as TOML-like here) and the expected configuration after parsing.
    """
    file_path, excepted_conf = env_file
    assert ENVParser.parse(file_path) == excepted_conf
