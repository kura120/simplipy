"""
simplipy Logger Utility
Simple logging wrapper for robot debugging.
"""

import wpilib


class SimpliPyLogger:
    """Simple logger for simplipy components."""
    
    @staticmethod
    def info(message: str, component: str = "simplipy"):
        """Log an info message."""
        wpilib.DataLogManager.log(f"[{component}] {message}")
    
    @staticmethod
    def warning(message: str, component: str = "simplipy"):
        """Log a warning message."""
        wpilib.DataLogManager.log(f"[{component}] WARNING: {message}")
    
    @staticmethod
    def error(message: str, component: str = "simplipy", exception: Exception = None):
        """Log an error message."""
        error_msg = f"[{component}] ERROR: {message}"
        if exception:
            error_msg += f" - {type(exception).__name__}: {str(exception)}"
        wpilib.DataLogManager.log(error_msg)
        if exception:
            wpilib.reportError(error_msg, exception)

