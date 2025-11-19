"""
simplipy Configuration System
Centralized configuration management to avoid hard-coded values.
"""

from typing import Dict, Any, Optional
from .errors import ConfigError, ValidationError


class Config:
    """
    Configuration manager for robot settings.
    Use this to store and retrieve configuration values instead of hard-coding.
    """
    
    _instance: Optional['Config'] = None
    _config: Dict[str, Any] = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        if not isinstance(key, str) or not key:
            raise ValidationError("Config key must be a non-empty string")
        self._config[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        if key not in self._config:
            if default is not None:
                return default
            raise ConfigError(f"Configuration key '{key}' not found", config_key=key)
        return self._config[key]
    
    def has(self, key: str) -> bool:
        """Check if a configuration key exists."""
        return key in self._config
    
    def load_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """Load configuration from a dictionary."""
        if not isinstance(config_dict, dict):
            raise ValidationError("Config must be loaded from a dictionary")
        self._config.update(config_dict)
    
    def get_motor_config(self, motor_name: str) -> Dict[str, Any]:
        """Get motor-specific configuration."""
        motor_key = f"motors.{motor_name}"
        if not self.has(motor_key):
            raise ConfigError(f"Motor configuration for '{motor_name}' not found")
        return self.get(motor_key)
    
    def set_motor_config(self, motor_name: str, config: Dict[str, Any]) -> None:
        """Set motor-specific configuration."""
        motor_key = f"motors.{motor_name}"
        self.set(motor_key, config)
    
    def clear(self) -> None:
        """Clear all configuration."""
        self._config.clear()

