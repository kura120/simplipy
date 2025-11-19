"""
simplipy Arm System (Experimental!)
Enhanced arm control with state management, encoder support, and error handling.
"""

from typing import Literal, Optional
from phoenix5 import NeutralMode

from .motors import MotorFactory, MotorController, MotorType
from .switch import LimitSwitch
from ..utils.errors import ValidationError, ConfigError
from ..utils.logger import SimpliPyLogger


class ArmConfig:
    """Configuration for arm system."""
    
    def __init__(self,
                 arm_motor_can_id: int,
                 arm_motor_type: MotorType = MotorType.SPARK_MAX_BRUSHLESS,
                 roller_motor_can_id: int = None,
                 roller_motor_type: MotorType = MotorType.TALON_SRX,
                 limit_switch_dio: int = 0,
                 gear_ratio: float = 64.0,
                 manual_power: float = 0.15,
                 auto_power: float = 0.25,
                 roller_power: float = 0.3,
                 extension_angle: float = 45.0,
                 retraction_limit: Literal["switch", "encoder"] = "switch",
                 override_extend_limit: bool = False):
        """
        Initialize arm configuration.
        
        Args:
            arm_motor_can_id: CAN ID of arm motor
            arm_motor_type: Type of arm motor controller
            roller_motor_can_id: CAN ID of roller motor (None if no roller)
            roller_motor_type: Type of roller motor controller
            limit_switch_dio: DIO port of limit switch
            gear_ratio: Gear box ratio (motor rotations per arm rotation)
            manual_power: Power for manual control (0.0 to 1.0)
            auto_power: Power for automatic control (0.0 to 1.0)
            roller_power: Power for roller (0.0 to 1.0)
            extension_angle: Target extension angle in degrees
            retraction_limit: Use "switch" or "encoder" for retraction limit
            override_extend_limit: Allow overriding extension limit
        """
        if not 0.0 <= manual_power <= 1.0:
            raise ValidationError(f"manual_power must be between 0.0 and 1.0, got {manual_power}")
        if not 0.0 <= auto_power <= 1.0:
            raise ValidationError(f"auto_power must be between 0.0 and 1.0, got {auto_power}")
        if not 0.0 <= roller_power <= 1.0:
            raise ValidationError(f"roller_power must be between 0.0 and 1.0, got {roller_power}")
        if gear_ratio <= 0:
            raise ValidationError(f"gear_ratio must be positive, got {gear_ratio}")
        
        self.arm_motor_can_id = arm_motor_can_id
        self.arm_motor_type = arm_motor_type
        self.roller_motor_can_id = roller_motor_can_id
        self.roller_motor_type = roller_motor_type
        self.limit_switch_dio = limit_switch_dio
        self.gear_ratio = gear_ratio
        self.manual_power = manual_power
        self.auto_power = auto_power
        self.roller_power = roller_power
        self.extension_angle = extension_angle
        self.retraction_limit = retraction_limit
        self.override_extend_limit = override_extend_limit


