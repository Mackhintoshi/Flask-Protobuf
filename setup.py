from setuptools import setup

setup(
    name='flask_protobuf',
    license='MIT',
    version='0.1.3',
    description='Flask-Protobuf is a Python package that provides integration between Flask and Protocol Buffers (protobuf). It allows you to easily handle incoming protobuf messages in your Flask application.',
    author='Jerick Gutierrez',
    packages=['flask_protobuf'],
    url='https://github.com/Mackhintoshi/Flask-Protobuf',
    keywords=['flask', 'protobuf', 'google', 'protocol buffers'],
    readme='README.md',
    install_requires=[
        'Flask>=2.3.2',
        'protobuf>=4.23.4'
    ],
)
