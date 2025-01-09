# ZeConfig
[![Buid](https://github.com/uadson/ZeConfig/actions/workflows/zconf-build.yml/badge.svg)](https://github.com/uadson/ZeConfig/actions/workflows/zconf-build.yml)
[![Tests](https://github.com/uadson/ZeConfig/actions/workflows/zconf-tests.yml/badge.svg)](https://github.com/uadson/ZeConfig/actions/workflows/zconf-tests.yml)
[![Release](https://github.com/uadson/ZeConfig/actions/workflows/release.yml/badge.svg?branch=main)](https://github.com/uadson/ZeConfig/actions/workflows/release.yml)

ZeConfig is a Python library designed to manage application configurations, making it easier to handle sensitive data and environment-specific settings. It supports configuration files in both TOML and JSON formats and provides utilities for identifying, reading, and parsing configuration files.

## Features

- Automatic detection of configuration file location within the current directory or its subdirectories.
- Support for TOML configuration files.
- Environment management (e.g., development, staging, production).
- Easy access to environment-specific keys and values.

## Installation

Clone the repository or copy the `zeconfig.py` file into your project directory.

```bash
# Clone the repository
git clone https://github.com/uadson/zeconfig.git
```

Ensure you have Python 3.11+ installed. If your Python version is below 3.11, you may need to install the `tomli` library for TOML parsing:

```bash
pip install tomli
```

## Usage

### 1. Initialize ZeConfig

Create an instance of the `ZeConfig` class:

```python
from zeconfig import ZeConfig

# Initialize with the configuration file name and project name
ze = ZeConfig(settings_file="config.toml", project_name="MyApp")
```

### 2. Retrieve Configuration File Location

```python
file_location = ze.get_file_location()
print(f"Configuration file is located at: {file_location}")
```

### 3. Read Configuration Data

Parse the TOML configuration file:

```python
config_data = ze.file_reader()
print(config_data)
```

### 4. Manage Environment Settings

Set the application environment:

```python
ze.set_env("staging")
```

Retrieve a value for a specific key in the current environment:

```python
database_url = ze.get_env("DATABASE_URL")
print(f"Database URL: {database_url}")
```

### 5. Command-Line Integration

The environment can also be set via command-line arguments:

```bash
python your_script.py --dev  # Set environment to development
```

## Configuration File Format

### Example `config.toml`

```toml
[development]
DATABASE_URL = "sqlite:///dev.db"
SECRET_KEY = "dev-secret"

[staging]
DATABASE_URL = "postgresql://staging-user:password@localhost/staging"
SECRET_KEY = "staging-secret"

[production]
DATABASE_URL = "postgresql://prod-user:password@localhost/production"
SECRET_KEY = "prod-secret"
```

## Error Handling

ZeConfig raises descriptive exceptions for common issues:

- `FileNotFoundError`: Configuration file not found.
- `KeyError`: Missing environment or key in the configuration file.
- `ValueError`: Unsupported file type or parsing error.
- `RuntimeError`: Unexpected runtime errors.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request on the [GitHub repository](https://github.com/uadson/zeconfig).

## Contact

For questions or support, please reach out to [uadsonpy@gmail.com](mailto:uadsonpy@gmail.com).


