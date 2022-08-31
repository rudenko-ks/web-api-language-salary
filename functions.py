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

    if ("rub" in currency) or ("RUR" in currency):
        if salary_from and salary_to:
            return (salary_from + salary_to) / 2
        elif salary_from:
            return salary_from * 1.2
        elif salary_to:
            return salary_to * 0.8
    return None