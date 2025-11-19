"""
simplipy Main Entry Point
Simplified robot.py interface for WPILib.
This is the main entry point that makes robot creation simple and error-resistant.
"""

import wpilib
from typing import Optional, Dict, Any
from dataclasses import dataclass

from .components.drive import Drive, DriveConfig
from .components.arm import Arm, ArmConfig
from .components.vision import Vision
from .components.gyro import Gyro, GyroConfig
from .components.pneumatics import PneumaticsConfig
from .components.servo import Servo, ServoConfig
from .components.nt import NetworkTable
from .utils.config import Config
from .utils.logger import SimpliPyLogger
from .utils.errors import SimpliPyError


@dataclass
class RobotConfig:
    """
    Main robot configuration.
    Use this to configure all robot subsystems in one place.
    """
    # Drive configuration
    drive_config: Optional[DriveConfig] = None
    
    # Arm configuration
    arm_config: Optional[ArmConfig] = None
    
    # Vision configuration
    vision_enabled: bool = False
    vision_table_name: str = "vision"
    
    # Gyro/IMU configuration
    gyro_config: Optional[GyroConfig] = None
    
    # Pneumatics configuration
    pneumatics_config: Optional[PneumaticsConfig] = None
    
    # NetworkTables configuration
    nt_enabled: bool = True
    nt_table_name: str = "datatable"
    
    # Robot-wide settings
    enable_logging: bool = True
    robot_name: str = "simplipy Robot"


class RobotBase(wpilib.TimedRobot):
    """
    Base robot class that simplifies robot.py creation.
    Inherit from this instead of wpilib.TimedRobot for simplified setup.
    
    Example usage:
        class MyRobot(RobotBase):
            def robotInit(self):
                # Configure your robot
                config = RobotConfig(
                    drive_config=DriveConfig(...),
                    arm_config=ArmConfig(...)
                )
                self.setup_robot(config)
            
            def teleopPeriodic(self):
                # Use self.drive, self.arm, etc.
                self.drive.arcadeDrive(xSpeed, zRotation)
    """
    
    def __init__(self):
        """Initialize robot base."""
        super().__init__()
        self.config: Optional[RobotConfig] = None
        self.drive: Optional[Drive] = None
        self.arm: Optional[Arm] = None
        self.vision: Optional[Vision] = None
        self.gyro: Optional[Gyro] = None
        self.nt: Optional[NetworkTable] = None
        self._initialized = False
    
    def setup_robot(self, config: RobotConfig) -> None:
        """
        Setup robot with configuration.
        Call this in robotInit() after creating your RobotConfig.
        
        Args:
            config: RobotConfig object with all subsystem configurations
        """
        if self._initialized:
            SimpliPyLogger.warning("Robot already initialized, skipping setup", "RobotBase")
            return
        
        self.config = config
        
        try:
            # Setup logging
            if config.enable_logging:
                wpilib.DataLogManager.start()
                SimpliPyLogger.info(f"Initializing {config.robot_name}", "RobotBase")
            
            # Setup NetworkTables
            if config.nt_enabled:
                try:
                    self.nt = NetworkTable(config.nt_table_name)
                    SimpliPyLogger.info("NetworkTables enabled", "RobotBase")
                except Exception as e:
                    SimpliPyLogger.error("Failed to setup NetworkTables", "RobotBase", e)
            
            # Setup Drive
            if config.drive_config is not None:
                try:
                    self.drive = Drive(config.drive_config)
                    SimpliPyLogger.info("Drive system initialized", "RobotBase")
                except Exception as e:
                    SimpliPyLogger.error("Failed to initialize drive system", "RobotBase", e)
                    raise
            
            # Setup Arm
            if config.arm_config is not None:
                try:
                    self.arm = Arm(config.arm_config)
                    SimpliPyLogger.info("Arm system initialized", "RobotBase")
                except Exception as e:
                    SimpliPyLogger.error("Failed to initialize arm system", "RobotBase", e)
                    # Don't raise - arm might be optional
            
            # Setup Vision
            if config.vision_enabled:
                try:
                    self.vision = Vision(config.vision_table_name)
                    SimpliPyLogger.info("Vision system initialized", "RobotBase")
                except Exception as e:
                    SimpliPyLogger.error("Failed to initialize vision system", "RobotBase", e)
                    # Don't raise - vision might be optional
            
            # Setup Gyro
            if config.gyro_config is not None:
                try:
                    from .components.gyro import Gyro
                    self.gyro = Gyro(config.gyro_config)
                    SimpliPyLogger.info("Gyro system initialized", "RobotBase")
                except Exception as e:
                    SimpliPyLogger.error("Failed to initialize gyro system", "RobotBase", e)
                    # Don't raise - gyro might be optional
            
            self._initialized = True
            SimpliPyLogger.info(f"{config.robot_name} setup complete", "RobotBase")
            
        except Exception as e:
            SimpliPyLogger.error("Critical error during robot setup", "RobotBase", e)
            raise SimpliPyError(f"Robot setup failed: {str(e)}")
    
    def robotInit(self) -> None:
        """
        Override this method to configure your robot.
        Example:
            def robotInit(self):
                config = RobotConfig(...)
                self.setup_robot(config)
        """
        pass
    
    def robotPeriodic(self) -> None:
        """Periodic robot code. Override if needed."""
        pass
    
    def autonomousInit(self) -> None:
        """Autonomous initialization. Override if needed."""
        if self.arm:
            self.arm.initializeArm()
    
    def autonomousPeriodic(self) -> None:
        """Autonomous periodic code. Override with your autonomous logic."""
        pass
    
    def teleopInit(self) -> None:
        """Teleop initialization. Override if needed."""
        pass
    
    def teleopPeriodic(self) -> None:
        """Teleop periodic code. Override with your teleop logic."""
        pass
    
    def testInit(self) -> None:
        """Test mode initialization. Override if needed."""
        if self.arm:
            self.arm.initializeArm()
    
    def testPeriodic(self) -> None:
        """Test mode periodic code. Override if needed."""
        pass
    
    def disabledInit(self) -> None:
        """Disabled initialization. Override if needed."""
        # Stop all subsystems when disabled
        if self.drive:
            self.drive.stop()
        if self.arm:
            self.arm.arm_motor.stopMotor()
    
    def disabledPeriodic(self) -> None:
        """Disabled periodic code. Override if needed."""
        pass


