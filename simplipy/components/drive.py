"""
simplipy Drive System
Simplified drive train setup with configuration and error handling.
"""

from wpilib import MotorControllerGroup
from wpilib.drive import DifferentialDrive
from typing import List, Optional
from phoenix5 import NeutralMode

from .motors import MotorFactory, MotorController, MotorType
from ..utils.config import Config
from ..utils.errors import ConfigError, ValidationError
from ..utils.logger import SimpliPyLogger


class DriveConfig:
    """Configuration for drive system."""
    
    def __init__(self,
                 left_motors: List[dict],
                 right_motors: List[dict],
                 max_power: float = 1.0,
                 invert_left: bool = True,
                 invert_right: bool = False,
                 use_follow_mode: bool = False):
        """
        Initialize drive configuration.
        
        Args:
            left_motors: List of motor configs for left side
                        [{"type": MotorType, "can_id": int, "inverted": bool, "neutral_mode": NeutralMode}, ...]
            right_motors: List of motor configs for right side
            max_power: Maximum output power (0.0 to 1.0)
            invert_left: Whether to invert left side
            invert_right: Whether to invert right side
            use_follow_mode: Use follow() instead of MotorControllerGroup (recommended for 2025+)
        """
        self.left_motors = left_motors
        self.right_motors = right_motors
        self.max_power = max_power
        self.invert_left = invert_left
        self.invert_right = invert_right
        self.use_follow_mode = use_follow_mode
        
        # Validation
        if not 0.0 <= max_power <= 1.0:
            raise ValidationError(f"max_power must be between 0.0 and 1.0, got {max_power}")
        if not left_motors or not right_motors:
            raise ValidationError("Must provide at least one motor for each side")
        if len(left_motors) != len(right_motors):
            SimpliPyLogger.warning("Left and right motor counts differ", "Drive")


