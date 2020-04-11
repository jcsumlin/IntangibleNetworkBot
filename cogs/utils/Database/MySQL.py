from sqlalchemy import create_engine

engine = None


def loadDB(user, password, hostname, dbname):
    global engine
    engine = create_engine(f'mysql://{user}:{password}@{hostname}/{dbname}')
    return engine
