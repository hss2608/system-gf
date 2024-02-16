import psycopg2


def create_connection():
    db_params = {
        'host': 'localhost',
        'database': 'db-gf',
        'user': 'postgres',
        'password': '123456',
        'port': '5432',
        'client_encoding': 'utf-8',
    }

    try:
        connection = psycopg2.connect(**db_params)

        cursor = connection.cursor()
        return connection, cursor

    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        raise


def close_connection(connection, cursor):
    if cursor:
        cursor.close()
    if connection:
        connection.close()
