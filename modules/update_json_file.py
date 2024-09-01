import json

from .config import json_file_path, year_month, empty_year_month_details


def get_json_file_content():
    with open(json_file_path) as json_file:
        db_ref = json.load(json_file)
    json_file.close()
    return db_ref


def save_to_json_file(db_ref, response, details_of):
    if details_of == "file":
        index = db_ref["months"].index(year_month)
        db_ref["months_details"][index][year_month]["file_details"] = response
    if details_of == "folder":
        db_ref["months"].append(year_month)
        db_ref["months_details"].append(empty_year_month_details)
        db_ref["months_details"][-1][year_month]["folder_details"] = response

    with open(json_file_path, 'w') as json_file:
        json.dump(db_ref, json_file)
    json_file.close()
    return