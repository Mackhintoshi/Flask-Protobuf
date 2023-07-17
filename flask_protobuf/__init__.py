from .extension import FlaskProtobuf

__version__ = "0.1.0"

def flask_protobuf(app, **kwargs):
    return FlaskProtobuf(app, **kwargs)
