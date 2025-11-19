"""
simplipy Motor Factory
Simplified motor creation with enhanced error handling and validation.
"""

from enum import Enum
from typing import Union, Optional
from phoenix5 import NeutralMode, WPI_TalonSRX, WPI_VictorSPX, IMotorController
from rev import SparkMax, SparkLowLevel
from ..utils.errors import MotorError, ValidationError
from ..utils.logger import SimpliPyLogger


class MotorType(Enum):
    """Supported motor controller types."""
    TALON_SRX = "talon_srx"
    VICTOR_SPX = "victor_spx"
    SPARK_MAX = "spark_max"
    SPARK_MAX_BRUSHLESS = "spark_max_brushless"
    SPARK_MAX_BRUSHED = "spark_max_brushed"


class MotorController:
    """
    Unified motor controller interface.
    Wraps different motor types with a common interface.
    """
    
    def __init__(self, controller: Union[WPI_TalonSRX, WPI_VictorSPX, SparkMax], 
                 motor_type: MotorType, can_id: int):
        self._controller = controller
        self._motor_type = motor_type
        self._can_id = can_id
        self._is_inverted = False
    
    @property
    def controller(self):
        """Get the underlying motor controller."""
        return self._controller
    
    @property
    def can_id(self) -> int:
        """Get the CAN ID of the motor."""
        return self._can_id
    
    @property
    def motor_type(self) -> MotorType:
        """Get the motor type."""
        return self._motor_type
    
    def set(self, speed: float) -> None:
        """Set motor speed (-1.0 to 1.0)."""
        if not -1.0 <= speed <= 1.0:
            raise ValidationError(f"Motor speed must be between -1.0 and 1.0, got {speed}")
        try:
            self._controller.set(speed)
        except Exception as e:
            raise MotorError(f"Failed to set motor speed: {str(e)}", can_id=self._can_id)
    
    def get(self) -> float:
        """Get current motor speed."""
        try:
            return self._controller.get()
        except Exception as e:
            raise MotorError(f"Failed to get motor speed: {str(e)}", can_id=self._can_id)
    
    def setInverted(self, inverted: bool) -> None:
        """Set motor inversion."""
        try:
            self._controller.setInverted(inverted)
            self._is_inverted = inverted
        except Exception as e:
            raise MotorError(f"Failed to set motor inversion: {str(e)}", can_id=self._can_id)
    
    def getInverted(self) -> bool:
        """Get motor inversion state."""
        return self._is_inverted
    
    def follow(self, leader: 'MotorController') -> None:
        """Follow another motor controller."""
        try:
            if hasattr(self._controller, 'follow'):
                self._controller.follow(leader.controller)
            else:
                raise MotorError("Motor type does not support follow mode", can_id=self._can_id)
        except Exception as e:
            raise MotorError(f"Failed to set follow mode: {str(e)}", can_id=self._can_id)
    
    def stopMotor(self) -> None:
        """Stop the motor."""
        self.set(0.0)
    
    def getEncoder(self):
        """Get encoder if available (SparkMax only)."""
        if self._motor_type in [MotorType.SPARK_MAX, MotorType.SPARK_MAX_BRUSHLESS, MotorType.SPARK_MAX_BRUSHED]:
            try:
                return self._controller.getEncoder()
            except Exception as e:
                raise MotorError(f"Failed to get encoder: {str(e)}", can_id=self._can_id)
        raise MotorError("Encoder not available for this motor type", can_id=self._can_id)


