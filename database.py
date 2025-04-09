from sqlalchemy.orm import Session
from models import User, Appointment, Patient
import datetime

class DatabaseManager:
    def __init__(self, session: Session):
        self.session = session

    # User Operations
    def get_user(self, user_id: int) -> User:
        return self.session.query(User).filter_by(uuid=user_id).first()

    def get_all_users(self) -> list[User]:
        return self.session.query(User).all()
    
    def get_user_by_username(self, username: str) -> User:
        return self.session.query(User).filter_by(username=username).first()

    # Appointment Operations
    def get_appointments_by_user(self, user_id: int) -> list[Appointment]:
        return self.session.query(Appointment).filter_by(patient_id=user_id).all()

    # Patient Operations
    def get_patient(self, user_id: int) -> Patient:
        return self.session.query(Patient).filter_by(user_id=user_id).first()