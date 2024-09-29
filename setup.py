from setuptools import setup, find_packages

setup(
    name="rockbox_db_manager",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "mutagen",
    ],
    entry_points={
        'console_scripts': [
            'rockbox_db_manager=rockbox_db_manager.cli:main',
        ],
    },
)