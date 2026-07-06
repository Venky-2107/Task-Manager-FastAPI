from pydantic import BaseModel, ConfigDict
from typing import Optional

# user registration fields
class RegisterUserRequest(BaseModel):
    name: str
    email: str
    password: str
    
# user registration response
class RegisterUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
     
    id: int
    name: str
    email: str
    is_active: bool
    
    # class Config:
    #     from_attributes = True
        
        
# Update user request
class UpdateUserRequest(BaseModel):
    name: str
    email:str
    
# user login fields
class UserLogin(BaseModel):
    email: str
    password: str
    
# user login response
class UserLoginResponse(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
    
# create task request fields
class CreateTaskRequest(BaseModel):
    title: str
    description: str
    status: Optional[str] = 'todo'
    priority: Optional[str] = 'medium'
    due_date: Optional[str] = None
    
# task creation response
class CreateTaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes = True)
    
    id: int
    title: str
    description: str
    status: str
    priority: str
    user_id: int
    due_date: Optional[str] = None
    
    # class Config:
    #     from_attributes = True