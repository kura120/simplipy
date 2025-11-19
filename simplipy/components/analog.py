"""
simplipy Analog Input Component
Simplified analog input interface for analog sensors.
Supports potentiometers, distance sensors, and other analog devices.
"""

from typing import Optional
import wpilib
from ..utils.errors import ValidationError
from ..utils.logger import SimpliPyLogger


class AnalogConfig:
    """Configuration for analog input."""
    
    def __init__(self,
                 channel: int,
                 inverted: bool = False,
                 voltage_range: tuple = (0.0, 5.0),
                 averaging_bits: int = 0,
                 oversample_bits: int = 0):
        """
        Initialize analog input configuration.
        
        Args:
            channel: Analog input channel (0-3)
            inverted: Whether to invert readings
            voltage_range: Tuple of (min_voltage, max_voltage) for scaling
            averaging_bits: Number of bits for averaging (0-12)
            oversample_bits: Number of bits for oversampling (0-12)
        """
        if not 0 <= channel <= 3:
            raise ValidationError(f"Channel must be between 0 and 3, got {channel}")
        if not 0 <= averaging_bits <= 12:
            raise ValidationError(f"averaging_bits must be between 0 and 12, got {averaging_bits}")
        if not 0 <= oversample_bits <= 12:
            raise ValidationError(f"oversample_bits must be between 0 and 12, got {oversample_bits}")
        if len(voltage_range) != 2 or voltage_range[0] >= voltage_range[1]:
            raise ValidationError(f"Invalid voltage_range: {voltage_range}")
        
        self.channel = channel
        self.inverted = inverted
        self.voltage_range = voltage_range
        self.averaging_bits = averaging_bits
        self.oversample_bits = oversample_bits


class AnalogInput:
    """
    Simplified analog input interface for analog sensors.
    """
    
    def __init__(self, config: Optional[AnalogConfig] = None):
        """
        Initialize analog input.
        
        Args:
            config: AnalogConfig object. If None, uses default configuration.
        """
        if config is None:
            config = AnalogConfig(channel=0)
            SimpliPyLogger.warning("Using default analog input configuration. Consider creating an AnalogConfig.", "Analog")
        
        self.config = config
        
        try:
            self._analog = wpilib.AnalogInput(config.channel)
            
            # Set averaging and oversampling if configured
            if config.averaging_bits > 0:
                self._analog.setAverageBits(config.averaging_bits)
            if config.oversample_bits > 0:
                self._analog.setOversampleBits(config.oversample_bits)
            
            SimpliPyLogger.info(f"Analog input initialized on channel {config.channel}", "Analog")
        except Exception as e:
            SimpliPyLogger.error(f"Failed to initialize analog input on channel {config.channel}", "Analog", e)
            raise
    
    def getVoltage(self) -> float:
        """
        Get voltage reading.
        
        Returns:
            Voltage in volts (0.0 to 5.0 typically)
        """
        try:
            voltage = self._analog.getVoltage()
            if self.config.inverted:
                voltage = self.config.voltage_range[1] - voltage
            return voltage
        except Exception as e:
            SimpliPyLogger.error("Failed to get analog voltage", "Analog", e)
            return 0.0
    
    def getValue(self) -> int:
        """
        Get raw ADC value.
        
        Returns:
            Raw ADC value (0 to 4095 for 12-bit ADC)
        """
        try:
            value = self._analog.getValue()
            if self.config.inverted:
                max_value = (1 << 12) - 1  # 12-bit ADC max
                value = max_value - value
            return value
        except Exception as e:
            SimpliPyLogger.error("Failed to get analog value", "Analog", e)
            return 0
    
    def getAverageVoltage(self) -> float:
        """
        Get averaged voltage reading (if averaging enabled).
        
        Returns:
            Averaged voltage in volts
        """
        try:
            voltage = self._analog.getAverageVoltage()
            if self.config.inverted:
                voltage = self.config.voltage_range[1] - voltage
            return voltage
        except Exception as e:
            SimpliPyLogger.error("Failed to get averaged analog voltage", "Analog", e)
            return 0.0
    
    def getScaledValue(self, min_output: float = 0.0, max_output: float = 1.0) -> float:
        """
        Get voltage scaled to output range.
        
        Args:
            min_output: Minimum output value
            max_output: Maximum output value
        
        Returns:
            Scaled value between min_output and max_output
        """
        try:
            voltage = self.getVoltage()
            min_voltage, max_voltage = self.config.voltage_range
            
            # Scale from voltage range to output range
            if max_voltage == min_voltage:
                return min_output
            
            scaled = min_output + ((voltage - min_voltage) / (max_voltage - min_voltage)) * (max_output - min_output)
            return max(min_output, min(max_output, scaled))
        except Exception as e:
            SimpliPyLogger.error("Failed to get scaled analog value", "Analog", e)
            return min_output

