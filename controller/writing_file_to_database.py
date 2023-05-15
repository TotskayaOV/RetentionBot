from datetime import date, time, datetime

from modul import read_mango_file, read_portal_file
from loader import user_db, call_db

# t1 = int(total_seconds / 3600)
# t2 = int((total_seconds - t1 * 3600) / 60)
# t3 = int(total_seconds - t1 * 3600 - t2 * 60)
# time_string = f'{t1}:{t2}:{t3}'
# time_obj2 = datetime.strptime(time_string, '%H:%M:%S').time()

def checking_name_database(name: str):
    """
    проверяет наличие фамилии в БД, в случае отсутствия, записывает
    :param name:
    :return:
    """
    if name == 'Итого':
        return False
    else:
        result_search = user_db.get_the_user(name=name)
        if result_search:
            return result_search[0]
        else:
            user_db.add_user({'name': name, 'status': 'deactivated'})
            return user_db.get_the_user(name=name)[0]

def writing_work_data(date_record: date):
    """
    запись из файла в базу данных производительности сотрудников
    преобразует время в int в секундах
    проверяет наличие записи, в случае наличия, делает перезапись
    через checking_name_database проверяет наличие пользователя в БД и получает его id
    :param date_record: datetime
    """
    raw_data = read_mango_file('./cred/work_time.csv')
    key_tl = ['in_call', 'out_call', 'w_hours', 'train']
    for elem in raw_data:
        user_id = checking_name_database(elem[0].split(" ")[0])
        temp_dict = {}
        if user_id:
            record_db = call_db.get_working_day(date=date_record)
            for point in range(1, len(elem)):
                time_obj = datetime.strptime(elem[point], '%H:%M:%S').time()
                total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
                temp_dict[key_tl[point-1]] = total_seconds
            rewriting_status = False
            if record_db:
                for record in record_db:
                    if record[2] == user_id:
                        rewriting_status = True
                        rec_id = record[0]
            if rewriting_status:
                call_dict = {'incoming_call': temp_dict.get('in_call'), 'outgoing_call': temp_dict.get('out_call'),
                             'working_hours': temp_dict.get('w_hours'), 'training': temp_dict.get('train'), 'wd_id': rec_id}
                call_db.update_working_day(call_dict)
            else:
                call_dict = {'date': date_record, 'user_fk': user_id,
                             'incoming_call': temp_dict.get('in_call'),
                             'outgoing_call': temp_dict.get('out_call'),
                             'working_hours': temp_dict.get('w_hours'),
                             'training': temp_dict.get('train')}
                call_db.add_working_day(call_dict)

def writing_call_data(date_record: date):
    """
    проверяет есть ли записи за заданную дату. если данные есть не производит запись. если нет, то записывает
    новые данные
    время разговора переводится в int  секунд
    :param date_record: datetime
    """
    stop_update = call_db.get_call(date=date_record)
    if len(stop_update) == 0:
        raw_data = read_mango_file('./cred/history_call.csv')
        for elem in raw_data:
            status = elem[0].split(" ")[0]
            time_obj = datetime.strptime(elem[2], '%H:%M:%S').time()
            total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
            if elem[3].isdigit():
                point = int(elem[3])
            else:
                point = 0
            call_db.add_call({'date': date_record, 'time': total_seconds,
                              'point_call': point, 'status': status})


