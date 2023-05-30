import sqlite3
import abc


class AbstractClass(abc.ABC):

    @abc.abstractmethod
    def create_table(self):
        pass

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


class BaseManager(AbstractClass):
    conn = sqlite3.connect('orm_example.db')
    curr = conn.cursor()

    def __init__(self, model_class):
        self.model_class = model_class

    def create_table(self):
        dic = self.model_class.__dict__
        print(dic)
        list_keys = [key for key in dic]
        fields_form = list_keys[1:-1]
        print(f"{','.join(fields_form)}")
        self.curr.execute(f"""CREATE TABLE IF NOT EXISTS {self.model_class.__name__}
                            ({','.join(fields_form)})
                            """)
        self.conn.commit()

    def insert(self, **data):
        print(data)
        fields = [key for key in data.keys()]
        print(', '.join(fields))
        self.curr.execute(f"""INSERT INTO {self.model_class.__name__} ({', '.join(fields)})
                            VALUES (:{', :'.join(fields)})""", data)
        print(f"""({', '.join(fields)}) VALUES (:{', :'.join(fields)})""", data)
        self.conn.commit()

    def select(self, *fields: tuple):
        fields_name = ','.join(fields)
        return self.curr.execute(f"""SELECT {fields_name} FROM {self.model_class.__name__}""").fetchall()

    def update(self, new_data):
        # new_data_fields_form = [key for key in new_data]
        # new_data_form = [value for value in new_data.values()]
        set_query = ", ".join([f"{i[0]} = '{i[1]}'" for i in zip([key for key in new_data],
                                                                 [value for value in new_data.values()])])
        print(set_query)
        self.curr.execute(f"""UPDATE {self.model_class.__name__} SET {set_query}""")
        print(f"""UPDATE {self.model_class.__name__} SET {set_query}""")
        return self.conn.commit()

    def delete(self):
        pass


class MetaModel(type):
    manager_class = BaseManager

    def get_manager(cls):
        return cls.manager_class(model_class=cls)

    @property
    def object(cls):
        return cls.get_manager()


class CharField:
    pass


class IntegerField:
    pass


class Model(metaclass=MetaModel):
    pass
