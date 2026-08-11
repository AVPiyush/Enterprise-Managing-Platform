from fastapi import APIRouter
from app.database.session import SessionLocal
from app.database.models.user import User

router = APIRouter(tags=["Users"])


@router.post("/users")
def create_user():
    db = SessionLocal()

    user = User(email="test@example.com", name="Test User")

    db.add(user)
    db.commit()
    db.refresh(user)

    db.close()

    return {
        "id": user.id,
        "email": user.email
    }


@router.get("/users")
def get_users():
    db = SessionLocal()

    users = db.query(User).all()

    db.close()

    return users