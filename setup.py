"""
Setup script for simplipy - Simplified Python Library for FRC
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="simplipy",
    version="1.0.0",
    description="simplipy - Simplified Python Library for FRC robot programming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Pre-Season 2026",
    url="https://github.com/yourusername/pre-season-2026",
    packages=find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Topic :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="frc robotics wpilib robotpy first",
    install_requires=[
        # Note: WPILib dependencies are typically installed via WPILib installer
        # These are listed for reference
    ],
    extras_require={
        "dev": [
            "flake8",
            "pylint",
            "mypy",
            "black",
            "bandit",
        ],
    },
)

