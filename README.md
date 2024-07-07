# Timeapp

Run tests: `make testlocal`

## Develop

.env file:

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

local.env:

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

## Firebase config


firebase_secret.json:

```json
{
  "type": "service_account",
  "project_id": *ChangeMe*,
  "private_key_id": *ChangeMe*,
  "private_key": *ChangeMe*,
  "client_email": *ChangeMe*,
  "client_id": *ChangeMe*,
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": *ChangeMe*,
  "universe_domain": "googleapis.com"
}
```

firebase_secret.env:

```ini
WEB_API_KEY=*ChangeMe* 
```

---

## Develop settings json

dev_user_list.json:

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

develop.json:

```json
{
    "develop_user_list": [
        {
            "id": "aboba_id",
            "name": "aboba",
            "active": true,
            "pic": "not",
            "email": "aboba@gmail.com",
            "email_verified": true,
            "provider": {
                "type": "GOOGLE",
                "data": {}
            }
        },
        {
            "id": "amogus_id",
            "name": "amogus",
            "active": true,
            "pic": "not",
            "email": "amogus@gmail.com",
            "email_verified": true,
            "provider": {
                "type": "GOOGLE",
                "data": {}
            }
        },
        {
            "id": "shrek_id",
            "name": "shrek",
            "active": true,
            "pic": "not",
            "email": "shrek@gmail.com",
            "email_verified": true,
            "provider": {
                "type": "GOOGLE",
                "data": {}
            }
        }
    ]
}
```

---

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
