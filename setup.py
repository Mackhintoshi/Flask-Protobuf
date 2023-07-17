from setuptools import setup

setup(
    name='flask_protobuf',
    version='0.1.0',
    packages=['flask_protobuf'],
    install_requires=[
        'Flask>=2.3.2',
        'protobuf>=4.23.4'
    ],
)
