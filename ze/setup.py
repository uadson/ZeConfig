from setuptools import find_packages, setup

setup(
    name='ze',
    version='0.1.1',
    packages=find_packages(),
    install_requires=[
        'pyyaml',
        'toml',
    ],
)
