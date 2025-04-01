from database import get_db_connection

def get_leilao_by_id(leilao_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT * FROM leiloes 
            WHERE id = %s AND data_fim > NOW()
            FOR UPDATE
        """, (leilao_id,))
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()

def create_lance(leilao_id, usuario, valor):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        conn.start_transaction()
        cursor.execute("""
            INSERT INTO lances (leilao_id, usuario, valor)
            VALUES (%s, %s, %s)
        """, (leilao_id, usuario, valor))
        cursor.execute("""
            UPDATE leiloes 
            SET preco_inicial = %s 
            WHERE id = %s
        """, (valor, leilao_id))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cursor.close()
        conn.close()