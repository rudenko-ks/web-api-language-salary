import requests
from pprint import pprint
from itertools import count

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
                "currency": "RUR",
                "only_with_salary": True,
                "page": page,
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


def main():
    try: 
        pprint(get_hh_vacancies())
    except requests.exceptions.HTTPError as error:
        print(error, error.response.text, sep="\n")
    
if __name__ == '__main__':
    main()
