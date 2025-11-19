"""
simplipy Pneumatics Component (Full Version)
Complete pneumatics interface with solenoids, compressors, and pressure management.
Full-featured version with double solenoids, pressure switches, and advanced control.
"""

from typing import Optional, Literal
import wpilib
from ..utils.errors import ValidationError
from ..utils.logger import SimpliPyLogger


class PneumaticsConfig:
    """Configuration for pneumatics system."""
    
    def __init__(self,
                 module_type: Literal["ctre", "rev"] = "ctre",
                 module_id: int = 0,
                 enable_compressor: bool = True,
                 compressor_type: Literal["analog", "digital", "hybrid"] = "digital",
                 min_pressure: float = 0.0,
                 max_pressure: float = 120.0):
        """
        Initialize pneumatics configuration.
        
        Args:
            module_type: Type of PCM ("ctre" for CTRE PCM, "rev" for REV PH)
            module_id: CAN ID of the pneumatics module
            enable_compressor: Whether to enable compressor automatically
            compressor_type: Type of compressor control
                - "analog": Analog pressure switch
                - "digital": Digital pressure switch
                - "hybrid": Hybrid control
            min_pressure: Minimum pressure in PSI (for analog)
            max_pressure: Maximum pressure in PSI (for analog)
        """
        if module_type not in ["ctre", "rev"]:
            raise ValidationError(f"Unsupported module type: {module_type}")
        if not 0 <= module_id <= 62:
            raise ValidationError(f"Module ID must be between 0 and 62, got {module_id}")
        if min_pressure < 0 or max_pressure <= min_pressure:
            raise ValidationError(f"Invalid pressure range: {min_pressure} to {max_pressure}")
        
        self.module_type = module_type
        self.module_id = module_id
        self.enable_compressor = enable_compressor
        self.compressor_type = compressor_type
        self.min_pressure = min_pressure
        self.max_pressure = max_pressure


class Solenoid:
    """
    Complete solenoid interface with single and double solenoid support.
    """
    
    def __init__(self, channel: int, config: Optional[PneumaticsConfig] = None, 
                 double: bool = False, forward_channel: Optional[int] = None):
        """
        Initialize solenoid.
        
        Args:
            channel: Solenoid channel (0-7 for single, forward channel for double)
            config: PneumaticsConfig object. If None, uses default.
            double: Whether this is a double solenoid
            forward_channel: Forward channel for double solenoid (if different from channel)
        """
        if not 0 <= channel <= 7:
            raise ValidationError(f"Channel must be between 0 and 7, got {channel}")
        
        if config is None:
            config = PneumaticsConfig()
        
        self.channel = channel
        self.config = config
        self.is_double = double
        
        try:
            module_type = (wpilib.PneumaticsModuleType.CTREPCM 
                          if config.module_type == "ctre" 
                          else wpilib.PneumaticsModuleType.REVPH)
            
            if double:
                forward = forward_channel if forward_channel is not None else channel
                reverse = forward + 1
                if reverse > 7:
                    raise ValidationError(f"Double solenoid reverse channel {reverse} out of range")
                self._solenoid = wpilib.DoubleSolenoid(
                    module_type,
                    config.module_id,
                    forward,
                    reverse
                )
                SimpliPyLogger.info(f"Double solenoid initialized on channels {forward}/{reverse}", "Pneumatics")
            else:
                self._solenoid = wpilib.Solenoid(
                    module_type,
                    config.module_id,
                    channel
                )
                SimpliPyLogger.info(f"Solenoid initialized on channel {channel}", "Pneumatics")
        except Exception as e:
            SimpliPyLogger.error(f"Failed to initialize solenoid on channel {channel}", "Pneumatics", e)
            raise
    
    def set(self, value: bool) -> None:
        """
        Set solenoid state.
        
        Args:
            value: True to extend, False to retract (for single)
                   For double: True = forward, False = reverse
        """
        try:
            if self.is_double:
                state = (wpilib.DoubleSolenoid.Value.kForward if value 
                        else wpilib.DoubleSolenoid.Value.kReverse)
                self._solenoid.set(state)
            else:
                self._solenoid.set(value)
        except Exception as e:
            SimpliPyLogger.error(f"Failed to set solenoid on channel {self.channel}", "Pneumatics", e)
    
    def setOff(self) -> None:
        """Set double solenoid to off (neutral) position."""
        if not self.is_double:
            SimpliPyLogger.warning("setOff() only works for double solenoids", "Pneumatics")
            return
        try:
            self._solenoid.set(wpilib.DoubleSolenoid.Value.kOff)
        except Exception as e:
            SimpliPyLogger.error(f"Failed to set solenoid off on channel {self.channel}", "Pneumatics", e)
    
    def get(self) -> bool:
        """
        Get current solenoid state.
        
        Returns:
            True if extended/forward, False if retracted/reverse
        """
        try:
            if self.is_double:
                state = self._solenoid.get()
                return state == wpilib.DoubleSolenoid.Value.kForward
            else:
                return self._solenoid.get()
        except Exception as e:
            SimpliPyLogger.error(f"Failed to get solenoid state on channel {self.channel}", "Pneumatics", e)
            return False


