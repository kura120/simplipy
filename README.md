# simplipy

simplipy is a simplified Python library for robot programming in the [FIRST Robotics Competition](https://www.firstinspires.org/robotics/frc). It provides a configuration-based approach to building FRC robots using [WPILib](https://github.com/wpilibsuite/allwpilib).

This library is designed to make FRC robot programming simpler and more accessible, especially for beginners.

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

2. **Install simplipy**

   Install simplipy using pip:
   ```bash
   # Install from GitHub (recommended for latest version)
   pip install git+https://github.com/kura120/simplify.git
   ```

   Or if published to PyPI (soon?):
   ```bash
   pip install simplipy
   ```

3. **Import simplipy in Your Code**
   ```python
   from simplipy import SimpliPyRobot, RobotConfig
   ```

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
simplipy/
├── simplipy/               # Main library package
│   ├── components/         # Robot subsystem components
│   ├── utils/              # Utilities (config, errors, logging)
│   └── main.py            # Core robot factory
├── examples/               # Example robot implementations
│   ├── example_simple.py  # Simplest usage example
│   └── example_robot.py   # Inheritance-based example
├── .github/                # GitHub workflows and templates
│   └── workflows/         # CI/CD pipelines
├── setup.py               # Python package setup
├── pyproject.toml         # Modern Python project config
├── MANIFEST.in            # Package manifest
├── README.md              # This file
└── LICENSE                # MIT License
```

### CI/CD

This project uses GitHub Actions for continuous integration. See `.github/workflows/` for workflow definitions.

The CI pipeline includes:

- **Package Build Testing**: Tests that the package can be built on Python 3.8-3.11
- **Installation Testing**: Verifies the package can be installed from GitHub
- **Syntax Validation**: Checks all Python files have valid syntax
- **Linting**: Code quality checks with flake8 and pylint
- **Manifest Validation**: Ensures all necessary files are included in the package

### Contributing

> [!WARNING]
> This is a pre-season project for learning and experimentation. Components marked as "WIP" are work-in-progress and may not be fully functional. Do not use WIP components in competition code without thorough testing.

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines.

### Building simplipy

> [!WARNING]
> It is not recommended for users to build their own copy of simplipy. Instead, you should use our prebuilt packages that are available via pip installation from GitHub. See [Installation](#installation) for details.

simplipy is a pure Python library. The package can be built like any standard Python package:

```bash
# Install build tools
pip install build wheel

# Build the package
python -m build --sdist --wheel
```

The resulting wheels and source distributions will be in the `dist/` directory and can be installed using `pip`.

### Development Environment

To set up a development environment for contributing to simplipy:

1. **Install development dependencies:**
   ```bash
   pip install -r requirements-dev.txt
   ```

2. **Install simplipy in editable mode:**
   ```bash
   pip install -e .
   ```

   This allows you to edit the source code and see changes immediately without reinstalling.

3. **For pure Python development:**
   You can edit files in the `simplipy/` directory in-place, and changes will take effect immediately (no rebuild needed).

> [!NOTE]
> simplipy is pure Python, so there's no compilation step. Changes to Python files take effect immediately after saving.

### Testing

> [!WARNING]
> simplipy is designed to run on the RoboRIO (robot hardware) or in simulation. Some features may not work correctly when testing on a regular computer without robot hardware connected.

To test simplipy:

1. Ensure you have WPILib Python environment set up (see [Installation](#installation))
2. Install simplipy: `pip install git+https://github.com/kura120/simplify.git`
3. Import and use as shown in [Examples](#examples)
4. Deploy to your robot or use simulation to test


## Examples

See the `examples/` directory for complete examples:
- `example_simple.py`: Simplest usage with `SimpliPyRobot(config)`
- `example_robot.py`: Traditional inheritance approach

To use the examples:
1. Copy the example file to your robot project
2. Adjust CAN IDs and configuration to match your hardware
3. Deploy and test

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
1. Make sure you're using the correct Python environment (WPILib Python)
2. Reinstall simplipy: `pip install git+https://github.com/kura120/simplify.git`
3. Verify installation: `python -c "import simplipy; print(simplipy.__version__)"`

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

[MIT](https://github.com/kura120/simplipy/blob/main/LICENSE)

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

