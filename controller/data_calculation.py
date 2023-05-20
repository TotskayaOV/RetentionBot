from datetime import datetime, date
from loader import call_db, air_db, comm_db

# time_obj = datetime.strptime(time_string, '%H:%M:%S').time()

def time_conversion(number):
    """
    преобразует время из секунд в формат HH:MM:SS
    :param number: int
    :return: string
    """
    hour_t1 = int(number / 3600)
    minute_t2 = int((number - hour_t1 * 3600) / 60)
    second_t3 = int(number - hour_t1 * 3600 - minute_t2 * 60)
    time_string = f'{hour_t1}:{minute_t2}:{second_t3}'
    return time_string
def result_people_call(date_obj: datetime):
    """
    count_people - Кол-во людей
    quantity_hours - Кол-во отработанных часов
    procent_talk - % времени в разговоре (Суммарное время принятых групповых вызовов + Суммарное время
                                            совершенных вызовов) / (Суммарное рабочее время - Суммарное
                                            время Обучение).

    :param date_obj:
    :return: dict {'work': count_people, 'time': time_conversion(quantity_work_hours), 'procent': procent_talk}
    """
    list_data = call_db.get_working_day(date=date_obj)
    if list_data:
        count_people = len(list_data)
        quantity_work_hours = 0
        duration_call = 0
        quantity_train_hours = 0
        for elem in list_data:
            quantity_work_hours += elem[5]
            duration_call += elem[3] + elem[4]
            quantity_train_hours += elem[6]
        procent_talk = round((duration_call/(quantity_work_hours-quantity_train_hours))*100, 2)
        return {'work': count_people, 'time': time_conversion(quantity_work_hours), 'procent': procent_talk}
    else:
        return {'work': 0}

def result_all_call(date_obj):
    """
    all_call - всего звонков
    in_successful- входящий успешный
    out_successful- исходящий успешный
    out_unsuccessful- исходящий неуспешный
    dial_up_percent - % дозвона по исходящим
    :param date_obj: datetime
    :return: dict: {'all': all_call, 'in_s': in_successful, 'in_u': in_unsuccessful, 'uniq': uniq_numbers,
                    'out_s': out_successful, 'out-u': out_unsuccessful, 'perc': dial_up_percent}
    """
    list_data = call_db.get_call(date=date_obj)
    all_call = 0
    in_successful, in_unsuccessful, out_successful, out_unsuccessful, dial_up_percent, uniq_numbers = 0, 0, 0, 0, 0, 0
    if list_data:
        for elem in list_data:
            match elem[3]:
                case 2: in_successful = elem[4]
                case 1: out_successful = elem[4]
                case 0: uniq_numbers = elem[4]
                case -1: out_unsuccessful = elem[4]
                case -2: in_unsuccessful = elem[4]
        all_call = in_successful + in_unsuccessful + out_successful + out_unsuccessful
        dial_up_percent = round(out_successful/(out_unsuccessful+out_successful)*100, 2)
        uniq_numbers = round((out_successful + out_unsuccessful) / uniq_numbers, 2)
    return {'all': all_call, 'in_s': in_successful, 'in_u': in_unsuccessful, 'uniq': uniq_numbers,
            'out_s': out_successful, 'out-u': out_unsuccessful, 'perc': dial_up_percent}

def processing_statuses(data_obj: datetime):
    """
    sig_trainig - Направлен на обучение
    sig_shift - Записано на смену
    sig_all -Всего запись
    conversion_record - Конверсия в запись из диалога (Всего запись / сумму вход. усп. и исход. усп. звонков)
    :param data_obj: datetime. date()
    :return:
    """
    list_data = air_db.get_airtable_status(date=data_obj)
    sig_training, sig_shift, sig_all, conversion_record = 0, 0, 0, 0
    if list_data:
        for elem in list_data:
            match elem[2]:
                case 1: sig_training = elem[3]
                case 2: sig_shift = elem[3]
        sig_all = sig_training + sig_shift
        data_call = result_all_call(data_obj)
        if data_call.get('in_s', 0) != 0 or data_call.get('out_s', 0) != 0:
            conversion_record = round((sig_all / (data_call.get('in_s', 0) + data_call.get('out_s', 0))) * 100, 2)
    return {'sig_training': sig_training, 'sig_shift': sig_shift,
            'sig_all': sig_all, 'conversion_record': conversion_record}

