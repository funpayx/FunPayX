
from sqlalchemy import String, BigInteger, Integer, Boolean, JSON, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime


class Base(DeclarativeBase):
    pass

class BaseConfig(Base):
    __tablename__ = 'base_configs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    new_message_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    new_order_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    closed_order_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    new_review_notifications: Mapped[bool] = mapped_column(Boolean, default=True)
    blacklist_buyers: Mapped[list[str]] = mapped_column(JSON, default=list)
    welcome_msg: Mapped[dict] = mapped_column(JSON)
    accept_order_answer: Mapped[str] = mapped_column(String(255), nullable=True)
    review_answer: Mapped[dict] = mapped_column(JSON, nullable=True)
    auto_issue: Mapped[dict] = mapped_column(JSON, nullable=True)
    auto_answer: Mapped[list] = mapped_column(JSON, nullable=True)
    global_settings: Mapped[dict] = mapped_column(JSON, nullable=True)
    
class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

class MeetingCooldowns(Base):
    __tablename__ = 'meet_cooldowns'
    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    meet_time: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)