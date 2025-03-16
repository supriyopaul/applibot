import os

import pandas as pd
from sqlalchemy import inspect
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from sqlalchemy_utils import database_exists, create_database

DEFAULT_DB_URL = "postgresql://applibot_user:default_password@localhost/applibot_db"
Base = declarative_base()
USER_TABLE_NAME = 'users'
RESUME_TABLE_NAME = 'resumes'

class PostgresStore:
    def __init__(self, database_url=DEFAULT_DB_URL):
        self.database_url = database_url
        self._create_db()
        self.engine = create_engine(database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)

    def _create_db(self):
        # Check if the database exists
        if not database_exists(self.database_url):
            print("Database does not exist, creating...")
            create_database(self.database_url)
            print("Database created.")
        else:
            print("Database already exists.")

    def get_db(self):
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()

    def backup_to_csv(self, backup_dir='backup'):
        """
        Back up all tables to CSV files in the specified directory.
        """
        # Ensure the backup directory exists
        os.makedirs(backup_dir, exist_ok=True)

        inspector = inspect(self.engine)
        table_names = inspector.get_table_names()
        for table_name in table_names:
            df = pd.read_sql_table(table_name, self.engine)
            df.to_csv(f'{backup_dir}/{table_name}.csv', index=False)
        print("Backup completed to CSV files.")

    def restore_from_csv(self, backup_dir='backup'):
        """
        Restore all tables from CSV files in the specified directory.
        """
        inspector = inspect(self.engine)
        table_names = inspector.get_table_names()
        for table_name in table_names:
            df = pd.read_csv(f'{backup_dir}/{table_name}.csv')
            df.to_sql(table_name, self.engine, if_exists='replace', index=False)
        print("Restore completed from CSV files.")

    def delete_user_and_related_data(self, email: str):
        """Delete a user and all their resumes."""
        db = self.SessionLocal()
        try:
            user = db.query(UserInDB).filter(UserInDB.email == email).first()
            if user:
                db.query(Resume).filter(Resume.user_id == user.id).delete()
                db.delete(user)
                db.commit()
                print(f"Deleted user and associated resumes for {email}")
                return user.id
            else:
                print(f"No user found with email: {email}")
        finally:
            db.close()

# Database models
class UserInDB(Base):
    __tablename__ = USER_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    openai_api_key = Column(String, nullable=True)

class Resume(Base):
    __tablename__ = RESUME_TABLE_NAME

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

if __name__ == '__main__':
    db_url = input("Enter the database URL (or press enter for the default): ")
    db_url = db_url if db_url else DEFAULT_DB_URL  # Use the input URL or the default if blank
    store = PostgresStore(database_url=db_url)
    
    action = input("Choose an action: [1] Create DB, [2] Delete DB, [3] Re-create DB, [4] Backup to CSV, [5] Restore from CSV: ")

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
    elif action == '4':
        # Backup DB to CSV
        store.backup_to_csv()
    elif action == '5':
        # Restore DB from CSV
        store.restore_from_csv()
    else:
        print("No valid action selected.")
