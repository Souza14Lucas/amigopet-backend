from app import app, db
from config.models import Usuario, Produto, PedidoCompra, ItemPedido # Todos os modelos
from utils.security import hash_password

# --- CÓDIGO DE SETUP DE TABELAS ---
with app.app_context():
    print("-> Iniciando setup de tabelas...")
    
    # Cria as tabelas se não existirem
    db.create_all()
    print("✅ Tabelas criadas ou verificadas.")

    # Insere o Admin se ele não existir
    admin_email = "admin@petamigo.com"
    if not Usuario.query.filter_by(email=admin_email).first():
        admin_user = Usuario(nome="Lucas de Souza", email=admin_email, senha_hash=hash_password("admin123"), tipo='admin')
        db.session.add(admin_user)
        db.session.commit()
        print("✅ Admin inserido.")
    else:
        print("Admin já existe.")