class SimpliPyRobot:
    """
    Factory class for creating configured robots without inheritance.
    Use this for the simplest robot setup - no class definition needed!
    
    Example usage:
        # Create configuration
        config = RobotConfig(
            drive_config=DriveConfig(...),
            arm_config=ArmConfig(...)
        )
        
        # Create robot class (no inheritance needed!)
        Robot = SimpliPyRobot(config)
        
        # Run robot
        if __name__ == "__main__":
            wpilib.run(Robot)
    
    For custom periodic methods, you can still inherit:
        class MyRobot(SimpliPyRobot.create(config)):
            def teleopPeriodic(self):
                # Custom teleop code
                super().teleopPeriodic()
                # Your code here
    """
    
    @staticmethod
    def create(config: RobotConfig) -> type:
        """
        Create a configured robot class.
        
        Args:
            config: RobotConfig with all subsystem configurations
        
        Returns:
            A configured RobotBase class ready to use with wpilib.run()
        
        Example:
            Robot = SimpliPyRobot.create(config)
            wpilib.run(Robot)
        """
        class ConfiguredRobot(RobotBase):
            """Auto-configured robot class created by SimpliPyRobot."""
            
            def robotInit(self):
                """Auto-configured robotInit - sets up all subsystems."""
                self.setup_robot(config)
        
        # Set class name for better debugging
        ConfiguredRobot.__name__ = config.robot_name.replace(" ", "")
        ConfiguredRobot.__qualname__ = ConfiguredRobot.__name__
        
        return ConfiguredRobot
    
    def __new__(cls, config: RobotConfig):
        """
        Allow instantiation syntax: Robot = SimpliPyRobot(config)
        This returns a class, not an instance.
        
        Args:
            config: RobotConfig with all subsystem configurations
        
        Returns:
            A configured RobotBase class
        
        Example:
            Robot = SimpliPyRobot(config)
            wpilib.run(Robot)
        """
        return cls.create(config)


# Convenience function for quick robot setup (backward compatibility)
def create_robot(config: RobotConfig) -> type:
    """
    Factory function to create a configured robot class.
    Alias for SimpliPyRobot.create()
    
    Args:
        config: RobotConfig with all subsystem configurations
    
    Returns:
        Configured RobotBase class ready to use with wpilib.run()
    
    Example:
        Robot = create_robot(config)
        wpilib.run(Robot)
    """
    return SimpliPyRobot.create(config)