class Drive(DifferentialDrive):
    """
    Enhanced drive train class with simplified setup and error handling.
    Inherits from DifferentialDrive for full WPILib compatibility.
    """
    
    def __init__(self, config: Optional[DriveConfig] = None):
        """
        Initialize drive system.
        
        Args:
            config: DriveConfig object. If None, uses default configuration.
        """
        if config is None:
            # Default configuration - update these values for your robot
            config = DriveConfig(
                left_motors=[
                    {"type": MotorType.TALON_SRX, "can_id": 0, "inverted": False, "neutral_mode": NeutralMode.Coast},
                    {"type": MotorType.VICTOR_SPX, "can_id": 1, "inverted": False, "neutral_mode": NeutralMode.Coast}
                ],
                right_motors=[
                    {"type": MotorType.VICTOR_SPX, "can_id": 2, "inverted": False, "neutral_mode": NeutralMode.Coast},
                    {"type": MotorType.VICTOR_SPX, "can_id": 3, "inverted": False, "neutral_mode": NeutralMode.Coast}
                ],
                max_power=0.6,
                invert_left=True,
                invert_right=False
            )
            SimpliPyLogger.warning("Using default drive configuration. Consider creating a DriveConfig.", "Drive")
        
        self.config = config
        self.left_motors: List[MotorController] = []
        self.right_motors: List[MotorController] = []
        
        try:
            # Create left side motors
            for motor_cfg in config.left_motors:
                motor = MotorFactory.create(
                    motor_type=motor_cfg["type"],
                    can_id=motor_cfg["can_id"],
                    neutral_mode=motor_cfg.get("neutral_mode", NeutralMode.Coast),
                    inverted=motor_cfg.get("inverted", False)
                )
                self.left_motors.append(motor)
            
            # Create right side motors
            for motor_cfg in config.right_motors:
                motor = MotorFactory.create(
                    motor_type=motor_cfg["type"],
                    can_id=motor_cfg["can_id"],
                    neutral_mode=motor_cfg.get("neutral_mode", NeutralMode.Coast),
                    inverted=motor_cfg.get("inverted", False)
                )
                self.right_motors.append(motor)
            
            # Setup motor groups
            if config.use_follow_mode:
                # Use follow mode (recommended for 2025+)
                self._setup_follow_mode()
                left_leader = self.left_motors[0]
                right_leader = self.right_motors[0]
            else:
                # Use MotorControllerGroup (deprecated but still works)
                SimpliPyLogger.warning("Using deprecated MotorControllerGroup. Consider use_follow_mode=True", "Drive")
                left_group = MotorControllerGroup(*[m.controller for m in self.left_motors])
                right_group = MotorControllerGroup(*[m.controller for m in self.right_motors])
                left_group.setInverted(config.invert_left)
                right_group.setInverted(config.invert_right)
                left_leader = left_group
                right_leader = right_group
            
            # Initialize DifferentialDrive
            super().__init__(leftMotor=left_leader, rightMotor=right_leader)
            self.setMaxOutput(config.max_power)
            
            SimpliPyLogger.info(f"Drive system initialized with {len(self.left_motors)} left and {len(self.right_motors)} right motors", "Drive")
            
        except Exception as e:
            SimpliPyLogger.error("Failed to initialize drive system", "Drive", e)
            raise
    
    def _setup_follow_mode(self):
        """Setup motors using follow mode instead of MotorControllerGroup."""
        # Set inversion on leaders
        if self.left_motors:
            self.left_motors[0].setInverted(self.config.invert_left)
        if self.right_motors:
            self.right_motors[0].setInverted(self.config.invert_right)
        
        # Make followers follow leaders
        for i in range(1, len(self.left_motors)):
            try:
                self.left_motors[i].follow(self.left_motors[0])
            except Exception as e:
                SimpliPyLogger.warning(f"Left motor {i} could not follow leader: {e}", "Drive")
        
        for i in range(1, len(self.right_motors)):
            try:
                self.right_motors[i].follow(self.right_motors[0])
            except Exception as e:
                SimpliPyLogger.warning(f"Right motor {i} could not follow leader: {e}", "Drive")
    
    def arcadeDrive(self, xSpeed: float, zRotation: float, squaredInputs: bool = True) -> None:
        """
        Arcade drive with validation.
        
        Args:
            xSpeed: Forward/backward speed (-1.0 to 1.0)
            zRotation: Rotation speed (-1.0 to 1.0)
            squaredInputs: Whether to square inputs for smoother control
        """
        try:
            if not -1.0 <= xSpeed <= 1.0:
                raise ValidationError(f"xSpeed must be between -1.0 and 1.0, got {xSpeed}")
            if not -1.0 <= zRotation <= 1.0:
                raise ValidationError(f"zRotation must be between -1.0 and 1.0, got {zRotation}")
            super().arcadeDrive(xSpeed, zRotation, squaredInputs)
        except Exception as e:
            SimpliPyLogger.error(f"Arcade drive error: {e}", "Drive", e)
    
    def tankDrive(self, leftSpeed: float, rightSpeed: float, squaredInputs: bool = True) -> None:
        """
        Tank drive with validation.
        
        Args:
            leftSpeed: Left side speed (-1.0 to 1.0)
            rightSpeed: Right side speed (-1.0 to 1.0)
            squaredInputs: Whether to square inputs for smoother control
        """
        try:
            if not -1.0 <= leftSpeed <= 1.0:
                raise ValidationError(f"leftSpeed must be between -1.0 and 1.0, got {leftSpeed}")
            if not -1.0 <= rightSpeed <= 1.0:
                raise ValidationError(f"rightSpeed must be between -1.0 and 1.0, got {rightSpeed}")
            super().tankDrive(leftSpeed, rightSpeed, squaredInputs)
        except Exception as e:
            SimpliPyLogger.error(f"Tank drive error: {e}", "Drive", e)
    
    def curvatureDrive(self, xSpeed: float, zRotation: float, isQuickTurn: bool = False) -> None:
        """
        Curvature drive with validation.
        
        Args:
            xSpeed: Forward/backward speed (-1.0 to 1.0)
            zRotation: Rotation speed (-1.0 to 1.0)
            isQuickTurn: Whether to enable quick turn
        """
        try:
            if not -1.0 <= xSpeed <= 1.0:
                raise ValidationError(f"xSpeed must be between -1.0 and 1.0, got {xSpeed}")
            if not -1.0 <= zRotation <= 1.0:
                raise ValidationError(f"zRotation must be between -1.0 and 1.0, got {zRotation}")
            super().curvatureDrive(xSpeed, zRotation, isQuickTurn)
        except Exception as e:
            SimpliPyLogger.error(f"Curvature drive error: {e}", "Drive", e)
    
    def stop(self) -> None:
        """Stop the drive system."""
        try:
            self.arcadeDrive(0, 0)
        except Exception as e:
            SimpliPyLogger.error("Failed to stop drive", "Drive", e)
