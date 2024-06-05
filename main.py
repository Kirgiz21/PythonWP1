from fastapi import FastAPI, Depends, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal, engine
import models, schemas, crud

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Home"})


@app.get("/users/", response_class=HTMLResponse)
def read_users(request: Request, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return templates.TemplateResponse("users.html", {"request": request, "users": users, "title": "Users"})


@app.get("/appointments/", response_class=HTMLResponse)
def read_appointments(request: Request, db: Session = Depends(get_db)):
    appointments = crud.get_appointments(db)
    return templates.TemplateResponse("appointments.html",
                                      {"request": request, "appointments": appointments, "title": "Appointments"})


@app.get("/treatments/", response_class=HTMLResponse)
def read_treatments(request: Request, db: Session = Depends(get_db)):
    treatments = crud.get_treatments(db)
    return templates.TemplateResponse("treatments.html",
                                      {"request": request, "treatments": treatments, "title": "Treatments"})


@app.get("/users/new/", response_class=HTMLResponse)
def new_user(request: Request):
    fields = [
        {"name": "username", "label": "Username", "type": "text", "value": ""},
        {"name": "password", "label": "Password", "type": "password", "value": ""},
        {"name": "role", "label": "Role", "type": "text", "value": ""}
    ]
    return templates.TemplateResponse("form.html", {"request": request, "title": "Create User", "action": "/users/",
                                                    "fields": fields})


@app.post("/users/")
def create_user(username: str = Form(...), password: str = Form(...), role: str = Form(...),
                db: Session = Depends(get_db)):
    user = schemas.UserCreate(username=username, password=password, role=role)
    crud.create_user(db, user)
    return RedirectResponse("/users/", status_code=303)


@app.get("/users/{user_id}/edit/", response_class=HTMLResponse)
def edit_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    fields = [
        {"name": "username", "label": "Username", "type": "text", "value": user.username},
        {"name": "role", "label": "Role", "type": "text", "value": user.role}
    ]
    return templates.TemplateResponse("form.html",
                                      {"request": request, "title": "Edit User", "action": f"/users/{user_id}/",
                                       "fields": fields})


@app.post("/users/{user_id}/")
def update_user(user_id: int, username: str = Form(...), role: str = Form(...), db: Session = Depends(get_db)):
    user = schemas.User(username=username, role=role, id=user_id)
    crud.update_user(db, user)
    return RedirectResponse("/users/", status_code=303)


@app.post("/users/{user_id}/delete/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    crud.delete_user(db, user_id)
    return RedirectResponse("/users/", status_code=303)


@app.get("/appointments/new/", response_class=HTMLResponse)
def new_appointment(request: Request, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    user_options = [{"value": user.id, "label": user.username} for user in users]
    fields = [
        {"name": "date", "label": "Date", "type": "text", "value": ""},
        {"name": "user_id", "label": "User ID", "type": "select", "options": user_options}
    ]
    return templates.TemplateResponse("form.html",
                                      {"request": request, "title": "Create Appointment", "action": "/appointments/",
                                       "fields": fields})


@app.post("/appointments/")
def create_appointment(date: str = Form(...), user_id: int = Form(...), db: Session = Depends(get_db)):
    appointment = schemas.AppointmentCreate(date=date, user_id=user_id)
    crud.create_appointment(db, appointment)
    return RedirectResponse("/appointments/", status_code=303)


@app.get("/appointments/{appointment_id}/edit/", response_class=HTMLResponse)
def edit_appointment(request: Request, appointment_id: int, db: Session = Depends(get_db)):
    appointment = crud.get_appointment(db, appointment_id=appointment_id)
    users = crud.get_users(db)
    user_options = [{"value": user.id, "label": user.username, "selected": user.id == appointment.user_id} for user in
                    users]
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    fields = [
        {"name": "date", "label": "Date", "type": "text", "value": appointment.date},
        {"name": "user_id", "label": "User ID", "type": "select", "options": user_options}
    ]
    return templates.TemplateResponse("form.html", {"request": request, "title": "Edit Appointment",
                                                    "action": f"/appointments/{appointment_id}/", "fields": fields})


@app.post("/appointments/{appointment_id}/")
def update_appointment(appointment_id: int, date: str = Form(...), user_id: int = Form(...),
                       db: Session = Depends(get_db)):
    appointment = schemas.Appointment(date=date, user_id=user_id, id=appointment_id)
    crud.update_appointment(db, appointment)
    return RedirectResponse("/appointments/", status_code=303)


@app.post("/appointments/{appointment_id}/delete/")
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    crud.delete_appointment(db, appointment_id)
    return RedirectResponse("/appointments/", status_code=303)


@app.get("/treatments/new/", response_class=HTMLResponse)
def new_treatment(request: Request, db: Session = Depends(get_db)):
    users = crud.get_users(db)
    user_options = [{"value": user.id, "label": user.username} for user in users]
    fields = [
        {"name": "name", "label": "Name", "type": "text", "value": ""},
        {"name": "description", "label": "Description", "type": "text", "value": ""},
        {"name": "user_id", "label": "User ID", "type": "select", "options": user_options}
    ]
    return templates.TemplateResponse("form.html",
                                      {"request": request, "title": "Create Treatment", "action": "/treatments/",
                                       "fields": fields})


@app.post("/treatments/")
def create_treatment(name: str = Form(...), description: str = Form(...), user_id: int = Form(...),
                     db: Session = Depends(get_db)):
    treatment = schemas.TreatmentCreate(name=name, description=description, user_id=user_id)
    crud.create_treatment(db, treatment)
    return RedirectResponse("/treatments/", status_code=303)


@app.get("/treatments/{treatment_id}/edit/", response_class=HTMLResponse)
def edit_treatment(request: Request, treatment_id: int, db: Session = Depends(get_db)):
    treatment = crud.get_treatment(db, treatment_id=treatment_id)
    users = crud.get_users(db)
    user_options = [{"value": user.id, "label": user.username, "selected": user.id == treatment.user_id} for user in
                    users]
    if not treatment:
        raise HTTPException(status_code=404, detail="Treatment not found")
    fields = [
        {"name": "name", "label": "Name", "type": "text", "value": treatment.name},
        {"name": "description", "label": "Description", "type": "text", "value": treatment.description},
        {"name": "user_id", "label": "User ID", "type": "select", "options": user_options}
    ]
    return templates.TemplateResponse("form.html", {"request": request, "title": "Edit Treatment",
                                                    "action": f"/treatments/{treatment_id}/", "fields": fields})


@app.post("/treatments/{treatment_id}/")
def update_treatment(treatment_id: int, name: str = Form(...), description: str = Form(...), user_id: int = Form(...),
                     db: Session = Depends(get_db)):
    treatment = schemas.Treatment(name=name, description=description, user_id=user_id, id=treatment_id)
    crud.update_treatment(db, treatment)
    return RedirectResponse("/treatments/", status_code=303)


@app.post("/treatments/{treatment_id}/delete/")
def delete_treatment(treatment_id: int, db: Session = Depends(get_db)):
    crud.delete_treatment(db, treatment_id)
    return RedirectResponse("/treatments/", status_code=303)
