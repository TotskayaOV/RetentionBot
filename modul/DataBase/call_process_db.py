from .data_base import DataBase


class Call(DataBase):
    def __init__(self):
        super().__init__()

    def create_table_call(self):
        sql = '''CREATE TABLE IF NOT EXISTS history_call 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE,
        time INTEGER, point_call INTEGER, count_call INTEGER)'''
        self.execute(sql, commit=True)

    def create_table_working_day(self):
        sql = '''CREATE TABLE IF NOT EXISTS working_day 
        (wd_id INTEGER PRIMARY KEY AUTOINCREMENT, date DATE,
        user_fk INTEGER, incoming_call INTEGER, outgoing_call INTEGER,
        working_hours INTEGER, training INTEGER, activ_user INTEGER)'''
        self.execute(sql, commit=True)

    def add_call(self, user_data: dict):
        parameters = (user_data.get('date'), user_data.get('time'),
                      user_data.get('point_call'), user_data.get('count_call'))
        sql = '''INSERT INTO history_call (date, time, point_call, count_call) 
        VALUES (?, ?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def add_working_day(self, user_data: dict):
        parameters = (user_data.get('date'), user_data.get('user_fk'), user_data.get('incoming_call'),
                      user_data.get('outgoing_call'), user_data.get('working_hours'), user_data.get('training'))
        sql = '''INSERT INTO working_day (date, user_fk, incoming_call, outgoing_call, working_hours, training) 
        VALUES (?, ?, ?, ?, ?, ?)'''
        self.execute(sql, parameters, commit=True)

    def get_working_day(self, **kwargs):
        sql = '''SELECT * FROM working_day WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def get_call(self, **kwargs):
        sql = '''SELECT * FROM history_call WHERE '''
        sql, parameters = self.extract_kwargs(sql, kwargs)
        return self.execute(sql, parameters, fetchall=True)

    def update_working_day(self, new_data: dict):
        parameters = (new_data.get('incoming_call'), new_data.get('outgoing_call'),
                      new_data.get('working_hours'), new_data.get('training'), new_data.get('wd_id'))
        sql = '''UPDATE working_day SET incoming_call=?, outgoing_call=?, working_hours=?, training=? WHERE wd_id=? '''
        self.execute(sql, parameters, commit=True)

    def update_working_day_user(self, new_data: dict):
        parameters = (new_data.get('activ_user'), new_data.get('user_fk'), new_data.get('date'))
        sql = '''UPDATE working_day SET activ_user=? WHERE user_fk=? AND date=? '''
        self.execute(sql, parameters, commit=True)

    def remove_call(self, date):
        parameters = (date,)
        sql = '''DELETE FROM history_call WHERE date=?'''
        self.execute(sql, parameters, commit=True)

    def remove_working_day(self, date):
        parameters = (date,)
        sql = '''DELETE FROM working_day WHERE date=?'''
        self.execute(sql, parameters, commit=True)

