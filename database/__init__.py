import mysql.connector.pooling
from config.config import Config

db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="leilao_pool",
    pool_size=Config.MYSQL_POOL_SIZE,
    host=Config.MYSQL_HOST,
    user=Config.MYSQL_USER,
    password=Config.MYSQL_PASSWORD,
    database=Config.MYSQL_DB,
    autocommit=False  # Importante para controle manual
)

def get_db_connection():
    return db_pool.get_connection()

def execute_query(query, params=None, fetch=False):
    conn = get_db_connection()
    cursor = None
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        # Só faz fetch se for uma SELECT e fetch=True
        if fetch and query.strip().upper().startswith('SELECT'):
            result = cursor.fetchall()
            conn.commit()  # Commit mesmo para SELECT (libera locks)
            return result
        else:
            conn.commit()
            return cursor.rowcount  # Retorna número de linhas afetadas
            
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()