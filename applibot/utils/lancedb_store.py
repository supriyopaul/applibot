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
