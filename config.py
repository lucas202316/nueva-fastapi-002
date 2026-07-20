from dotenv import load_dotenv
import os

load_dotenv()#"Busca un archivo llamado .env y carga todas sus variables."



DATABASE_PATH = os.getenv("DATABASE_PATH")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
