from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, ForeignKey, Text
import enum
import datetime
import bcrypt


class Base(DeclarativeBase):
    pass

# Enum for user roles
class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    NURSE = "NURSE"
    PATIENT = "PATIENT"


class User(Base):
    __tablename__ = "user"

    uuid: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)
    security_question: Mapped[str] = mapped_column(String(255), nullable=False)
    security_answer_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Additional Fields
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    contact_info: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relationships
    appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment", back_populates="patient", foreign_keys="Appointment.patient_id"
    )
    created_appointments: Mapped[list["Appointment"]] = relationship(
        "Appointment", back_populates="created_by", foreign_keys="Appointment.created_by_id"
    )

    # One-to-one relationship to Patient, only if the user is a patient
    patient: Mapped["Patient"] = relationship("Patient", back_populates="user", uselist=False)

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())
    
    def set_security_answer(self, answer: str):
        self.security_answer_hash = bcrypt.hashpw(answer.encode(), bcrypt.gensalt()).decode()

    def check_security_answer(self, answer: str):
        return bcrypt.checkpw(answer.encode(), self.security_answer_hash.encode())

    def __init__(self, username: str, password: str, security_question: str, security_answer: str, role: str, full_name: str, age: int, gender: str, contact_info: str):
        super().__init__()
        self.username = username
        self.set_password(password)
        self.security_question = security_question
        self.set_security_answer(security_answer)
        self.role = role
        self.full_name = full_name
        self.age = age
        self.gender = gender
        self.contact_info = contact_info
        

    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"


class Appointment(Base):
    __tablename__ = "appointment"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("user.uuid"), nullable=False)
    scheduled_time: Mapped[datetime.datetime] = mapped_column(nullable=False)
    reason: Mapped[str] = mapped_column(Text)
    created_by_id: Mapped[int] = mapped_column(ForeignKey("user.uuid"))

    patient: Mapped["User"] = relationship(
        foreign_keys=[patient_id], back_populates="appointments"
    )
    created_by: Mapped["User"] = relationship(
        foreign_keys=[created_by_id], back_populates="created_appointments"
    )
    
    def __init__(self, patient_id, scheduled_time, reason, created_by_id):
        self.patient_id = patient_id
        self.scheduled_time = scheduled_time
        self.reason = reason
        self.created_by_id = created_by_id

class Patient(Base):
    __tablename__ = "patient"

    # user_id is the primary key and foreign key linking to the User table
    user_id: Mapped[int] = mapped_column(ForeignKey("user.uuid"), primary_key=True)

    # Additional patient-specific information
    treatments: Mapped[str] = mapped_column(Text, nullable=True)
    allergies: Mapped[str] = mapped_column(Text, nullable=True)
    diseases: Mapped[str] = mapped_column(Text, nullable=True)

    # Relationship to User (one-to-one relationship)
    user: Mapped["User"] = relationship("User", back_populates="patient")

    def __init__(self, user_id: int, treatments: str = "", allergies: str = "", diseases: str = ""):
        self.user_id = user_id
        self.treatments = treatments
        self.allergies = allergies
        self.diseases = diseases

    def __repr__(self):
        return f"<Patient(user_id={self.user_id}, treatments={self.treatments}, allergies={self.allergies}, diseases={self.diseases})>"
