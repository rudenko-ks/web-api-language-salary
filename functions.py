from terminaltables import AsciiTable


def predict_rub_salary(vacancy: dict) -> float:
    if vacancy.get("salary"):  # headhunter
        currency = vacancy["salary"]["currency"]
        salary_from = vacancy["salary"]["from"]
        salary_to = vacancy["salary"]["to"]
    elif vacancy.get("currency"):  # superjob
        currency = vacancy["currency"]
        salary_from = vacancy["payment_from"]
        salary_to = vacancy["payment_to"]
    else:
        return None

    if not (("rub" in currency) or ("RUR" in currency)):
        return None
    elif salary_from and salary_to:
        return (salary_from + salary_to) / 2
    elif salary_from:
        return salary_from * 1.2
    elif salary_to:
        return salary_to * 0.8


def format_vacancies_to_table_view(title: str, vacancies: dict) -> AsciiTable:
    table_data = [
        [
            "Язык программирования",
            "Вакансий найдено",
            "Вакансий обработано",
            "Средняя зарплата"
        ]
    ]

    for vacancy in vacancies:
        table_data.append(
            [
                vacancy,
                vacancies[vacancy]["vacancies_found"],
                vacancies[vacancy]["vacancies_processed"],
                vacancies[vacancy]["average_salary"],
            ])
    return AsciiTable(table_data, title)
