# Contributing to simplipy

Thank you for your interest in contributing to simplipy! This document provides guidelines and instructions for contributing.

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a branch for your changes
4. Make your changes
5. Test your changes
6. Submit a pull request

## Code Style

- Follow PEP 8 Python style guide
- Use meaningful variable and function names
- Add docstrings to all classes and functions
- Keep functions focused and small
- Add error handling and logging

## Component Guidelines

### Creating New Components

1. Create component file in `simplipy/components/`
2. Include configuration class (e.g., `ComponentConfig`)
3. Include main component class
4. Add error handling and validation
5. Add logging with `SimpliPyLogger`
6. Export in `simplipy/components/__init__.py`
7. Update `simplipy/__init__.py` if needed
8. Add examples if applicable

### WIP Components

Components marked as WIP are experimental. They should:
- Have clear WIP warnings in docstrings
- Include basic functionality
- Be clearly documented as incomplete

## Testing

- Test on robot hardware when possible
- Verify error handling works
- Check that examples still work
- Ensure imports are correct

## Pull Request Process

1. Update documentation if needed
2. Update examples if API changes
3. Ensure all checks pass
4. Write clear commit messages
5. Reference any related issues

## Questions?

Open an issue for questions or discussions about contributions.

