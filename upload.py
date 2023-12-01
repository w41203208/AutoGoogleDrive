import os
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


# Scopes
# https://www.googleapis.com/auth/drive	                  See, edit, create, and delete all of your Google Drive files
# https://www.googleapis.com/auth/drive.appdata	          See, create, and delete its own configuration data in your Google Drive
# https://www.googleapis.com/auth/drive.file	            See, edit, create, and delete only the specific Google Drive files you use with this app
# https://www.googleapis.com/auth/drive.metadata	        View and manage metadata of files in your Google Drive
# https://www.googleapis.com/auth/drive.metadata.readonly	See information about your Google Drive files
# https://www.googleapis.com/auth/drive.photos.readonly	  View the photos, videos and albums in your Google Photos
# https://www.googleapis.com/auth/drive.readonly	        See and download all your Google Drive files
# https://www.googleapis.com/auth/drive.scripts	          Modify your Google Apps Script scripts' behavior
SCOPES = ['https://www.googleapis.com/auth/drive.file']
TOKEN_AUTH_FILE = './key/google_auth.json'
CLIENT_SECRET_FILE = './key/client_secret.json'
UPLOAD_FOLDER_ID = '1NoUtT4OzLTVgrA3inKXgi_Ag7mXyY05X' #1jUJBwKx5fMMuXxxXWiOK6L4a1FuxLrsr


def authorization():
  creds = None
  if os.path.exists(TOKEN_AUTH_FILE):
    creds = Credentials.from_authorized_user_file(TOKEN_AUTH_FILE, scopes=SCOPES)
  
  if creds.expired:
    print('憑證已過期')

  if not creds.valid:
    print("憑證無效")


  if not creds or not creds.valid:
    flow = InstalledAppFlow.from_client_secrets_file(
      CLIENT_SECRET_FILE, scopes=SCOPES
    )
    creds = flow.run_local_server(port=0)

  with open(TOKEN_AUTH_FILE, "w") as token:
      token.write(creds.to_json())
  return creds

def create_drive_service():
  creds = authorization();
  # Use service account file
  
  # create drive api client
  service = build("drive", "v3", credentials=creds)
  

  return service

def upload_file(file_path, file_type):
  drive_service = create_drive_service()

  file_metadata = {
    'name': os.path.basename(file_path),
    'parents': [UPLOAD_FOLDER_ID],
  }
  file = None
  if file_type in ['media', 'text', 'zip']:
    if file_type == 'media':
      file = MediaFileUpload(file_path, mimetype="image/png")
    if file_type == 'text':
      file = MediaFileUpload(file_path, mimetype='text/plain')
    if file_type == 'zip':
      file = MediaFileUpload(file_path, mimetype='application/zip')
  else:
    print("沒有此檔案格式")

  try:
    response = drive_service.files().create(
      body=file_metadata,
      media_body=file,
    ).execute()
  except HttpError as error:
    print(f"An error occurred: {error}")
    response = None

  # print(f'File uploaded: {file}')  
  print(f'File uploaded: {response["name"]} ({response["id"]})')


def get_file(service, file_id):
  file_info = service.files().get(fileId=file_id).execute()
  print(file_info)
  

def check_authorization(service, file_id):
  permissions = service.permissions().list(fileId=file_id).execute()
  print('檔案的權限:', permissions.get('permissions', []))  

if __name__ == "__main__":
  file_path = "D:\\MingProgram\\unity-learning\\build\\Coin Pusher.zip"

  upload_file(file_path, 'zip')