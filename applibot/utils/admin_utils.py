import argparse
from applibot.utils.config_loader import load_config
from applibot.utils.postgres_store import PostgresStore, Base
from applibot.utils.lancedb_store import LanceDBStore

def main():
    # Create the parser
    parser = argparse.ArgumentParser(description='Postgres Database Management Tool')
    parser.add_argument('--config', required=True, type=str, help='Path to the configuration YAML file.')
    parser.add_argument('--action', required=True, choices=['create', 'delete', 'recreate', 'backup', 'restore', 'delete_user'],
                        help='Database action to perform')

    # Parse the arguments
    args = parser.parse_args()
    if args.action == 'delete_user':
        args.email = input('Enter the email of the user to delete: ')
    
    # Load the configuration
    config = load_config(args.config)
    db_url = config.objects.postgres_store.database_url
    store = PostgresStore(database_url=db_url)
    backup_dir = config.raw.service.data_path + "backup/"

    # Perform the specified action
    if args.action == 'create':
        Base.metadata.create_all(bind=store.engine)
        print("Database created.")
    elif args.action == 'delete':
        Base.metadata.drop_all(bind=store.engine)
        print("Database deleted.")
    elif args.action == 'recreate':
        Base.metadata.drop_all(bind=store.engine)
        Base.metadata.create_all(bind=store.engine)
        print("Database re-created.")
    elif args.action == 'backup':
        store.backup_to_csv(backup_dir=backup_dir)
         # Backup LanceDB data to JSON
        lancedb_path = config.objects.info_store.db_path
        table_name = config.objects.info_store.table_name
        lancedb_store = LanceDBStore(db_path=lancedb_path, table_name=table_name, pydantic_model_str='InfoSchema')
        lancedb_store.export_to_json(f'{backup_dir}/{table_name}_backup.json')
        print("Data from both PostgreSQL and LanceDB has been backed up.")
    elif args.action == 'restore':
        store.restore_from_csv(backup_dir=backup_dir)
        # Import LanceDB data from JSON
        lancedb_path = config.objects.info_store.db_path
        table_name = config.objects.info_store.table_name
        lancedb_store = LanceDBStore(db_path=lancedb_path, table_name=table_name, pydantic_model_str='InfoSchema')
        lancedb_store.import_from_json(f'{backup_dir}/{table_name}_backup.json')
        print("Data from both PostgreSQL and LanceDB has been restored.")
    elif args.action == 'delete_user':
        deleted_user_id = store.delete_user_and_related_data(args.email)
        lancedb_path = config.objects.info_store.db_path
        table_name = config.objects.info_store.table_name
        lancedb_store = LanceDBStore(db_path=lancedb_path, table_name=table_name, pydantic_model_str='InfoSchema')
        lancedb_store.delete_user_info(deleted_user_id)

if __name__ == "__main__":
    main()
