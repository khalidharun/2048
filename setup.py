from setuptools import setup, find_packages

setup(
    name="2048",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pygame==2.5.2",
        "pytest==7.4.2",
    ],
)
