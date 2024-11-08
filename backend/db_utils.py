from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_session():  # nova abordagem para conexão com BD através do SQLAlchemy
    db = 'postgresql://postgres:123456@localhost/db-gf'
    engine = create_engine(db)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
