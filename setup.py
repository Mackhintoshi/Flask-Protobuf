from setuptools import setup

setup(
    name='flask_protobuf',
    license='MIT',
    version='0.1.2',
    description='Flask-Protobuf is a Python package that provides integration between Flask and Protocol Buffers (protobuf). It allows you to easily handle incoming protobuf messages in your Flask application.',
    author='Jerick Gutierrez',
    packages=['flask_protobuf'],
    url='https://github.com/Mackhintoshi/Flask-Protobuf',
    keywords=['flask', 'protobuf', 'google', 'protocol buffers'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown', 
    install_requires=[
        'Flask>=2.3.2',
        'protobuf>=3.17.3'
    ],
)
