# ride_app

## create virtual environment
```sh
python -m venv venv
```

## activate virtual environment
```sh
 ./venv/bin/activate
```

## install dependencies
```sh
pip install -U pip setuptools wheel
pip install -r requirements.txt
```

## run application
```sh
uvicorn app.main:create_app --factory --host=0.0.0.0 --port=8000 --reload
OR
uvicorn app.main:create_app --factory --reload
```

## run tests
```sh
pytest
```

## Open Swagger UI:

http://127.0.0.1:8000/docs


# Environment Variables

The app uses environment variables for JWT configuration.
All variables are optional and have safe development defaults.

SECRET_KEY
Used for signing JWT tokens.

Default (dev):
SECRET_KEY="dev-secret-key-change-me"


For production:
export SECRET_KEY="your-secure-random-key"

ALGORITHM
HS256

ACCESS_TOKEN_EXPIRE_MINUTES
60


# Seeding & Database Management

## Reset the database
Completely remove all tables and recreate an empty schema:

```sh
python seed_data.py --reset
```

Use this when you want to start with a fully clean database.

## Seed default demo data

Creates:
- the fixed user vadim / 123456
- several demo rides
- several demo participation records

```sh
python seed_data.py
```
The script is idempotent — it will not create duplicate records.

## Seed large amounts of random data

Creates:
- the fixed user vadim / 123456
- random users
- random rides
- random participation entries

```sh
python seed_data.py --massive
```

## Seed with custom data volumes

You can specify how many users, rides, and participations to generate:
```sh
python seed_data.py --massive --users=50 --rides=100 --participations=500
```

This will generate:
- 50 random users
- 100 rides
- 500 participation records
- Plus the fixed user vadim / 123456.