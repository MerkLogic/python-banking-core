from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, ForeignKey, Numeric, Boolean, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Client(Base):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    accounts: Mapped[List['Account']] = relationship('Account', back_populates='client',
                                                     cascade='all, delete-orphan')

class Account(Base):
    __tablename__ = "accounts"
    id: Mapped[int] = mapped_column(primary_key=True)
    account_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"),nullable=False)
    balance: Mapped[float] = mapped_column(Numeric(12, 2), default=0.0, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    client: Mapped['Client'] = relationship('Client', back_populates='accounts')


class TransactionHistory(Base):
    __tablename__ = "transaction_history"
    id: Mapped[int] = mapped_column(primary_key=True)
    sender_account_id: Mapped[Optional[int]] = mapped_column(ForeignKey("accounts.id"), nullable=True)
    receiver_account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)
    amount: Mapped[float] = mapped_column(Numeric(12,2), nullable=False)
    status: Mapped[str]= mapped_column(String(10), nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)


