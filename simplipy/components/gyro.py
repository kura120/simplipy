"""
simplipy Gyro/IMU Component (WIP)
Simplified gyro/IMU interface for orientation sensing.
This is a wip, please don't trust this code, im learning how gyros work as i go
"""

from typing import Optional
import wpilib
from ..utils.errors import ValidationError
from ..utils.logger import SimpliPyLogger


class GyroConfig:
    """Configuration for gyro/IMU system.
    Honestly, im not sure if this gyro config system works... hopefully we wont use it
    """
    
    def __init__(self,
                 gyro_type: str = "analog",
                 port: int = 0,
                 inverted: bool = False):
        """
        Initialize gyro configuration.
        
        Args:
            gyro_type: Type of gyro ("analog" for AnalogGyro, "navx" for NavX, etc.)
            port: Port number (analog port for AnalogGyro, or SPI/I2C port)
            inverted: Whether to invert gyro readings
        """
        if gyro_type not in ["analog", "navx"]:
            raise ValidationError(f"Unsupported gyro type: {gyro_type}")
        if not 0 <= port <= 3:
            raise ValidationError(f"Port must be between 0 and 3, got {port}")
        
        self.gyro_type = gyro_type
        self.port = port
        self.inverted = inverted


class Gyro:
    """
    Simplified gyro/IMU interface (WIP Version).
    Basic functionality for getting robot orientation.
    """
    
    def __init__(self, config: Optional[GyroConfig] = None):
        """
        Initialize gyro system.
        
        Args:
            config: GyroConfig object. If None, uses default configuration.
        """
        if config is None:
            config = GyroConfig()
            SimpliPyLogger.warning("Using default gyro configuration. Consider creating a GyroConfig.", "Gyro")
        
        self.config = config
        self._gyro = None
        
        try:
            if config.gyro_type == "analog":
                self._gyro = wpilib.AnalogGyro(config.port)
                self._gyro.calibrate()
                SimpliPyLogger.info(f"Analog gyro initialized on port {config.port}", "Gyro")
            elif config.gyro_type == "navx":
                # NavX requires additional setup - placeholder for now
                SimpliPyLogger.warning("NavX support is WIP - using placeholder", "Gyro")
                self._gyro = None
        except Exception as e:
            SimpliPyLogger.error("Failed to initialize gyro", "Gyro", e)
            raise
    
    def getAngle(self) -> float:
        """
        Get current angle in degrees.
        
        Returns:
            Current angle in degrees (0-360, continuous)
        """
        if self._gyro is None:
            SimpliPyLogger.warning("Gyro not initialized, returning 0", "Gyro")
            return 0.0
        
        try:
            angle = self._gyro.getAngle()
            if self.config.inverted:
                angle = -angle
            return angle
        except Exception as e:
            SimpliPyLogger.error("Failed to get gyro angle", "Gyro", e)
            return 0.0
    
    def getRate(self) -> float:
        """
        Get current rotation rate in degrees per second.
        
        Returns:
            Rotation rate in degrees/second
        """
        if self._gyro is None:
            return 0.0
        
        try:
            rate = self._gyro.getRate()
            if self.config.inverted:
                rate = -rate
            return rate
        except Exception as e:
            SimpliPyLogger.error("Failed to get gyro rate", "Gyro", e)
            return 0.0
    
    def reset(self) -> None:
        """Reset gyro to zero."""
        if self._gyro is None:
            return
        
        try:
            self._gyro.reset()
            SimpliPyLogger.info("Gyro reset", "Gyro")
        except Exception as e:
            SimpliPyLogger.error("Failed to reset gyro", "Gyro", e)
    
    def calibrate(self) -> None:
        """Calibrate the gyro."""
        if self._gyro is None:
            return
        
        try:
            if hasattr(self._gyro, 'calibrate'):
                self._gyro.calibrate()
                SimpliPyLogger.info("Gyro calibrated", "Gyro")
        except Exception as e:
            SimpliPyLogger.error("Failed to calibrate gyro", "Gyro", e)

