from sqlmodel import SQLModel, Field, create_engine
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str

connection_string = os.getenv("DATABASE_URL")
engine = create_engine(connection_string)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == "__main__":
    create_db_and_tables()