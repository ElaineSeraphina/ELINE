from setuptools import setup, find_packages

setup(
    name="websocket_app",
    version="1.0",
    packages=find_packages(where='src'),
    install_requires=[
        "websockets",
        "fake_useragent",
        "loguru",
        "argparse",
    ],
    entry_points={
        'console_scripts': [
            'websocket-app = src.main:main',
        ],
    },
)