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

🔐 Environment Variables

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