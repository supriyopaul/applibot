import json
from json import JSONEncoder
import numpy as np

import lancedb
from lancedb.pydantic import pydantic_to_schema
import pydantic
from typing import List, Type
from lancedb.pydantic import Vector

class InfoSchema(pydantic.BaseModel):
    id: str
    text: str
    vector:  Vector(1536)
    user_id: str

MODEL_MAP = {
    'InfoSchema': InfoSchema
}

class NumpyArrayEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return JSONEncoder.default(self, obj)

class LanceDBStore:
    def __init__(self, db_path, table_name, pydantic_model_str: str):
        self.db_path = db_path
        self.table_name = table_name
        self.schema = self.get_schema_from_str(pydantic_model_str)
        self.table = self.get_lance_db_table(self.db_path, self.table_name, self.schema)
    
    def get_schema_from_str(self, model_str: str) -> Type[pydantic.BaseModel]:
        model = MODEL_MAP.get(model_str)
        if not model:
            raise ValueError(f"Invalid model name: {model_str}")
        return pydantic_to_schema(model)

    def get_lance_db_table(self, db_path, table_name, schema):
        db = lancedb.connect(db_path)
        if table_name not in db.table_names():
            db.create_table(table_name, schema=schema)
        table = db.open_table(table_name)
        return table

    def export_to_json(self, file_path: str):
        """
        Export the table data to a JSON file.
        """
        data = [dict(item) for item in self.table.to_pandas().to_dict('records')]
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, cls=NumpyArrayEncoder)

    def import_from_json(self, file_path: str):
        """
        Import data from a JSON file into the table.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for item in data:
                self.table.add([item])

    def delete_user_info(self, user_id: int):
        """Delete information associated with a user."""
        delete_condition = f"user_id = '{user_id}'"
        self.table.delete(delete_condition)
        
        print(f"Deleted information for user_id: {user_id}")


if __name__ == "__main__":
    action = input("Choose an action: [1] Export to JSON, [2] Import from JSON and Verify: ")
    table_name = 'info'

    if action == '1':
        db_path = input("Enter the database path (default: 'my-data/lancedb'): ")
        db_path = db_path if db_path else 'my-data/lancedb'
        db_store = LanceDBStore(db_path=db_path, table_name=table_name, pydantic_model_str='InfoSchema')
        # Export to JSON
        db_store.export_to_json('exported_info.json')
        print("Data exported to JSON.")
    elif action == '2':
        backup_dir = input("Enter the backup directory path: ")
        backup_table_name = table_name + '_backup'
        db_store_backup = LanceDBStore(backup_dir, table_name=backup_table_name, pydantic_model_str='InfoSchema')
        db_store_backup.import_from_json('exported_info.json')

        # Assuming you need to compare with original data from the original path
        db_store = LanceDBStore(db_path='my-data/lancedb', table_name=table_name, pydantic_model_str='InfoSchema')
        original_data = db_store.table.to_pandas()
        backup_data = db_store_backup.table.to_pandas()

        all_data_matched = original_data.equals(backup_data)
        if all_data_matched:
            print("DB backed up successfully!")
        else:
            print("Backup failed to match original DB.")
    else:
        print("No valid action selected.")
