# config/database.py
import psycopg2
import os
from dotenv import load_dotenv

# Garantimos que as variáveis de ambiente sejam carregadas aqui também
load_dotenv() 

def get_db_connection():
    """Cria e retorna uma nova conexão com o banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=os.getenv('DB_PORT')
        )
        return conn
    except psycopg2.Error as e:
        # Imprime o erro caso haja falha na conexão (útil para debug)
        print(f"❌ Erro ao conectar ao PostgreSQL. Detalhes: {e}", flush=True)
        return None

def close_db_connection(conn):
    """Fecha a conexão com o banco de dados, se ela existir."""
    if conn:
        conn.close()