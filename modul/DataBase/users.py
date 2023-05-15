from .data_base import DataBase


class User(DataBase):
    def __init__(self):
        super().__init__()

    def create_table_users(self):
        sql = '''CREATE TABLE IF NOT EXISTS users 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, name VARCHAR, status VARCHAR)'''
        self.execute(sql, commit=True)

    def create_table_users_contacts(self):
        sql = '''CREATE TABLE IF NOT EXISTS contacts_users 
        (fk_users INTEGER PRIMARY KEY, tg_id INTEGER, mango_mail VARCHAR)'''
        self.execute(sql, commit=True)

    def add_user(self, user_data: dict):
        parameters = (user_data.get('name'), user_data.get('status'))
        sql = '''INSERT INTO users (name, status) 
        VALUES (?, ?)'''
        self.execute(sql, parameters, commit=True)

    def add_contacts(self, user_data: dict):
        parameters = (user_data.get('fk_users'), user_data.get('tg_id'), user_data.get('mango_mail'))
        sql = '''INSERT INTO contacts_users (fk_users, tg_id, mango_mail) 
         VALUES (?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def get_user(self):
        sql = '''SELECT * FROM users'''
        return self.execute(sql, fetchall=True)

    def get_the_user(self, **kwargs):
        sql = '''SELECT * FROM users WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def get_the_contact(self, **kwargs):
        sql = '''SELECT * FROM contacts_users WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def update_user_status(self, new_data: dict):
        parameters = (new_data.get('status'), new_data.get('id'))
        sql = '''UPDATE users SET status=? WHERE id=? '''
        self.execute(sql, parameters, commit=True)

    def remove_user(self, **kwargs):
        sql = '''DELETE FROM users WHERE id=?'''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        self.execute(sql, parameters, commit=True)
