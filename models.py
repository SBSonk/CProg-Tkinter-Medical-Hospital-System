from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Enum, ForeignKey, Text
import enum
import datetime
import bcrypt


class Base(DeclarativeBase):
    pass

# Enum for user roles
class UserRole(enum.Enum):
    ADMIN = "admin"
    DOCTOR = "doctor"
    NURSE = "nurse"
    PATIENT = "patient"


class User(Base):
    __tablename__ = "user"

    uuid: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String(60), nullable=False)

    # Additional Fields
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(10), nullable=True)
    contact_info: Mapped[str] = mapped_column(String(255), nullable=True)
    security_question: Mapped[str] = mapped_column(String(255), nullable=True)
    security_answer_hash: Mapped[str] = mapped_column(String(255), nullable=True)

    # Relationships
    doctor_notes: Mapped[list["DoctorNote"]] = relationship(
        back_populates="doctor", foreign_keys="DoctorNote.doctor_id"
    )
    patient_notes: Mapped[list["DoctorNote"]] = relationship(
        back_populates="patient", foreign_keys="DoctorNote.patient_id"
    )
    medical_history: Mapped[list["MedicalHistory"]] = relationship(
        back_populates="patient"
    )
    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="patient", foreign_keys="Appointment.patient_id"
    )
    created_appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="created_by", foreign_keys="Appointment.created_by_id"
    )

    def set_password(self, password: str):
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    def check_password(self, password: str):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

    def __init__(self, username: str, password: str, role: str, full_name: str):
        super().__init__()
        self.username = username
        self.set_password(password)
        self.role = role
        self.full_name = full_name

    def __repr__(self):
        return f"<User(username={self.username}, role={self.role})>"


class MedicalHistory(Base):
    __tablename__ = "medical_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("user.uuid"), nullable=False)
    chronic_diseases: Mapped[str] = mapped_column(Text)
    past_treatments: Mapped[str] = mapped_column(Text)
    allergies: Mapped[str] = mapped_column(Text)

    patient: Mapped["User"] = relationship(back_populates="medical_history")


class DoctorNote(Base):
    __tablename__ = "doctor_note"

    id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("user.uuid"), nullable=False)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("user.uuid"), nullable=False)
    note: Mapped[str] = mapped_column(Text)
    prescription: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime.datetime] = mapped_column(
        default=datetime.datetime.utcnow
    )

    patient: Mapped["User"] = relationship(
        foreign_keys=[patient_id], back_populates="patient_notes"
    )
    doctor: Mapped["User"] = relationship(
        foreign_keys=[doctor_id], back_populates="doctor_notes"
    )


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
