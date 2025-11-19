"""
simplipy Limit Switch
Enhanced limit switch with better state management and error handling.
"""

import wpilib as wpi
from typing import Optional
from ..utils.errors import ValidationError
from ..utils.logger import SimpliPyLogger


class LimitSwitch(wpi.DigitalInput):
    """
    Enhanced limit switch with state tracking and edge detection.
    Inherits from wpilib.DigitalInput for full compatibility.
    """
    
    def __init__(self, dio_id: int, normally_open: bool = True):
        """
        Initialize limit switch.
        
        Args:
            dio_id: Digital I/O port ID (0-9)
            normally_open: True if switch is normally open, False if normally closed
        """
        if not isinstance(dio_id, int) or not 0 <= dio_id <= 9:
            raise ValidationError(f"DIO ID must be an integer between 0 and 9, got {dio_id}")
        
        try:
            super().__init__(dio_id)
            self._normally_open = normally_open
            self._is_triggered = False
            self._last_state = False
            self._dio_id = dio_id
            SimpliPyLogger.info(f"Limit switch initialized on DIO {dio_id}", "LimitSwitch")
        except Exception as e:
            SimpliPyLogger.error(f"Failed to initialize limit switch on DIO {dio_id}", "LimitSwitch", e)
            raise
    
    def get(self) -> bool:
        """
        Get current switch state.
        
        Returns:
            True if switch is pressed (or released if normally closed), False otherwise
        """
        try:
            state = super().get()
            # Invert if normally closed
            if not self._normally_open:
                state = not state
            self._last_state = state
            return state
        except Exception as e:
            SimpliPyLogger.error(f"Failed to read limit switch on DIO {self._dio_id}", "LimitSwitch", e)
            return False
    
    def getPressed(self) -> bool:
        """
        Detect rising edge (switch just pressed).
        Returns True only once when switch transitions from not pressed to pressed.
        
        Returns:
            True if switch was just pressed, False otherwise
        """
        current_state = self.get()
        
        if current_state and not self._is_triggered:
            self._is_triggered = True
            SimpliPyLogger.info(f"Limit switch on DIO {self._dio_id} pressed", "LimitSwitch")
            return True
        
        return False
    
    def getReleased(self) -> bool:
        """
        Detect falling edge (switch just released).
        Returns True only once when switch transitions from pressed to not pressed.
        
        Returns:
            True if switch was just released, False otherwise
        """
        current_state = self.get()
        
        if not current_state and self._is_triggered:
            self._is_triggered = False
            SimpliPyLogger.info(f"Limit switch on DIO {self._dio_id} released", "LimitSwitch")
            return True
        
        return False
    
    def isPressed(self) -> bool:
        """
        Check if switch is currently pressed (state tracking).
        
        Returns:
            True if switch is pressed, False otherwise
        """
        return self._is_triggered
    
    def reset(self) -> None:
        """Reset the switch state tracking."""
        self._is_triggered = False
        self._last_state = False
