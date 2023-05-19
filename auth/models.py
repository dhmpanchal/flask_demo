from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    fullname = Column(String(50))
    email = Column(String(120), unique=True)
    phone = Column(String(14))
    password = Column(String(100))

    def __repr__(self):
        return f'<User {self.email!r}>'