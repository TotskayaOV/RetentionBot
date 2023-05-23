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