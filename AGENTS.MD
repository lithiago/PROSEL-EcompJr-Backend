# Criar as tabelas no PostgreSQL

Os models das entidades estão em `src/models/`. O comando abaixo importa todos os
models registrados no pacote e cria no PostgreSQL as tabelas que ainda não existem:

1. Configure no arquivo `.env` a variável `DATABASE_URL` com a URL do PostgreSQL:

   ```env
   DATABASE_URL=postgresql+psycopg://USUARIO:SENHA@HOST:5432/NOME_DO_BANCO
   ```

   Se a senha tiver caracteres especiais, aplique URL encoding nela.
2. Instale as dependências do projeto:

   ```powershell
   pip install -r requirements.txt
   ```
3. Na raiz do repositório, execute:

   ```powershell
   python -m src.create_tables
   ```

O processo é explícito e deve ser executado depois que o banco estiver acessível.
`create_all` cria tabelas ausentes, mas não altera tabelas já existentes nem
substitui migrações de schema. Ao adicionar uma entidade, importe seu model em
`src/models/__init__.py` para que ela seja incluída na criação.