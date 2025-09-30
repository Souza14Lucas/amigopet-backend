from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

# Define as convenções de nomenclatura para o PostgreSQL
# (Garante nomes de tabela em minúsculas e singulares)
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# 1. Cria a base de declaração do ORM ANTES de instanciar o SQLAlchemy
# Passamos o metadata=None e a convenção
Base = declarative_base(naming_convention=convention)

# 2. Inicializa o objeto SQLAlchemy e o objeto Base
db = SQLAlchemy(model_class=Base)

# 3. CRUCIAL: Agora, garantimos que a Base use o metadata do db
Base.metadata = db.metadata