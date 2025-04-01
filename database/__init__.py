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

# Função para gerenciar transações
def execute_query(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        conn.commit()
        return cursor.fetchall()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()