from sqlalchemy.orm import Session
import models, schemas


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user: schemas.User):
    db_user = db.query(models.User).filter(models.User.id == user.id).first()
    db_user.username = user.username
    db_user.role = user.role
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete(db_user)
    db.commit()


def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment).offset(skip).limit(limit).all()


def get_appointment(db: Session, appointment_id: int):
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()


def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def update_appointment(db: Session, appointment: schemas.Appointment):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment.id).first()
    db_appointment.date = appointment.date
    db_appointment.user_id = appointment.user_id
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


def delete_appointment(db: Session, appointment_id: int):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    db.delete(db_appointment)
    db.commit()


def get_treatments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Treatment).offset(skip).limit(limit).all()


def get_treatment(db: Session, treatment_id: int):
    return db.query(models.Treatment).filter(models.Treatment.id == treatment_id).first()


def create_treatment(db: Session, treatment: schemas.TreatmentCreate):
    db_treatment = models.Treatment(**treatment.dict())
    db.add(db_treatment)
    db.commit()
    db.refresh(db_treatment)
    return db_treatment


def update_treatment(db: Session, treatment: schemas.Treatment):
    db_treatment = db.query(models.Treatment).filter(models.Treatment.id == treatment.id).first()
    db_treatment.name = treatment.name
    db_treatment.description = treatment.description
    db_treatment.user_id = treatment.user_id
    db.commit()
    db.refresh(db_treatment)
    return db_treatment


def delete_treatment(db: Session, treatment_id: int):
    db_treatment = db.query(models.Treatment).filter(models.Treatment.id == treatment_id).first()
    db.delete(db_treatment)
    db.commit()
