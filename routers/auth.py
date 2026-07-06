from fastapi import APIRouter, HTTPException, Depends
from schemas import RegisterUserRequest, RegisterUserResponse, UserLogin, UserLoginResponse
from database import get_db
from sqlalchemy.orm import Session
from models import User
from auth import hash_password, verify_password, create_access_token

auth_router = APIRouter(prefix='/auth', tags=["Auth"])

# Register User
@auth_router.post('/register', response_model=RegisterUserResponse, status_code=201)
def register_user(user: RegisterUserRequest, db: Session = Depends(get_db)):
    # check if the user exists
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    # check if user exists -> raise exception if yes
    if existing_user:
        raise HTTPException(status_code=400, detail="User email already exists")
    
    # hash the incoming password.
    password_hash = hash_password(user.password)
    
    # create new instance of the User model with incoming data
    user_to_register = User(name=user.name, email=user.email, password=password_hash)
    
    # add, commit and refresh the new user data onto the table.
    db.add(user_to_register)
    db.commit()
    db.refresh(user_to_register)
    
    # now this is the sql alchemy model and should match the response model.
    return user_to_register

# Login user
@auth_router.post('/login', response_model= UserLoginResponse, status_code=200)
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    # find if the user exists
    check_user_exists = db.query(User).filter(User.email == user.email).first()
    
    # raise exception if the user doesnot exist
    if not check_user_exists:
        raise HTTPException(status_code=400, detail='Invalid Credentials')
    
    # check if password is valid
    check_valid_password = verify_password(user.password, check_user_exists.password)
    
    # raise if invalid password
    if not check_valid_password:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    
    # if everything is fine, return the token. 
    # since the other field is already default, no need to explicitly mention here
    return {'access_token': create_access_token({"sub": check_user_exists.email})}