class Compressor:
    """
    Complete compressor interface with pressure management.
    """
    
    def __init__(self, config: Optional[PneumaticsConfig] = None):
        """
        Initialize compressor.
        
        Args:
            config: PneumaticsConfig object. If None, uses default.
        """
        if config is None:
            config = PneumaticsConfig()
        
        self.config = config
        
        try:
            module_type = (wpilib.PneumaticsModuleType.CTREPCM 
                          if config.module_type == "ctre" 
                          else wpilib.PneumaticsModuleType.REVPH)
            
            self._compressor = wpilib.Compressor(config.module_id, module_type)
            
            if config.enable_compressor:
                if config.compressor_type == "analog":
                    self._compressor.enableAnalog(config.min_pressure, config.max_pressure)
                elif config.compressor_type == "digital":
                    self._compressor.enableDigital()
                elif config.compressor_type == "hybrid":
                    self._compressor.enableHybrid(config.min_pressure, config.max_pressure)
                SimpliPyLogger.info(f"Compressor enabled with {config.compressor_type} control", "Pneumatics")
            else:
                self._compressor.disable()
                SimpliPyLogger.info("Compressor disabled", "Pneumatics")
        except Exception as e:
            SimpliPyLogger.error("Failed to initialize compressor", "Pneumatics", e)
            raise
    
    def enable(self) -> None:
        """Enable the compressor with configured control type."""
        try:
            if self.config.compressor_type == "analog":
                self._compressor.enableAnalog(self.config.min_pressure, self.config.max_pressure)
            elif self.config.compressor_type == "digital":
                self._compressor.enableDigital()
            elif self.config.compressor_type == "hybrid":
                self._compressor.enableHybrid(self.config.min_pressure, self.config.max_pressure)
            SimpliPyLogger.info("Compressor enabled", "Pneumatics")
        except Exception as e:
            SimpliPyLogger.error("Failed to enable compressor", "Pneumatics", e)
    
    def disable(self) -> None:
        """Disable the compressor."""
        try:
            self._compressor.disable()
            SimpliPyLogger.info("Compressor disabled", "Pneumatics")
        except Exception as e:
            SimpliPyLogger.error("Failed to disable compressor", "Pneumatics", e)
    
    def isEnabled(self) -> bool:
        """
        Check if compressor is enabled.
        
        Returns:
            True if enabled, False otherwise
        """
        try:
            return self._compressor.isEnabled()
        except Exception as e:
            SimpliPyLogger.error("Failed to check compressor state", "Pneumatics", e)
            return False
    
    def getPressure(self) -> float:
        """
        Get current pressure in PSI (if analog sensor available).
        
        Returns:
            Pressure in PSI, or -1 if not available
        """
        try:
            if hasattr(self._compressor, 'getPressure'):
                return self._compressor.getPressure()
            return -1.0
        except Exception as e:
            SimpliPyLogger.error("Failed to get pressure", "Pneumatics", e)
            return -1.0
    
    def getCurrent(self) -> float:
        """
        Get compressor current draw in amps.
        
        Returns:
            Current in amps, or -1 if not available
        """
        try:
            if hasattr(self._compressor, 'getCurrent'):
                return self._compressor.getCurrent()
            return -1.0
        except Exception as e:
            SimpliPyLogger.error("Failed to get compressor current", "Pneumatics", e)
            return -1.0

