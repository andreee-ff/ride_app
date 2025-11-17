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
```

## run tests
```sh
pytest
```
