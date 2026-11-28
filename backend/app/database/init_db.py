
from app.database.base import Base
from app.database.session import engine

# Import models so SQLAlchemy registers them.
from app.database.models.user import User
from app.database.models.document import Document
from app.database.models.purchase_order import PurchaseOrder

def init_db():
    Base.metadata.create_all(bind=engine)
