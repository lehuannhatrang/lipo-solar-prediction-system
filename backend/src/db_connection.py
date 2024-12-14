import psycopg2
from psycopg2 import pool

class DBConnection:
    _instance = None  # Singleton instance
    _connection_pool = None
    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DBConnection, cls).__new__(cls)
        return cls._instance
    
    def __init__(self, dbname, user, password, host, port):
        if not DBConnection._connection_pool:  # Initialize the connection pool only once
            try:
                DBConnection._connection_pool = pool.SimpleConnectionPool(
                    1, 20,  # Min and max connections in the pool
                    dbname=dbname,
                    user=user,
                    password=password,
                    host=host,
                    port=port
                )
                print("Connection pool created successfully")
            except (Exception, psycopg2.DatabaseError) as error:
                print(f"Error while connecting to PostgreSQL: {error}")

    def get_connection(self):
        try:
            return DBConnection._connection_pool.getconn()
        except Exception as error:
            print(f"Error getting connection: {error}")

    def release_connection(self, connection):
        try:
            DBConnection._connection_pool.putconn(connection)
        except Exception as error:
            print(f"Error releasing connection: {error}")

    def close_all_connections(self):
        if DBConnection._connection_pool:
            DBConnection._connection_pool.closeall()
            print("All connections in the pool are closed")

    # def connect():
    #     """ Connect to the PostgreSQL database server """
    #     config = {
    #         "host":  os.getenv('DB_CONNECTION_HOST', 'localhost'),
    #         "port": os.getenv('DB_CONNECTION_PORT', '32432'),
    #         "user": os.getenv('DB_USERNAME', 'postgres'),
    #         "password": os.getenv('DB_PASSWORD', 'postgres')
    #     }
    #     try:
    #         # connecting to the PostgreSQL server
    #         with psycopg2.connect(**config) as conn:
    #             print('Connected to the PostgreSQL server.')
    #             return conn
    #     except (psycopg2.DatabaseError, Exception) as error:
    #         print(error)
