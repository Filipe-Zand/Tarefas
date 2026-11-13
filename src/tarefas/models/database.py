from os import getenv
from pathlib import Path
 
import mysql.connector as mc
from dotenv import load_dotenv
from mysql.connector import Error
 
 
class Database:
 
    def __init__(self):
        load_dotenv()
 
        self.host = getenv('DB_HOST')
        self.username = getenv('DB_USER')
        self.password = getenv('DB_PASSWORD')
        self.database = getenv('DB_SCHEMA')
 
        self.connection = None
        self.cursor = None
 
    def conectar(self):
        try:
            self.connection = mc.connect(
                host=self.host,
                database=self.database,
                user=self.username,
                password=self.password
            )
 
            if self.connection.is_connected():
                self.cursor = self.connection.cursor(dictionary=True)
                print('Conexão ao banco realizada com sucesso!')
 
        except Error as e:
            print(f'Erro de conexão: {e}')
            self.connection = None
            self.cursor = None
 
    def desconectar(self):
 
        if self.cursor:
            self.cursor.close()
 
        if self.connection:
            self.connection.close()
 
    def executar(self, sql, params=None):
 
        if not self.connection or not self.cursor:
            print('Conexão com o banco não estabelecida!')
            return None
 
        try:
            self.cursor.execute(sql, params)
 
            if self.cursor.description:
                return self.cursor.fetchall()
 
            self.connection.commit()
            return self.cursor.rowcount
 
        except Error as e:
            print(f'Erro ao executar SQL: {e}')
            self.connection.rollback()
            return None
 
    def __enter__(self):
        self.conectar()
        return self
 
    def __exit__(self, exc_type, exc_value, exc_tb):
        self.desconectar()
 
 
BASE_DIR = Path(__file__).resolve().parent.parent
SQL_PATH = BASE_DIR / 'data' / 'tarefas.sql'
 
 
def init_db(sql_filepath=SQL_PATH):
 
    load_dotenv()
 
    conexao = None
    cursor = None
 
    try:
        conexao = mc.connect(
            host=getenv('DB_HOST'),
            user=getenv('DB_USER'),
            password=getenv('DB_PASSWORD')
        )
 
        cursor = conexao.cursor()
 
        with open(sql_filepath, 'r', encoding='utf-8') as arquivo:
            sql = arquivo.read()
 
        for comando in sql.split(';'):
            if comando.strip():
                cursor.execute(comando)
 
        conexao.commit()
 
        print('Banco de dados inicializado com sucesso!')
 
    except (Error, FileNotFoundError) as e:
        print(f'Erro ao inicializar banco: {e}')
 
    finally:
        if cursor:
            cursor.close()
 
        if conexao:
            conexao.close()