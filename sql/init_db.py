from config.database import get_db_connection, close_db_connection
from sql.schema import SCHEMA_SQL
from sql.drop import DROP_SQL
from sql.seed import seed_for_db

def create_tables():
    conn = get_db_connection()
    if not conn:
        print("Erro ao conectar ao DB.")
        return
    
    try:
        cur = conn.cursor()

        print("-> Limpando tabelas...")
        cur.execute(DROP_SQL)

        print("-> Criando tabelas...")
        cur.execute(SCHEMA_SQL)

        conn.commit()
        print("Tabelas criadas com sucesso!")

    except Exception as e:
        conn.rollback()
        print("Erro ao criar tabelas:", e)

    finally:
        close_db_connection(conn)


def seed_data():
    conn = get_db_connection()
    if not conn:
        print("Erro ao conectar ao DB.")
        return

    try:
        cur = conn.cursor()

        print("-> Inserindo dados de teste...")

        statements = seed_for_db()

        # Executa o INSERT do admin
        admin_query, admin_params = statements[0]
        cur.execute(admin_query, admin_params)

        # Insere produtos
        products_query, _ = statements[1]
        cur.execute(products_query)

        conn.commit()
        print("Dados inseridos com sucesso!")

    except Exception as e:
        conn.rollback()
        print("Erro ao fazer seed:", e)

    finally:
        close_db_connection(conn)

