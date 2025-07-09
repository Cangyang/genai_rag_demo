import yaml
import sys



def load_config():
    with open('config.yaml', 'r') as stream:
        config = yaml.safe_load(stream) 
        return config


def get_config_val(config_name:str, config_prefix:str = None ):
    config = load_config()
    child_config = config.get(config_prefix) if config_prefix and config.get(config_prefix) else config
    return child_config.get(config_name) if config_name else child_config


def get_operating_system_name():
    sys_name = "Linux"
    if sys.platform.startswith('linux'):
        sys_name = "Linux"
    elif sys.platform.startswith('darwin'):
        sys_name = "macOS"
    elif sys.platform.startswith('win32'):
        sys_name = "Windows"
    return sys_name





