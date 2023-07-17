
# Flask-Protobuf

Flask-Protobuf is a Python package that provides integration between Flask and Protocol Buffers (protobuf). It allows you to easily handle incoming protobuf messages in your Flask application.



## Installation

Install Flask-Protobuf with pip

```bash
  pip install flask-protobuf

```
    

## Dependencies

Aside from Flask, you need to have protobuf installed.

```bash
  pip install protobuf

```
    
## Features

- #### Receive Serialized Protobuf Message

- #### Allows seemless migration from JSON to Protobuf. No need to modify your route functions.
    - If you wish to read the data as JSON without worrying about deserializing the protobuf message. This is because FlaskProtobuf handles the conversion and converts the request.data for you. You can set the parse_dict to True in 2 ways:
        - #### globally
            ```
            fb = FlaskProtobuf(app,parse_dict=True)
            ```
         - #### per decorator instance
            ```
            fb = FlaskProtobuf(app)

            @app.route('/add-branch', methods=['POST'])
            @fb(branch)
            def index():
                pass
            ```

        - #### Default:
            By default, if you do not declare the parse_dict parameter, the request.data will not be converted to dict and can be read as a protobof message. 


- #### Built in Response Messages
    - If it encounters an error parsing your protobuf message, the response can tell what is the expected protobuf message format.
    - #### Example HTTP Response for errors
        ```
        HTTP CODE: 500

        {
        "expxected_message":"Employees",
        "fields":{
            "position":"TYPE_ENUM",
            "id":"TYPE_INT32",
            "full_name":"TYPE_STRING",
            "email":"TYPE_STRING"
            }
        "message":"The message received was not the expected message in the protobuf decorator"
        }
        ```


## Usage/Examples

```python
from flask import Flask as flask,request,jsonify
from flask_protobuf import flask_protobuf as FlaskProtobuf
from Employees_pbs import Employees as employees, Branch as branch


#declare Flask app
app = flask(__name__)
#declare FlaskProtobuf
fb = FlaskProtobuf(app,parse_dict=True)



@app.route('/add-branch', methods=['POST'])
@fb(branch) #provide the message you are expecting
def index():
    print(request.data)
    branch = branch()
    b.id = 1
    b.country = "PH"
    return b.SerializeToString() #can return a protobuff message

@app.route('/employees', methods=['POST'])
@fb(employees) #provide the message you are expecting
def index():
    employees_array = request.data
    for employee in employees_array #sample protobuff REPEATED Type
        print(employee)
    
    return jsonify({"status":"SUCCESS"}) #can return other formats

```

