from copy import deepcopy


# Преобразуем элементы стр в числа (ТОЛЬКО ДЛЯ НАЧАЛЬНОГО БАЗИСА)
def getListFloatOdds(str_temp, ex=None):
    try:
        result = list()
        for i in str_temp.split(";"):
            if i == "":
                continue
            result.append(float(i))
        return result
    except ex:
        return ex


# Получаем канонический вид уравнения (ТОЛЬКО ДЛЯ НАЧАЛЬНОГО БАЗИСА)
def getCanonicalViewCondition(list_odds_condition, list_condition, index):
    result = list_odds_condition
    for i in range(len(list_condition)):
        if i == index:
            if list_condition[index] == "<=" or list_condition[index] == "=":
                result.append(float(1))
            else:
                result.append(float(-1))
        else:
            result.append(float(0))
    return result


# Присоединяем свободные элементы (ТОЛЬКО ДЛЯ НАЧАЛЬНОГО БАЗИСА)
def connectFreeElement(list_odds, list_condition, list_free_odds):
    result = list_odds
    for _, i in enumerate(list_condition):
        # это условие связано с r_i, где i = 1,2,3 ...
        if list_condition[_] == "=>":
            for index, j in enumerate(list_odds):
                if index == _:
                    result[index].append(float(1))
                else:
                    result[index].append(float(0))
    for _, i in enumerate(list_free_odds):
        result[_].append(list_free_odds[_])
    return result


# Заполняет строку функции(F) начального базиса (ТОЛЬКО ДЛЯ НАЧАЛЬНОГО БАЗИСА)
def getRowFunction(list_odds_function, int_value, str_extremum, last_element=0):
    result = list()
    if str_extremum == "max":
        for i in list_odds_function:
            result.append(i * (-1))
        for i in range(int_value - len(list_odds_function) - 1):
            result.append(float(0))
        result.append(float(last_element))
    else:
        result = list_odds_function
        for i in range(int_value - len(list_odds_function) - 1):
            result.append(float(0))
        result.append(float(last_element))
    return result


# получаем начальную базисную таблицу
def getDictBasic(str_function, str_extremum, list_str_odds, list_condition, list_str_free_element):
    # Список членов функций при переменных
    list_odds_function = getListFloatOdds(str_function)
    # Список челенов в условиях при переменных
    list_odds_condition = list()
    # Список свободных членов
    list_free_element = list()
    # Начальная базисная таблица, дальше - НБТ
    dict_basic = dict()

    # Цикл заполняющий "list_free_element" и "list_odds_condition"
    for _, i in enumerate(list_str_odds):
        list_odds_condition.append(getListFloatOdds(i))
        list_free_element.append(float(list_str_free_element[_]))
    # Условие определяющие к чему стримиться фукция

    # Приводим к каноническому виду условия
    for _, i in enumerate(list_odds_condition):
        list_odds_condition[_] = getCanonicalViewCondition(i, list_condition, _)

    # Присоединяем свободные элементы
    list_odds_condition = connectFreeElement(list_odds_condition, list_condition, list_free_element)

    # Заполняем НБТ (X_, R_)
    r = 1
    dict_basic["Basic"] = list()
    for i in range(len(list_odds_function) + len(list_odds_condition)):
        dict_basic["Basic"].append("X_" + str(i + 1))
    for _, i in enumerate(list_odds_condition):
        if list_condition[_] == "<=" or list_condition[_] == "=":
            dict_basic["X_" + str(_ + len(list_odds_function) + 1)] = i
        elif list_condition[_] == "=>":
            dict_basic["Basic"].append("R_" + str(r))
            dict_basic["R_" + str(r)] = i
            r += 1
    # Заполняем строку "F" в НБТ
    dict_basic["F"] = getRowFunction(list_odds_function, len(list_odds_condition[0]), str_extremum)

    # Продолжаем заполняем НБТ (W_)
    w = 1
    for _, i in enumerate(list_condition):
        if i == "=>":
            temp_row = list()
            for j in list_odds_condition[_]:
                temp_row.append(j * (-1))
            temp_row[-2] = float(0)
            dict_basic["W_" + str(w)] = temp_row
            w += 1

    # Определяем ведущую строку
    name_row = list(dict_basic.keys())[-1]
    leading_column = dict_basic[name_row].index(min(dict_basic[name_row][0:-1]))

    # Считаем столбец отношений
    dict_basic["Basic"].append("Free element")
    dict_basic["Basic"].append("Attitude")
    for i in dict_basic:
        if str(i) == "Basic":
            continue
        dict_basic[i].append(getAttitude(dict_basic[i][-1], dict_basic[i][leading_column]))
    return dict_basic


# Заполяняет столбец "Отношение"
def getAttitude(float_free_element, float_element_main_row):
    result = 0
    if float_free_element <= 0 or float_element_main_row <= 0:
        return None
    result = float_free_element/float_element_main_row
    return result


# правило треугольника
def roleTriangle(past_element_1, past_element_2, past_element_3):
    result = past_element_1 - (past_element_2 * past_element_3)
    return result


