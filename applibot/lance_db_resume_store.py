import lancedb

class LanceDBResumeStore:
    def __init__(self, db_path, table_name):
        self.db_path = db_path
        self.table_name = table_name
        self.table = self.get_lance_db(self.db_path, self.table_name)

    def get_lance_db(self, db_path, table_name):
        # Connect to the database
        db = lancedb.connect(db_path)
        
        # Check if the table already exists, if not create it
        if table_name not in db.table_names():
            db.create_table(table_name)
        
        # Open the table and return the table object
        table = db.open_table(table_name)
        return table

if __name__ == "__main__":
    resume_store = LanceDBResumeStore("path_to_db", "table_name")
    print(resume_store.table)