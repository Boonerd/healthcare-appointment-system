## Healthcare Apointment System (HAS) Backend

## How to setup the backend

Must have:

- Python3.12
- Postgresql
-

```bash
# setup the virtualenv and install dependecies
virtualenv .venv

source .venv/bin/activate # linux

pip install -r requirements.txt

python manage.py makemigrations # create and track all migrations

python manage.py migrate # apply migrations to DB

python manage.py createsuperuser #superadmin

python manage.py runserver
```

```bash
#then test the api endpoint
curl http://localhost:5000/api/test
```

Expected response:

```json
{
  "success": true,
  "message": "API is okay",
  "data": { "time": "2025-07-26T18:19:34.163671" }
}
```
