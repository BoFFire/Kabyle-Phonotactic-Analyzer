# setup.py

from setuptools import setup

setup(
    name="kab_phonolyzer",
    version="0.1.0",
    packages=["kab_phonolyzer"],
    install_requires=["nltk", "regex"],
    entry_points={
        "console_scripts": [
            "kab-phonolyzer=kab_phonolyzer.phono:main",
        ],
    },
)
