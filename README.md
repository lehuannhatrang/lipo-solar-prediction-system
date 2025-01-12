# Lipo Solar Prediction System

## Start to deploy:
```
docker-compose build
docker-compose up -d  
```

## Development
### Start DB and Redis

```
docker compose up db -d
docker compose up redis -d
```

### Start Backend
```
cd backend
flask --app .\src\app.py run --reloadry_init.py
```
### Start Celery worker
On Windows, install eventlet first
```
pip install eventlet
```

Start celery worker

```
cd backend/src
celery -A celery_init worker --loglevel=INFO -P eventlet
```

Open a terminal and start celery beat
```
cd backend/src
celery -A celery_init beat --loglevel INFO
```

### Start Frontend
```
cd frontend
streamlit run .\Homepage.py
```