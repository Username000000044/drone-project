import json

def load_config_file(config_file, required_keys=None):
    """
    Loads a JSON config file and optionally returns only the specified keys.

    Args:
        config_file (str): Path to the JSON config file.
        required_keys (list of str): Specific keys to extract from the config. 
                                     If None, returns the entire JSON object.

    Returns:
        A tuple of values corresponding to the required_keys if provided,
        or the entire JSON object.
    """
    try:
        with open(config_file, "r") as file:
            config_data = json.load(file)

        if required_keys:
            return tuple(config_data.get(key) for key in required_keys)
        return config_data

    except FileNotFoundError:
        print(f"📁 {config_file} file not found. Make sure it's in the correct folder.")
        return (None,) * len(required_keys) if required_keys else None
    except json.JSONDecodeError:
        print(f"📁 Error decoding {config_file}. Please check the file format.")
        return (None,) * len(required_keys) if required_keys else None
