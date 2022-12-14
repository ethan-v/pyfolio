from pyfolio.repositories.base_repository import BaseRepository
from pyfolio.models.setting import Setting


class SettingRepository(BaseRepository):

    model = Setting

    def find_by_name(self, name: str):
        return self.db.query(self.model).filter(self.model.name == name).first()

    def find_by_key(self, key: str):
        return self.db.query(self.model).filter(self.model.key == key).first()

    def get_formatted(self):
        items = self.get()
        data_dict = {}
        if len(items):
            data_dict = {x.key: x.value for x in items}
        return data_dict

