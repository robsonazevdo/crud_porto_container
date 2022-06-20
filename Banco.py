from distutils.util import execute
import sqlite3  
from contextlib import closing






def criar_container(cliente, numero_container, tipo, status, categoria):
    container_ja_existe = db_verificar_container(cliente, numero_container, tipo, status, categoria)
    if container_ja_existe is not None: return True, container_ja_existe
    novo_container = db_criar_container(cliente, numero_container, tipo, status, categoria)
    return False, novo_container



def criar_movimentacao(tipo, data_inicio, data_fim, id_container):
    movimentacao_ja_existe = db_verificar_movimentacao(tipo, data_inicio, data_fim, id_container)
    if movimentacao_ja_existe is not None: return True, movimentacao_ja_existe
    novo_movimentacao = db_criar_movimentacao(tipo, data_inicio, data_fim, id_container)
    return False, novo_movimentacao



# Converte uma linha em um dicionário.
def row_to_dict(description, row):
    if row is None: return None
    d = {}
    for i in range(0, len(row)):
        d[description[i][0]] = row[i]
    return d

# Converte uma lista de linhas em um lista de dicionários.
def rows_to_dict(description, rows):
    result = []
    for row in rows:
        result.append(row_to_dict(description, row))
    return result




sql_create = '''

CREATE TABLE IF NOT EXISTS container (
    id_container INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente VACHAR(50) NOT NULL,
    numero_container VACHAR(11) NOT NULL,
    tipo VACHAR(2) NOT NULL,
    status VACHAR(5) NOT NULL,
    categoria VACHAR(11) NOT NULL,
    UNIQUE(numero_container)
    
    );

CREATE TABLE IF NOT EXISTS movimentacao (
    id_movimentacao INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo VACHAR(20) NOT NULL,
    data_inicio DATE NOT NULL,
    data_fim DATE NOT NULL,
    id_container INTERGER NOT NULL,
    FOREIGN KEY (id_container) REFERENCES container(id_container)

    );



'''

def conectar():
    return sqlite3.connect('container')


def db_inicialiar():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.executescript(sql_create)
        con.commit




def db_verificar_container(cliente, numero_container, tipo, status, categoria):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute(" SELECT id_container, cliente, numero_container, tipo, status, categoria FROM container where cliente = ? AND numero_container = ?", [cliente, numero_container])
        return row_to_dict(cur.description, cur.fetchone())



def db_verificar_movimentacao(tipo, data_inicio, data_fim, id_container):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute(" SELECT id_movimentacao, tipo, data_inicio, data_fim, id_container FROM movimentacao where tipo = ? AND id_container = ?", [tipo, id_container])
        return row_to_dict(cur.description, cur.fetchone())



def db_criar_container(cliente, numero_container, tipo, status, categoria):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO container(cliente, numero_container, tipo, status, categoria) VALUES (?,?,?,?,?)", [cliente, numero_container, tipo, status, categoria])
        id_container = cur.lastrowid
        con.commit()
        return {'id_container':id_container, 'cliente': cliente, 'numero_container':numero_container, 'tipo':tipo, 'status':status, 'categoria':categoria}



def db_criar_movimentacao(tipo, data_inicio, data_fim, id_container):
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("INSERT INTO movimentacao (tipo, data_inicio, data_fim, id_container) VALUES (?,?,?,?)", [tipo, data_inicio, data_fim, id_container])
        id_movimentacao = cur.lastrowid
        con.commit()
        return {'id_movimentacao':id_movimentacao, 'tipoe': tipo, 'data_inicio':data_inicio,  'data_fim':data_fim, 'id_container':id_container}






def db_lista_container():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute(" SELECT id_container, cliente, numero_container FROM container")
        return rows_to_dict(cur.description, cur.fetchall())



def db_lista_relatario():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT c.id_container, c.cliente, m.tipo FROM container as c INNER JOIN movimentacao as m on c.id_container = m.id_container")
        return rows_to_dict(cur.description, cur.fetchall())



def db_total_categoria():
    with closing(conectar()) as con, closing(con.cursor()) as cur:
        cur.execute("SELECT categoria, count(*) AS total_categoria from container GROUP BY categoria")
        return rows_to_dict(cur.description, cur.fetchall())