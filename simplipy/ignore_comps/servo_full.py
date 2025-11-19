"""
simplipy Servo Component (Full Version)
Complete servo interface with advanced features and multi-servo support.
Full-featured version with speed control, continuous rotation, and servo groups.
"""

from typing import Optional, List
import wpilib
from ..utils.errors import ValidationError
from ..utils.logger import SimpliPyLogger


class ServoConfig:
    """Configuration for servo system."""
    
    def __init__(self,
                 channel: int,
                 min_angle: float = 0.0,
                 max_angle: float = 180.0,
                 continuous: bool = False,
                 speed: float = 1.0):
        """
        Initialize servo configuration.
        
        Args:
            channel: PWM channel (0-9)
            min_angle: Minimum angle in degrees
            max_angle: Maximum angle in degrees
            continuous: Whether this is a continuous rotation servo
            speed: Speed multiplier for continuous servos (0.0 to 1.0)
        """
        if not 0 <= channel <= 9:
            raise ValidationError(f"Channel must be between 0 and 9, got {channel}")
        if min_angle >= max_angle:
            raise ValidationError(f"min_angle ({min_angle}) must be less than max_angle ({max_angle})")
        if not 0.0 <= speed <= 1.0:
            raise ValidationError(f"Speed must be between 0.0 and 1.0, got {speed}")
        
        self.channel = channel
        self.min_angle = min_angle
        self.max_angle = max_angle
        self.continuous = continuous
        self.speed = speed


class Servo:
    """
    Complete servo interface with advanced features.
    Supports standard and continuous rotation servos.
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
            if self.config.continuous:
                SimpliPyLogger.warning("setAngle() not recommended for continuous servos, use setSpeed()", "Servo")
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
    
    def setSpeed(self, speed: float) -> None:
        """
        Set continuous rotation servo speed.
        
        Args:
            speed: Speed from -1.0 (full reverse) to 1.0 (full forward), 0.0 = stop
        """
        try:
            if not self.config.continuous:
                SimpliPyLogger.warning("setSpeed() is for continuous servos, use setAngle() or setPosition()", "Servo")
            if not -1.0 <= speed <= 1.0:
                raise ValidationError(f"Speed must be between -1.0 and 1.0, got {speed}")
            # Convert speed to position (0.5 = stop, 0.0 = full reverse, 1.0 = full forward)
            position = 0.5 + (speed * self.config.speed * 0.5)
            self._servo.set(position)
        except Exception as e:
            SimpliPyLogger.error(f"Failed to set servo speed to {speed}", "Servo", e)
    
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
    
    def stop(self) -> None:
        """Stop continuous rotation servo (set to neutral)."""
        if self.config.continuous:
            self.setSpeed(0.0)
        else:
            SimpliPyLogger.warning("stop() is for continuous servos", "Servo")


class ServoGroup:
    """
    Group of servos that can be controlled together.
    """
    
    def __init__(self, servos: List[Servo]):
        """
        Initialize servo group.
        
        Args:
            servos: List of Servo objects to control together
        """
        if not servos:
            raise ValidationError("ServoGroup must have at least one servo")
        self.servos = servos
        SimpliPyLogger.info(f"ServoGroup initialized with {len(servos)} servos", "Servo")
    
    def setAngle(self, angle: float) -> None:
        """Set all servos to the same angle."""
        for servo in self.servos:
            servo.setAngle(angle)
    
    def setPosition(self, position: float) -> None:
        """Set all servos to the same position."""
        for servo in self.servos:
            servo.setPosition(position)

