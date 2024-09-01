import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from .config import year_month, local_db_path, scopes, credentials_file_path


def authenticate_with_google_drive():
    credentials = service_account.Credentials.from_service_account_file(credentials_file_path, scopes=scopes)
    drive_service = build('drive', 'v3', credentials=credentials)
    return drive_service


def upload_to_google_drive(folder_id, new_file_name):
    drive_service = authenticate_with_google_drive()
    media_body = MediaFileUpload(local_db_path, resumable=True)
    file_metadata = {
        'name': f'{new_file_name}.db',
        'parents': [folder_id]
    }

    file_result = drive_service.files().create(
        body=file_metadata,
        media_body=media_body
    ).execute()

    return file_result


def create_folder(folder_name, parent_folder_id=None):
    drive_service = authenticate_with_google_drive()
    folder_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_folder_id:
        folder_metadata['parents'] = [parent_folder_id]
    folder = drive_service.files().create(body=folder_metadata, fields='id').execute()
    # print(folder)
    return folder


# if __name__ == "__main__":
    # json_keyfile_path = "../GCP_Service_Account_Key_my_third_account.json"
    # local_file_path = "../../Data Base/Test/finance_database.db"
    # # folder_id = "https://drive.google.com/drive/folders/1-q568zpzep_tX-kkdOJrnpYVjQ7nJyj0"  # Replace with the actual folder ID
    # folder_id = "1-q568zpzep_tX-kkdOJrnpYVjQ7nJyj0"  # Replace with the actual folder ID
    # scopes = ['https://www.googleapis.com/auth/drive']
    # new_folder_name = "New Folder 2"
    # parent_folder_id = folder_id

    # drive_service = authenticate_with_google_drive(json_keyfile_path, scopes)
    # upload_to_google_drive(local_file_path, folder_id, drive_service)
    # folder_id = create_folder(drive_service, new_folder_name, parent_folder_id)

