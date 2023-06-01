from manager_db import ConnectionSqliteManager
from settings_db import DATABASES
# from models_creating_process import model_list

import sqlite3
import abc


class AbstractClass(abc.ABC):

    @abc.abstractmethod
    def insert(self):
        pass

    @abc.abstractmethod
    def select(self):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def delete(self):
        pass


class CharField:
    def __init__(self, **max_length):
        self.max_length = max_length
        # print(self.__dict__)


class BaseManager(AbstractClass):
    conn = sqlite3.connect(DATABASES['NAME'])
    curr = conn.cursor()

    def __init__(self, model_class):
        self.model_class = model_class
        self.table_name = self.model_class.__name__

    # def create_table(self):
    #     dic = self.model_class.__dict__
    #     # print(dic)
    #     list_keys = [key for key in dic]
    #     fields_form = list_keys[1:-1]
    #     # print(f"{','.join(fields_form)}")
    #     self.curr.execute(f"""CREATE TABLE IF NOT EXISTS {self.model_class.__name__}
    #                         ({','.join(fields_form)})
    #                         """)
    #     self.conn.commit()

    def insert(self, **data: dict):
        fields = [key for key in data.keys()]
        # print(', '.join(fields))
        self.curr.execute(f"""INSERT INTO {self.table_name} ({', '.join(fields)})
                            VALUES (:{', :'.join(fields)})""", data)
        # print(f"""({', '.join(fields)}) VALUES (:{', :'.join(fields)})""", data)
        self.conn.commit()

    def select(self, *fields: tuple, **kwargs: dict):
        fields_name = ','.join(fields)
        query = [f'{key} = "{value}"' for key, value in kwargs.items()]
        # print(''.join(query))
        if kwargs:
            return self.curr.execute(f"""SELECT {fields_name} FROM {self.table_name}
                                        WHERE {''.join(query)}""").fetchall()
        return self.curr.execute(f"""SELECT {fields_name} FROM {self.table_name}""").fetchall()

    def update(self, *new_data, **kwargs):
        # new_data_fields_form = [key for key in new_data]
        # new_data_form = [value for value in new_data.values()]
        set_query = ", ".join([f"{i[0]} = '{i[1]}'" for i in zip([key for key in new_data[0]],
                                                                 [value for value in new_data[0].values()])])
        query = [f'{key} = "{value}"' for key, value in kwargs.items()]
        if kwargs:
            self.curr.execute(f"""UPDATE {self.table_name} SET {set_query} WHERE {''.join(query)} """)
        # print(set_query)
        else:
            self.curr.execute(f"""UPDATE {self.table_name} SET {set_query}""")
        # print(f"""UPDATE {self.model_class.__name__} SET {set_query}""")
        return self.conn.commit()

    def delete(self, **kwargs):
        query = [f'{key} = "{value}"' for key, value in kwargs.items()]
        self.curr.execute(f"""DELETE FROM {self.table_name} WHERE {''.join(query)}""")
        return self.conn.commit()


class Migrate:
    def __init__(self, models_list):
        self.models_list = models_list
        self.table_name = self.models_list.__name__
        dic = self.models_list.__dict__
        list_keys = [key for key in dic]
        self.fields_form = list_keys[1:-1]

    def migrate(self):
        print("Begin database Migration ...")
        print(f"**{self.table_name}** Migration")
        db_name = DATABASES['NAME']
        with ConnectionSqliteManager(db_name) as Connection:
            Connection.create_table(table_name=self.table_name, fields=self.fields_form)


class MetaModel(type):
    manager_class = BaseManager
    model_class = Migrate

    def get_migrate(cls):
        return cls.model_class(models_list=cls)

    def get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def object_(cls):
        return cls.get_migrate()

    @property
    def object(cls):
        return cls.get_manager()


class IntegerField:
    pass


class Model(metaclass=MetaModel):
    def __init__(self):
        pass
        # self.table_name = self.__class__.__name__
        # setattr(self, 'table_name', self.table_name)
        # # print(self.__dict__)

    # def __repr__(self):
    #     return self.__dict__['table_name']


