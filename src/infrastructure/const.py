from json import load


def get_default_categories() -> list[dict]:
    with open("static/const/category/default_categories.json") as file:
        data = load(file)
    return data
