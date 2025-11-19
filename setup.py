"""
Setup script for simplipy - Simplified Python Library for FRC
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read version from simplipy package
version_file = Path(__file__).parent / "simplipy" / "__init__.py"
version = "1.0.0"
if version_file.exists():
    for line in version_file.read_text(encoding="utf-8").splitlines():
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

setup(
    name="simplipy",
    version=version,
    description="simplipy - Simplified Python Library for FRC robot programming",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Pre-Season 2026",
    url="https://github.com/kura120/simplify",
    project_urls={
        "Bug Reports": "https://github.com/kura120/simplify/issues",
        "Source": "https://github.com/kura120/simplify",
        "Documentation": "https://github.com/kura120/simplify#readme",
    },
    packages=find_packages(exclude=["examples", "tests", "*.tests", "*.tests.*", "tests.*"]),
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
        # Note: WPILib dependencies (wpilib, phoenix5, rev, ntcore) are typically
        # installed via WPILib installer and should not be listed here to avoid conflicts
    ],
    extras_require={
        "dev": [
            "flake8>=6.0.0",
            "pylint>=2.15.0",
            "mypy>=1.0.0",
            "black>=23.0.0",
            "bandit>=1.7.0",
            "safety>=2.3.0",
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)

