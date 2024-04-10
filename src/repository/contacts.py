from typing import List
from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import extract, or_

from src.database.models import Contact
from src.schemas import ContactIn


async def get_contacts(skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).offset(skip).limit(limit).all()


async def get_contact(contact_id: int, db: Session) -> Contact:
    return db.query(Contact).filter(Contact.id == contact_id).first()


async def create_contact(body: ContactIn, db: Session) -> Contact:
    contact = Contact(first_name=body.first_name, last_name=body.last_name, email=body.email, phone_number = body.phone_number, date_of_birth = body.date_of_birth)
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def remove_contact(contact_id: int, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def update_contact(contact_id: int, body: ContactIn, db: Session) -> Contact | None:
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone_number = body.phone_number
        contact.date_of_birth = body.date_of_birth
        db.commit()
    return contact


async def get_contacts_by_query(query: str, skip: int, limit: int, db: Session) -> List[Contact]:
    return db.query(Contact).filter(
        or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.last_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%")
        )
    ).offset(skip).limit(limit).all()


async def get_contacts_with_upcoming_birthdays(db: Session) -> List[Contact]:
    today = datetime.today()
    end_date = today + timedelta(days=7)
    return db.query(Contact).filter(
        extract('month', Contact.date_of_birth) == today.month,
        extract('day', Contact.date_of_birth) >= today.day,
        extract('day', Contact.date_of_birth) <= end_date.day
    ).all()
