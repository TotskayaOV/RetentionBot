from loader import call_db, user_db

def check_work_in_data(date_obj):
    list_data = call_db.get_working_day(date=date_obj)
    result_string = ''
    if list_data:
        for elem in list_data:
            user_list = user_db.get_the_user(id=elem[2])
            if elem[7]:
                result_string += f"№ {elem[2]}. {user_list[1]}\n статус деактивирован\n"
            else:
                result_string += f"№ {elem[2]}. {user_list[1]}\n статус активен\n"
    return result_string

def show_full_data_db(method_db)-> str:
    list_data = method_db()
    result_string = ''
    for tuple_elem in list_data:
        for elem in tuple_elem:
            result_string = result_string + str(elem)
        result_string = result_string + '\n'
    return result_string

def show_date_data_db(method_db, date_obj)-> str:
    list_data = method_db(date=date_obj)
    result_string = ''
    for tuple_elem in list_data:
        for elem in tuple_elem:
            result_string = result_string + str(elem) + ' '
        result_string = result_string + '\n'
    return result_string
