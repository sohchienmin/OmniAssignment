from sqlalchemy import create_engine


user = "postgres"
password = "password"
host = "host.docker.internal"
port = "5432"
database = "url_shortener"

local_database_connection_string = (
    f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
)


engine = None


def open_connection():
    global engine

    if engine is None:
        engine = create_engine(local_database_connection_string)

    connection = engine.connect()
    return connection
