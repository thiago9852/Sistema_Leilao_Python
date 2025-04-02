from models import db
from models import Leilao, Lance, User
from datetime import datetime
from sqlalchemy import func, and_
import time
from flask_socketio import emit

lamport_clock = 0

def register_socket_handlers(socketio):
    @socketio.on('connect')
    def handle_connect():
        print('Cliente conectado')

    @socketio.on('disconnect')
    def handle_disconnect():
        print('Cliente desconectado')

    @socketio.on('novo_lance')
    def handle_novo_lance(data):
        global lamport_clock
        print(f"Recebido novo lance: {data}")  # Log de depuração
        
        try:
            # Atualizar relógio de Lamport
            received_clock = data.get('lamport_clock', 0)
            lamport_clock = max(lamport_clock, received_clock) + 1
            
            leilao_id = data['leilao_id']
            valor = float(data['valor'])
            usuario_id = data['usuario_id']
            
            # Verificar se o leilão existe
            leilao = Leilao.query.get(leilao_id)
            if not leilao:
                emit('erro_lance', {'message': 'Leilão não encontrado'})
                return
                
            # Verificar se o leilão está ativo
            if not leilao.esta_ativo():
                emit('erro_lance', {'message': 'Leilão não está ativo'})
                return
            
            # Obter o maior lance atual
            maior_lance_atual = db.session.query(
                func.coalesce(func.max(Lance.valor), leilao.lance_inicial)
            ).filter(Lance.leilao_id == leilao_id).scalar()
            
            # Verificar valor mínimo do lance
            valor_minimo = maior_lance_atual + leilao.lance_minimo
            if valor <= valor_minimo:
                emit('erro_lance', {
                    'message': f'Lance deve ser maior que R$ {valor_minimo:.2f}'
                })
                return
            
            # Criar novo lance
            novo_lance = Lance(
                valor=valor,
                leilao_id=leilao_id,
                usuario_id=usuario_id,
                timestamp=datetime.utcnow()
            )
            
            db.session.add(novo_lance)
            db.session.commit()
            print(f"Lance registrado: {novo_lance.id}")  # Log de depuração
            
            # Obter informações atualizadas do maior lance
            maior_lance_info = db.session.query(
                Lance.valor,
                User.id,
                User.nome
            ).join(User).filter(
                Lance.leilao_id == leilao_id
            ).order_by(
                Lance.valor.desc()
            ).first()
            
            if not maior_lance_info:
                emit('erro_lance', {'message': 'Erro ao recuperar informações do lance'})
                return
            
            # Preparar resposta
            response = {
                'leilao_id': leilao_id,
                'maior_lance': float(maior_lance_info.valor),
                'usuario_id': maior_lance_info.id,
                'usuario_nome': maior_lance_info.nome,
                'lamport_clock': lamport_clock,
                'timestamp': time.time()
            }
            
            # Broadcast para todos os clientes
            emit('atualizacao_lance', response, broadcast=True)
            print(f"Atualização enviada: {response}")  # Log de depuração
            
        except Exception as e:
            db.session.rollback()
            print(f"Erro ao processar lance: {str(e)}")  # Log de erro
            emit('erro_lance', {'message': f'Erro interno: {str(e)}'})