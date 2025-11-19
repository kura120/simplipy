"""
simplipy Error Handling
Custom exceptions for better error management and debugging.
"""


class SimpliPyError(Exception):
    """Base exception for all simplipy-related errors."""
    def __init__(self, message: str, component: str = None):
        self.message = message
        self.component = component
        super().__init__(self._format_message())
    
    def _format_message(self) -> str:
        if self.component:
            return f"[{self.component}] {self.message}"
        return self.message


class MotorError(SimpliPyError):
    """Exception raised for motor-related errors."""
    def __init__(self, message: str, can_id: int = None):
        self.can_id = can_id
        super().__init__(message, component="Motor")
        if can_id:
            self.message = f"CAN ID {can_id}: {self.message}"


class ConfigError(SimpliPyError):
    """Exception raised for configuration-related errors."""
    def __init__(self, message: str, config_key: str = None):
        self.config_key = config_key
        super().__init__(message, component="Config")
        if config_key:
            self.message = f"Config '{config_key}': {self.message}"


class ValidationError(SimpliPyError):
    """Exception raised for validation errors."""
    def __init__(self, message: str, value=None):
        self.value = value
        super().__init__(message, component="Validation")
        if value is not None:
            self.message = f"{self.message} (value: {value})"

