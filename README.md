# Timeapp

Run tests: `make testlocal`

## Develop

Env file:

```ini
DEBUG=true
MONGODB_COLLECTION_USER=User
MONGODB_COLLECTION_CATEGORY=Category
MONGODB_COLLECTION_INTERVAL=Interval
MONGODB_COLLECTION_TIMEDAY=TimeDay
MONGODB_COLLECTION_TIMEALL=TimeAll

MONGO_INITDB_ROOT_USERNAME=*ChangeMe*
MONGO_INITDB_ROOT_PASSWORD=*ChangeMe*
MONGO_INITDB_DATABASE=*ChangeMe*

MONGODB_HOST=0.0.0.0
MONGODB_PORT=27017
MONGODB_URL=mongodb://${MONGO_INITDB_ROOT_USERNAME}:${MONGO_INITDB_ROOT_PASSWORD}@${MONGODB_HOST}:${MONGODB_PORT}/${MONGO_INITDB_DATABASE}

APP_HOST=0.0.0.0
```

Run commands on start:

```bash
make mongotestcontainer # Create mongo container
make mongotest # Start exist container
make envbuild # Create venv
*Create .env file*
make run # Run app
```

If venv exist:

```bash
*In env*
make envupdate # Update venv
make run # Run app
```
