from fastapi import Depends, HTTPException, APIRouter
from schemas import RegisterUserResponse, RegisterUserRequest, UpdateUserRequest
from sqlalchemy.orm import Session
from database import get_db
from oauth2 import get_current_user
from models import User

# creating instance of API router
user_router = APIRouter(prefix='/users', tags=["users"])

# helper function to check if user exist by id
def check_user_exists(id: int, db):
    return db.query(User).filter(User.id == id).first()
    

# get all users
@user_router.get('/', response_model=list[RegisterUserResponse], status_code=200)
def get_all_users(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # fetch all users
    users = db.query(User).all()
    return users

# get user by id
@user_router.get('/{user_id}', response_model=RegisterUserResponse, status_code=200)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # fetch user by id
    user = check_user_exists(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail='User not available by this id')
    return user

# udpate user details
@user_router.put('/update/{user_id}', response_model=RegisterUserResponse, status_code=200)
def update_user(user_id: int, new_data: UpdateUserRequest, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user_exist = check_user_exists(user_id, db)
    if not user_exist:
        raise HTTPException(status_code=404, detail='User not available by this id')
    
    # update the user details if exists
    user_exist.name = new_data.name
    user_exist.email = new_data.email
    db.commit()
    db.refresh(user_exist)
    
    return user_exist

# delete user
@user_router.delete('/delete/{user_id}', status_code=200)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    user_exist = check_user_exists(user_id, db)
    
    if not user_exist:
        raise HTTPException(status_code=404, detail='User not available by this id')
    
    db.delete(user_exist)
    db.commit()
    
    return {"message": "user deleted successfully!!"}
    

    