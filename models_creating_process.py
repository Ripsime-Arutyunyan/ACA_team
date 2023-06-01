import models


class User(models.Model):
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=25)
    age = models.IntegerField()


class UserTwo(models.Model):
    first_name = models.CharField
    last_name = models.CharField
    age = models.IntegerField


model_list = [User, UserTwo]


# User.object_.create_()
# User.object.insert(name='Alo', last_name='Bloyan', age=99)
# print(User.object.select('name', 'last_name', 'age'))
# print(User.object.select('name', 'age', name='Blo'))
new_data = {'name': 'Blo', 'last_name': 'Aloyan', 'age': 120}
# User.object.update(new_data)
# User.object.update(new_data, name='Alo')
# User.object.delete(name='Blo')

