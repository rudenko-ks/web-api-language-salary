from itertools import count
import requests

from functions import predict_rub_salary
    

def get_hh_vacancies(programming_language: str) -> dict:
    city = 1  # 1 - Москва
    vacansies_per_page = 100
    days_ago_vacansies_published = 30
    start_page = 0
    
    params = {
        "area": city,
        "text": f"Программист {programming_language}",
        "period": days_ago_vacansies_published,
        "page": start_page,
        'per_page': vacansies_per_page,
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
        "vacancies_found": response.json()["found"],
        "vacancies_processed": len(salaries),
        "average_salary": int(average_salary)
    }
