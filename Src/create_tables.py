from database import engine
import models

models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)

print("Tables created in newsagent.db:")
for table in models.Base.metadata.sorted_tables:
    print(f"  - {table.name}")