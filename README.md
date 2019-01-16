# Flask-REST-API
REST API using Python and Flask Framework

## The built-in user dataset looks like the following:
```python
users = [
    {
        "name": "Jade",
        "age": 42,
        "occupation": "Network Engineer"
    },
    {
        "name": "Josh",
        "age": 21,
        "occupation": "Sales Manager"
    },
    {
        "name": "Agata",
        "age": 25,
        "occupation": "CEO"
    }
]
```


## How to use the app:

### Install and activate the virtual environment with Python 3(tested on Fedora 29 only):
```
virtualenv venv --python=`which python3`
source venv/bin/activate
```

### Install dependencies:
```pip install -r requirements.txt```

### Run the application
```python app.py```
Check what the adress is like, for example, 127.0.0.1:5000

### When you are done with requests below, deactivate the environment:
```deactivate```

## Use cURL to send HTTTP requests(your address may be different):
```curl --request GET http://127.0.0.1:5000/user/Jade```

```curl --request POST http://127.0.0.1:5000/user/Jade```

```curl --request POST http://127.0.0.1:5000/user/Janny?age=19&occupation=Student```

```curl --request POST http://127.0.0.1:5000/user/Janny?age=19&occupation=Developer```

```curl --request DELETE http://127.0.0.1:5000/user/Janny```
