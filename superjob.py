import datetime
from itertools import count
import time
import requests

from functions import predict_rub_salary


def get_superjob_vacancies(programming_language: str, token: str) -> dict:
    city = 4  # 4 - Москва
    vacansies_per_page = 100
    published_from = datetime.datetime.now() - datetime.timedelta(days=30)
    published_from_in_unix_time = int(time.mktime(published_from.timetuple()))
    start_page = 0
    
    headers = {
        "X-Api-App-Id": token,
    }
    params = {
        "town": city,
        "count": vacansies_per_page,
        "page": start_page,
        "keyword": f"Программист {programming_language}",
        "date_published_from ": published_from_in_unix_time,
    }    

    vacancies = []
    for page in count():
        params["page"] = page
        response = requests.get('https://api.superjob.ru/2.0/vacancies/', headers=headers, params=params)
        response.raise_for_status()
        superjob_vacancies_search_result = response.json()
        vacancies.extend(superjob_vacancies_search_result["objects"])
        if not superjob_vacancies_search_result["more"]:
            break
        
    salaries = [rub_salary for vacancy in vacancies if (rub_salary := predict_rub_salary(vacancy))]
    average_salary = sum(salaries) / len(salaries) if salaries else 0

    return {
        "vacancies_found": superjob_vacancies_search_result["total"],
        "vacancies_processed": len(salaries),
        "average_salary": int(average_salary)
    }
