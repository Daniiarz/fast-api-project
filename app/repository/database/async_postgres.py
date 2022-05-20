import databases
from config import settings

database = databases.Database(settings.postgres_url, min_size=5, max_size=10)
