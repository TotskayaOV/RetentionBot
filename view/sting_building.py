from controller import recorder_lead, result_people_call, result_all_call, processing_statuses
from controller import general_data, reasons_self_denial, reasons_all_stat
from datetime import datetime, date
def string_all_result(date_obj: datetime):
    working_dict = result_people_call(date_obj)
    work_string = f"Количество людей {working_dict.get('work')}\n" \
                  f"Количество отработанных часов: {working_dict.get('time')}\n" \
                  f"Процент времени в разговоре: {working_dict.get('procent')}%\n\n"
    call_dict = result_all_call(date_obj)
    call_string = f"Всего звонков: {call_dict.get('all')}\nВходящий успешный: {call_dict.get('in_s')}\n" \
                  f"Исходящий успешный: {call_dict.get('out_s')}\nИсходящий неуспешный: {call_dict.get('out-u')}\n" \
                  f"Процент дозвона по исходящим: {call_dict.get('perc')}\n\n"
    status_dict = processing_statuses(date_obj)
    status_string = f"Записано на обучение: {status_dict.get('sig_training')}\n" \
                    f"Записано на смену: {status_dict.get('sig_shift')}\nВсего запись: {status_dict.get('sig_all')}\n" \
                    f"Конверсия в запись из диалога: {status_dict.get('conversion_record')}\n\n"
    general_dict = general_data(date_obj)
    general_stirng = f"Звонки в час: {general_dict.get('candidates_per_hour')}\n" \
                     f"Успешные звонки / час: {general_dict.get('successful_calls')}\n" \
                     f"Ср.звонков на кандидата: {general_dict.get('average_calls_candidate')}\n" \
                     f"Всего статусов: {general_dict.get('total_statuses')}\n" \
                     f"Процент самоотказов: {general_dict.get('percentage_self_cancel')}\n" \
                     f"Валидные самоотказы: {general_dict.get('total_valid_cansel')}\n\n"
    result_dict = reasons_all_stat(date_obj)
    res_string = "\nПроставленные статусы:\n"
    if result_dict:
        for k, v in result_dict.items():
            res_string += f"{k}: {v}\n"
    cansel_dict = reasons_self_denial(date_obj)
    record_dict = recorder_lead(date_obj)
    cansel_string = "\nСамоотказы:\n"
    if cansel_dict:
        for k, v in cansel_dict.items():
            cansel_string += f"{k}: {v}\n"
    record_string = f"\nВышли в смену:\n"
    transcription_string = "\n"
    if record_dict:
        for k, v in record_dict.items():
            if type(k) == int:
                transcription_string += f"{k} - {v}\n"
            else:
                record_string += f"{k}: {v}\n"
    return work_string + call_string + status_string + general_stirng + res_string\
        + cansel_string + record_string + transcription_string


