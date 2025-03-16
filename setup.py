"""Setup file for the public holiday analyzer package."""

from setuptools import find_packages, setup

setup(
    name="public_holiday_analyzer",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "python-dateutil>=2.8.2",
        "holidays>=0.38",
    ],
    python_requires=">=3.8",
) 