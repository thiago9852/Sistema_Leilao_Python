import os

class Config:
    # MySQL
    
    MYSQL_HOST = os.getenv("MYSQL_HOST", "127.0.0.1")
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_DB = os.getenv("MYSQL_DB", "leilao_db")
    MYSQL_POOL_SIZE = 10
    
    # WebSockets
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    SECRET_KEY = os.getenv("SECRET_KEY", "segredo_super_secreto")
    
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        auth = f"{self.MYSQL_USER}:{self.MYSQL_PASSWORD}" if self.MYSQL_PASSWORD else self.MYSQL_USER
        return f"mysql+mysqlconnector://{auth}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DB}?charset=utf8mb4"