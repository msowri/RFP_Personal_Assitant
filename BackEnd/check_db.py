
import os
from dotenv import load_dotenv

load_dotenv()

from sqlalchemy import create_engine, inspect, text
from app.db.base import Base

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Connecting to: {DATABASE_URL}")

engine = create_engine(DATABASE_URL)

print("\n=== Database Tables ===")
inspector = inspect(engine)
tables = inspector.get_table_names()
if tables:
    for table in tables:
        print(f"  ✓ {table}")
        columns = inspector.get_columns(table)
        for col in columns:
            print(f"    - {col['name']}: {col['type']}")
else:
    print("  (No tables found)")

print("\n=== Alembic Version ===")
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT * FROM alembic_version ORDER BY version_num DESC LIMIT 1"))
        row = result.fetchone()
        if row:
            print(f"  Current version: {row[0]}")
        else:
            print("  (No migrations applied)")
except Exception as e:
    print(f"  Error: {e}")

print("\n=== Schema Verification ===")
expected_tables = ['documents', 'document_chunks', 'questions', 'drafts', 'users', 'orders']
for table_name in expected_tables:
    if table_name in tables:
        print(f"  ✓ {table_name}")
    else:
        print(f"  ✗ {table_name} (MISSING)")
