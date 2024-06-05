from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    role: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class AppointmentBase(BaseModel):
    date: str
    user_id: int


class AppointmentCreate(AppointmentBase):
    pass


class Appointment(AppointmentBase):
    id: int

    class Config:
        orm_mode = True


class TreatmentBase(BaseModel):
    name: str
    description: str


class TreatmentCreate(TreatmentBase):
    user_id: int


class Treatment(TreatmentBase):
    id: int

    class Config:
        orm_mode = True
