import os
import requests
from src.abstract_classes import AbstractAPI


class HHGetVacansies(AbstractAPI):
    """Получает вакансии по API с сайта HH"""

    def __init__(self, vacansy: str):
        self.vacansy = vacansy
        self.vacansies = []
        self.__api_str = "https://api.hh.ru/vacancies"
        self.__first_key = 'items'
        self.__header = ''
        self.__param = {"text": self.vacansy,
                        "page": 0,
                        "per_page": 100
                        }

    @property
    def get_api_str(self):
        return self.__api_str

    @property
    def get_first_key(self):
        return self.__first_key

    @property
    def get_header(self):
        return self.__header

    @property
    def get_param(self):
        return self.__param

    def get_response(self):
        """Парсинг одной страницы с вакансиями"""

        response = requests.get(self.get_api_str,
                                headers=self.get_header, params=self.get_param)
        if response.status_code == 200:
            return response.json()[self.get_first_key]

    def get_vacansies(self, count_page=5):
        """Получение списка вакансий по предустановленному количеству страниц
        Возвращает: список с вакансиями"""

        while self.__param['page'] < count_page:
            one_page_vacansies = self.get_response()
            if one_page_vacansies is not None:
                self.vacansies.extend(one_page_vacansies)
                self.__param['page'] += 1
            else:
                print(f'На странице {self.__param["page"] + 1} ошибка при запросе данных')
                break

        return self.vacansies

    def filtred_vacansies(self):
        """Фильтрация вакансий не входящих в запрос"""

        self.get_vacansies()
        filtred_vacansies = []
        for v in self.vacansies:
            if self.vacansy in v['name'].lower():
                if v.get('salary') is not None:
                    salary = {'salary': True,
                              'salary_from': v['salary']['from'],
                              'salary_to': v['salary']['to'],
                              'currency': v['salary']['currency']
                              }
                else:
                    salary = {'salary': False,
                              'salary_from': None,
                              'salary_to': None,
                              'currency': None
                              }
                vacansy_params = {'id': v['id'],
                                  'title': v['name'],
                                  'employer': v['employer']['name'],
                                  'url': v['alternate_url'],
                                  'area': v['area']['name'],
                                  'experience': v['experience']['name'],
                                  'employment': v['employment']['name'],
                                  'portal': 'HeadHunter'
                                  }
                vacansy_params.update(salary)
                filtred_vacansies.append(vacansy_params)

        return filtred_vacansies


class SJGetVacansies(HHGetVacansies):
    """Получает вакансии по API с сайта HH"""

    def __init__(self, vacansy: str):
        super().__init__(vacansy)
        self.vacansy = vacansy
        self.__vacansies = []
        self.__api_str = "https://api.superjob.ru/2.0/vacancies"
        self.__first_key = "objects"
        self.__header = {"X-Api-App-Id": os.getenv("SJ_API_KEY")}
        self.__param = {"keyword": self.vacansy,
                        "page": 0,
                        "count": 100
                        }

    @property
    def get_api_str(self):
        return self.__api_str

    @property
    def get_first_key(self):
        return self.__first_key

    @property
    def get_header(self):
        return self.__header

    @property
    def get_param(self):
        return self.__param

    def filtred_vacansies(self):
        """Фильтрация вакансий не входящих в запрос"""

        self.get_vacansies()
        filtred_vacansies = []
        for v in self.vacansies:
            if self.vacansy in v['profession'].lower():
                if v['payment_from'] == 0 and v['payment_to'] == 0:
                    salary = {'salary': False}
                else:
                    salary = {'salary': True}

                vacansy_params = {'id': v['id'],
                                  'title': v['profession'],
                                  'employer': v['firm_name'],
                                  'url': v['link'],
                                  'area': v['town']['title'],
                                  'experience': v['experience']['title'],
                                  'employment': v['type_of_work']['title'],
                                  'salary_from': v['payment_from'],
                                  'salary_to': v['payment_to'],
                                  'currency': v['currency'],
                                  'portal': 'SuperJob'
                                  }
                vacansy_params.update(salary)
                filtred_vacansies.append(vacansy_params)

        return filtred_vacansies
