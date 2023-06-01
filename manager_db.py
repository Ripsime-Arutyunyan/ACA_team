import colorama
import sqlite3
import datetime


class ConnectionSqliteManager:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        print("Connection started ...")
        self.conn = sqlite3.connect(self.filename)
        self.curr = self.conn.cursor()
        return self

    def create_table(self, table_name, fields):
        fields = ", ".join(fields)
        create_command = f"""CREATE TABLE {table_name} ({fields})"""
        try:
            self.curr.execute(create_command)
            print(f"{colorama.Fore.CYAN}{table_name}: created successfully!")
            print(f"{datetime.datetime.now()}: Commit is successful!! {colorama.Style.RESET_ALL} \U0001F44D")
        except sqlite3.Error as er:
            print(f"{colorama.Fore.RED}SQLite ERROR!!: {' '.join(er.args)} {colorama.Style.RESET_ALL} "
                  f"\U0001F612 \U0001F608")

    @property
    def show_tables(self):
        command = """SELECT * FROM sqlite_master WHERE type='table';"""
        return self.curr.execute(command)

    def __exit__(self, type, value, traceback):
        print("Connection ended ...")
        print()
        self.conn.close()


