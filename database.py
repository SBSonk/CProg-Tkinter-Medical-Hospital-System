from sqlalchemy.orm import Session
from models import User, Appointment, DoctorNote, MedicalHistory


class DatabaseManager:
    def __init__(self, session: Session):
        self.session = session

    def get_user(self, user_id: int) -> User:
        return self.session.query(User).filter_by(uuid=user_id).first()

    def get_all_users(self) -> list[User]:
        return self.session.query(User).all()
    
    def get_user_by_username(self, username: str) -> User:
        return self.session.query(User).filter_by(username=username).first()

    def create_user(self, username: str, password: str, role: str, full_name: str, **kwargs) -> User:
        user = User(username=username, password=password, role=role, full_name=full_name)
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.session.add(user)
        self.session.commit()
        return user

    def update_user(self, user_id: int, **kwargs) -> User:
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.session.commit()
        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        self.session.delete(user)
        self.session.commit()
        return True

    def get_appointments_by_user(self, user_id: int) -> list[Appointment]:
        return self.session.query(Appointment).filter_by(patient_id=user_id).all()

    def get_medical_history_by_user(self, user_id: int) -> list[MedicalHistory]:
        return self.session.query(MedicalHistory).filter_by(patient_id=user_id).all()

    def get_doctor_notes_by_user(self, user_id: int, as_doctor=False) -> list[DoctorNote]:
        if as_doctor:
            return self.session.query(DoctorNote).filter_by(doctor_id=user_id).all()
        return self.session.query(DoctorNote).filter_by(patient_id=user_id).all()
