from setuptools import (
    setup,
    find_packages
)


install_requires = open('requirements.txt', 'r').read()

setup(
    name='gbank',
    version='0.1',
    author_name='',
    author_email='',
    package=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=install_requires,
    entry_points={
        'console_scripts': [
            'gbank=gbank.cli.main:main'
        ]
    }
)
