from sqlmodel import SQLModel, Field, create_engine, Session, select
from typing import Optional
import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends
from pydantic import BaseModel

load_dotenv()

class Todo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str

class TodoAdd(SQLModel):
    name: str
    description: str

class TodoResponse(BaseModel):  # Define Pydantic model for response
    id: int
    name: str
    description: str

connection_string = os.getenv("DATABASE_URL")
engine = create_engine(connection_string)

def get_data():
    with Session(engine) as session:
        yield session

app = FastAPI(
    title="Todo API", description="My todo app", version="0.1.0"
)

@app.get("/")  # Use @app.get for defining route handlers
def list_todos(session: Session = Depends(get_data)):  # Remove Annotated and Annotated[...] in Depends
    todos = session.exec(select(Todo)).all()
    return todos

@app.post("/add_todo", response_model=TodoResponse)  # Use @app.post for defining POST route
def add(todo: TodoAdd, session: Session = Depends(get_data)):  # Remove Annotated[...] in Depends
    todo_add = Todo.from_orm(todo)  # Create SQLModel object from TodoAdd
    session.add(todo_add)
    session.commit()
    session.refresh(todo_add)
    return todo_add

@app.delete("/delete_todo/{id}")  # Use @app.delete for defining DELETE route
def delete(id: int, session: Session = Depends(get_data)):  # Remove Annotated[...] in Depends
    todo = session.get(Todo, id)
    if todo:
        session.delete(todo)
        session.commit()
        return {"message": "Todo deleted successfully"}
    else:
        return {"message": "Todo not found"}
    
@app.put("/update_todo/{id}")  # Use @app.put for defining PUT route
def update(id: int, todo: TodoAdd, session: Session = Depends(get_data)):  # Remove Annotated[...] in Depends
    todo_update = session.get(Todo, id)
    if todo_update:
        todo_update.name = todo.name
        todo_update.description = todo.description
        session.commit()
        session.refresh(todo_update)
        return todo_update
    else:
        return {"message": "Todo not found"}