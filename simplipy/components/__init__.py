"""
simplipy Components Package
Contains all robot subsystem components.
"""

# Core components
from .motors import MotorFactory, MotorType, MotorController
from .drive import Drive, DriveConfig
from .switch import LimitSwitch

# Subsystem components
from .arm import Arm, ArmConfig
from .vision import Vision

# Sensor components
from .gyro import Gyro, GyroConfig
from .encoder import Encoder, EncoderConfig
from .analog import AnalogInput, AnalogConfig

# Actuator components
from .pneumatics import Solenoid, Compressor, PneumaticsConfig
from .servo import Servo, ServoConfig

# Control components
from .pid import PIDController, PIDConfig

# Utility components
from .nt import NetworkTable

__all__ = [
    # Core
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
]

