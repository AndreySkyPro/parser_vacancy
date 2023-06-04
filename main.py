from src.get_data_classes import HHGetVacansies, SJGetVacansies
from src.treatment_data_classes import JsonFile


def any_key():
    return f'Любое другое значение (или просто Enter) - '


def chose_vacancy():
    vacansy = input(f'Введите ключевое слово для поиска вакансии: ').lower()
    return vacansy


def choise_site():
    """Выбор сайта для поиска вакансий
    Возвращает параметр поиска для дальнейшей обработки"""

    user_input = input(f'Для поиска вакансий введите одно из значений:\n'
                       f'1 - поиск только на сайте HeadHanter\n'
                       f'2 - поиск только на сайте SuperJob\n'
                       f'{any_key()}поиск на обоих сайтах\n'
                       f'Ваш выбор: '
                       )
    if user_input == '1':
        choise = '1'
    elif user_input == '2':
        choise = '2'
    else:
        choise = '3'

    return choise


def start_parsing(vacansy, choise):
    """Старт парсинга. Выбор пользователем порталов используемых для поиска"""

    if choise == '1':
        hh = HHGetVacansies(vacansy)
        filtred_vacansies = hh.filtred_vacansies()
    elif choise == '2':
        sj = SJGetVacansies(vacansy)
        filtred_vacansies = sj.filtred_vacansies()
    else:
        hh = HHGetVacansies(vacansy)
        sj = SJGetVacansies(vacansy)
        filtred_vacansies = hh.filtred_vacansies()
        filtred_vacansies.extend(sj.filtred_vacansies())

    return filtred_vacansies


def main():
    print("Здравствуйте!")
    vacansy = chose_vacancy()
    choise = choise_site()
    filtred_vacansies = start_parsing(vacansy, choise)
    print(f'Найдено результатов: {len(filtred_vacansies)}\n\n')

    fh = JsonFile(vacansy, filtred_vacansies)

    choise_filtred = input(f'Вы можете фильтровать вакансии, выбрав одно из значений:\n'
                           f'1 - по городу\n'
                           f'2 - по работодателю\n'
                           f'3 - по опыту работы\n'
                           f'4 - по занятости\n'
                           f'{any_key()}не фильтровать\n'
                           f'Ваш выбор: '
                           )

    if choise_filtred == '1':
        filter_field = 'area'
        filter_value = input('Введите название города: ').lower()
        filter_value_1 = filter_value
        vacansies = fh.sorted_vacansies(filter_field, filter_value, filter_value_1)
    elif choise_filtred == '2':
        filter_field = 'employer'
        filter_value = input('Введите название работодателя: ').lower()
        filter_value_1 = filter_value
        vacansies = fh.sorted_vacansies(filter_field, filter_value, filter_value_1)
    elif choise_filtred == '3':
        filter_field = 'experience'
        userinput = input('Введите желаемый уровень опыта: \n'
                          '1 - "Нет опыта"\n'
                          '2 - "От 1 года до 3 лет"\n'
                          '3 - "От 3 до 6 лет"\n'
                          '4 - "Более 6 лет"\n'
                          'Ваш выбор: ')
        if userinput == '1':
            filter_value = 'нет опыта'
            filter_value_1 = 'без опыта'
        elif userinput == '2':
            filter_value = 'от 1 года до 3 лет'
            filter_value_1 = 'от 1 года'
        elif userinput == '3':
            filter_value = 'от 3 до 6 лет'
            filter_value_1 = 'от 3 лет'
        elif userinput == '4':
            filter_value = 'более 6 лет'
            filter_value_1 = 'от 6 лет'
        else:
            print('Введено некорректное значение, значение будет установлено по дефолту')
            filter_value = ' '
            filter_value_1 = ' '

        vacansies = fh.sorted_vacansies(filter_field, filter_value, filter_value_1)

    elif choise_filtred == '4':
        filter_field = 'employment'
        userinput = input('Введите желаемый уровень занятости: \n'
                          '1 - "Полная занятость"\n'
                          '2 - "Частичная занятость"\n'
                          'Ваш выбор: \n')
        if userinput == '1':
            if choise == '1':
                filter_value = 'полная занятость'
            elif choise == '2':
                filter_value = 'полный рабочий день'
            else:
                print('Введено некорректное значение, значение будет установлено по дефолту')
                filter_value = ' '
        elif userinput == '2':
            if choise == '1':
                filter_value = 'частичная занятость'
            elif choise == '2':
                filter_value = 'сменный график работы'
            else:
                print('Введено некорректное значение, значение будет установлено по дефолту')
                filter_value = ' '
        else:
            print('Введено некорректное значение, значение будет установлено по дефолту')
            filter_value = ' '

        vacansies = fh.sorted_vacansies(filter_field, filter_value)
    else:
        vacansies = fh.not_sorted_vacansies()

    choise_sorted = input(f'Вы можете сортировать вакансии, выбрав одно из значений:\n'
                          f'1 - по минимальной зарплате по убыванию\n'
                          f'2 - по максимальной зарплате по убыванию\n'
                          f'{any_key()}не сортировать')

    if choise_sorted == '1':
        vacansies = sorted(vacansies, key=lambda x: x.salary_to if x.salary_to else 0, reverse=False)
    elif choise_sorted == '2':
        vacansies = sorted(vacansies, key=lambda x: x.salary_to if x.salary_to else 0, reverse=True)

    for vacans in vacansies:
        print(vacans, end='\n\n')

    print(f'Подобрано вакансий: {len(vacansies)}')


if __name__ == '__main__':
    main()
