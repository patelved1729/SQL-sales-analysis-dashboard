#!/usr/bin/env python
"""Setup script for SQL Sales Analysis"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sql-sales-analysis-dashboard",
    version="1.0.0",
    author="Your Name",
    description="SQL-based sales analysis using SQLite, Pandas, and Matplotlib",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/patelved1729/SQL-sales-analysis-dashboard",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas>=1.5.0",
        "numpy>=1.24.0",
        "matplotlib>=3.7.0",
        "seaborn>=0.12.0",
        "jupyter>=1.0.0",
    ],
)
