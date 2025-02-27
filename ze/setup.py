from setuptools import find_packages, setup

setup(
    name='zeconfig',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'toml',
    ],
)
