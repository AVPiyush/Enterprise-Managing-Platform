
from uuid import uuid4

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.database.models.user import User

router = APIRouter(tags=["Users"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/users")
def create_user(db: Session = Depends(get_db)):
    user = User(
        email=f"test-{uuid4().hex[:8]}@example.com",
        hashed_password="temporary-placeholder",
        name="Test User",
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "email": user.email,
        "name": user.name,
    }


@router.get("/users")
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()
