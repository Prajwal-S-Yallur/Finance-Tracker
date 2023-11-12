import json
import pytz
import datetime

json_file_path = "database_lookup.json"
year_month = f'{pytz.timezone("Asia/Kolkata").localize(datetime.datetime.now()) :%Y-%m}'

def get_json_file_content():
    with open(json_file_path) as json_file:
        db_ref = json.load(json_file)
    json_file.close()
    return db_ref


def save_to_json_file(db_ref, response):    
    db_ref[year_month] = response

    with open(json_file_path, 'w') as json_file:
        json.dump(db_ref, json_file)
    json_file.close()
    return