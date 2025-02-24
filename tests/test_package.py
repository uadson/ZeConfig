from src.ze import ConfigManager, config


def test_load_settings_file(settings_file):
    ConfigManager.add_config_file(str(settings_file / '.env'))
    ConfigManager.add_config_file(str(settings_file / 'config.json'))
    ConfigManager.add_config_file(str(settings_file / 'config.toml'))
    ConfigManager.add_config_file(str(settings_file / 'config.yml'))
    ConfigManager.add_config_file(str(settings_file / 'config.yaml'))

    assert config('DATABASE_URL_ENV') == 'postgres://env_user:pass@localhost/db'
    assert config('DATABASE_URL') == 'postgres://json_user:pass@localhost/db'
    assert config('database_url') == 'postgres://toml_user:pass@localhost/db'
    assert config('DATABASE_URL_YML') == 'postgres://yml_user:pass@localhost/db'
    assert config('DATABASE_URL_YAML') == 'postgres://yaml_user:pass@localhost/db'
