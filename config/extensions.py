from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData 

# 1. Define as convenções de nomenclatura para o PostgreSQL
# Garante nomes de tabela em minúsculas (ex: "usuarios" em vez de "Usuarios")
convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# 2. Cria a instância de MetaData com a convenção
metadata = MetaData(naming_convention=convention)

# 3. Inicializa o objeto SQLAlchemy, passando o metadata
# Isso garante que todas as tabelas criadas no models.py usem a convenção de minúsculas
# E que os modelos herdem do db.Model padrão.
db = SQLAlchemy(metadata=metadata)