# init_db.py
from config.database import get_db_connection, close_db_connection
from utils.security import hash_password 
import psycopg2.extras
import sys # Importação necessária!

def seed_data():
    conn = None 
    try:
        conn = get_db_connection()
        if conn is None:
            print("Não foi possível conectar ao DB para popular os dados.", flush=True)
            return

        cur = conn.cursor()

        # 1. Cria um usuário ADMINISTRADOR para testes
        print("-> Inserindo usuário administrador...", flush=True)
        admin_email = "admin@petamigo.com"
        admin_senha_hash = hash_password("admin123") 
        
        # Insere/Atualiza o usuário Admin
        cur.execute("""
            INSERT INTO usuarios (nome, email, senha_hash, tipo) 
            VALUES (%s, %s, %s, 'admin') 
            ON CONFLICT (email) DO UPDATE SET nome = EXCLUDED.nome, senha_hash = EXCLUDED.senha_hash
            RETURNING id;
        """, ("Admin Pet Amigo", admin_email, admin_senha_hash))
        
        admin_id = cur.fetchone()[0]

        # 2. Insere 5 Produtos Fictícios
        print("-> Inserindo 5 produtos fictícios...", flush=True)
        produtos_ficticios = [
            ("Ração Premium", "Ração de alta performance, 15kg.", 129.90, "Ração", 50, admin_id),
            ("Bola de Corda", "Bola de corda resistente para cães.", 19.99, "Brinquedos", 200, admin_id),
            ("Shampoo Gatos", "Frasco de 500ml, hipoalergênico.", 35.00, "Higiene", 80, admin_id),
            ("Coleira Azul", "Coleira de nylon para filhotes.", 25.50, "Acessórios", 150, admin_id),
            ("Consulta Veterinária", "Serviço de check-up geral.", 90.00, "Serviços", 999, admin_id),
        ]
        
        # Limpa produtos existentes antes de inserir (Garantiu o DROP TABLE em create_tables)
        # O INSERT a seguir é mais simples, sem o ON CONFLICT.
        for nome, desc, preco, cat, estoque, fornecedor_id in produtos_ficticios:
            cur.execute("""
                INSERT INTO produtos (nome, descricao, preco, categoria, estoque, fornecedor_id)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (nome, desc, preco, cat, estoque, fornecedor_id))
        
        
        # 3. Confirma e Salva
        conn.commit()
        print("✅ COMMIT REALIZADO.", flush=True) # Mensagem para confirmar que o commit ocorreu

        # 4. VERIFICAÇÃO FINAL APÓS O COMMIT (Lê o que foi salvo)
        cur.execute("SELECT COUNT(*) FROM produtos;")
        count = cur.fetchone()[0]
        print(f"VERIFICAÇÃO: {count} produtos encontrados na tabela após o commit.", flush=True)

    except Exception as e:
        print(f"❌ ERRO GRAVE DURANTE O SEEDING: {e}", flush=True)
        if conn:
            conn.rollback() # Garante que nada parcialmente criado seja salvo
    
    finally:
        close_db_connection(conn)

# ... (bloco if __name__ == '__main__':) ...