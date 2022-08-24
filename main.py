import requests
from pprint import pprint


def get_hh_vacancies():
    programming_languages = dict.fromkeys(
        ["Python", "C", "Java", "C++", "C#", "Javacsript", "PHP", "Go", "Swift", "Kotlin"]
    )

    for lang in programming_languages:
        data = {
            "area": 1,  # 1 - Москва
            "text": f"Программист {lang}",
            "period": 30,
            "currency": "RUR",
            "gross": False,
            "only_with_salary": True,
        }
        response = requests.get('https://api.hh.ru/vacancies', params=data)
        response.raise_for_status()
        programming_languages[lang] = response.json()["found"]

    pprint(programming_languages)
    return response.json()['items']


def main():
    try: 
        get_hh_vacancies()
    except requests.exceptions.HTTPError as error:
        print(error, error.response.text, sep="\n")
    
if __name__ == '__main__':
    main()

