from fastapi import Depends, HTTPException, APIRouter, WebSocket
from schemas import CreateTaskRequest, CreateTaskResponse 
from sqlalchemy.orm import Session
from database import get_db
from oauth2 import get_current_user
from models import Task, User
from websocket_manager import manager
from auth import decode_access_token
import json

task_router = APIRouter(prefix='/tasks', tags=["tasks"])

@task_router.websocket("/ws")
async def websocket_connection(websocket: WebSocket, token:str):
    token_retrieved = decode_access_token(token)
    
    if token_retrieved is None:
        await websocket.close(code=1008)
    else:
        await manager.connect(websocket)
        try: 
            while True:
                # keeps connection alive
                data = await websocket.receive_text() 
        except: 
            manager.disconnect(websocket)
    

# create tasks
@task_router.post('/', status_code=201, response_model=CreateTaskResponse)
async def create_task(task: CreateTaskRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    # since we stored the email as sub in auth.py
    user_email = current_user['sub']
    
    # find the user using email
    user = db.query(User).filter(User.email == user_email).first()
    
    # check for user
    if not user:
        raise HTTPException(status_code=404, detail='user not found!!')
    
    # creating new task instance
    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        due_date=task.due_date,
        user_id=user.id
    )
    
    db.add(new_task)
    db.commit()
    await manager.broadcast(json.dumps({"event": "task_created"}))
    db.refresh(new_task)
    
    return new_task

# get all tasks
@task_router.get('/', status_code=200, response_model=list[CreateTaskResponse])
def get_all_tasks(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    user_email = current_user['sub']
    user = db.query(User).filter(User.email == user_email).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # find tasks only for the current_user
    tasks = db.query(Task).filter(Task.user_id == user.id).all()
    
    return tasks

# get task by task id
@task_router.get('/{task_id}', status_code=200, response_model=CreateTaskResponse)
def get_task_by_id(task_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)): 
    is_task = db.query(Task).filter(Task.id == task_id).first()
    
    if not is_task:
        raise HTTPException(status_code=404, detail="Task with id not found")
    
    return is_task

# update task by id
@task_router.put('/{task_id}', status_code=200, response_model=CreateTaskResponse)
async def update_task(task_id: int, task: CreateTaskRequest, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    is_task = db.query(Task).filter(Task.id == task_id).first()
    
    if not is_task:
        raise HTTPException(status_code=404, detail="Task with id not found")
    
    is_task.title = task.title
    is_task.description = task.description
    is_task.status = task.status or is_task.status
    is_task.priority = task.priority or is_task.priority
    is_task.due_date = task.due_date
    
    db.commit()
    await manager.broadcast(json.dumps({"event": "task_updated"}))
    db.refresh(is_task)
    
    return is_task

# delete task
@task_router.delete('/{task_id}', status_code=200)
async def delete_task(task_id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    is_task = db.query(Task).filter(Task.id == task_id).first()
    
    if not is_task:
        raise HTTPException(status_code=404, detail="Task with id not found")
    
    db.delete(is_task)    
    db.commit()
    await manager.broadcast(json.dumps({"event": "task_deleted"}))
    
    return {"message": "task deleted!!!"}


