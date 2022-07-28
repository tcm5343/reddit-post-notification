from json import load
from pathlib import Path
import sys


# pylint: disable=broad-except
def import_config(config_file_name: str) -> dict:
    try:
        with Path(config_file_name).open('r', encoding='utf-8') as file_stream:
            config = load(file_stream)
            return config
    except FileNotFoundError as err:
        simple_error_message = f"Error: {config_file_name} is not found, \
            create it based on the example_config.json"
        print(simple_error_message, err)
        sys.exit()
    except ValueError as err:
        simple_error_message = f"Error: {config_file_name} is not formatted correctly"
        print(simple_error_message, err)
        sys.exit()
    except Exception as err:
        simple_error_message = "Error: Unhandled exception with regard to importing config"
        print(simple_error_message, err)
        sys.exit()
# pylint: enable=broad-except
