from flask_socketio import emit
from database import get_db_connection
import mysql.connector

def register_socket_handlers(socketio):
    @socketio.on('novo_lance')
    def handle_novo_lance(data):
        conn = None
        try:
            conn = get_db_connection()
            conn.start_transaction()  # Inicia transação
            
            cursor = conn.cursor(dictionary=True)
            
            # 1. Verifica leilão
            cursor.execute("""
                SELECT * FROM leiloes 
                WHERE id = %s AND status = 'ativo'
                FOR UPDATE  # Lock pessimista
            """, (data['leilao_id'],))
            leilao = cursor.fetchone()
            
            if not leilao:
                emit('erro', {'msg': 'Leilão não encontrado'})
                return
            
            # 2. Insere lance
            cursor.execute("""
                INSERT INTO lances (valor, user_id, leilao_id)
                VALUES (%s, %s, %s)
            """, (data['valor'], data['user_id'], data['leilao_id']))
            
            # 3. Atualiza preço atual
            cursor.execute("""
                UPDATE leiloes 
                SET preco_atual = %s 
                WHERE id = %s
            """, (data['valor'], data['leilao_id']))
            
            conn.commit()  # Confirma transação
            
            # 4. Notifica todos via WebSocket
            emit('atualizacao_lance', {
                'valor': data['valor'],
                'user_id': data['user_id']
            }, room=str(data['leilao_id']))
            
        except mysql.connector.Error as err:
            if conn:
                conn.rollback()
            emit('erro', {'msg': str(err)})
        finally:
            if conn and conn.is_connected():
                cursor.close()
                conn.close()