SELECT 'CREATE DATABASE prediction_core'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'prediction-core')\gexec