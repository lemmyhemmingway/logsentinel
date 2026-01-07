import yaml
from pathlib import Path
from typing import Dict, Any
from src.exceptions import ConfigurationError

class ConfigLoader:
    """Read and parse config yaml"""
    
    @staticmethod
    def load_config(config_path: str = "config.yaml") -> Dict[str, Any]:
        path = Path(config_path)
        
        if not path.exists():
            raise ConfigurationError(f"Config not found: {path.absolute()}")

        try:
            with open(path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                
            if not config:
                raise ConfigurationError("Config file empty!")
                
            return config
            
        except yaml.YAMLError as e:
            raise ConfigurationError(f"YAML format error: {e}")
