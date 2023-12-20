import yaml


def parse_config():
    file_path = 'config/config.yaml'

    yaml_data = None
    try:
        with open(file_path, 'r') as yaml_file:
            yaml_data = yaml.safe_load(yaml_file)
    except FileNotFoundError:
        pass
    return yaml_data
