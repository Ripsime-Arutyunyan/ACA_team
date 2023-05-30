import model


class User(model.Model):
    name = model.CharField()
    last_name = model.CharField()
    age = model.IntegerField()


User.object.create_table()
# User.object.insert(name='Alo', last_name='Bloyan', age=88)
print(User.object.select('name', 'last_name', 'age'))

User.object.update({'name': 'Blo', 'last_name': 'Aloyan', 'age': 90})