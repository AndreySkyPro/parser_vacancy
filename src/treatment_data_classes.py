import json

from src.abstract_classes import AbstractJson


class JsonFile(AbstractJson):
    """Инициализация класса по работе с файлом JSON, базовые функции для обработки
    файлов"""
    def __init__(self, vacansy, all_vacansies):
        self.__filename = f'{vacansy.title()}.json'
        self.all_vacansies = all_vacansies
        self.create_jfile()

    def create_jfile(self):
        """Создание файла со списком вакансий"""

        with open(self.__filename, 'w', encoding='utf-8') as file:
            json.dump(self.all_vacansies, file, ensure_ascii=False, indent=4)

    def load_jfile(self):
        """Загрузка из файла списка вакансий"""

        with open(self.__filename, 'r', encoding='utf-8') as file:
            data = json.load(file)

        return data

    def sorted_vacansies(self, filter_field, filter_value: str, filter_value_1=None):
        """Фильтрация списка вакансий"""

        data = self.load_jfile()
        vacansies = [Vacansy(x['title'], x['employer'], x['url'], x['area'], x['experience'], x['employment'],
                             x['salary'], x['salary_from'], x['salary_to'], x['currency'], x['portal'])
                     for x in data
                     if filter_value in x[filter_field].lower() or filter_value_1 in x[filter_field].lower()
                     ]
        return vacansies

    def not_sorted_vacansies(self):
        """Фильтрация не включена в список вакансий"""

        data = self.load_jfile()
        vacansies = [Vacansy(x['title'], x['employer'], x['url'], x['area'], x['experience'], x['employment'],
                             x['salary'], x['salary_from'], x['salary_to'], x['currency'], x['portal'])
                     for x in data]
        return vacansies


class Vacansy:
    """Инициалзация класса Вакансия по полученным параметрам"""
    __slots__ = ("title", "employer", "url", "area", "experience", "employment", "salary",
                 "salary_from", "salary_to", "currency", "portal")
    def __init__(self, title, employer, url, area, experience, employment, salary,
                 salary_from, salary_to, currency, portal):
        self.title = title
        self.employer = employer
        self.url = url
        self.area = area
        self.experience = experience
        self.employment = employment
        self.salary = salary
        self.salary_from = salary_from
        self.salary_to = salary_to
        self.currency = currency
        self.portal = portal


    def __str__(self):
        if self.salary is False:
            salary_from = 'не указана'
            salary_to = ''
            currency = ''

        else:
            currency = self.currency
            if self.salary_from and self.salary_from != 0:
                salary_from = f'От {self.salary_from}'
            else:
                salary_from = f''
            if self.salary_to and self.salary_to != 0:
                salary_to = f'До {self.salary_to}'
            else:
                salary_to = f''

        return f'Вакансия: {self.title}\nРаботодатель: {self.employer}\nГород: {self.area}\nURL: {self.url}\n' \
               f'Зарплата: {salary_from} {salary_to} {currency}\nОпыт: {self.experience}\n' \
               f'Занятость: {self.employment}\nВакансия с сайта: {self.portal}'