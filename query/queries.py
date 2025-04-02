from database import execute_query

def get_leiloes_veiculos():
    execute_query = """
        SELECT 
            l.*,
            COALESCE(
                (SELECT MAX(valor) FROM lance WHERE leilao_id = l.id),
                l.lance_inicial
            ) as maior_lance,
            (
                SELECT u.nome 
                FROM lance ln 
                JOIN user u ON ln.usuario_id = u.id 
                WHERE ln.leilao_id = l.id 
                ORDER BY ln.valor DESC 
                LIMIT 1
            ) as maior_lance_user,
            (
                SELECT COUNT(*) 
                FROM lance 
                WHERE leilao_id = l.id
            ) as total_lances
        FROM leilao l
        WHERE l.categoria = 'veiculos'
          AND l.status = 'ativo'
          AND l.data_inicio <= CURRENT_TIMESTAMP
        ORDER BY l.data_inicio DESC
        LIMIT 4
    """
    return _processar_resultados(execute_query(fetch=True))

def get_leiloes_imoveis():
    query = """
        SELECT 
            l.*,
            COALESCE(
                (SELECT MAX(valor) FROM lance WHERE leilao_id = l.id),
                l.lance_inicial
            ) as maior_lance,
            (
                SELECT u.nome 
                FROM lance ln 
                JOIN user u ON ln.usuario_id = u.id 
                WHERE ln.leilao_id = l.id 
                ORDER BY ln.valor DESC 
                LIMIT 1
            ) as maior_lance_user,
            (
                SELECT COUNT(*) 
                FROM lance 
                WHERE leilao_id = l.id
            ) as total_lances
        FROM leilao l
        WHERE l.categoria = 'imoveis'
          AND l.status = 'ativo'
          AND l.data_inicio <= CURRENT_TIMESTAMP
        ORDER BY l.data_inicio DESC
        LIMIT 4
    """
    return _processar_resultados(execute_query(query, fetch=True))

def get_leiloes_outros():
    query = """
        SELECT 
            l.*,
            COALESCE(
                (SELECT MAX(valor) FROM lance WHERE leilao_id = l.id),
                l.lance_inicial
            ) as maior_lance,
            (
                SELECT u.nome 
                FROM lance ln 
                JOIN user u ON ln.usuario_id = u.id 
                WHERE ln.leilao_id = l.id 
                ORDER BY ln.valor DESC 
                LIMIT 1
            ) as maior_lance_user,
            (
                SELECT COUNT(*) 
                FROM lance 
                WHERE leilao_id = l.id
            ) as total_lances
        FROM leilao l
        WHERE l.categoria = 'outros'
          AND l.status = 'ativo'
          AND l.data_inicio <= CURRENT_TIMESTAMP
        ORDER BY l.data_inicio DESC
        LIMIT 4
    """
    return _processar_resultados(execute_query(query, fetch=True))

def _processar_resultados(result):
    """Função auxiliar para processar os resultados das queries"""
    leiloes = []
    for row in result:
        row_data = dict(row)
        
        leilao = {
            **row_data,
            'maior_lance': float(row_data.get('maior_lance') or row_data.get('lance_inicial') or 0),
            'maior_lance_info': {
                'nome': row_data['maior_lance_user']
            } if row_data.get('maior_lance_user') else None,
            'total_lances': row_data.get('total_lances', 0)
        }
        leiloes.append(leilao)
    return leiloes