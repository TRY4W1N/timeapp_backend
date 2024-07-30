from json import load


def read_default_categories_json() -> list[dict]:
    with open("src/static/ui/category/default_categories.json") as file:
        data = load(file)
    return data
