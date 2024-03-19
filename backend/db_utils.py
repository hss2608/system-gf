# import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_session():  # nova abordagem para conexão com BD através do SQLAlchemy
    db = 'postgresql://postgres:123456@localhost/db-gf'
    engine = create_engine(db)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


# funçao antiga para conectar com o banco de dados usando psycopg2
"""def create_connection():
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
"""