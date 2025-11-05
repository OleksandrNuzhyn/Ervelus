### Apply migrations
```bash
python manage.py migrate
```

### Create a superuser
```bash
python manage.py createsuperuser
```
    
### Create new migrations
```bash
python manage.py makemigrations
```

### Running the Application
```bash
uvicorn core.asgi:application --reload
```