
from app.database.base import Base
from app.database.session import engine

# Import models so SQLAlchemy registers them.
from app.database.models.user import User
from app.database.models.document import Document

def init_db():
    Base.metadata.create_all(bind=engine)
