# Changelog

All notable changes to simplipy will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.1] - 2026-01-XX

### Changed
- Converted project to proper Python package structure
- Moved example files from `simplipy/` to `examples/` directory
- Updated installation instructions to support pip installation
- Enhanced package configuration in `setup.py` and `pyproject.toml`

### Added
- `MANIFEST.in` for proper package distribution
- `.gitignore` file for build artifacts and development files
- Support for installing via `pip install simplipy`
- Support for editable/development installs with `pip install -e .`

### Fixed
- Package structure now follows Python packaging best practices
- Examples are no longer included in the installed package

## [1.0.0] - 2026-01-XX

### Added
- Initial release of simplipy library
- Core components: Motors, Drive, Limit Switches
- Subsystem components: Arm, Vision
- Sensor components: Gyro (WIP), Encoders, Analog Inputs
- Actuator components: Pneumatics (WIP), Servos (WIP)
- Control components: PID Controller
- Utility components: NetworkTables
- Simplified robot creation with `SimpliPyRobot(config)` factory
- Configuration-based setup system
- Enhanced error handling and logging
- Comprehensive documentation and examples

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- N/A (initial release)

[1.0.0]: https://github.com/yourusername/pre-season-2026/releases/tag/v1.0.0

