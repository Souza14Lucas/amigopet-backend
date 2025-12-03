from utils.security import hash_password

def seed_for_db():
    admin_email = "admin@petamigo.com"
    admin_password = hash_password("admin123")

    return [
        #Usuário admin
        (
            """
            INSERT INTO usuarios (nome, email, senha_hash, tipo)
            VALUES (%s, %s, %s, 'admin')
            ON CONFLICT (email) DO UPDATE SET
                nome = EXCLUDED.nome,
                senha_hash = EXCLUDED.senha_hash
            RETURNING id;
            """,
            ("Admin Pet Amigo", admin_email, admin_password)
        ),

        # Mock dos Produtos fictícios
        (
            """
            INSERT INTO produtos (nome, descricao, preco, categoria, estoque, imagem_url, especie)
            VALUES 
                ('Ração Premium para Cães Adultos', 'Ração seca super premium sabor frango para cães adultos de raças médias. Nutrição completa e balanceada.', 159.90, 'Rações', 50, 'https://place-pet.com/dog-food.png', 'Cachorros'),
                ('Arranhador Torre para Gatos', 'Arranhador de sisal com 3 andares, bolinha e toca. Ideal para o entretenimento e saúde das unhas do seu gato.', 249.90, 'Brinquedos', 40, 'https://place-pet.com/rope-ball.png', 'Gatos'),
                ('Coleira de Couro para Cães', 'Coleira de couro legítimo com fivela de metal reforçada. Confortável e durável.', 89.90, 'Acessórios', 60, 'https://place-pet.com/coleira.png', 'Cachorros'),
                ('Shampoo Neutro Hipoalergênico', 'Shampoo para cães e gatos com pele sensível. Limpa suavemente sem agredir a pele.', 45.50, 'Higiene', 30, 'https://place-pet.com/shampoo.png', 'Geral'),
                ('Antipulgas e Carrapatos', 'Medicamento em comprimidos para administração oral. Protege seu pet contra pulgas e carrapatos.', 75.00, 'Medicamentos', 40, 'https://place-pet.com/antipulgas.png', 'Geral'),
                ('Ração Seca para Gatos Sabor Salmão', 'Ração seca sabor salmão. Uma refeição deliciosa e nutritiva para seu felino.', 89.99, 'Rações', 60, 'https://place-pet.com/racaosalmao.png', 'Cachorros'),
                ('Bolinha de Tênis para Cães', 'Pacote com 3 bolinhas de tênis resistentes, perfeitas para brincadeiras de buscar.', 29.90, 'Brinquedos', 30, 'https://place-pet.com/bolinhatenis.png', 'Cachorros'),
                ('Gaiola para Pássaros', 'Gaiola espaçosa com comedouros, bebedouro e poleiros. Fácil de limpar.', 199.90, 'Acessórios', 40, 'https://place-pet.com/gaiola.png', 'Geral'),
                ('Aquário de Vidro 20L', 'Aquário completo com filtro e iluminação LED. Perfeito para iniciantes na aquariofilia.', 350.00, 'Acessórios', 50, 'https://place-pet.com/aquario.png', 'Geral'),
                ('Roda de Exercícios para Hamster', 'Roda silenciosa para exercícios. Essencial para a saúde e bem-estar de pequenos roedores.', 55.00, 'Brinquedos', 20, 'https://place-pet.com/rodahamster.png', 'Roedores'),
                ('Cama Aconchegante para Gatos', 'Cama tipo toca, super macia e fofa para gatos. Proporciona um sono tranquilo e seguro.', 139.90, 'Acessórios', 40, 'https://place-pet.com/camagatos.png', 'Gatos'),
                ('Tapete Higiênico Super Absorvente', 'Pacote com 30 unidades de tapetes higiênicos com atrativo canino e alta absorção.', 69.90, 'Acessórios', 50, 'https://place-pet.com/tapete.png', 'Geral');
            """,
            None
        ),
        ]
