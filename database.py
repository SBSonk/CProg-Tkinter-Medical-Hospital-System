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

    def create_user(self, username: str, password: str, role: str, full_name: str, **kwargs) -> User:
        user = User(username=username, password=password, role=role, full_name=full_name)
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.session.add(user)
        self.session.commit()

        # If the user is a patient, also create a corresponding Patient record
        if role == "patient":
            new_patient = Patient(
                user_id=user.uuid,
                treatments=kwargs.get("treatments", ""),
                allergies=kwargs.get("allergies", ""),
                diseases=kwargs.get("diseases", "")
            )
            self.session.add(new_patient)
            self.session.commit()

        return user

    def update_user(self, user_id: int, **kwargs) -> User:
        user = self.get_user(user_id)
        if not user:
            return None
        for key, value in kwargs.items():
            setattr(user, key, value)
        self.session.commit()

        # If it's a patient, update their patient record as well
        if "treatments" in kwargs or "allergies" in kwargs or "diseases" in kwargs:
            patient = user.patient
            if patient:
                if "treatments" in kwargs:
                    patient.treatments = kwargs["treatments"]
                if "allergies" in kwargs:
                    patient.allergies = kwargs["allergies"]
                if "diseases" in kwargs:
                    patient.diseases = kwargs["diseases"]
                self.session.commit()

        return user

    def delete_user(self, user_id: int) -> bool:
        user = self.get_user(user_id)
        if not user:
            return False
        # Delete the patient record if it's a patient
        if user.role == "patient":
            self.session.delete(user.patient)
        self.session.delete(user)
        self.session.commit()
        return True

    # Appointment Operations
    def get_appointments_by_user(self, user_id: int) -> list[Appointment]:
        return self.session.query(Appointment).filter_by(patient_id=user_id).all()

    def create_appointment(self, patient_id: int, scheduled_time: datetime.datetime, reason: str, created_by_id: int) -> Appointment:
        appointment = Appointment(
            patient_id=patient_id,
            scheduled_time=scheduled_time,
            reason=reason,
            created_by_id=created_by_id
        )
        self.session.add(appointment)
        self.session.commit()
        return appointment

    # Patient Operations
    def get_patient(self, user_id: int) -> Patient:
        return self.session.query(Patient).filter_by(user_id=user_id).first()

    def update_patient(self, user_id: int, treatments: str = None, allergies: str = None, diseases: str = None) -> Patient:
        patient = self.get_patient(user_id)
        if patient:
            if treatments is not None:
                patient.treatments = treatments
            if allergies is not None:
                patient.allergies = allergies
            if diseases is not None:
                patient.diseases = diseases
            self.session.commit()
        return patient
