"""
simplipy Encoder Component
Unified encoder interface for position and velocity feedback.
Supports quadrature encoders, motor encoders, and absolute encoders.
"""

from typing import Optional, Literal
import wpilib
from ..utils.errors import ValidationError
from ..utils.logger import SimpliPyLogger


class EncoderConfig:
    """Configuration for encoder system."""
    
    def __init__(self,
                 encoder_type: Literal["quadrature", "motor", "absolute"] = "quadrature",
                 channel_a: int = 0,
                 channel_b: Optional[int] = None,
                 motor_controller=None,
                 inverted: bool = False,
                 distance_per_pulse: float = 1.0,
                 encoding_type: Literal["k1X", "k2X", "k4X"] = "k4X"):
        """
        Initialize encoder configuration.
        
        Args:
            encoder_type: Type of encoder
                - "quadrature": Quadrature encoder (DIO ports)
                - "motor": Encoder built into motor controller
                - "absolute": Absolute encoder
            channel_a: Channel A (DIO port for quadrature, or encoder channel)
            channel_b: Channel B (DIO port for quadrature, None for motor/absolute)
            motor_controller: Motor controller object (for motor encoder type)
            inverted: Whether to invert encoder readings
            distance_per_pulse: Distance traveled per encoder pulse
            encoding_type: Encoding type for quadrature ("k1X", "k2X", "k4X")
        """
        if encoder_type not in ["quadrature", "motor", "absolute"]:
            raise ValidationError(f"Unsupported encoder type: {encoder_type}")
        if encoder_type == "quadrature" and channel_b is None:
            raise ValidationError("channel_b required for quadrature encoder")
        if encoder_type == "motor" and motor_controller is None:
            raise ValidationError("motor_controller required for motor encoder")
        if not 0 <= channel_a <= 9:
            raise ValidationError(f"channel_a must be between 0 and 9, got {channel_a}")
        if channel_b is not None and not 0 <= channel_b <= 9:
            raise ValidationError(f"channel_b must be between 0 and 9, got {channel_b}")
        
        self.encoder_type = encoder_type
        self.channel_a = channel_a
        self.channel_b = channel_b
        self.motor_controller = motor_controller
        self.inverted = inverted
        self.distance_per_pulse = distance_per_pulse
        self.encoding_type = encoding_type


class Encoder:
    """
    Unified encoder interface for position and velocity feedback.
    """
    
    def __init__(self, config: Optional[EncoderConfig] = None):
        """
        Initialize encoder.
        
        Args:
            config: EncoderConfig object. If None, uses default configuration.
        """
        if config is None:
            config = EncoderConfig(channel_a=0, channel_b=1)
            SimpliPyLogger.warning("Using default encoder configuration. Consider creating an EncoderConfig.", "Encoder")
        
        self.config = config
        self._encoder = None
        self._motor_encoder = None
        
        try:
            if config.encoder_type == "quadrature":
                encoding_type_map = {
                    "k1X": wpilib.Encoder.EncodingType.k1X,
                    "k2X": wpilib.Encoder.EncodingType.k2X,
                    "k4X": wpilib.Encoder.EncodingType.k4X
                }
                self._encoder = wpilib.Encoder(
                    config.channel_a,
                    config.channel_b,
                    inverted=config.inverted,
                    encodingType=encoding_type_map.get(config.encoding_type, wpilib.Encoder.EncodingType.k4X)
                )
                self._encoder.setDistancePerPulse(config.distance_per_pulse)
                SimpliPyLogger.info(f"Quadrature encoder initialized on channels {config.channel_a}/{config.channel_b}", "Encoder")
            
            elif config.encoder_type == "motor":
                # Motor encoder accessed through motor controller
                if hasattr(config.motor_controller, 'getEncoder'):
                    self._motor_encoder = config.motor_controller.getEncoder()
                    SimpliPyLogger.info("Motor encoder initialized", "Encoder")
                else:
                    raise ValidationError("Motor controller does not support encoders")
            
            elif config.encoder_type == "absolute":
                # Absolute encoder (e.g., through analog input or CAN)
                SimpliPyLogger.warning("Absolute encoder support is basic - may need custom implementation", "Encoder")
                # Placeholder - absolute encoders vary by hardware
                self._encoder = None
                
        except Exception as e:
            SimpliPyLogger.error("Failed to initialize encoder", "Encoder", e)
            raise
    
    def getPosition(self) -> float:
        """
        Get current encoder position.
        
        Returns:
            Position in encoder units (or distance if distance_per_pulse set)
        """
        try:
            if self._encoder is not None:
                position = self._encoder.getDistance() if self.config.distance_per_pulse != 1.0 else self._encoder.get()
            elif self._motor_encoder is not None:
                position = self._motor_encoder.getPosition()
            else:
                return 0.0
            
            if self.config.inverted:
                position = -position
            return position
        except Exception as e:
            SimpliPyLogger.error("Failed to get encoder position", "Encoder", e)
            return 0.0
    
    def getVelocity(self) -> float:
        """
        Get current encoder velocity.
        
        Returns:
            Velocity in units per second
        """
        try:
            if self._encoder is not None:
                velocity = self._encoder.getRate()
            elif self._motor_encoder is not None:
                velocity = self._motor_encoder.getVelocity()
            else:
                return 0.0
            
            if self.config.inverted:
                velocity = -velocity
            return velocity
        except Exception as e:
            SimpliPyLogger.error("Failed to get encoder velocity", "Encoder", e)
            return 0.0
    
    def getRaw(self) -> int:
        """
        Get raw encoder count.
        
        Returns:
            Raw encoder count (not scaled by distance_per_pulse)
        """
        try:
            if self._encoder is not None:
                count = self._encoder.get()
            elif self._motor_encoder is not None:
                count = int(self._motor_encoder.getPosition())
            else:
                return 0
            
            if self.config.inverted:
                count = -count
            return count
        except Exception as e:
            SimpliPyLogger.error("Failed to get raw encoder count", "Encoder", e)
            return 0
    
    def reset(self) -> None:
        """Reset encoder to zero."""
        try:
            if self._encoder is not None:
                self._encoder.reset()
            elif self._motor_encoder is not None:
                self._motor_encoder.setPosition(0.0)
            SimpliPyLogger.info("Encoder reset", "Encoder")
        except Exception as e:
            SimpliPyLogger.error("Failed to reset encoder", "Encoder", e)
    
    def setPosition(self, position: float) -> None:
        """
        Set encoder position (for motor encoders).
        
        Args:
            position: Position to set
        """
        try:
            if self._motor_encoder is not None:
                self._motor_encoder.setPosition(position)
                SimpliPyLogger.info(f"Encoder position set to {position}", "Encoder")
            else:
                SimpliPyLogger.warning("setPosition() only works for motor encoders", "Encoder")
        except Exception as e:
            SimpliPyLogger.error(f"Failed to set encoder position to {position}", "Encoder", e)

