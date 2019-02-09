# REST API with Flask

REST API using Python, Flask Framework and PostgreSQL 11 on Windows 10

SQLAlchemy is used as ORM

Three modes: Production, Development, Testing

# Entity diagram:
![Entities](https://gist.github.com/MiddleZwei/1525d33d3b9a0dc48503300b07dd82fc/raw/71bca97bc7d4297de8e920354cfc80e2ee568dee/entity_diagram.png)

# How to use the app:

## Install and activate the virtual environment with Python 3.6:

Run the following
```
virtualenv venv --python=3.6
cd venv/Scripts
activate
```

Or, if using PyCharm, go to File > Settings > Project Interpreter > create your environment here

## Install dependencies:
```pip install -r requirements.txt```

## Set the environment variables
5432 is the default port set up bduring the PostgreSQL installation. 

It can be found and changed in the PostgreSQL/11/data/postgresql.conf

Host is most likely be localhost for you.

The secret key may be whatever you wish.

A lot of problems I had during this stage, for further solutions for your specific cases refer to the official documentation.

Windows
```
SET FLASK_ENV=development
SET DATABASE_URL=postgres://<username>:<password>@<host>:<port>/<name_of_your_database>
SET JWT_SECRET_KEY=hhgaghhgsdhdhdd
```
Linux(tested on Windows only, though)
```
export FLASK_ENV=development
export DATABASE_URL=postgres://<username>:<password>@<host>:<port>/<name_of_your_database>
export JWT_SECRET_KEY=hhgaghhgsdhdhdd
```

## Database:
Initialize, create migrations and apply
```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```
Check if everything is good:
```
psql {U- otheruser}
# \connect db_name
# \dt
```
You should see "users" and "blogposts" tables


## Run the application
```python manage.py runserver {custom port number if needed}```

The default port is 5000. Check by going to http://127.0.0.1:5000/

You should see a congratulation message

The start point of the API is http://127.0.0.1:5000/api/v1/users/

But to access it, you'll have to provide your credentials(POST request): email, password and name.

See below:

## Requests(I used Postman):
Content-Type:
``` application/json ```

### Create User 
POST http://127.0.0.1:5000/api/v1/users

Body
```
{
	"email": "email@gmail.comm",
	"password": "password123",
	"name": "Jessy Pane"
}
```

### Login User 
POST http://127.0.0.1:5000/api/v1/users/login
```
{
	"email": "email@gmail.comm",
	"password": "password123"
}
```

Keep the jwt_token, you'll need it later!

### Get A User Info 
GET http://127.0.0.1:5000/api/v1/users/<user_id>

### Get All users 
GET http://127.0.0.1:5000/api/v1/users

### Get My Info
GET http://127.0.0.1:5000/api/v1/users/me

In the request header put the token you saved as ```api-token```

### Edit My Info
PUT http://127.0.0.1:5000/api/v1/users/me

In the request header put the token you saved as ```api-token```

Body: 
```
{        
    "name": "updated name"
}
```

### DELETE My Account
DELETE http://127.0.0.1:5000/api/v1/users/me

In the request header put the token you saved as ```api-token```

<hr>

### Create Blogpost 
POST http://127.0.0.1:5000/api/v1/blogposts

In the request header put the token you saved as ```api-token```

Body
```
{
	"title": "test",
	"contents": "test"
}
```

### Get all Blogposts
GET http://127.0.0.1:5000/api/v1/blogposts


### Get a Blogpost by id
GET http://127.0.0.1:5000/api/v1/blogposts/<blogpost_id>

### Update Blogpost
PUT http://127.0.0.1:5000/api/v1/blogposts/1

In the request header put the token you saved as ```api-token```

Body
```
{
	"title": "updated",
	"contents": "updated"
}
```

### Delete Blogpost
PUT http://127.0.0.1:5000/api/v1/blogposts/1

In the request header put the token you saved as ```api-token```


## In order to deactivate the virtual environment, just type this in:
```deactivate```
