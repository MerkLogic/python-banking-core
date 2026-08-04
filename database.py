import os
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker, create_async_engine)
from sqlalchemy.orm import DeclarativeBase

DB_URL = "sqlite+aiosqlite:///./banking.db"

engine = create_async_engine(DB_URL, echo=False)
async_session_factory = async_sessionmaker(engine, expire_on_commit=False)

class Base(AsyncAttrs, DeclarativeBase):
    pass

