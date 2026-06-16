
from sqlalchemy import String, BigInteger, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class BaseConfig(Base):
    __tablename__ = 'base_configs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
class User(Base):
    __tablename__ = 'users'
    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)