# Temporary in-memory database service

cases_db = []


def create_case(case: dict):
    new_case = case.copy()
    new_case["id"] = len(cases_db) + 1
    cases_db.append(new_case)
    return new_case


def get_all_cases():
    return cases_db


def get_case_by_id(case_id: int):
    for case in cases_db:
        if case["id"] == case_id:
            return case
    return None