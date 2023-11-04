from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

DEFAULT_DB_URL = "postgresql://applibot_user:change_this_password@localhost/applibot_db"
Base = declarative_base()

class PostgresStore:
    def __init__(self, database_url=DEFAULT_DB_URL):
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

# Database models
class UserInDB(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Resume(Base):
    __tablename__ = 'resumes'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

if __name__ == '__main__':
    db_url = input("Enter the database URL (or press enter for the default): ")
    db_url = db_url if db_url else DEFAULT_DB_URL  # Use the input URL or the default if blank
    store = PostgresStore(database_url=db_url)
    
    action = input("Choose an action: [1] Create DB, [2] Delete DB, [3] Re-create DB: ")

    if action == '1':
        # Create DB
        Base.metadata.create_all(bind=store.engine)
        print("Database created.")
    elif action == '2':
        # Delete DB
        Base.metadata.drop_all(bind=store.engine)
        print("Database deleted.")
    elif action == '3':
        # Re-create DB
        Base.metadata.drop_all(bind=store.engine)
        Base.metadata.create_all(bind=store.engine)
        print("Database re-created.")
    else:
        print("No valid action selected.")
