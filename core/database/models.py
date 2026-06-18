
from sqlalchemy import String, BigInteger, Integer, Boolean, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


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
    welcome_msg: Mapped[str] = mapped_column(String(255), nullable=True)
    accept_order_answer: Mapped[str] = mapped_column(String(255), nullable=True)
    review_answer: Mapped[dict] = mapped_column(JSON, nullable=True)
    auto_issue: Mapped[dict] = mapped_column(JSON, nullable=True)
    auto_answer: Mapped[dict] = mapped_column(JSON, nullable=True)
    
class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)