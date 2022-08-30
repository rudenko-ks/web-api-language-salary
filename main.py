import os
from dotenv import load_dotenv
from terminaltables import AsciiTable

from headhunter import get_hh_vacancies
from superjob import get_superjob_vacancies


def print_vacansies(title: str, vacansies: dict):
    table_data = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
        ]
    ]

    for vacancy in vacansies:
        table_data.append(
            [
                vacancy,
                vacansies[vacancy]["vacancies_found"],
                vacansies[vacancy]["vacancies_processed"],
                vacansies[vacancy]["average_salary"],
            ])
    table_instance = AsciiTable(table_data, title)
    print(table_instance.table)


def main():
    load_dotenv()
    superjob_api_token = os.environ["SUPERJOB_API_TOKEN"]
    programming_languages = ["Python", "C", "Java", "C++", "C#", "Javacsript", "PHP", "Go", "Swift", "Kotlin"]

    hh_vacansies = {}
    superjob_vacansies = {}

    for language in programming_languages:
        hh_vacansies[language] = get_hh_vacancies(language)
        superjob_vacansies[language] = get_superjob_vacancies(language, superjob_api_token)

    print_vacansies(title="HeadHunter", vacansies=hh_vacansies)
    print_vacansies(title="SuperJob", vacansies=superjob_vacansies)

if __name__ == '__main__':
    main()
