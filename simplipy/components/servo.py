"""
simplipy Servo Component (WIP)
Simplified servo interface for precise positioning.
This is a work-in-progress version
"""

from typing import Optional
import wpilib
from ..utils.errors import ValidationError
from ..utils.logger import SimpliPyLogger


class ServoConfig:
    """Configuration for servo system."""
    
    def __init__(self,
                 channel: int,
                 min_angle: float = 0.0,
                 max_angle: float = 180.0):
        """
        Initialize servo configuration.
        
        Args:
            channel: PWM channel (0-9)
            min_angle: Minimum angle in degrees
            max_angle: Maximum angle in degrees
        """
        if not 0 <= channel <= 9:
            raise ValidationError(f"Channel must be between 0 and 9, got {channel}")
        if min_angle >= max_angle:
            raise ValidationError(f"min_angle ({min_angle}) must be less than max_angle ({max_angle})")
        
        self.channel = channel
        self.min_angle = min_angle
        self.max_angle = max_angle


class Servo:
    """
    Simplified servo interface (WIP Version).
    Basic position control for servos.
    """
    
    def __init__(self, config: Optional[ServoConfig] = None):
        """
        Initialize servo.
        
        Args:
            config: ServoConfig object. If None, uses default configuration.
        """
        if config is None:
            config = ServoConfig(channel=0)
            SimpliPyLogger.warning("Using default servo configuration. Consider creating a ServoConfig.", "Servo")
        
        self.config = config
        
        try:
            self._servo = wpilib.Servo(config.channel)
            SimpliPyLogger.info(f"Servo initialized on channel {config.channel}", "Servo")
        except Exception as e:
            SimpliPyLogger.error(f"Failed to initialize servo on channel {config.channel}", "Servo", e)
            raise
    
    def setAngle(self, angle: float) -> None:
        """
        Set servo angle in degrees.
        
        Args:
            angle: Angle in degrees (clamped to min/max)
        """
        try:
            # Clamp angle to valid range
            angle = max(self.config.min_angle, min(self.config.max_angle, angle))
            self._servo.setAngle(angle)
        except Exception as e:
            SimpliPyLogger.error(f"Failed to set servo angle to {angle}", "Servo", e)
    
    def setPosition(self, position: float) -> None:
        """
        Set servo position (0.0 to 1.0).
        
        Args:
            position: Position from 0.0 (min) to 1.0 (max)
        """
        try:
            if not 0.0 <= position <= 1.0:
                raise ValidationError(f"Position must be between 0.0 and 1.0, got {position}")
            self._servo.set(position)
        except Exception as e:
            SimpliPyLogger.error(f"Failed to set servo position to {position}", "Servo", e)
    
    def getAngle(self) -> float:
        """
        Get current servo angle in degrees.
        
        Returns:
            Current angle in degrees
        """
        try:
            return self._servo.getAngle()
        except Exception as e:
            SimpliPyLogger.error("Failed to get servo angle", "Servo", e)
            return 0.0
    
    def getPosition(self) -> float:
        """
        Get current servo position (0.0 to 1.0).
        
        Returns:
            Current position from 0.0 to 1.0
        """
        try:
            return self._servo.get()
        except Exception as e:
            SimpliPyLogger.error("Failed to get servo position", "Servo", e)
            return 0.0

