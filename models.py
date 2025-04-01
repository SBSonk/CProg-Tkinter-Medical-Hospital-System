from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Integer
import bcrypt

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'user'

    uuid: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
    
    def __init__(self, username, password): # converts plaintext password to hash upon creation.
        super().__init__()
        self.username = username
        self.set_password(password)

    def __repr__(self):
        return f"Username: {self.username}\nPassword: {self.password_hash}"