class Arm:
    """
    Enhanced arm system with encoder support, limit switches, and state management.
    """
    
    def __init__(self, config: Optional[ArmConfig] = None):
        """
        Initialize arm system.
        
        Args:
            config: ArmConfig object. If None, uses default configuration.
        """
        if config is None:
            config = ArmConfig(
                arm_motor_can_id=5,
                roller_motor_can_id=7,
                limit_switch_dio=0
            )
            SimpliPyLogger.warning("Using default arm configuration. Consider creating an ArmConfig.", "Arm")
        
        self.config = config
        
        # State variables
        self._calibrated = False
        self._initialized = False
        self._is_extended = False
        self._is_retracted = False
        self._set_extended = False
        self._switching_arm_state = False
        
        try:
            # Create arm motor
            self.arm_motor = MotorFactory.create(
                motor_type=config.arm_motor_type,
                can_id=config.arm_motor_can_id
            )
            
            # Get encoder if available
            try:
                self.arm_encoder = self.arm_motor.getEncoder()
                self.arm_encoder.setPosition(0)
                SimpliPyLogger.info("Arm encoder initialized", "Arm")
            except Exception as e:
                self.arm_encoder = None
                SimpliPyLogger.warning(f"Arm encoder not available: {e}", "Arm")
            
            # Create roller motor if configured
            if config.roller_motor_can_id is not None:
                self.roller_motor = MotorFactory.create(
                    motor_type=config.roller_motor_type,
                    can_id=config.roller_motor_can_id,
                    neutral_mode=NeutralMode.Brake
                )
            else:
                self.roller_motor = None
                SimpliPyLogger.info("No roller motor configured", "Arm")
            
            # Create limit switch
            self.arm_limit = LimitSwitch(config.limit_switch_dio)
            
            SimpliPyLogger.info(f"Arm initialized on CAN {config.arm_motor_can_id}", "Arm")
            
        except Exception as e:
            SimpliPyLogger.error("Failed to initialize arm", "Arm", e)
            raise
    
    def retractArm(self) -> None:
        """Retract arm to neutral position."""
        if not self.arm_encoder:
            SimpliPyLogger.error("Cannot retract arm: encoder not available", "Arm")
            return
        
        self._switching_arm_state = True
        self._set_extended = False
        
        try:
            current_rotations = self.getArmRotations(enable_cutoff=True, cutoff="positive")
            target_change = self.config.extension_angle
            
            if current_rotations + self.config.extension_angle < target_change:
                # Calculate speed based on position
                if current_rotations > target_change / 3:
                    speed = (current_rotations / target_change) * self.config.auto_power
                else:
                    speed = self.config.manual_power
                
                if self.config.retraction_limit == "switch":
                    if self.arm_limit.getPressed():
                        self.calibrate()
                        self._switching_arm_state = False
                    else:
                        self.arm_motor.set(speed)
                elif self.config.retraction_limit == "encoder":
                    if current_rotations <= 0:
                        self.calibrate()
                    else:
                        self.arm_motor.set(speed)
        except Exception as e:
            SimpliPyLogger.error("Error during arm retraction", "Arm", e)
            self.arm_motor.stopMotor()
    
    def extendArm(self) -> None:
        """Extend arm to target position."""
        if not self.arm_encoder:
            SimpliPyLogger.error("Cannot extend arm: encoder not available", "Arm")
            return
        
        self._switching_arm_state = True
        self._set_extended = True
        
        try:
            current_rotations = -self.getArmRotations(enable_cutoff=True, cutoff="negative")
            target_change = self.config.extension_angle
            
            if current_rotations < target_change:
                # Calculate speed based on position
                if current_rotations > (2/3 * target_change):
                    speed = (1 - (current_rotations / target_change)) * self.config.auto_power
                else:
                    speed = self.config.manual_power
                
                if current_rotations > target_change:
                    self.arm_motor.set(0)
                    self._switching_arm_state = False
                else:
                    self.arm_motor.set(speed)
        except Exception as e:
            SimpliPyLogger.error("Error during arm extension", "Arm", e)
            self.arm_motor.stopMotor()
    
    def toggleArm(self, toggle: bool) -> None:
        """
        Toggle arm between extended and retracted positions.
        
        Args:
            toggle: True to toggle, False to continue current operation
        """
        if toggle and not self._switching_arm_state:
            self._set_extended = not self._set_extended
            self._switching_arm_state = True
        
        if self._switching_arm_state:
            if self._set_extended:
                self.extendArm()
            else:
                self.retractArm()
    
    def checkArmPosition(self) -> None:
        """Check and update arm position state."""
        if not self.arm_encoder:
            return
        
        try:
            arm_angle = self.getArmRotations()
            
            # Check if arm is extended
            if arm_angle <= -120 and not self.config.override_extend_limit:
                self._is_extended = True
            else:
                self._is_extended = False
            
            # Check if arm is retracted (calibrated)
            if self.arm_limit.get() and not self._calibrated:
                self.arm_encoder.setPosition(0)
                self._calibrated = True
                self._is_retracted = True
                SimpliPyLogger.info("Arm calibrated at retracted position", "Arm")
            elif int(arm_angle) != 0:
                self._is_retracted = False
                self._calibrated = False
        except Exception as e:
            SimpliPyLogger.error("Error checking arm position", "Arm", e)
    
    def activateRollers(self, direction: float) -> None:
        """
        Activate roller motor.
        
        Args:
            direction: Roller direction (-1.0 reverse, 0.0 stop, 1.0 forward)
        """
        if self.roller_motor is None:
            SimpliPyLogger.warning("Roller motor not configured", "Arm")
            return
        
        if not -1.0 <= direction <= 1.0:
            raise ValidationError(f"direction must be between -1.0 and 1.0, got {direction}")
        
        try:
            self.roller_motor.set(direction * self.config.roller_power)
        except Exception as e:
            SimpliPyLogger.error("Failed to activate rollers", "Arm", e)
    
    def calibrate(self) -> None:
        """Calibrate arm to neutral position."""
        self._is_retracted = True
        self._calibrated = True
        self.arm_motor.stopMotor()
        if self.arm_encoder:
            self.arm_encoder.setPosition(0)
        SimpliPyLogger.info("Arm calibrated", "Arm")
    
    def getArmRotations(self, enable_cutoff: bool = False, 
                       cutoff: Literal["negative", "positive"] = "positive") -> float:
        """
        Get arm rotations relative to arm itself (not motor).
        
        Args:
            enable_cutoff: Enable cutoff filtering
            cutoff: Cutoff type ("negative" or "positive")
        
        Returns:
            Arm rotation angle in degrees
        """
        if not self.arm_encoder:
            return 0.0
        
        try:
            # Convert encoder position to arm angle
            position = (self.arm_encoder.getPosition() / self.config.gear_ratio) * 360
            
            if enable_cutoff:
                if cutoff == "negative":
                    position = 0 if position < 0 else position
                elif cutoff == "positive":
                    position = 0 if position > 0 else position
            
            return position
        except Exception as e:
            SimpliPyLogger.error("Error getting arm rotations", "Arm", e)
            return 0.0
    
    def initializeArm(self) -> None:
        """Initialize arm during test mode. Calibrates to neutral position."""
        if self._initialized:
            return
        
        try:
            if not self._calibrated:
                # Low power to wind back to neutral
                self.arm_motor.set(0.05)
            
            if self.arm_limit.getPressed():
                self._initialized = True
                self.calibrate()
                SimpliPyLogger.info("Arm initialized and calibrated", "Arm")
        except Exception as e:
            SimpliPyLogger.error("Error initializing arm", "Arm", e)
    
    def manualArmControl(self, dpad: float) -> None:
        """
        Manual arm control using D-pad.
        
        Args:
            dpad: D-pad value (90=extend, 270=retract, others=stop)
        """
        self.checkArmPosition()
        
        if dpad == 90:
            direction = -1
        elif dpad == 270:
            direction = 1
        else:
            direction = 0
        
        try:
            if not self._is_extended and direction < 0:
                self.arm_motor.set(direction * self.config.manual_power)
            elif not self._is_retracted and direction > 0:
                self.arm_motor.set(direction * self.config.manual_power)
            else:
                self.arm_motor.stopMotor()
        except Exception as e:
            SimpliPyLogger.error("Error in manual arm control", "Arm", e)
    
    def isExtended(self) -> bool:
        """Check if arm is extended."""
        return self._is_extended
    
    def isRetracted(self) -> bool:
        """Check if arm is retracted."""
        return self._is_retracted
    
    def isCalibrated(self) -> bool:
        """Check if arm is calibrated."""
        return self._calibrated
