import yaml
import json


class Parser:
    def parse_config(self):
        file_path = 'config/config.yaml'

        yaml_data = None
        try:
            with open(file_path, 'r') as yaml_file:
                yaml_data = yaml.safe_load(yaml_file)
        except FileNotFoundError:
            pass
        return yaml_data

    def parse_level(self, level):
        json_file_path = "levels/level_" + level + ".json"

        # Read JSON data from the file
        with open(json_file_path, 'r') as file:
            level_data = json.load(file)

        return level_data["events"]
