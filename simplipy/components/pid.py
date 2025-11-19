"""
simplipy PID Controller Component
Complete PID controller interface for closed-loop control.
Supports position, velocity, and motion profiling control.
"""

from typing import Optional
import wpilib
from ..utils.errors import ValidationError
from ..utils.logger import SimpliPyLogger


class PIDConfig:
    """Configuration for PID controller."""
    
    def __init__(self,
                 kp: float = 0.0,
                 ki: float = 0.0,
                 kd: float = 0.0,
                 kf: float = 0.0,
                 tolerance: float = 0.05,
                 integral_range: Optional[float] = None,
                 continuous: bool = False,
                 min_output: float = -1.0,
                 max_output: float = 1.0):
        """
        Initialize PID configuration.
        
        Args:
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
            kf: Feedforward gain
            tolerance: Position tolerance for onTarget()
            integral_range: Range around setpoint for integral term (None = no limit)
            continuous: Whether input is continuous (wraps around, e.g., 0-360 degrees)
            min_output: Minimum output value
            max_output: Maximum output value
        """
        if tolerance < 0:
            raise ValidationError(f"Tolerance must be non-negative, got {tolerance}")
        if min_output >= max_output:
            raise ValidationError(f"min_output ({min_output}) must be less than max_output ({max_output})")
        
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.kf = kf
        self.tolerance = tolerance
        self.integral_range = integral_range
        self.continuous = continuous
        self.min_output = min_output
        self.max_output = max_output


class PIDController:
    """
    Complete PID controller for closed-loop control.
    Can be used for position, velocity, or other control loops.
    """
    
    def __init__(self, config: Optional[PIDConfig] = None):
        """
        Initialize PID controller.
        
        Args:
            config: PIDConfig object. If None, uses default configuration.
        """
        if config is None:
            config = PIDConfig()
            SimpliPyLogger.warning("Using default PID configuration. Consider creating a PIDConfig.", "PID")
        
        self.config = config
        
        try:
            self._pid = wpilib.PIDController(
                config.kp,
                config.ki,
                config.kd
            )
            
            # Set additional parameters
            self._pid.setTolerance(config.tolerance)
            if config.integral_range is not None:
                self._pid.setIntegratorRange(-config.integral_range, config.integral_range)
            self._pid.setContinuous(config.continuous)
            self._pid.setOutputRange(config.min_output, config.max_output)
            
            SimpliPyLogger.info(f"PID controller initialized (P={config.kp}, I={config.ki}, D={config.kd})", "PID")
        except Exception as e:
            SimpliPyLogger.error("Failed to initialize PID controller", "PID", e)
            raise
    
    def setSetpoint(self, setpoint: float) -> None:
        """
        Set the desired setpoint.
        
        Args:
            setpoint: Desired value
        """
        try:
            self._pid.setSetpoint(setpoint)
        except Exception as e:
            SimpliPyLogger.error(f"Failed to set PID setpoint to {setpoint}", "PID", e)
    
    def getSetpoint(self) -> float:
        """
        Get the current setpoint.
        
        Returns:
            Current setpoint value
        """
        try:
            return self._pid.getSetpoint()
        except Exception as e:
            SimpliPyLogger.error("Failed to get PID setpoint", "PID", e)
            return 0.0
    
    def calculate(self, measurement: float) -> float:
        """
        Calculate PID output from measurement.
        
        Args:
            measurement: Current measured value
        
        Returns:
            PID output (clamped to min/max output)
        """
        try:
            output = self._pid.calculate(measurement)
            # Add feedforward if configured
            if self.config.kf != 0.0:
                error = self._pid.getSetpoint() - measurement
                output += self.config.kf * error
            return output
        except Exception as e:
            SimpliPyLogger.error(f"Failed to calculate PID output for measurement {measurement}", "PID", e)
            return 0.0
    
    def atSetpoint(self) -> bool:
        """
        Check if controller is at setpoint (within tolerance).
        
        Returns:
            True if at setpoint, False otherwise
        """
        try:
            return self._pid.atSetpoint()
        except Exception as e:
            SimpliPyLogger.error("Failed to check PID setpoint", "PID", e)
            return False
    
    def getPositionError(self) -> float:
        """
        Get current position error.
        
        Returns:
            Error (setpoint - measurement)
        """
        try:
            return self._pid.getPositionError()
        except Exception as e:
            SimpliPyLogger.error("Failed to get PID position error", "PID", e)
            return 0.0
    
    def getVelocityError(self) -> float:
        """
        Get current velocity error (if velocity PID).
        
        Returns:
            Velocity error
        """
        try:
            return self._pid.getVelocityError()
        except Exception as e:
            SimpliPyLogger.error("Failed to get PID velocity error", "PID", e)
            return 0.0
    
    def reset(self) -> None:
        """Reset PID controller (clears integral term)."""
        try:
            self._pid.reset()
            SimpliPyLogger.info("PID controller reset", "PID")
        except Exception as e:
            SimpliPyLogger.error("Failed to reset PID controller", "PID", e)
    
    def setPID(self, kp: float, ki: float, kd: float) -> None:
        """
        Update PID gains.
        
        Args:
            kp: Proportional gain
            ki: Integral gain
            kd: Derivative gain
        """
        try:
            self._pid.setPID(kp, ki, kd)
            self.config.kp = kp
            self.config.ki = ki
            self.config.kd = kd
            SimpliPyLogger.info(f"PID gains updated (P={kp}, I={ki}, D={kd})", "PID")
        except Exception as e:
            SimpliPyLogger.error("Failed to update PID gains", "PID", e)
    
    def enable(self) -> None:
        """Enable the PID controller."""
        try:
            self._pid.enable()
            SimpliPyLogger.info("PID controller enabled", "PID")
        except Exception as e:
            SimpliPyLogger.error("Failed to enable PID controller", "PID", e)
    
    def disable(self) -> None:
        """Disable the PID controller."""
        try:
            self._pid.disable()
            SimpliPyLogger.info("PID controller disabled", "PID")
        except Exception as e:
            SimpliPyLogger.error("Failed to disable PID controller", "PID", e)

