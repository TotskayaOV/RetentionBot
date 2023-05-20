from .data_base import DataBase


class Airtable(DataBase):
    def __init__(self):
        super().__init__()

    def create_table_airtable_status(self):
        sql = '''CREATE TABLE IF NOT EXISTS airtable_status 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE,
        num_status INTEGER, count_status INTEGER)'''
        self.execute(sql, commit=True)

    def create_table_airtable_comments(self):
        sql = '''CREATE TABLE IF NOT EXISTS airtable_comments 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE,
        num_comm INTEGER, count_comments INTEGER)'''
        self.execute(sql, commit=True)

    def create_table_recorded_leads(self):
        sql = '''CREATE TABLE IF NOT EXISTS recorded_leads 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE,
        date_down DATE, phone_number INTEGER, role_leads VARCHAR, comment INTEGER)'''
        self.execute(sql, commit=True)

    def add_airtable_status(self, user_data: dict):
        parameters = (user_data.get('date'), user_data.get('num_status'),
                      user_data.get('count_status'))
        sql = '''INSERT INTO airtable_status (date, num_status, count_status) 
        VALUES (?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def add_airtable_comments(self, user_data: dict):
        parameters = (user_data.get('date'), user_data.get('num_comm'),
                      user_data.get('count_comments'))
        sql = '''INSERT INTO airtable_comments (date, num_comm, count_comments) 
         VALUES (?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def add_recorded_leads(self, user_data: dict):
        parameters = (user_data.get('date'), user_data.get('phone_number'))
        sql = '''INSERT INTO recorded_leads (date, phone_number) 
        VALUES (?, ?)'''
        self.execute(sql, parameters, commit=True)

    def get_airtable_status(self, **kwargs):
        sql = '''SELECT * FROM airtable_status WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def get_airtable_comment(self, **kwargs):
        sql = '''SELECT * FROM airtable_comments WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def get_recorded_leads(self, **kwargs):
        sql = '''SELECT * FROM recorded_leads WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def update_recorded_leads(self, new_data: dict):
        parameters = (new_data.get('date_down'), new_data.get('comment'),
                      new_data.get('role_leads'), new_data.get('id'))
        sql = '''UPDATE recorded_leads SET date_down=?, comment=?, role_leads=? WHERE id=? '''
        self.execute(sql, parameters, commit=True)
