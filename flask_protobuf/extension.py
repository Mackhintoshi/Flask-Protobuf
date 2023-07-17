import json
from flask import Flask, request,jsonify
from functools import wraps
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message


class FlaskProtobuf:
    def __init__(self, app=None,**kwargs):
        if app is not None:
            self.init_app(app)
            '''
            by default, protobuf message as read as protobuf message and you can use the protobuf schema to access the data within the method you used the decorator
            if you want to parse the protobuf to a dict, pass parse_dict=True to the decorator
            '''
            self.parse_to_dict = kwargs.get('parse_dict',False) 
            self.strict_message_validation = kwargs.get('strict_message_validation',False)
        else:
            #Raise error
            raise Exception("Flask app not found. Please pass a Flask app to the constructor")

    def init_app(self, app):
        pass  # No need to register extension globally

    def __parse_protobuf_to_dict(self,message):
        return MessageToDict(message)
    
    def __create_protobuf_guide(self,message):
        '''
        The function returns a message that the message received was not expected.
        Also returns all the fields in the message and their types
        '''
        response_message= {
            "message":"The message received was not the expected message in the protobuf decorator",
            "expxected_message":message.DESCRIPTOR.name,
            "fields":{}
        }
        #iterate through the fields in the message
        for field in message.DESCRIPTOR.fields:
            #return the name of the field and the type name
            response_message["fields"][field.name] = self.__field_type_to_string(field.type)
            
        return response_message

    def __is_message_valid(self,message):
        '''
        checks if the message received is the expected message.
        If the parsing from binary fails, the message becomes empty, which we can use to check if the message is valid
        NOTE: This does not fully validate the content of the message just yet. And is not a replacement for a full validation
        this is an experimental feature and by default is turned off. To turn it on, pass strict_message_validation=True to the decorator
        Turning this on enables this behavior for now:
        1. If the message expected is a repeated field, and the length of the field is 0, the message is considered invalid
        '''
        try:
            for field in message.DESCRIPTOR.fields:
                f = message.DESCRIPTOR.fields_by_name[field.name]
                v = getattr(message, f.name)
                #if the type is a repeated field, check if the length is greater than 0
                if f.label == f.LABEL_REPEATED:
                    if len(v) == 0 and message.ByteSize() > 0: 
                        '''
                        the bytesize is chcked, because an indication that the message is invalid is when a bytesize is not 0, but the conversion is 0.
                        '''
                        return False

        except Exception as e:
            return False
        return True

    def __field_type_to_string(self,field_type):
        type_mapping = {
            1: 'TYPE_DOUBLE',
            2: 'TYPE_FLOAT',
            5: 'TYPE_INT32',
            3: 'TYPE_INT64',
            13: 'TYPE_UINT32',
            4: 'TYPE_UINT64',
            8: 'TYPE_BOOL',
            9: 'TYPE_STRING',
            14: 'TYPE_ENUM',
            11: 'TYPE_MESSAGE',
        }
        return type_mapping.get(field_type, f'Unknown Type ({field_type})')

    def __call__(self, requestMessage=None,**decor_kwargs):
        def decorator(view_func):
            @wraps(view_func)
            def decorated_view(*args, **kwargs):
                # Customizations using the 'param' before the request
                #check if the request is a protobuf message before anything else
                instance_parse_to_dict = decor_kwargs.get('parse_dict',None)
                instance_strict_message_validation = decor_kwargs.get('strict_message_validation',None)
                exception_message = None
                d = requestMessage()
                if requestMessage==None:
                    raise Exception("No protobuf message passed to decorator")
                try:
                    '''
                    enforces a default behavior of returning a 500 error if the message received is not a protobuf message
                    '''
                    d.ParseFromString(request.data)
                    if((self.strict_message_validation or instance_strict_message_validation) and instance_strict_message_validation != False):
                        #when the global values are set to true, the decorator will check if the message received is the expected message
                        #the behavior can be overriden by passing strict_message_validation=False to the decorator
                        #when the global is set to False, the behavior can be overriden by passing strict_message_validation=True to the decorator
                        if(self.__is_message_valid(d) == False):
                            exception_message = self.__create_protobuf_guide(d)

                except:
                    exception_message = self.__create_protobuf_guide(d)
        
                if((self.parse_to_dict or instance_parse_to_dict) and instance_parse_to_dict != False):
                    #some users might want to parse the protobuf to a dict, so they can use the data outside the protobuf schema
                    #the behavior can be overriden by passing instance_parse_to_dict=False to the decorator
                    #when the global is set to False, the behavior can be overriden by passing instance_parse_to_dict=True to the decorator
                    request.data = self.__parse_protobuf_to_dict(d)
                # Call the original view function

                #if there was an exception, return the guide to the user
                if(exception_message):
                    return jsonify(exception_message),500

                response = view_func(*args, **kwargs)
                
                return response
               

            return decorated_view

        return decorator

