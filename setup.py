#!/usr/bin/env python
"""Setuptools script"""

from setuptools import find_packages, setup

setup(
    name="check_aruba_ap",
    version="1.0",
    description="A set Icinga check plugin to check Aruba APs status via SNMP",
    classifiers=[
        "Programming Language :: Python",
    ],
    install_requires="easysnmp",
    author="Benjamin Renard",
    author_email="brenard@easter-eggs.com",
    url="https://github.com/brenard/check_aruba_ap",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "console_scripts": [
            "check_aruba_aps = check_aruba_ap.scripts.check_aruba_aps:main",
            "check_aruba_ap = check_aruba_ap.scripts.check_aruba_ap:main",
        ],
    },
)
