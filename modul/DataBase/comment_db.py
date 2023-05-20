from .data_base import DataBase


class Comment(DataBase):
    def __init__(self):
        super().__init__()

    def create_table_comments(self):
        sql = '''CREATE TABLE IF NOT EXISTS comments 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, com_name VARCHAR)'''
        self.execute(sql, commit=True)

    def create_table_results(self):
        sql = '''CREATE TABLE IF NOT EXISTS results 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, res_name VARCHAR)'''
        self.execute(sql, commit=True)

    def add_comments(self, new_comm):
        parameters = (new_comm, )
        sql = '''INSERT INTO comments (com_name) 
        VALUES (?)'''
        self.execute(sql, parameters, commit=True)

    def add_results(self, new_comm):
        parameters = (new_comm, )
        sql = '''INSERT INTO results (res_name) 
        VALUES (?)'''
        self.execute(sql, parameters, commit=True)

    def get_comments(self):
        sql = '''SELECT * FROM comments'''
        return self.execute(sql, fetchall=True)

    def get_results(self):
        sql = '''SELECT * FROM results'''
        return self.execute(sql, fetchall=True)

    def get_the_comments(self, **kwargs):
        sql = '''SELECT * FROM comments WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def get_the_results(self, **kwargs):
        sql = '''SELECT * FROM results WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def update_comments(self, new_data: dict):
        parameters = (new_data.get('com_name'), new_data.get('id'))
        sql = '''UPDATE comments SET com_name=? WHERE id=? '''
        self.execute(sql, parameters, commit=True)

    def update_results(self, new_data: dict):
        parameters = (new_data.get('res_name'), new_data.get('id'))
        sql = '''UPDATE results SET res_name=? WHERE id=? '''
        self.execute(sql, parameters, commit=True)

    def remove_comments(self, **kwargs):
        sql = '''DELETE FROM comments WHERE id=?'''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        self.execute(sql, parameters, commit=True)

    def remove_results(self, **kwargs):
        sql = '''DELETE FROM results  WHERE id=?'''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        self.execute(sql, parameters, commit=True)
