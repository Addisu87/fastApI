from sqlmodel import SQLModel, create_engine


# Create an Engine
sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# Create the Tables

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)