class MotorFactory:
    """
    Factory for creating motor controllers with validation and error handling.
    Simplifies motor creation and provides consistent interface.
    """
    
    @staticmethod
    def validate_can_id(can_id: int) -> None:
        """Validate CAN ID is in acceptable range."""
        if not isinstance(can_id, int):
            raise ValidationError(f"CAN ID must be an integer, got {type(can_id).__name__}")
        if not 0 <= can_id <= 62:
            raise ValidationError(f"CAN ID must be between 0 and 62, got {can_id}")
    
    @staticmethod
    def create(motor_type: MotorType, can_id: int, 
               neutral_mode: Optional[NeutralMode] = None,
               inverted: bool = False,
               motor_kind: Optional[SparkLowLevel.MotorType] = None) -> MotorController:
        """
        Create a motor controller with validation and error handling.
        
        Args:
            motor_type: Type of motor controller to create
            can_id: CAN bus ID (0-62)
            neutral_mode: Neutral mode for Phoenix motors (Coast/Brake)
            inverted: Whether to invert motor direction
            motor_kind: Motor type for SparkMax (kBrushless/kBrushed)
        
        Returns:
            MotorController instance
        
        Raises:
            MotorError: If motor creation fails
            ValidationError: If parameters are invalid
        """
        MotorFactory.validate_can_id(can_id)
        
        try:
            if motor_type == MotorType.TALON_SRX:
                if neutral_mode is None:
                    neutral_mode = NeutralMode.Coast
                motor = WPI_TalonSRX(can_id)
                motor.setNeutralMode(neutral_mode)
                SimpliPyLogger.info(f"Created TalonSRX on CAN {can_id}", "MotorFactory")
                
            elif motor_type == MotorType.VICTOR_SPX:
                if neutral_mode is None:
                    neutral_mode = NeutralMode.Coast
                motor = WPI_VictorSPX(can_id)
                motor.setNeutralMode(neutral_mode)
                SimpliPyLogger.info(f"Created VictorSPX on CAN {can_id}", "MotorFactory")
                
            elif motor_type in [MotorType.SPARK_MAX, MotorType.SPARK_MAX_BRUSHLESS]:
                if motor_kind is None:
                    motor_kind = SparkLowLevel.MotorType.kBrushless
                motor = SparkMax(can_id, motor_kind)
                SimpliPyLogger.info(f"Created SparkMax (brushless) on CAN {can_id}", "MotorFactory")
                
            elif motor_type == MotorType.SPARK_MAX_BRUSHED:
                motor = SparkMax(can_id, SparkLowLevel.MotorType.kBrushed)
                SimpliPyLogger.info(f"Created SparkMax (brushed) on CAN {can_id}", "MotorFactory")
                
            else:
                raise MotorError(f"Unsupported motor type: {motor_type}", can_id=can_id)
            
            controller = MotorController(motor, motor_type, can_id)
            if inverted:
                controller.setInverted(inverted)
            
            return controller
            
        except Exception as e:
            error_msg = f"Failed to create {motor_type.value} on CAN {can_id}: {str(e)}"
            SimpliPyLogger.error(error_msg, "MotorFactory", e)
            raise MotorError(error_msg, can_id=can_id)
    
    @staticmethod
    def create_talon_srx(can_id: int, neutral_mode: NeutralMode = NeutralMode.Coast, 
                        inverted: bool = False) -> MotorController:
        """Convenience method to create TalonSRX."""
        return MotorFactory.create(MotorType.TALON_SRX, can_id, neutral_mode, inverted)
    
    @staticmethod
    def create_victor_spx(can_id: int, neutral_mode: NeutralMode = NeutralMode.Coast,
                         inverted: bool = False) -> MotorController:
        """Convenience method to create VictorSPX."""
        return MotorFactory.create(MotorType.VICTOR_SPX, can_id, neutral_mode, inverted)
    
    @staticmethod
    def create_spark_max(can_id: int, brushless: bool = True, inverted: bool = False) -> MotorController:
        """Convenience method to create SparkMax."""
        motor_type = MotorType.SPARK_MAX_BRUSHLESS if brushless else MotorType.SPARK_MAX_BRUSHED
        motor_kind = SparkLowLevel.MotorType.kBrushless if brushless else SparkLowLevel.MotorType.kBrushed
        return MotorFactory.create(motor_type, can_id, motor_kind=motor_kind, inverted=inverted)


# Legacy function compatibility
def createSparkMax(can_id: int, motor_type: SparkLowLevel.MotorType) -> SparkMax:
    """Legacy function for backward compatibility."""
    SimpliPyLogger.warning("createSparkMax is deprecated, use MotorFactory.create_spark_max() instead", "Motors")
    motor = SparkMax(can_id, motor_type)
    return motor

def createVictorSPX(can_id: int, neutral_mode: NeutralMode) -> WPI_VictorSPX:
    """Legacy function for backward compatibility."""
    SimpliPyLogger.warning("createVictorSPX is deprecated, use MotorFactory.create_victor_spx() instead", "Motors")
    motor = WPI_VictorSPX(can_id)
    motor.setNeutralMode(neutral_mode)
    return motor

def createTalonSRX(can_id: int, neutral_mode: NeutralMode) -> WPI_TalonSRX:
    """Legacy function for backward compatibility."""
    SimpliPyLogger.warning("createTalonSRX is deprecated, use MotorFactory.create_talon_srx() instead", "Motors")
    motor = WPI_TalonSRX(can_id)
    motor.setNeutralMode(neutral_mode)
    return motor

def createSparkMaxEncoder(controller: SparkMax):
    """Legacy function for backward compatibility."""
    SimpliPyLogger.warning("createSparkMaxEncoder is deprecated, use MotorController.getEncoder() instead", "Motors")
    return controller.getEncoder()
