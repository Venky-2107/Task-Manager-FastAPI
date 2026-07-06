from database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import Optional

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
    
    
class Task(Base):
    __tablename__ = 'tasks'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    status: Mapped[str] = mapped_column(default='todo')
    priority: Mapped[str] = mapped_column(default='medium')
    due_date: Mapped[Optional[str]] = mapped_column(nullable=True)
    
    # foreign key-> mapping to each user
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

