import os
from dotenv import load_dotenv
from functions import format_vacancies_to_table_view

from headhunter import get_hh_vacancies
from superjob import get_superjob_vacancies


def main():
    load_dotenv()
    superjob_api_token = os.environ["SUPERJOB_API_TOKEN"]
    programming_languages = ["Python", "C", "Java", "C++", "C#", "Javacsript", "PHP", "Go", "Swift", "Kotlin"]

    hh_vacanсies = {}
    superjob_vacanсies = {}

    for language in programming_languages:
        hh_vacanсies[language] = get_hh_vacancies(language)
        superjob_vacanсies[language] = get_superjob_vacancies(language, superjob_api_token)

    hh_table_view = format_vacancies_to_table_view(title="HeadHunter", vacansies=hh_vacanсies)
    print(hh_table_view.table)
    superjob_table_view = format_vacancies_to_table_view(title="SuperJob", vacansies=superjob_vacanсies)
    print(superjob_table_view.table)

if __name__ == '__main__':
    main()
