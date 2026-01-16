from fastapi import FastAPI, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import os

from database import Base, engine, SessionLocal
from models import User, Task
from schemas import *
from auth import *

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
        user = db.query(User).filter(User.id == int(payload["sub"])).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except JWTError as e:
        print(f"JWT Error: {e}")
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(f"Auth Error: {e}")
        raise HTTPException(status_code=401, detail=str(e))

@app.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    return {"message": "User created"}

@app.post("/login", response_model=Token)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=401)

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}

@app.post("/tasks")
def create_task(task: TaskCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    new_task = Task(title=task.title, owner_id=user.id)
    db.add(new_task)
    db.commit()
    return new_task

@app.get("/tasks", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return db.query(Task).filter(Task.owner_id == user.id).all()

@app.put("/tasks/{task_id}")
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404)

    task.title = data.title
    task.completed = data.completed
    db.commit()
    return task

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404)

    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

@app.get("/")
def read_root():
    return FileResponse("index.html")
