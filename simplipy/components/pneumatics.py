"""
simplipy Pneumatics Component (WIP)
Simplified pneumatics interface for solenoids and compressors.
This is a wip (again), im not so sure if this will work, im learning how pneumatics work as i go..
"""

from typing import Optional, List
import wpilib
from ..utils.errors import ValidationError
from ..utils.logger import SimpliPyLogger


class PneumaticsConfig:
    """Configuration for pneumatics system."""
    
    def __init__(self,
                 module_type: str = "ctre",
                 module_id: int = 0,
                 enable_compressor: bool = True,
                 compressor_type: str = "analog"):
        """
        Initialize pneumatics configuration.
        
        Args:
            module_type: Type of PCM ("ctre" for CTRE PCM, "rev" for REV PH)
            module_id: CAN ID of the pneumatics module
            enable_compressor: Whether to enable compressor automatically
            compressor_type: Type of compressor control ("analog" or "digital")
        """
        if module_type not in ["ctre", "rev"]:
            raise ValidationError(f"Unsupported module type: {module_type}")
        if not 0 <= module_id <= 62:
            raise ValidationError(f"Module ID must be between 0 and 62, got {module_id}")
        
        self.module_type = module_type
        self.module_id = module_id
        self.enable_compressor = enable_compressor
        self.compressor_type = compressor_type


class Solenoid:
    """
    Simplified solenoid interface (WIP Version).
    Basic on/off control for single and double solenoids.
    """
    
    def __init__(self, channel: int, config: Optional[PneumaticsConfig] = None):
        """
        Initialize solenoid.
        
        Args:
            channel: Solenoid channel (0-7 for single, 0-6 for double)
            config: PneumaticsConfig object. If None, uses default.
        """
        if not 0 <= channel <= 7:
            raise ValidationError(f"Channel must be between 0 and 7, got {channel}")
        
        if config is None:
            config = PneumaticsConfig()
        
        self.channel = channel
        self.config = config
        
        try:
            if config.module_type == "ctre":
                self._solenoid = wpilib.Solenoid(
                    wpilib.PneumaticsModuleType.CTREPCM,
                    config.module_id,
                    channel
                )
            else:  # rev
                self._solenoid = wpilib.Solenoid(
                    wpilib.PneumaticsModuleType.REVPH,
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
            value: True to extend, False to retract
        """
        try:
            self._solenoid.set(value)
        except Exception as e:
            SimpliPyLogger.error(f"Failed to set solenoid on channel {self.channel}", "Pneumatics", e)
    
    def get(self) -> bool:
        """
        Get current solenoid state.
        
        Returns:
            True if extended, False if retracted
        """
        try:
            return self._solenoid.get()
        except Exception as e:
            SimpliPyLogger.error(f"Failed to get solenoid state on channel {self.channel}", "Pneumatics", e)
            return False


class Compressor:
    """
    Simplified compressor interface (WIP Version).
    Basic compressor control.
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
                self._compressor.enableDigital()
                SimpliPyLogger.info("Compressor enabled", "Pneumatics")
            else:
                self._compressor.disable()
                SimpliPyLogger.info("Compressor disabled", "Pneumatics")
        except Exception as e:
            SimpliPyLogger.error("Failed to initialize compressor", "Pneumatics", e)
            raise
    
    def enable(self) -> None:
        """Enable the compressor."""
        try:
            self._compressor.enableDigital()
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
        Get current pressure (if pressure switch available).
        
        Returns:
            Pressure reading (0.0 to 1.0, or -1 if not available)
        """
        try:
            if hasattr(self._compressor, 'getPressure'):
                return self._compressor.getPressure()
            return -1.0
        except Exception as e:
            SimpliPyLogger.error("Failed to get pressure", "Pneumatics", e)
            return -1.0

