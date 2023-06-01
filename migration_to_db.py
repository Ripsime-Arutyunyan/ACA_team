from models_creating_process import model_list

import argparse


class MigrateCommand:

    def __init__(self):

        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("migrate", type=str, help="Migrate all models in base.py to database")
        self.args = self.parser.parse_args()

    @property
    def get_args(self):
        return self.args

    def migrate(self):
        if self.get_args.migrate == "migrate":
            for idx, model in enumerate(model_list, 1):
                print(f'Migration {idx}')
                mig = model.object_
                mig.migrate()
        elif self.get_args.migrate == "show-what-to-migrate":
            print(model_list)


Command = MigrateCommand()
Command.migrate()
