"""
simplipy - Simplified Python Library for WPILib
A simplified, enhanced library for FIRST Robotics Competition robot development.

This library provides:
- Simplified motor creation and management
- Enhanced error handling
- Configuration-based setup
- Reusable components for common robot subsystems
"""

__version__ = "1.0.0"
__author__ = "Pre-Season 2026"

from .main import RobotBase, RobotConfig, SimpliPyRobot
from .components.motors import MotorFactory, MotorType, MotorController
from .components.drive import Drive, DriveConfig
from .components.arm import Arm, ArmConfig
from .components.switch import LimitSwitch
from .components.vision import Vision
from .components.gyro import Gyro, GyroConfig
from .components.pneumatics import Solenoid, Compressor, PneumaticsConfig
from .components.servo import Servo, ServoConfig
from .components.pid import PIDController, PIDConfig
from .components.encoder import Encoder, EncoderConfig
from .components.analog import AnalogInput, AnalogConfig
from .components.nt import NetworkTable
from .utils.config import Config
from .utils.errors import SimpliPyError, MotorError, ConfigError, ValidationError
from .utils.logger import SimpliPyLogger

__all__ = [
    # Core
    'RobotBase',
    'RobotConfig',
    'SimpliPyRobot',
    'MotorFactory',
    'MotorType',
    'MotorController',
    'Drive',
    'DriveConfig',
    'LimitSwitch',
    # Subsystems
    'Arm',
    'ArmConfig',
    'Vision',
    # Sensors
    'Gyro',
    'GyroConfig',
    'Encoder',
    'EncoderConfig',
    'AnalogInput',
    'AnalogConfig',
    # Actuators
    'Solenoid',
    'Compressor',
    'PneumaticsConfig',
    'Servo',
    'ServoConfig',
    # Control
    'PIDController',
    'PIDConfig',
    # Utilities
    'NetworkTable',
    'Config',
    'SimpliPyError',
    'MotorError',
    'ConfigError',
    'ValidationError',
    'SimpliPyLogger',
]

