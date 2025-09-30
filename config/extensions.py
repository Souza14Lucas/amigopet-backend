# config/extensions.py
from flask_sqlalchemy import SQLAlchemy

# Inicializa o objeto SQLAlchemy, mas não o associa ao app (app=None)
db = SQLAlchemy()