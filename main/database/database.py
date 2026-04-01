import os
import clickhouse_connect
from dotenv import load_dotenv

load_dotenv()

client = clickhouse_connect.get_client(
    host=os.getenv("DB_HOST", "localhost"),
    username=os.getenv("DB_USERNAME", "default"),
    password=os.getenv("DB_PASSWORD"),
    port=8123,
)