def general_data(date_obj: datetime):
    """
    candidates_per_hour - Общее кол-во звонков / Кол-во отработанных часов
    successful_calls - (входящий успешный + исходящий успешный)/ кол-во отработанных часов
    average_calls_candidate - Ср. звонков на кандидата (Сейчас делаем сводную по всем исходящим,
                                смотрим среднее значение, исключая sip) статусы/исходящие
    total_statuses - Общее кол-во статусов
    percentage_self_cancel - Кол-во самоотказов / "всего" финальных статусов
    total_valid_cansel -  Общее кол-во самоотказов минус самоотказы по причине Не выходит на связь более 3 дней
    quantity_work_hours - количество отработанных часов
    :param data_obj:
    :return: {'candidates_per_hour': candidates_per_hour, 'successful_calls': successful_calls,
            'average_calls_candidate': average_calls_candidate, 'total_statuses': total_statuses,
            'percentage_self_cancel': percentage_self_cancel, 'total_valid_cansel': total_valid_cansel}
    """
    candidates_per_hour = 0
    successful_calls = 0
    percentage_self_cancel = 0
    reasons_self_denial = 0
    total_statuses = 0
    quantity_work_hours = 0
    total_out_calls = 0
    total_cansel = 0
    total_valid_cansel = 0
    all_calls = 0
    res_pc = call_db.get_working_day(date=date_obj)
    if res_pc:
        for elem in res_pc:
            quantity_work_hours += elem[5]
        quantity_work_hours = int(round(quantity_work_hours / 3600, 0))
    list_statuses = air_db.get_airtable_status(date=date_obj)
    if list_statuses:
        for record_st in list_statuses:
            if record_st[2] == 13:
                total_cansel += record_st[3]
            if record_st[2] > 2:
                total_statuses += record_st[3]
    succ_list = call_db.get_call(date=date_obj)
    if succ_list:
        for calls_st in succ_list:
            if calls_st[3] == 1 or calls_st == -1:
                total_out_calls += calls_st[4]
            if calls_st[3] > 0:
                successful_calls += calls_st[4]
            if calls_st[3] == 0:
                all_calls += calls_st[4]
    list_comment = air_db.get_airtable_comment(date=date_obj)
    if list_comment:
        for comm_st in list_comment:
            if comm_st[2] > 1 and comm_st != 11:
                total_valid_cansel += comm_st[3]
    # рассчет данных
    if quantity_work_hours:
        candidates_per_hour = round(all_calls / quantity_work_hours, 2)
        successful_calls = round(successful_calls / quantity_work_hours, 2)
    if total_statuses:
        percentage_self_cancel = round((total_valid_cansel / total_statuses) * 100, 2)
    if total_out_calls:
        average_calls_candidate = round(total_statuses / total_out_calls, 2)
    return {'candidates_per_hour': candidates_per_hour, 'successful_calls': successful_calls,
            'average_calls_candidate': average_calls_candidate, 'total_statuses': total_statuses,
            'percentage_self_cancel': percentage_self_cancel, 'total_valid_cansel': total_valid_cansel}

def reasons_self_denial(date_obj: datetime):
    res_comm = air_db.get_airtable_comment(date=date_obj)
    dict_comment = {}
    if res_comm:
        for elem in res_comm:
            name_status = comm_db.get_the_comments(id=elem[2])
            dict_comment[name_status[1]] = elem[3]
    return dict_comment

def recorder_lead(date_obj: datetime):
    list_recorder = air_db.get_recorded_leads(date_down=date_obj)
    dict_recorder = {}
    count_rec = 0
    if list_recorder:
        for elem in list_recorder:
            check_role = dict_recorder.get(elem[4], 0)
            if check_role:
                dict_recorder[elem[4]] = check_role + 1
            else:
                dict_recorder[elem[4]] = 1
            count_rec += 1
        dict_recorder['Вышло всего'] = count_rec
    return dict_recorder

def reasons_all_stat(date_obj: datetime):
    res_stat = air_db.get_airtable_status(date=date_obj)
    dict_comment = {}
    if res_stat:
        for elem in res_stat:
            name_status = comm_db.get_the_results(id=elem[2])
            dict_comment[name_status[1]] = elem[3]
    return dict_comment
