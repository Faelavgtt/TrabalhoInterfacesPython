import sqlite3

from config import DB_DIR, DB_FILE


class Banco:
    def __init__(self):
        DB_DIR.mkdir(exist_ok=True)
        self.conn = sqlite3.connect(DB_FILE)
        self.conn.row_factory = sqlite3.Row
        self.criar_tabelas()

    def executar(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        self.conn.commit()
        return cur

    def listar(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

    def um(self, sql, params=()):
        cur = self.conn.cursor()
        cur.execute(sql, params)
        return cur.fetchone()

    def criar_tabelas(self):
        self.executar("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE NOT NULL,
                senha TEXT NOT NULL
            )
        """)
        self.executar("""
            CREATE TABLE IF NOT EXISTS clientes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cpf TEXT,
                telefone TEXT,
                email TEXT,
                endereco TEXT
            )
        """)
        self.executar("""
            CREATE TABLE IF NOT EXISTS carros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                marca TEXT NOT NULL,
                modelo TEXT NOT NULL,
                placa TEXT,
                ano INTEGER,
                FOREIGN KEY(cliente_id) REFERENCES clientes(id)
            )
        """)
        self.executar("""
            CREATE TABLE IF NOT EXISTS servicos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                descricao TEXT,
                valor REAL DEFAULT 0
            )
        """)
        self.executar("""
            CREATE TABLE IF NOT EXISTS ordens_servico (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cliente_id INTEGER NOT NULL,
                carro_id INTEGER NOT NULL,
                servico_id INTEGER NOT NULL,
                data TEXT NOT NULL,
                status TEXT NOT NULL,
                valor REAL DEFAULT 0,
                observacoes TEXT,
                FOREIGN KEY(cliente_id) REFERENCES clientes(id),
                FOREIGN KEY(carro_id) REFERENCES carros(id),
                FOREIGN KEY(servico_id) REFERENCES servicos(id)
            )
        """)
        self.executar(
            "INSERT OR IGNORE INTO usuarios (usuario, senha) VALUES (?, ?)",
            ("admin", "admin"),
        )
