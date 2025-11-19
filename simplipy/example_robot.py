"""
Example Robot Implementation using simplipy Library
This demonstrates the inheritance-based approach (RobotBase).

For an even simpler approach without inheritance, see example_simple.py
"""

import wpilib
from phoenix5 import NeutralMode

from simplipy.main import RobotBase, RobotConfig
from simplipy.components.drive import DriveConfig
from simplipy.components.arm import ArmConfig
from simplipy.components.motors import MotorType


class MyRobot(RobotBase):
    """
    Example robot implementation.
    This is much simpler than traditional robot.py files!
    """
    
    def robotInit(self):
        """Initialize robot with configuration."""
        # Create drive configuration
        drive_config = DriveConfig(
            left_motors=[
                {"type": MotorType.TALON_SRX, "can_id": 0, "inverted": False, "neutral_mode": NeutralMode.Coast},
                {"type": MotorType.VICTOR_SPX, "can_id": 1, "inverted": False, "neutral_mode": NeutralMode.Coast}
            ],
            right_motors=[
                {"type": MotorType.VICTOR_SPX, "can_id": 2, "inverted": False, "neutral_mode": NeutralMode.Coast},
                {"type": MotorType.VICTOR_SPX, "can_id": 3, "inverted": False, "neutral_mode": NeutralMode.Coast}
            ],
            max_power=0.6,
            invert_left=True,
            invert_right=False,
            use_follow_mode=False  # Set to True for 2025+ (recommended)
        )
        
        # Create arm configuration
        arm_config = ArmConfig(
            arm_motor_can_id=5,
            arm_motor_type=MotorType.SPARK_MAX_BRUSHLESS,
            roller_motor_can_id=7,
            roller_motor_type=MotorType.TALON_SRX,
            limit_switch_dio=0,
            gear_ratio=64.0,
            manual_power=0.15,
            auto_power=0.25,
            roller_power=0.3,
            extension_angle=45.0,
            retraction_limit="switch"
        )
        
        # Create main robot configuration
        config = RobotConfig(
            drive_config=drive_config,
            arm_config=arm_config,
            vision_enabled=False,
            nt_enabled=True,
            robot_name="Example Robot"
        )
        
        # Setup robot with configuration
        self.setup_robot(config)
    
    def teleopPeriodic(self):
        """Teleop control code."""
        # Get joystick input (example)
        joystick = wpilib.Joystick(0)
        
        # Drive control
        if self.drive:
            x_speed = joystick.getY()
            z_rotation = joystick.getZ()
            self.drive.arcadeDrive(x_speed, z_rotation)
        
        # Arm control
        if self.arm:
            # Manual arm control with D-pad
            dpad = joystick.getPOV()
            self.arm.manualArmControl(dpad)
            
            # Roller control
            if joystick.getRawButton(1):
                self.arm.activateRollers(1.0)  # Intake
            elif joystick.getRawButton(2):
                self.arm.activateRollers(-1.0)  # Outtake
            else:
                self.arm.activateRollers(0.0)


if __name__ == "__main__":
    wpilib.run(MyRobot)

