Q: What is from_attributes = True in Pydantic and why do we need it?
A: By default, Pydantic only knows how to read data from dictionaries. When FastAPI returns a SQLAlchemy object, Pydantic needs to read object attributes instead of dict keys. from_attributes = True tells Pydantic to also look at object attributes.

Q: When do I need it?
A: Depends on what your route returns:
python# ❌ does NOT need from_attributes — returning a plain dict
@app.post('/login', response_model=UserLoginResponse)
def login(user: UserLogin):
    token = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# ✅ NEEDS from_attributes — returning a SQLAlchemy object
@app.post('/register', response_model=RegisterUserResponse)
def register(user: RegisterUserRequest, db: Session = Depends(get_db)):
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user  # ← SQLAlchemy object

Q: Where does it go?
python# ❌ Without — Pydantic can only read dicts
class RegisterUserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

# ✅ With — Pydantic can read both dicts AND SQLAlchemy objects
class RegisterUserResponse(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool

    class Config:
        from_attributes = True

Q: What happens if I forget it?
python# FastAPI throws this error:
fastapi.exceptions.ResponseValidationError:
    Input should be a valid dictionary or object to extract fields from


<!-- Crypt context -->

CryptContext is a class provided by the Passlib library that manages the secure hashing and verification of passwords in Python applications.

It acts as a centralized configuration layer, allowing you to define which hashing algorithms (like bcrypt or argon2) your application supports, automatically handles cryptographic salts, and enables seamless password migrations.