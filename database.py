from dotenv import load_dotenv
import os

from langchain_community.utilities.sql_database import SQLDatabase
load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
database_uri = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
os.environ["OPENAI_API_KEY"] = os.getenv('OPENAI_API_KEY')
db = SQLDatabase.from_uri(database_uri)

