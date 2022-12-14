from pyfolio.repositories.base_repository import BaseRepository
from pyfolio.models.category import Category


class CategoryRepository(BaseRepository):

    model = Category

    def find_by_title(self, title: str):
        return self.db.query(self.model).filter(self.model.title == title).first()
