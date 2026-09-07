from app.database import Base, engine
from app.models import Character

Base.metadata.create_all(engine)

print("Database tables created successfully.")