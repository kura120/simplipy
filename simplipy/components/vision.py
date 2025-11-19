"""
simplipy Vision System
Simplified vision processing integration.
"""

from typing import Optional, Dict, Any
import ntcore
from ..utils.logger import SimpliPyLogger


class Vision:
    """
    Enhanced vision system with NetworkTables integration.
    """
    
    def __init__(self, table_name: str = "vision"):
        """
        Initialize vision system.
        
        Args:
            table_name: NetworkTables table name for vision data
        """
        try:
            self.inst = ntcore.NetworkTableInstance.getDefault()
            self.table = self.inst.getTable(table_name)
            SimpliPyLogger.info(f"Vision system initialized with table '{table_name}'", "Vision")
        except Exception as e:
            SimpliPyLogger.error("Failed to initialize vision system", "Vision", e)
            raise
    
    def get_target_data(self, target_name: str = "target") -> Optional[Dict[str, Any]]:
        """
        Get target data from NetworkTables.
        
        Args:
            target_name: Name of the target entry
        
        Returns:
            Dictionary with target data or None if not found
        """
        try:
            has_target = self.table.getBoolean("hasTarget", False)
            if not has_target:
                return None
            
            return {
                "has_target": has_target,
                "x": self.table.getNumber("x", 0.0),
                "y": self.table.getNumber("y", 0.0),
                "area": self.table.getNumber("area", 0.0),
                "distance": self.table.getNumber("distance", 0.0),
            }
        except Exception as e:
            SimpliPyLogger.error("Failed to get target data", "Vision", e)
            return None
    
    def publish_data(self, data: Dict[str, Any]) -> None:
        """
        Publish vision data to NetworkTables.
        
        Args:
            data: Dictionary of vision data to publish
        """
        try:
            for key, value in data.items():
                if isinstance(value, bool):
                    self.table.putBoolean(key, value)
                elif isinstance(value, (int, float)):
                    self.table.putNumber(key, float(value))
                elif isinstance(value, str):
                    self.table.putString(key, value)
            SimpliPyLogger.info(f"Published vision data: {list(data.keys())}", "Vision")
        except Exception as e:
            SimpliPyLogger.error("Failed to publish vision data", "Vision", e)

