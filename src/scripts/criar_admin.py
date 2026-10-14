
# scripts/criar_admin_inicial.py

from getpass import getpass

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from src.utils.auth_rules import get_senha_hash
from src.database import SessionLocal
from src.models.usuario import Usuario, UserRole
from src.core.config import ADMIN_NOME, ADMIN_EMAIL, ADMIN_SENHA

def criar_admin_inicial() -> None:
    db = SessionLocal()

    try:
        # Impede que o script seja usado para criar vários administradores.
        admin_existente = db.scalar(
            select(Usuario.id)
            .where(Usuario.role == UserRole.ADMIN)
            .limit(1)
        )

        if admin_existente is not None:
            print("Já existe um administrador cadastrado.")
            print("Use a rota administrativa protegida para criar outros.")
            return

        print("=== Cadastro do primeiro administrador ===")

        nome = ADMIN_NOME
        email = ADMIN_EMAIL
        senha = ADMIN_SENHA

        if not nome or not email or not senha:
            print("Erro: todos os campos são obrigatórios.")
            return


        if len(senha) < 8:
            print("Erro: a senha deve ter pelo menos 8 caracteres.")
            return

        # Utiliza o mesmo mecanismo de hash da aplicação.
        senha_hash = get_senha_hash(senha)

        admin = Usuario(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            role=UserRole.ADMIN,
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

        print("\nAdministrador criado com sucesso!")
        print(f"ID: {admin.id}")
        print(f"Nome: {admin.nome}")
        print(f"E-mail: {admin.email}")
        print(f"Perfil: {admin.role.value}")

    except IntegrityError:
        db.rollback()
        print(
            "Erro: conflito com uma restrição do banco de dados. "
            "Verifique se o e-mail já está cadastrado."
        )

    except SQLAlchemyError as erro:
        db.rollback()
        print(f"Erro ao acessar o banco de dados: {erro}")

    finally:
        db.close()


if __name__ == "__main__":
    criar_admin_inicial()