## Healthcare Apointment System (HAS) Backend

## How to setup the backend

Must have:

- Python3.12 (incase you have python < 3.12, use (<https://webinstall.dev/pyenv/>))
- Postgresql
-

```bash
python -V # must return >=3.12
# setup the virtualenv and install dependecies
virtualenv .venv

source .venv/bin/activate # linux

pip install -r requirements.txt

cp .env.example .env # create a copy of .env variables

python manage.py makemigrations # create and track all migrations

python manage.py migrate # apply migrations to DB

python manage.py createsuperuser #superadmin

python manage.py runserver

gunicorn has.wsgi # with gunicorn

python manage.py flush # reset the db
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

For swagger UI head over to: <http://127.0.0.1:8000/api/schema/swagger-ui/>
