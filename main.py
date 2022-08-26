import datetime
import os
import time
import requests
from pprint import pprint
from itertools import count
from dotenv import load_dotenv


def predict_rub_salary(vacancy: dict) -> float:
    if (vacancy["salary"]["currency"] != "RUR" or 
        (vacancy["salary"]["from"] is None and vacancy["salary"]["to"] is None)):
        return None
    elif vacancy["salary"]["from"] and vacancy["salary"]["to"]:
        return (vacancy["salary"]["from"] + vacancy["salary"]["to"]) / 2
    elif vacancy["salary"]["from"]:
        return vacancy["salary"]["from"] * 1.2
    else:
        return vacancy["salary"]["to"] * 0.8


def get_hh_vacancies() -> dict:
    programming_languages_vacansies = dict.fromkeys(
        ["Python", "C", "Java", "C++", "C#", "Javacsript", "PHP", "Go", "Swift", "Kotlin"]
    )
    
    for language_vacancy in programming_languages_vacansies:
        vacansies = []
        for page in count():
            params = {
                "area": 1,  # 1 - Москва
                "text": f"Программист {language_vacancy}",
                "period": 30,
                "page": page,
                'per_page': 100,
                "currency": "RUR",                
                "only_with_salary": True,                
            }
            response = requests.get('https://api.hh.ru/vacancies', params=params)
            response.raise_for_status()
            vacansies.extend(response.json()["items"])
            if page >= response.json()["pages"]:
                break
            
        salaries = [predict_rub_salary(vacancy) for vacancy in vacansies if predict_rub_salary(vacancy)]
        average_salary = sum(salaries) / len(salaries)
        programming_languages_vacansies[language_vacancy] = {
            "vacancies_found": response.json()["found"],
            "vacancies_processed": len(salaries),
            "average_salary": int(average_salary)
        }
    return programming_languages_vacansies


def predict_rub_salary_for_superJob(vacancy: dict) -> float:
    if (vacancy["currency"] != "rub" or 
        (vacancy["payment_from"] is None and vacancy["payment_to"] is None)):
        return None
    elif vacancy["payment_from"] and vacancy["payment_to"]:
        return (vacancy["payment_from"] + vacancy["payment_to"]) / 2
    elif vacancy["payment_from"]:
        return vacancy["payment_from"] * 1.2
    else:
        return vacancy["payment_to"] * 0.8


def get_superjob_vacancies(programming_language: str, token: str) -> dict:
    published_from = datetime.datetime.now() - datetime.timedelta(days=30)
    published_from_in_unix_time = int(time.mktime(published_from.timetuple()))
    
    headers = {
        "X-Api-App-Id": token,
    }
    params = {
        "town": 4,  # 4 - Москва
        "count": 100,
        "page": 0,
        "keyword": f"Программист {programming_language}",
        "date_published_from ": published_from_in_unix_time,
    }    

    vacancies = []
    for page in count():
        params["page"] = page
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers, params=params)
        response.raise_for_status()
        vacancies.extend(response.json()["objects"])
        if not response.json()["more"]:
            break
        
    salaries = [predict_rub_salary_for_superJob(vacancy) for vacancy in vacancies if predict_rub_salary_for_superJob(vacancy)]
    average_salary = sum(salaries) / len(salaries) if len(salaries) else 0

    return {
        programming_language: {
            "vacancies_found": response.json()["total"],
            "vacancies_processed": len(salaries),
            "average_salary": int(average_salary)
        }
    }


def main():
    load_dotenv()
    superjob_api_token = os.environ["SUPERJOB_API_TOKEN"]
    programming_languages = ["Python", "C", "Java", "C++", "C#", "Javacsript", "PHP", "Go", "Swift", "Kotlin"]

    superjob_vacansies = dict.fromkeys(programming_languages)
    
    for language in programming_languages:
        # pprint(get_hh_vacancies())
        superjob_vacansies.update(get_superjob_vacancies(language, superjob_api_token))

    pprint(superjob_vacansies)

if __name__ == '__main__':
    main()
