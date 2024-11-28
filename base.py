from sqlmodel import SQLModel, Field, create_engine, Session

class Product(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str
    price: str

DATABASE_URL = "sqlite:///./products.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session