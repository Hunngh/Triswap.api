from sqlalchemy import Column, Integer, String, ForeignKey
from app.database.database import Base


class AdminAccount(Base):
    __tablename__ = "admin_account"

    account=Column(String(255), primary_key=True,nullable=False)
    password=Column(String(255),nullable=False)