# Получаем главный элемент, номер строки и столбца главного элемента
def getMainElement(dict_basic):
    # Номер строки и столбца и элемент этого индекса
    result = list()

    # Номер стобца
    name_row = list(dict_basic.keys())[-1]
    leading_column = dict_basic[name_row].index(min(dict_basic[name_row][0:-2]))

    # Номер строки
    str_key = ""
    temp_value = 0
    for i in dict_basic:
        if str(i.title()) == "Basic":
            continue
        if dict_basic[i.title()][-1] is not None:
            temp_value = dict_basic[i.title()][-1]
            str_key = i.title()
            break

    for i in dict_basic:
        if str(i.title()) == "Basic":
            continue
        if dict_basic[i.title()][-1] is not None and temp_value > dict_basic[i.title()][-1]:
            temp_value = dict_basic[i.title()][-1]
            str_key = i.title()
    leading_row = list(dict_basic.keys()).index(str_key)

    # Добавление элементов
    result.append(dict_basic[str_key][leading_column])
    result.append(leading_column)
    result.append(leading_row)
    return result


# Провверка столбца "Отношение" на неопределенные значения
def validAttitude(dict_basic):
    result = True
    for i in dict_basic:
        if i == "Basic":
            continue
        if dict_basic[i][-1] is not None:
            return False
    return result


def getIntitle(list_odds, denominator):
    result = list()
    if denominator == 1:
        return list_odds
    for i in list_odds:
        result.append(i/denominator)
    return result


def validOnDelFunc(list_odds, int_index):
    result = True
    for i in range(len(list_odds)):
        if i == int_index:
            if list_odds[i] == 1:
                continue
            else:
                result = False
                break
        if list_odds[i] != 0:
            result = False
            break
    return result


def dropRow(dict_basic):
    result = deepcopy(dict_basic)
    value = 0

    # Ищем псевдофункции
    for _, i in enumerate(dict_basic["Basic"]):
        if i[0] == "R":
            value += 1

    # если value равно ноль значит в таблице нет псевдофункий
    if value == 0:
        return dict_basic

    # ищем строки которые нужно дропнуть, если таковые есть
    for i in range(value):
        list_odds = dict_basic["W_" + str(i + 1)][0:-1]
        int_index = dict_basic["Basic"].index("R_" + str(i + 1))
        if validOnDelFunc(list_odds, int_index):
            for j in dict_basic:
                if j == "Basic":
                    del result[j][int_index]
                    continue
                if j == "W_" + str(i + 1):
                    del result["W_" + str(i + 1)]
                    continue
                temp_list = list()
                for k in range(len(dict_basic[j])):
                    if k == int_index:
                        continue
                    temp_list.append(dict_basic[j][k])
                result[j] = temp_list
    return result


def validFunction(list_function):
    result = False
    for i in list_function:
        if 0 > i:
            return result
    return True


def getNewDictBasic(dict_basic):
    result = dict()

    # [0] - главный элемент, [1] - номер столбцаб, [2] - номер строки
    main_element = getMainElement(dict_basic)

    # шапка таблицы
    result["Basic"] = dict_basic["Basic"]

    # список коэффициентов для подсчета новых элементов для таблицы
    list_row = dict_basic[list(dict_basic.keys())[main_element[2]]][0:-1]
    row_coefficient = getIntitle(list_row, main_element[0])

    # Считаем костяк таблицы
    for _, i in enumerate(dict_basic):
        if str(i) == "Basic":
            continue
        if _ == main_element[2]:
            str_key = result["Basic"][main_element[1]]
            result[str_key] = row_coefficient
            continue
        temp_row = list()
        for __, j in enumerate(dict_basic[i][0:-1]):
            y = row_coefficient[__]
            temp_row.append(roleTriangle(j, y, dict_basic[i][main_element[1]]))
        result[i] = temp_row

    # Проверяем можем ли удалить псевдофункции (Если таковые есть)
    result = dropRow(result)

    # Считаем столбец отношений
    name_row = list(result.keys())[-1]
    leading_column = result[name_row].index(min(result[name_row][0:-1]))
    for i in result:
        if i == "Basic":
            continue
        result[i].append(getAttitude(result[i][-1], result[i][leading_column]))

    return result


func = "1;2"
extremum = "max"
odd = ["-1;1", "1;-2", "1;1"]
condition = ["<=", "<=", "<="]
free_e = ["1", "1", "3"]
"""
func = "-1;2"
extremum = "max"
odd = ["1;1", "2;1"]
condition = ["<=", "=>"]
free_e = ["2", "1"]

func = "-6;4;4"     
extremum = "min"
odd = ["-3;-1;1", "-2;-4;1"]
condition = ["<=", "=>"]
free_e = ["2", "3"]
"""

basic = getDictBasic(func, extremum, odd, condition, free_e)

while True:
    if validAttitude(basic):
        print("break")
        break
    if validFunction(basic["F"][0:-1]):
        break
    basic = getNewDictBasic(basic)
    pass

print(basic)