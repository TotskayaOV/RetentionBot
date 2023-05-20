from datetime import date, time, datetime
from functools import reduce

from modul import read_mango_file, read_portal_file
from loader import user_db, call_db, air_db, comm_db


def checking_name_database(name: str):
    """
    проверяет наличие фамилии в БД, в случае отсутствия, записывает
    :param name:
    :return:
    """
    name = name.lstrip('"')
    if name == 'Итого':
        return False
    else:
        result_search = user_db.get_the_user(name=name)
        if result_search:
            return result_search[0]
        else:
            user_db.add_user({'name': name, 'status': 'deactivated'})
            return user_db.get_the_user(name=name)[0]

def withheld_check(initial_status: int, dict_result: dict, date_obj: datetime, status_comm: str):
    match initial_status:
        case 3: status_num = 1
        case 4: status_num = 2
    try:
        date_status = datetime.strptime(status_comm, '%d.%m.%Y').date()
        if date_status >= date_obj:
            value_already = dict_result.get(status_num, 0)
            if value_already == 0:
                dict_result[status_num] = 1
            else:
                dict_result[status_num] = value_already + 1
        return dict_result
    except:
        return dict_result


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
    in_successful, in_unsuccessful, out_successful, out_unsuccessful = 0, 0, 0, 0
    time_in, time_in_un, time_successful, time_unsucceful = 0, 0, 0, 0
    dict_numbers = {}
    if len(stop_update) == 0:
        raw_data = read_mango_file('./cred/history_call.csv')
        for elem in raw_data:
            status = elem[0].split(" ")[0]
            time_obj = datetime.strptime(elem[2], '%H:%M:%S').time()
            total_seconds = time_obj.hour * 3600 + time_obj.minute * 60 + time_obj.second
            if status == 'Входящий':
                if total_seconds < 15:
                    in_unsuccessful += 1
                    time_in_un += total_seconds
                else:
                    in_successful += 1
                    time_in += total_seconds
            else:
                dict_numbers[elem[3]] = 0
                if total_seconds < 15:
                    out_unsuccessful += 1
                    time_unsucceful += total_seconds
                else:
                    out_successful += 1
                    time_successful += total_seconds
        count_numbers = len(list(dict_numbers.keys()))
        call_db.add_call({'date': date_record, 'time': time_unsucceful+time_successful,
                          'point_call': 0, 'count_call': count_numbers})
        call_db.add_call({'date': date_record, 'time': time_in,
                          'point_call': 2, 'count_call': in_successful})
        call_db.add_call({'date': date_record, 'time': time_in_un,
                          'point_call': -2, 'count_call': in_unsuccessful})
        call_db.add_call({'date': date_record, 'time': time_unsucceful,
                          'point_call': -1, 'count_call': out_unsuccessful})
        call_db.add_call({'date': date_record, 'time': time_successful,
                          'point_call': 1, 'count_call': out_successful})


def writing_went_on_shift():
    lis_data = read_portal_file('./cred/metabase.csv')
    for elem in lis_data:
        if 2 <= float(elem[10].replace(',', '.')) and 0 < float(elem[13].replace(',', '.')):
            date_obj = datetime.strptime(elem[6], "%d.%m.%Y").date()
            phone = int(elem[0].lstrip('+'))
            role = elem[5]
            result_search = air_db.get_recorded_leads(phone_number=phone)
            if result_search:
                air_db.update_recorded_leads({'date_down': date_obj,
                                              'role_leads': elem[5],
                                              'comment': 1,
                                              'id': result_search[0][0]})


def writing_airtable(date_record: datetime):
    stop_update = air_db.get_airtable_status(date=date_record)
    dict_writing_status = {}
    dict_writing_comment = {}
    if len(stop_update) == 0:
        list_data = read_portal_file('./cred/airtable.csv')
        list_fin_stat = comm_db.get_results()
        list_fin_com = comm_db.get_comments()
        for elem in list_data:
            for record_status in list_fin_stat:
                if elem[1] == record_status[1]:
                    value_already = dict_writing_status.get(record_status[0], 0)
                    if value_already == 0:
                        dict_writing_status[record_status[0]] = 1
                    else:
                        dict_writing_status[record_status[0]] = value_already + 1
                    if record_status[0] == 3 or record_status[0] == 4:
                            if elem[3]:
                                dict_writing_status = withheld_check(record_status[0], dict_writing_status,
                                                                     date_record, elem[3])
            for record_comment in list_fin_com:
                if elem[2] == record_comment[1] and elem[1] == 'Самоотказ':
                    value_already = dict_writing_comment.get(record_comment[0], 0)
                    if value_already == 0:
                        dict_writing_comment[record_comment[0]] = 1
                    else:
                        dict_writing_comment[record_comment[0]] = value_already + 1
            if len(elem) == 5: bool_res = bool(elem[3]) + bool(elem[4])
            else: bool_res = bool(elem[3])
            if bool_res:         # проверяет телефон в базе удержанных и ее статус
                check_db = air_db.get_recorded_leads(phone_number=elem[0])
                if check_db:
                    lst = []
                    for result_check in check_db:
                        if result_check[2]: lst.append(True)
                        elif not result_check[2]: lst.append(False)
                    result = reduce(lambda x, y: x and y, lst)
                    if result:
                        air_db.add_recorded_leads({'date': date_record, 'phone_number': elem[0]})
                else:
                    air_db.add_recorded_leads({'date': date_record, 'phone_number': elem[0]})
        for key, values in dict_writing_status.items():
            air_db.add_airtable_status({'date': date_record, 'num_status': key, 'count_status': values})
        for key, values in dict_writing_comment.items():
            air_db.add_airtable_comments({'date': date_record, 'num_comm': key, 'count_comments': values})
