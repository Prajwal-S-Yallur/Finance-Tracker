import pytz
import datetime

json_file_path = "database_lookup.json"

year_month = f'{pytz.timezone("Asia/Kolkata").localize(datetime.datetime.now()) :%Y-%m}'
year = year_month[:4]

credentials_file_path = "GCP_Service_Account_Key_my_third_account.json"

local_db_path = f"../Data Base/Production/{year_month}.db"

scopes = ['https://www.googleapis.com/auth/drive']

#Test Folder
parent_folder_id = "1-q568zpzep_tX-kkdOJrnpYVjQ7nJyj0"

# #Production Folder
# parent_folder_id = "1LWxbmB_44aafMkebO-DHWc3CSEgVGzmX"

# Backup Folder
backup_folder_id = "1xotj0OUE0f2ecxZw2EdHws6QcJs0XMTF"

# empty_year_month_details = {
#     year_month: {
#         "folder_details": {}, 
#         "file_details" : {}
#     }
# }

empty_year_month_details = {
    year_month: {
        "folder_details": {}, 
        "file_details" : {}
    }
}