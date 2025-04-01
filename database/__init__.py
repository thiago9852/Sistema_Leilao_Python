import mysql.connector.pooling
from config.config import Config

db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="leilao_pool",
    pool_size=Config.MYSQL_POOL_SIZE,
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DB
)

def get_db_connection():
    return db_pool.get_connection()