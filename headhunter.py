from itertools import count
import requests


def predict_rub_salary(vacancy: dict) -> float:
    if (vacancy["salary"]["currency"] != "RUR" 
        or (vacancy["salary"]["from"] is None and vacancy["salary"]["to"] is None)):
        return None
    elif vacancy["salary"]["from"] and vacancy["salary"]["to"]:
        return (vacancy["salary"]["from"] + vacancy["salary"]["to"]) / 2
    elif vacancy["salary"]["from"]:
        return vacancy["salary"]["from"] * 1.2
    else:
        return vacancy["salary"]["to"] * 0.8


def get_hh_vacancies(programming_language: str) -> dict:
    params = {
        "area": 1,  # 1 - Москва
        "text": f"Программист {programming_language}",
        "period": 30,
        "page": 0,
        'per_page': 100,
        "currency": "RUR",                
        "only_with_salary": True,                
    }

    vacansies = []
    for page in count():
        params["page"] = page
        response = requests.get('https://api.hh.ru/vacancies', params=params)
        response.raise_for_status()
        vacansies.extend(response.json()["items"])
        if page >= response.json()["pages"]:
            break
        
    salaries = [predict_rub_salary(vacancy) for vacancy in vacansies if predict_rub_salary(vacancy)]
    average_salary = sum(salaries) / len(salaries) if len(salaries) else 0
    return {
        programming_language: {
            "vacancies_found": response.json()["found"],
            "vacancies_processed": len(salaries),
            "average_salary": int(average_salary)
        }
    }
