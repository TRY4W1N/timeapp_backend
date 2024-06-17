# Timeapp

## Develop

Env file:

```ini
DEBUG=true
MONGODB_COLLECTION_USER=User
MONGODB_COLLECTION_CATEGORY=Category
MONGODB_COLLECTION_INTERVAL=Interval
MONGODB_COLLECTION_TIMEDAY=TimeDay
MONGODB_COLLECTION_TIMEALL=TimeAll
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
