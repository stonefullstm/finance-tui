# dao.py
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from models.models import Category
from db.config import SessionLocal
from typing import List, Optional


class CategoryDAO:
    """Data Access Object para a tabela Categories"""

    def __init__(self):
        self.session = SessionLocal()

    def __enter__(self):
        """Método chamado quando entra no bloco 'with'"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Método chamado quando sai do bloco 'with'"""
        if exc_type is not None:
            # Se houve exceção, faz rollback
            self.session.rollback()
        # Sempre fecha a sessão
        self.close()
        # Retorna False para propagar exceções (se houver)
        return False

    def get_all_categories(self) -> List[Category]:
        """Retorna todas as categorias"""
        try:
            categories = self.session.execute(select(Category)).scalars().all()
            return categories
        except SQLAlchemyError as e:
            print(f"Erro ao buscar categorias: {e}")
            return []

    def get_category_by_id(self, category_id: int) -> Optional[Category]:
        """Retorna uma categoria pelo ID"""
        try:
            category = self.session.get(Category, category_id)
            return category
        except SQLAlchemyError as e:
            print(f"Erro ao buscar categoria por ID: {e}")
            return None

    def create_category(self, name: str) -> Optional[Category]:
        """Cria uma nova categoria"""
        new_category = Category(name=name)
        try:
            self.session.add(new_category)
            self.session.commit()
            self.session.refresh(new_category)
            return new_category
        except IntegrityError as e:
            self.session.rollback()
            print(f"Erro de integridade ao criar categoria: {e}")
            return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Erro ao criar categoria: {e}")
            return None

    def update_category(self, category_id: int, new_name: str) -> Optional[Category]:
        """Atualiza o nome de uma categoria existente"""
        try:
            category = self.session.get(Category, category_id)
            if category:
                category.name = new_name
                self.session.commit()
                self.session.refresh(category)
                return category
            else:
                print("Categoria não encontrada")
                return None
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Erro ao atualizar categoria: {e}")
            return None

    def delete_category(self, category_id: int) -> bool:
        """Remove uma categoria pelo ID"""
        try:
            category = self.session.get(Category, category_id)
            if category:
                self.session.delete(category)
                self.session.commit()
                return True
            else:
                print("Categoria não encontrada")
                return False
        except SQLAlchemyError as e:
            self.session.rollback()
            print(f"Erro ao remover categoria: {e}")
            return False

    def get_category_by_name(self, name: str) -> Optional[Category]:
        """Retorna uma categoria pelo nome"""
        try:
            category = (
                self.session.execute(
                    select(Category).where(Category.name == name)
                )
                .scalars()
                .first()
            )
            return category
        except SQLAlchemyError as e:
            print(f"Erro ao buscar categoria por nome: {e}")
            return None

    def close(self):
        """Fecha a sessão do banco de dados"""
        if self.session:
            self.session.close()
