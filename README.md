# Timeapp

Run tests: `make testlocal`

Run develop docker: `make rundocker`

## Develop

**All actions do in root project directory!**

### Common

- Create `dev_user_list.json` file:

    ```json
    {
        "aboba_token": {
            "token": "aboba_token",
            "id": "aboba_id",
            "name": "aboba_name",
            "email": "aboba@mail.ru"
        }
    }
    ```

- Get `firebase_secret.json` file and put in directory

- See further steps below based on the task!

---

### Python setup locally

First run:

```bash
make mongotestcontainer # Create mongo container
make envbuild # Create venv
*Create local.env file*
make run # Run app
```

After:

```bash
source venv/bin/activate # Go to venv
make mongotest
make envupdate # Update venv
make run # Run app
```

Create `local.env` file:

```ini
# Env
ENV=LOCAL

# Application
DEBUG=true
APP_HOST=127.0.0.1
APP_PORT=8000
APP_ENV=DEV
FIREBASE_SECRET_PATH=firebase_secret.json
DEV_USERS_JSON_PATH=dev_user_list.json

MONGODB_HOST=127.0.0.1
MONGODB_PORT=27017
MONGODB_DATABASE=timeappdb
MONGODB_COLLECTION_USER=User
MONGODB_COLLECTION_CATEGORY=Category
MONGODB_COLLECTION_INTERVAL=Interval
MONGODB_COLLECTION_TIMEDAY=TimeDay
MONGODB_COLLECTION_TIMEALL=TimeAll
# MONGODB_USERNAME=*ChangeMe*
# MONGODB_PASSWORD=*ChangeMe*
```

---

### Docker setup locally

Run:

```bash
*Create .env file*
make rundocker # Build container and run
```

Create `.env` file:

```ini
ENV=DOCKER

DEBUG=true
MONGODB_COLLECTION_USER=User
MONGODB_COLLECTION_CATEGORY=Category
MONGODB_COLLECTION_INTERVAL=Interval
MONGODB_COLLECTION_TIMEDAY=TimeDay
MONGODB_COLLECTION_TIMEALL=TimeAll

MONGO_INITDB_ROOT_USERNAME=*ChangeMe*
MONGO_INITDB_ROOT_PASSWORD=*ChangeMe*

MONGODB_USERNAME=*ChangeMe*
MONGODB_PASSWORD=*ChangeMe*
MONGODB_DATABASE=*ChangeMe*

MONGODB_HOST=0.0.0.0
MONGODB_PORT=27017

APP_HOST=0.0.0.0
APP_PORT=8000
APP_ENV=DEV
FIREBASE_SECRET_PATH=firebase_secret.json
DEV_USERS_JSON_PATH=dev_user_list.json
```
