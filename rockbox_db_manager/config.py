import json
import logging

def load_config(config_file):
    """Load the configuration file for tag mappings and default values."""
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
            logging.info(f"Loaded config: {config_file}")
            return config
    except FileNotFoundError:
        logging.error(f"Config file not found: {config_file}")
        return {}
    except json.JSONDecodeError as e:
        logging.error(f"Error parsing config file {config_file}: {e}")
        return {}

def get_mapping(config, tag):
    """Get the tag mapping from the configuration, if it exists."""
    return config.get("mappings", {}).get(tag, tag)  # Return the mapped tag or the original tag if no mapping is found

def get_default_value(config, tag):
    """Get the default value for a tag from the configuration, if it exists."""
    return config.get("default_values", {}).get(tag, f"Unknown {tag.capitalize()}")