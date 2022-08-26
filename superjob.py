import datetime
from itertools import count
import time
import requests


def predict_rub_salary_for_superJob(vacancy: dict) -> float:
    if (vacancy["currency"] != "rub" \
        or (vacancy["payment_from"] is None and vacancy["payment_to"] is None)):
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
