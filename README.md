# Flask-REST-API
REST API using Python, Flask Framework and PostgreSQL 11 on Windows 10
SQLAlchemy is used as ORM
So far only users are available. Blogposts are yet to come.

## Entity diagram:
image to be uploaded


## How to use the app:

### Install and activate the virtual environment with Python 3.6:
#### Run the following
```
virtualenv venv --python=3.6
cd venv/Scripts
activate
```
#### Or, if using PyCharm, go to File > Settings > Project Interpreter > create your environment here

### Install dependencies:
```pip install -r requirements.txt```

### Set the environment variables
5432 is the default port set up bduring the PostgreSQL installation. 

It can be found and changed in the PostgreSQL/11/data/postgresql.conf

Host is most likely be localhost for you.

The secret key may be whatever you wish.

The most problems I had during this stage, for further questions refer to the official documentation.

Windows
```
SET FLASK_ENV=development
SET DATABASE_URL=postgres://<username>:<password>@<host>:<port>/<name_of_your_database>
SET JWT_SECRET_KEY=hhgaghhgsdhdhdd
```
Linux(tested on Windows only, though)
```
export FLASK_ENV=development
export DATABASE_URL=postgres://username:password@localhost:5432/<name_of_your_database>
export JWT_SECRET_KEY=hhgaghhgsdhdhdd
```

### Database:
Initialize, create migrations and apply to the database
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


### Run the application
```python manage.py runserver {custom port number if needed}```
The default port is 5000. Check by going to http://127.0.0.1:5000/
You should see a congratulation message

The start point of the API is http://127.0.0.1:5000/api/v1/users/
But to access it, you'll have to provide your credentials(POST request): email, password and name.
See below:

## Using POSTMAN:
Content-Type:
``` application/json ```

##### Create User 
POST http://127.0.0.1:5000/api/v1/users

Body
```
{
	"email": "email@gmail.comm",
	"password": "password123",
	"name": "Jessy Pane"
}
```

##### Login User 
POST http://127.0.0.1:5000/api/v1/users/login
```
{
	"email": "email@gmail.comm",
	"password": "password123"
}
```

Keep the jwt_token, you'll need it later!

##### Get A User Info 
GET http://127.0.0.1:5000/api/v1/users/\<user_id>

##### Get All users 
GET http://127.0.0.1:5000/api/v1/users

##### Get My Info
GET http://127.0.0.1:5000/api/v1/users/me

In the request header put the token you saved as ```api-token```

##### Edit My Info
PUT http://127.0.0.1:5000/api/v1/users/me

In the request header put the token you saved as ```api-token```

Body: 
```
{        
    "name": "updated name"
}
```

##### DELETE My Account
DELETE http://127.0.0.1:5000/api/v1/users/me

In the request header put the token you saved as ```api-token```


### In order to deactivate the virtual environment, just type this in:
```deactivate```