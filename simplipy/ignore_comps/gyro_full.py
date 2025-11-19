"""
simplipy Gyro/IMU Component (Full Version)
Complete gyro/IMU interface with support for multiple sensor types.
Full-featured version with NavX, Pigeon, ADIS, and AnalogGyro support.
"""

from typing import Optional, Literal
import wpilib
from ..utils.errors import ValidationError
from ..utils.logger import SimpliPyLogger


class GyroConfig:
    """Configuration for gyro/IMU system."""
    
    def __init__(self,
                 gyro_type: Literal["analog", "navx", "pigeon", "adis"] = "analog",
                 port: int = 0,
                 can_id: Optional[int] = None,
                 inverted: bool = False,
                 calibration_time: float = 1.0):
        """
        Initialize gyro configuration.
        
        Args:
            gyro_type: Type of gyro/IMU
                - "analog": AnalogGyro (analog port)
                - "navx": NavX (SPI/I2C)
                - "pigeon": Pigeon IMU (CAN)
                - "adis": ADIS16470 (SPI)
            port: Port number (analog port for AnalogGyro, SPI/I2C port for NavX/ADIS)
            can_id: CAN ID for Pigeon IMU (required for pigeon type)
            inverted: Whether to invert gyro readings
            calibration_time: Time in seconds for calibration
        """
        if gyro_type not in ["analog", "navx", "pigeon", "adis"]:
            raise ValidationError(f"Unsupported gyro type: {gyro_type}")
        if gyro_type == "pigeon" and can_id is None:
            raise ValidationError("CAN ID required for Pigeon IMU")
        if not 0 <= port <= 3:
            raise ValidationError(f"Port must be between 0 and 3, got {port}")
        
        self.gyro_type = gyro_type
        self.port = port
        self.can_id = can_id
        self.inverted = inverted
        self.calibration_time = calibration_time


class Gyro:
    """
    Complete gyro/IMU interface with support for multiple sensor types.
    Supports AnalogGyro, NavX, Pigeon IMU, and ADIS16470.
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
        self._navx = None
        self._pigeon = None
        
        try:
            if config.gyro_type == "analog":
                self._gyro = wpilib.AnalogGyro(config.port)
                self._gyro.calibrate()
                SimpliPyLogger.info(f"Analog gyro initialized on port {config.port}", "Gyro")
            
            elif config.gyro_type == "navx":
                try:
                    from navx import AHRS
                    self._navx = AHRS.create_spi()
                    SimpliPyLogger.info("NavX IMU initialized via SPI", "Gyro")
                except ImportError:
                    SimpliPyLogger.error("NavX library not found. Install with: pip install navx", "Gyro")
                    raise
                except Exception as e:
                    SimpliPyLogger.error("Failed to initialize NavX", "Gyro", e)
                    raise
            
            elif config.gyro_type == "pigeon":
                try:
                    from phoenix5 import PigeonIMU
                    self._pigeon = PigeonIMU(config.can_id)
                    SimpliPyLogger.info(f"Pigeon IMU initialized on CAN {config.can_id}", "Gyro")
                except Exception as e:
                    SimpliPyLogger.error("Failed to initialize Pigeon IMU", "Gyro", e)
                    raise
            
            elif config.gyro_type == "adis":
                try:
                    from wpilib import ADIS16470_IMU
                    self._gyro = ADIS16470_IMU()
                    SimpliPyLogger.info("ADIS16470 IMU initialized", "Gyro")
                except Exception as e:
                    SimpliPyLogger.error("Failed to initialize ADIS16470", "Gyro", e)
                    raise
                    
        except Exception as e:
            SimpliPyLogger.error("Failed to initialize gyro system", "Gyro", e)
            raise
    
    def getAngle(self) -> float:
        """
        Get current yaw angle in degrees.
        
        Returns:
            Current yaw angle in degrees (0-360, continuous)
        """
        try:
            if self._gyro is not None:
                angle = self._gyro.getAngle()
            elif self._navx is not None:
                angle = self._navx.getYaw()
            elif self._pigeon is not None:
                ypr = [0.0, 0.0, 0.0]
                self._pigeon.getYawPitchRoll(ypr)
                angle = ypr[0]
            else:
                return 0.0
            
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
        try:
            if self._gyro is not None:
                rate = self._gyro.getRate()
            elif self._navx is not None:
                rate = self._navx.getRate()
            elif self._pigeon is not None:
                xyz = [0.0, 0.0, 0.0]
                self._pigeon.getRawGyro(xyz)
                rate = xyz[2]  # Z-axis rotation
            else:
                return 0.0
            
            if self.config.inverted:
                rate = -rate
            return rate
        except Exception as e:
            SimpliPyLogger.error("Failed to get gyro rate", "Gyro", e)
            return 0.0
    
    def getPitch(self) -> float:
        """
        Get current pitch angle in degrees (if supported).
        
        Returns:
            Pitch angle in degrees
        """
        try:
            if self._navx is not None:
                return self._navx.getPitch()
            elif self._pigeon is not None:
                ypr = [0.0, 0.0, 0.0]
                self._pigeon.getYawPitchRoll(ypr)
                return ypr[1]
            else:
                return 0.0
        except Exception as e:
            SimpliPyLogger.error("Failed to get pitch", "Gyro", e)
            return 0.0
    
    def getRoll(self) -> float:
        """
        Get current roll angle in degrees (if supported).
        
        Returns:
            Roll angle in degrees
        """
        try:
            if self._navx is not None:
                return self._navx.getRoll()
            elif self._pigeon is not None:
                ypr = [0.0, 0.0, 0.0]
                self._pigeon.getYawPitchRoll(ypr)
                return ypr[2]
            else:
                return 0.0
        except Exception as e:
            SimpliPyLogger.error("Failed to get roll", "Gyro", e)
            return 0.0
    
    def reset(self) -> None:
        """Reset gyro to zero."""
        try:
            if self._gyro is not None:
                self._gyro.reset()
            elif self._navx is not None:
                self._navx.zeroYaw()
            elif self._pigeon is not None:
                self._pigeon.setYaw(0.0)
            SimpliPyLogger.info("Gyro reset", "Gyro")
        except Exception as e:
            SimpliPyLogger.error("Failed to reset gyro", "Gyro", e)
    
    def calibrate(self) -> None:
        """Calibrate the gyro."""
        try:
            if self._gyro is not None and hasattr(self._gyro, 'calibrate'):
                self._gyro.calibrate()
            elif self._pigeon is not None:
                self._pigeon.calibrate()
            SimpliPyLogger.info("Gyro calibrated", "Gyro")
        except Exception as e:
            SimpliPyLogger.error("Failed to calibrate gyro", "Gyro", e)
    
    def isConnected(self) -> bool:
        """
        Check if gyro is connected and working.
        
        Returns:
            True if gyro is connected, False otherwise
        """
        try:
            if self._gyro is not None:
                return True
            elif self._navx is not None:
                return self._navx.isConnected()
            elif self._pigeon is not None:
                return True  # Pigeon doesn't have explicit connection check
            return False
        except Exception:
            return False

