"""
simplipy NetworkTables
Enhanced NetworkTables wrapper for easier data management.
"""

import ntcore
from typing import Any, Optional
from ..utils.logger import SimpliPyLogger


class NetworkTable:
    """
    Enhanced NetworkTables wrapper with simplified interface.
    """
    
    _instance: Optional[ntcore.NetworkTableInstance] = None
    _tables: dict = {}
    
    def __init__(self, table_name: str = "datatable"):
        """
        Initialize NetworkTable.
        
        Args:
            table_name: Name of the NetworkTable
        """
        if NetworkTable._instance is None:
            NetworkTable._instance = ntcore.NetworkTableInstance.getDefault()
            SimpliPyLogger.info("NetworkTables instance created", "NetworkTable")
        
        if table_name not in NetworkTable._tables:
            NetworkTable._tables[table_name] = NetworkTable._instance.getTable(table_name)
            SimpliPyLogger.info(f"NetworkTable '{table_name}' initialized", "NetworkTable")
        
        self.table = NetworkTable._tables[table_name]
        self.table_name = table_name
    
    def put_number(self, key: str, value: float) -> None:
        """Put a number value."""
        try:
            self.table.putNumber(key, value)
        except Exception as e:
            SimpliPyLogger.error(f"Failed to put number '{key}'", "NetworkTable", e)
    
    def get_number(self, key: str, default: float = 0.0) -> float:
        """Get a number value."""
        try:
            return self.table.getNumber(key, default)
        except Exception as e:
            SimpliPyLogger.error(f"Failed to get number '{key}'", "NetworkTable", e)
            return default
    
    def put_boolean(self, key: str, value: bool) -> None:
        """Put a boolean value."""
        try:
            self.table.putBoolean(key, value)
        except Exception as e:
            SimpliPyLogger.error(f"Failed to put boolean '{key}'", "NetworkTable", e)
    
    def get_boolean(self, key: str, default: bool = False) -> bool:
        """Get a boolean value."""
        try:
            return self.table.getBoolean(key, default)
        except Exception as e:
            SimpliPyLogger.error(f"Failed to get boolean '{key}'", "NetworkTable", e)
            return default
    
    def put_string(self, key: str, value: str) -> None:
        """Put a string value."""
        try:
            self.table.putString(key, value)
        except Exception as e:
            SimpliPyLogger.error(f"Failed to put string '{key}'", "NetworkTable", e)
    
    def get_string(self, key: str, default: str = "") -> str:
        """Get a string value."""
        try:
            return self.table.getString(key, default)
        except Exception as e:
            SimpliPyLogger.error(f"Failed to get string '{key}'", "NetworkTable", e)
            return default
    
    @classmethod
    def get_instance(cls) -> ntcore.NetworkTableInstance:
        """Get the NetworkTables instance."""
        if cls._instance is None:
            cls._instance = ntcore.NetworkTableInstance.getDefault()
        return cls._instance
