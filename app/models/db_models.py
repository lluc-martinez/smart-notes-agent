from datetime import datetime, timezone
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class User(SQLModel, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    telegram_id: int = Field(unique=True, index=True)
    username: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    oauth_token: Optional["OAuthToken"] = Relationship(back_populates="user")
    messages: List["ConversationHistory"] = Relationship(back_populates="user")

class OAuthToken(SQLModel, table=True):
    __tablename__ = "oauth_tokens"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True)
    access_token: str
    refresh_token: Optional[str] = None
    expires_at: datetime
    
    user: User = Relationship(back_populates="oauth_token")

class ConversationHistory(SQLModel, table=True):
    __tablename__ = "conversation_history"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    role: str = Field(description="'user' or 'assistant'")
    content: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    user: User = Relationship(back_populates="messages")

class Note(SQLModel, table=True):
    __tablename__ = "notes"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    content: str
    tags: str = Field(default="")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ShoppingItem(SQLModel, table=True):
    __tablename__ = "shopping_items"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    item_name: str
    is_bought: bool = Field(default=False)
    added_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))