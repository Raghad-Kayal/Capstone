## Full Stack Capstone Backend

## Project description 

Many hospitals and medical centers still depend on the manual hospital management system. Medical management system methods continued to cause many setbacks and problems for medical practitioners, patients, nurses, and other personnel in both government and private hospitals. from this problem, we came up with this app which is a database that arranges doctors, patients, and their appointments.

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/starter` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.


##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. `/models.py` file has the database.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.


## Running the server

From within the `starter` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

Setting the `FLASK_APP` variable to `app` directs flask to use the `app.py` file to find the application. 

## Running the API
API endpoints can be accessed via : 

Auth0 information for endpoints that require authentication can be found in setup.sh.

## Running tests
To run the unittests, first CD into the starter folder and run the following command:

```bash
python -m test_app
```

## Setup Auth0


1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
`delete:doctor, post:doctor, delete:patient,  get:doctors, get:patient, patch:doctor, patch:patient, post:patient`

6. Create new roles for:
    1- Receptionist
        -Can view doctors and patient
        its permissions are (`get:doctors,  get:patient`)

    2- Nurse
        -All permissions a Receptionist has and…
        -Add or delete a patient from the database
        -Modify patient or doctors
        its permissions are (`delete:patient,  get:doctors, get:patient, patch:doctor, patch:patient, post:patient`)

    3- Executive Manager
        -All permissions a Nurse has and…
        -Add or delete a doctors from the database 
        its permissions are (`delete:doctor, post:doctor, delete:patient,  get:doctors, get:patient, patch:doctor, patch:patient, post:patient`)

7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 3 users - assign the Receptionist role to one, Nurse role, and Executive Manager role to the other.
    - Sign into each account and make note of the JWT.
    - run each endpoint and correct anr errors.


## API Endpoints Documintation
``` GET '/doctors' ``` 

- Fetches a list of doctors in which the keys are the id, deparment, level, name.
- Request Arguments: None
- Returns: list of available doctors with thier id, name, deparment where they work, and level of the degree.

```bash
{
    "doctors": [
        {
            "deparment": "Pulmonary",
            "id": 2,
            "level": "Consultant",
            "name": "Dr. Ahmed A. Aljohaney"
        },
        {
            "deparment": "Cardiac Surgery",
            "id": 3,
            "level": "Senior Registrar",
            "name": "Dr. Ahmed A. Bajaber"
        },
        {
            "deparment": "OB,Gyne",
            "id": 1,
            "level": "Senior Registrar",
            "name": "Dr.Dina M. Fetyani"
        }
    ],
    "success": true
}
```

``` GET '/patient' ``` 

- Fetches a list of patints in which the keys are the name, id, age, doctor_id, date_of_appointment, gender.
- Request Arguments: None
- Returns: list of patients with thier id, name, gender, age, id of the doctor they had an appointment with, and the appointment date.

```bash
{
    "patients": [
        {
            "age": 23,
            "date_of_appointment": "Sun, 08 Nov 2020 00:00:00 GMT",
            "doctor_id": 2,
            "gender": "female",
            "id": 2,
            "name": "raghad"
        },
        {
            "age": 40,
            "date_of_appointment": "Wed, 13 Jan 2021 00:00:00 GMT",
            "doctor_id": 3,
            "gender": "female",
            "id": 4,
            "name": "mama"
        },
        {
            "age": 23,
            "date_of_appointment": "Wed, 13 Jan 2021 00:00:00 GMT",
            "doctor_id": 3,
            "gender": "female",
            "id": 5,
            "name": "raghad"
        }
    ],
    "success": true
}
```

``` POST '/doctors' ``` 

- Add a new doctor
- Request body: name, deparment, and level.
- Returns: true if successfully created, and the created doctor.

```bash
{
    "doctor": {
        "deparment": "OB/Gyne",
        "id": 7,
        "level": "Senior Registrar",
        "name": "Dr. Dina M. Fetyani"
    },
    "success": true
}
```

``` POST '/patient' ``` 

- Add a new patient
- Request body: name, age, gender, doctor_id, and date_of_appointment.
- Returns: true if successfully created, and the created patient.

```bash
{
    "patient": {
        "age": 23,
        "date_of_appointment": "Wed, 13 Jan 2021 00:00:00 GMT",
        "doctor_id": 3,
        "gender": "female",
        "id": 7,
        "name": "raghad"
    },
    "success": true
}
```

``` DELETE '/doctors/<int:id>' ``` 
- Delete a doctor from the database.
- Request Arguments: doctor Id
- Returns: true if successfully deleted, and the deleted doctor id.

```bash
{
    "Deleted doctor": 6,
    "success": true
}

```

``` DELETE '/patient/<int:id>' ``` 
- Delete a patient from the database.
- Request Arguments: patient Id
- Returns: true if successfully deleted, and the deleted patient id.

```bash
{
    "Deleted patient": 2,
    "success": true
}

```

``` PATCH '/doctors/<int:id>' ``` 

- Update a doctor
- Request body: name, deparment, and level.
- Returns: true if successfully patched, and the patched doctor.

```bash
{
    "doctor": {
        "deparment": "OB/Gyne",
        "id": 7,
        "level": "Senior Registrar",
        "name": "Dr. Dina M. Fetyani"
    },
    "success": true
}
```


``` PATCH '/patient/<int:id>' ``` 

- Update a patient
- Request body: name, age, gender, doctor_id, and date_of_appointment.
- Returns: true if successfully patched, and the patched patient.

```bash
{
    "patient": {
        "age": 23,
        "date_of_appointment": "Wed, 13 Jan 2021 00:00:00 GMT",
        "doctor_id": 3,
        "gender": "female",
        "id": 7,
        "name": "raghad"
    },
    "success": true
}
```

## Testing
To run the tests, run
```
python test_app.py
```
