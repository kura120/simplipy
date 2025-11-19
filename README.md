# simplipy - Simplified Python Library for FRC

This repository contains a Python library that simplifies robot programming for the [FIRST Robotics Competition](https://www.firstinspires.org/robotics/frc). simplipy provides a simplified, configuration-based approach to building FRC robots using [WPILib](https://github.com/wpilibsuite/allwpilib).

simplipy wraps WPILib's robot framework to make robot creation as simple as:

```python
from simplipy import SimpliPyRobot, RobotConfig
from simplipy.components.drive import DriveConfig
from simplipy.components.motors import MotorType
from phoenix5 import NeutralMode

# Configure your robot
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
    invert_right=False
)

config = RobotConfig(drive_config=drive_config)
Robot = SimpliPyRobot(config)

if __name__ == "__main__":
    wpilib.run(Robot)
```

**No class inheritance needed!** Just configure and go.

## Features

- **Simplified Motor Creation**: Unified factory pattern for all motor types (TalonSRX, VictorSPX, SparkMax)
- **Configuration-Based Setup**: Avoid hard-coded values with centralized configuration
- **Enhanced Error Handling**: Comprehensive error handling with custom exceptions and logging
- **Easy Robot Setup**: Simple `SimpliPyRobot` factory that creates configured robots without class definitions
- **Foundational Components**: Pre-built components for common robot subsystems (drive, arm, sensors, actuators)
- **Better State Management**: Improved state tracking for subsystems
- **Validation**: Input validation for all operations
- **Logging**: Built-in logging system for debugging

## Installation

> [!WARNING]
> simplipy requires WPILib Python to be installed. You cannot use simplipy without the full WPILib development environment. Make sure you have completed the WPILib installation before proceeding.

### Step 1: Install WPILib

simplipy is designed to work with WPILib Python projects. You must first install WPILib:

1. **Download WPILib Installer**
   - Go to the official WPILib website: [https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/wpilib-setup.html](https://docs.wpilib.org/en/stable/docs/zero-to-robot/step-2/wpilib-setup.html)
   - Or directly: [https://github.com/wpilibsuite/allwpilib/releases](https://github.com/wpilibsuite/allwpilib/releases)
   - Look for the latest release and download the installer for your operating system:
     - **Windows**: `WPILibInstaller-Windows64.exe`
     - **macOS**: `WPILibInstaller-macOS.dmg`
     - **Linux**: `WPILibInstaller-Linux64.AppImage`

2. **Run the Installer**
   - Follow the installation wizard
   - Select "Install for this user" (recommended)
   - Choose installation location (default is fine)
   - Wait for installation to complete

3. **Verify Installation**
   - Open VS Code
   - You should see the WPILib extension installed
   - Create a new WPILib project to verify everything works

> [!WARNING]
> If you don't have VS Code installed, WPILib installer will prompt you to install it. VS Code is required for WPILib development.

### Step 2: Install simplipy in Your Robot Project

Once WPILib is installed:

1. **Create a New WPILib Robot Project**
   - Open VS Code
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "WPILib: Create a new project"
   - Follow the wizard to create your robot project

2. **Copy simplipy to Your Project**
   - Copy the entire `simplipy` folder from this repository
   - Paste it into your robot project's root directory
   - Your project structure should look like:
     ```
     my-robot-project/
     ├── simplipy/         # simplipy library (copied here)
     ├── robot.py          # Your robot code
     └── ...
     ```

3. **Import simplipy in Your Code**
   ```python
   from simplipy import SimpliPyRobot, RobotConfig
   ```

> [!WARNING]
> Do not modify files inside the `simplipy` folder unless you know what you're doing. Changes may break the library or cause unexpected behavior.

## Quick Start

> [!WARNING]
> Make sure you have completed the WPILib installation (see Installation section above) before trying to use simplipy. simplipy will not work without WPILib.

See the [simplipy Documentation](simplipy/README.md) for detailed usage instructions and examples.

### Minimal Example

> [!WARNING]
> This example assumes you have motors connected to CAN IDs 0 and 1. Make sure your motor CAN IDs match what you configure in Phoenix Tuner or REV Hardware Client. Using incorrect CAN IDs will cause errors.

```python
import wpilib
from simplipy import SimpliPyRobot, RobotConfig
from simplipy.components.drive import DriveConfig
from simplipy.components.motors import MotorType
from phoenix5 import NeutralMode

# Configure drive system
drive_config = DriveConfig(
    left_motors=[
        {"type": MotorType.TALON_SRX, "can_id": 0, "inverted": False, "neutral_mode": NeutralMode.Coast}
    ],
    right_motors=[
        {"type": MotorType.TALON_SRX, "can_id": 1, "inverted": False, "neutral_mode": NeutralMode.Coast}
    ],
    max_power=0.6
)

# Create and run robot
Robot = SimpliPyRobot(RobotConfig(drive_config=drive_config))

if __name__ == "__main__":
    wpilib.run(Robot)
```

## Components

simplipy provides foundational components for FRC robots:

### Core Components
- **Motors**: Unified motor factory (TalonSRX, VictorSPX, SparkMax)
- **Drive**: Simplified drive train setup
- **Limit Switches**: Enhanced limit switch interface

### Subsystem Components
- **Arm**: Arm mechanism with encoder and limit switch support
- **Vision**: Vision processing integration

### Sensor Components
- **Gyro/IMU**: Orientation sensing
  > [!WARNING]
  > Gyro component is WIP (Work In Progress). It may not work correctly. Use at your own risk and test thoroughly on hardware.
- **Encoders**: Unified encoder interface
- **Analog Inputs**: Analog sensor interface

### Actuator Components
- **Pneumatics**: Solenoids and compressors
  > [!WARNING]
  > Pneumatics component is WIP (Work In Progress). It may not work correctly. Use at your own risk and test thoroughly on hardware.
- **Servos**: Precise positioning control
  > [!WARNING]
  > Servo component is WIP (Work In Progress). It may not work correctly. Use at your own risk and test thoroughly on hardware.

### Control Components
- **PID Controller**: Closed-loop control

### Utility Components
- **NetworkTables**: Enhanced NetworkTables wrapper

## Requirements

> [!WARNING]
> These dependencies are automatically installed with WPILib. You do NOT need to install them separately using pip. Installing them manually may cause conflicts with WPILib.

simplipy requires the following (all included with WPILib):

- **WPILib Python** (2024 or later) - Core FRC library
- **phoenix5** - For TalonSRX/VictorSPX motor controllers (included with WPILib)
- **rev** - For SparkMax motor controllers (included with WPILib)
- **ntcore** - For NetworkTables (included with WPILib)

> [!WARNING]
> Do NOT run `pip install phoenix5` or `pip install rev` manually. These are installed by the WPILib installer and must match the WPILib version. Installing them separately will cause version conflicts.

## Development

### Project Structure

```
your_project/
├── simplipy/               # Main library package
│   ├── components/         # Robot subsystem components
│   ├── utils/              # Utilities (config, errors, logging)
│   ├── main.py            # Core robot factory
│   └── example_*.py       # Example implementations
├── .github/                # GitHub workflows and templates
│   ├── workflows/         # CI/CD pipelines
│   └── ISSUE_TEMPLATE/    # Issue templates
├── setup.py               # Python package setup
├── pyproject.toml         # Modern Python project config
└── README.md              # This file
```

### CI/CD

This project uses GitHub Actions for continuous integration:

- **Linting**: Code quality checks with flake8, pylint, and mypy
- **Syntax Testing**: Validates Python syntax
- **Code Quality**: Security scanning and dependency checks
- **Release Automation**: Automated release package creation

See `.github/workflows/` for workflow definitions.

### Contributing

> [!WARNING]
> This is a pre-season project for learning and experimentation. Components marked as "WIP" are work-in-progress and may not be fully functional. Do not use WIP components in competition code without thorough testing.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

### Building/Testing

> [!WARNING]
> simplipy is designed to run on the RoboRIO (robot hardware) or in simulation. Some features may not work correctly when testing on a regular computer without robot hardware connected.

simplipy is a pure Python library and doesn't require building. To test:

1. Ensure you have WPILib Python environment set up (see Installation section)
2. Copy simplipy to your robot project
3. Import and use as shown in examples
4. Deploy to your robot or use simulation to test

For development:

```bash
pip install -r requirements-dev.txt
```

> [!WARNING]
> Only install development dependencies if you plan to modify simplipy. Regular users do not need these.

### Installation from Source

```bash
git clone https://github.com/yourusername/pre-season-2026.git
cd pre-season-2026
# Copy simplipy folder to your robot project
```

## Examples

See the `simplipy/` directory for complete examples:
- `example_simple.py`: Simplest usage with `SimpliPyRobot(config)`
- `example_robot.py`: Traditional inheritance approach

## Documentation

For detailed documentation, see [simplipy/README.md](simplipy/README.md) which includes:
- Step-by-step setup instructions
- Component configuration guides
- Hardware setup (CAN IDs, DIO ports)
- Common questions and troubleshooting

## Troubleshooting

### Common Issues for Beginners

#### "ModuleNotFoundError: No module named 'wpilib'"

> [!WARNING]
> This error means WPILib is not installed or not properly configured. You MUST install WPILib using the official installer (see Installation section). You cannot install wpilib using pip.

**Solution:**
1. Make sure you installed WPILib using the official installer
2. Create your robot project using "WPILib: Create a new project" in VS Code
3. Do NOT try to install wpilib with `pip install wpilib` - it won't work

#### "ModuleNotFoundError: No module named 'simplipy'"

**Solution:**
1. Make sure you copied the `simplipy` folder into your robot project directory
2. Check that the folder is named exactly `simplipy` (case-sensitive)
3. Verify the folder structure:
   ```
   your-robot-project/
   ├── simplipy/     ← Must be here
   │   ├── __init__.py
   │   └── ...
   └── robot.py
   ```

#### "Motor not responding" or "CAN timeout"

> [!WARNING]
> This usually means your CAN IDs don't match. Double-check every CAN ID in your code matches what's configured in Phoenix Tuner or REV Hardware Client.

**Solution:**
1. Open Phoenix Tuner (for TalonSRX/VictorSPX) or REV Hardware Client (for SparkMax)
2. Connect to your robot
3. Write down each motor's CAN ID
4. Make sure your code uses the exact same CAN IDs
5. Check that motors are properly connected to CAN bus

#### "Robot moves backwards"

**Solution:**
1. Try changing `invert_left` or `invert_right` in your DriveConfig
2. Try changing individual motor `inverted` settings
3. Test one change at a time to see what fixes it

#### "Import errors in VS Code"

> [!WARNING]
> VS Code may show import errors even when code works. This is because WPILib packages aren't available in the standard Python environment. If your code deploys and runs on the robot, the errors can be ignored.

**Solution:**
1. These errors are often false positives
2. Try deploying to robot - if it works, the errors are safe to ignore
3. Make sure you're using the WPILib Python interpreter (check bottom-right of VS Code)

## License

Part of Pre-Season 2026 project.

## Important Notes

> [!WARNING]
> Always test your robot code on hardware before competitions. simplipy simplifies coding but cannot prevent all errors. Verify motor directions, CAN IDs, and sensor readings before matches.

### For Beginners

If you're new to FRC programming:

1. **Start Simple**: Begin with just a drive train. Don't add all components at once.
2. **Test Often**: Deploy code frequently and test each component individually.
3. **Check CAN IDs**: Use Phoenix Tuner or REV Hardware Client to verify all CAN IDs match your code.
4. **Read Error Messages**: simplipy provides helpful error messages - read them carefully!
5. **Ask for Help**: If something doesn't work, check the error logs and ask your mentors.

> [!WARNING]
> Never deploy untested code to a robot during a competition. Always test in the pit first.

## Acknowledgments

> Before any questions, yes I made most of this, yes I had help from the internet here and there, yes I used AI in extremely complex parts I needed help with. (Used all my available tools..)

simplipy is designed to simplify FRC robot programming by providing a clean, configuration-based interface over WPILib's powerful but complex framework.

