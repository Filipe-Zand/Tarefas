from os import getenv
from pathlib import Path

import mysql.connector as mc
from dotenv import load_dotenv
from mysql.connector import Error


class Database:
    """
    Classe que gerencia conexões e operações com um banco de dados MySQL.
    """
    def __init__(self):
        load_dotenv()
        self.host = getenv('DB_HOST')
        self.username = getenv('DB_USER')
        self.password = getenv('DB_PASSWORD')
        self.database = getenv('DB_SCHEMA')
        self.connection = None
        self.cursor = None

    def conectar(self) -> None:
        """Estabelece uma conexão com banco de dados MySQL."""
        try:
            self.connection = mc.connect(
                host = self.host,
                database = self.database,
                user = self.username,
                password = self.password
            )

            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print('Conexão ao banco de dados realizada com sucesso!')
        except Error as e:
            print(f'Erro de conexão: {e}')
            self.connection = None
            self.cursor = None

    def desconectar(self) -> None:
        """Encerra a conexão com banco de dados e o cursor, se existirem."""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print('Conexão encerrada com sucesso!')

    def executar(self, sql, params = None):
        """Executa uma instrução no banco de dados."""

        if not self.connection or not self.cursor:
            print('Conexão ao banco de dados não estabelecida')
            return

        try:
            self.cursor.execute(sql, params)       

            if self.cursor.description:
                return self.cursor.fetchall()

            self.connection.commit()
            return self.cursor.rowcount

        except Error as e:
            print(f'Erro de execução: {e}')
            return

    # Método de entrada no contexto (para uso com `with`)
    def __enter__(self):
        self.conectar()
        return self

    # Método de saída de contexto (para uso com `with`)
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.desconectar()

BASE_DIR = Path(__file__).resolve().parent.parent
SQL_PATH = BASE_DIR / "data" / "tarefas.sql"

def init_db(sql_filepath=SQL_PATH):
    """Função responsavel por inicializar o schema (database) 
    no banco de dados."""

    load_dotenv()

    try:
        conexao = mc.connect(
            host = getenv('DB_HOST'),
            user = getenv('DB_USER'),
            password = getenv('DB_PASSWORD')
        )
        cursor = conexao.cursor()

        # Leitura do arquivo de criação do banco
        with open(sql_filepath, 'r', encoding = 'utf-8') as arquivo:
            sql = arquivo.read()

        cursor.execute(sql)
        conexao.commit()

        cursor.close()
        conexao.close()
        print('Schema e tabelas inicializadas com sucesso!')

    except Error as e:
        print(f'Erro no banco de dados: {e}')
    except FileNotFoundError:
        print('O arquivo especificado não pode ser encontrado')


"""Área de testes (51)
Tudo o que for escrito dessa área 
será lido e executado como string.
"""
# db = Database() 
# db.conectar()
# print(db.executar('SHOW DATABASES;'))
# db.desconectar()