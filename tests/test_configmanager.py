from src.models.configmanager import ConfigManager
from src.ze import config


def test_load_env_file():
    """Tests whether .env takes priority over other files."""
    # Cache reset
    ConfigManager._files_checked = False
    assert config('DATABASE_URL') == 'postgres://env_user:pass@localhost/db'
