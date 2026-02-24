### Create new migrations
```bash
python manage.py makemigrations
```

### Apply migrations
```bash
python manage.py migrate
```

### Create a superuser
```bash
python manage.py createsuperuser
```

### Running the Application
```bash
uvicorn core.asgi:application --reload
```