import csv

def read_mango_file(path: str)  -> list:
    '''
    Метод работает с файлом с данными с манго. Парсит строки, формирует список убирая знак переноса строки в конце
    :param path: путь к файлу
    :return: []
    '''
    working_list = []
    with open(path, 'r', encoding='1251') as file:
        my_list = file.readlines()
        for line in range(1, len(my_list)):
            temp_string = my_list[line]
            temp_string2 = temp_string.rstrip("\n")
            working_list.append(temp_string2.split(';'))
        return working_list

def read_portal_file(path: str)  -> list:
    '''
    Метод работает с файлом с данными с манго. Парсит строки, формирует список убирая знак переноса строки в конце
    :param path: путь к файлу
    :return: []
    '''
    working_list = []
    with open(path, 'r', encoding='UTF-8') as file:
        my_list = file.readlines()
        for line in range(1, len(my_list)):
            temp_string = my_list[line]
            temp_string2 = temp_string.rstrip("\n")
            working_list.append(temp_string2.split(';'))
        return working_list
